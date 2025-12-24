# Druid 连接创建卡死问题排查全流程

## 问题现象

```
com.alibaba.druid.pool.GetConnectionTimeoutException:
wait millis 60000, active 0, maxActive 64, creating 1, createElapseMillis 5669649
```

**关键信息**：
- `creating=1` - 有连接正在创建
- `createElapseMillis=5669649` - 已卡死 94 分钟
- `active=0` - 无活跃连接
- 重启后恢复

---

## 排查思路：逐步排除法

### 第一步：验证 connectTimeout 是否生效

#### 假设
配置了 `connectTimeout`，但可能没生效，导致 `driver.connect()` 无限等待。

#### 验证方法
```java
@GetMapping("/test-connect-timeout")
public String testConnectTimeout() throws Exception {
    DruidDataSource druid = (DruidDataSource) dataSource;

    // 使用无效IP测试
    String originalUrl = druid.getUrl();
    druid.setUrl("jdbc:mysql://192.0.2.1:3306/test");

    long start = System.currentTimeMillis();
    try {
        Connection conn = druid.getConnection();
        conn.close();
    } catch (Exception e) {
        long elapsed = System.currentTimeMillis() - start;
        return "失败耗时: " + elapsed + " ms";
    } finally {
        druid.setUrl(originalUrl);
    }
}
```

#### 验证结果
- **设置 60 秒** → 失败耗时 ≈ 21 秒
- **设置 10 秒** → 失败耗时 ≈ 10 秒

**结论**：✅ `connectTimeout` **已生效**，排除 `driver.connect()` 卡死。

---

### 第二步：验证 socketTimeout 是否生效

#### 假设
`initPhysicalConnection()` 或 `validateConnection()` 中的 SQL 执行卡死。

#### 验证方法
```java
@GetMapping("/test-socket-timeout")
public String testSocketTimeout() throws Exception {
    try (Connection conn = dataSource.getConnection();
         Statement stmt = conn.createStatement()) {

        long start = System.currentTimeMillis();
        try {
            stmt.execute("SELECT SLEEP(120)");  // 睡眠 120 秒
        } catch (SQLException e) {
            long elapsed = System.currentTimeMillis() - start;
            return "超时耗时: " + elapsed + " ms";
        }
    }
}
```

#### 验证结果
- 执行耗时 ≈ 60 秒（符合 `socketTimeout=60000`）

**结论**：✅ `socketTimeout` **已生效**，排除 SQL 执行超时问题。

---

### 第三步：检查配置是否会导致线程退出

#### 假设
`CreateConnectionThread` 因配置问题退出，导致无法创建新连接。

#### 检查方法
```java
@Component
public class DruidConfigCheck implements ApplicationRunner {

    @Autowired
    private DataSource dataSource;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        DruidDataSource druid = (DruidDataSource) dataSource;

        System.out.println("=== 配置检查 ===");
        System.out.println("breakAfterAcquireFailure: " + druid.isBreakAfterAcquireFailure());
        System.out.println("connectionErrorRetryAttempts: " + druid.getConnectionErrorRetryAttempts());
        System.out.println("timeBetweenConnectErrorMillis: " + druid.getTimeBetweenConnectErrorMillis());
    }
}
```

#### 检查结果
```
breakAfterAcquireFailure: false
connectionErrorRetryAttempts: 1
timeBetweenConnectErrorMillis: 500
```

**结论**：✅ 线程不会退出，排除线程死亡问题。

---

### 第四步：分析剩余可能性

经过验证：
- ✅ 所有超时配置都生效
- ✅ 线程不会退出
- 🔴 但仍然卡死 94 分钟

**推论**：卡死点在**不受超时保护**的地方。

---

## 最终结论：死锁或等待锁

### 源码分析

`CreateConnectionThread` 的执行流程：

```java
public void run() {
    for (;;) {
        // 1. 获取锁（⚠️ 没有超时保护）
        lock.lockInterruptibly();

        try {
            // 2. 判断是否需要创建
            if (条件判断) {
                empty.await();  // 可能等待信号
            }
        } finally {
            lock.unlock();
        }

        // 3. 创建连接（有超时保护）
        connection = createPhysicalConnection();
    }
}
```

**关键发现**：`lock.lockInterruptibly()` **没有超时限制**！

### 可能的卡死场景

```
1. 业务线程A获取 lock，执行数据库操作
2. 数据库操作遇到慢查询/锁等待，卡住 94 分钟
3. CreateConnectionThread 尝试获取 lock，一直等待
4. 显示 creating=1, createElapseMillis=94分钟
```

---

## 后续问题发生时的排查步骤

### 1. 立即导出线程堆栈

```bash
jstack <PID> > thread_dump.txt
```

### 2. 查找 CreateConnectionThread

```bash
grep -A 100 "CreateConnectionThread" thread_dump.txt
```

### 3. 判断卡死类型

#### 类型A：等待锁

```
"CreateConnectionThread" daemon prio=5
java.lang.Thread.State: WAITING (parking)
    at sun.misc.Unsafe.park(Native Method)
    at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt
    at java.util.concurrent.locks.ReentrantLock.lockInterruptibly(ReentrantLock.java:335)
    at com.alibaba.druid.pool.DruidDataSource$CreateConnectionThread.run(DruidDataSource.java:2901)
```

**说明**：卡在获取锁，找谁持有锁：

```bash
grep -B 10 "locked.*DruidDataSource" thread_dump.txt
```

#### 类型B：等待条件变量

```
"CreateConnectionThread" daemon prio=5
java.lang.Thread.State: WAITING (parking)
    at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await
    at com.alibaba.druid.pool.DruidDataSource$CreateConnectionThread.run(DruidDataSource.java:2930)
```

**说明**：等待 `empty.signal()`，检查连接是否泄漏：

```bash
# 查看连接池状态
curl http://localhost:8080/druid/datasource.html
```

---

## 预防措施

### 1. 监控告警

```java
@Component
public class DruidMonitor {

    @Autowired
    private DataSource dataSource;

    @Scheduled(fixedRate = 30000)  // 每 30 秒
    public void monitor() throws Exception {
        DruidDataSource druid = (DruidDataSource) dataSource;

        Field createStartNanosField = DruidAbstractDataSource.class
            .getDeclaredField("createStartNanos");
        createStartNanosField.setAccessible(true);
        long createStartNanos = (long) createStartNanosField.get(druid);

        if (createStartNanos > 0) {
            long elapsed = (System.nanoTime() - createStartNanos) / (1000 * 1000);

            if (elapsed > 60000) {  // 超过 1 分钟
                log.error("连接创建卡死 {} 秒", elapsed / 1000);
                // 发送告警
            }
        }
    }
}
```

### 2. 优化配置

```properties
# 增加重试次数
spring.datasource.druid.connection-error-retry-attempts=3

# 启用 KeepAlive
spring.datasource.druid.keep-alive=true

# 连接验证超时
spring.datasource.druid.validation-query-timeout=5
```

### 3. 代码规范

```java
// ❌ 错误：持有连接时间过长
public void badExample() {
    Connection conn = dataSource.getConnection();
    try {
        // 大量业务逻辑...
        Thread.sleep(10000);
    } finally {
        conn.close();
    }
}

// ✅ 正确：尽快释放连接
public void goodExample() {
    BusinessData data = prepareData();

    try (Connection conn = dataSource.getConnection()) {
        saveToDatabase(conn, data);
    }

    postProcess(data);
}
```

---

## 快速排查清单

问题发生时，按顺序执行：

1. ☐ `jstack <PID> > dump.txt` - 导出线程堆栈
2. ☐ `grep -A 100 "CreateConnectionThread" dump.txt` - 查看卡在哪里
3. ☐ `grep -B 10 "locked.*DruidDataSource" dump.txt` - 找持有锁的线程
4. ☐ `curl http://localhost:8080/druid/datasource.html` - 查看连接池状态
5. ☐ `SHOW PROCESSLIST;` - 查看数据库慢查询
6. ☐ 查看应用日志是否有 "create connection SQLException"

---

## 总结

### 排查过程

1. **假设**：`connectTimeout` 未生效 → **测试验证** → ✅ 已生效
2. **假设**：`socketTimeout` 未生效 → **测试验证** → ✅ 已生效
3. **假设**：线程退出 → **配置检查** → ✅ 不会退出
4. **结论**：等待锁或条件变量（不受超时保护）

### 核心要点

- **所有超时只保护创建连接过程，不保护获取锁**
- **线程堆栈是定位问题的唯一真相**
- **预防大于治疗：监控 + 代码规范**

---

**版本**: 1.0
**日期**: 2024-12-16
