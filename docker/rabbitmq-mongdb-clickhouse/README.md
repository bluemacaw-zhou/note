# MongoDB + RabbitMQ + ClickHouse 数据处理管道

基于 Docker Compose 的部署方案，提供完整的数据存储、消息队列和分析能力。

## 架构说明

```
MongoDB 8.0.15 → RabbitMQ 3.12 → 业务服务（消费者） → ClickHouse 24.3
  (主数据库)       (消息队列)        (业务逻辑处理)        (分析数据库)
```

### 核心特性

- **MongoDB 8.0.15**: 副本集模式，支持 CDC（Change Data Capture）和高可用
- **RabbitMQ 3.12**: 消息队列缓冲，解耦数据生产和消费
- **ClickHouse 24.3 LTS**: 高性能列式数据库，支持实时分析查询
- **Web 管理界面**: RabbitMQ Management、ClickHouse Tabix 可视化管理

### 统一认证信息

| 服务 | 用户名 | 密码 |
|------|--------|------|
| MongoDB | admin | admin |
| ClickHouse | admin | admin |
| RabbitMQ | admin | admin |

## 系统要求

- **操作系统**: Ubuntu 20.04+ (推荐 22.04 LTS)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **内存**: 8GB+ (推荐 16GB)
- **磁盘**: 50GB+ 可用空间

## 部署步骤

### 步骤 1: 设置项目目录权限

**目的**: 确保 Docker 容器可以正确读写文件和目录

```bash
# 进入项目目录
cd ~/mongo-clickhouse

# 设置项目目录权限
chmod 755 .
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# 设置脚本可执行权限
chmod +x *.sh

# 设置 init-scripts 目录权限
chmod 755 init-scripts
chmod 644 init-scripts/clickhouse-init.sql
chmod 644 init-scripts/mongo-init.js
```

### 步骤 2: 生成 MongoDB 副本集 KeyFile

**目的**: 创建 MongoDB 副本集认证密钥，启用安全的副本集模式

```bash
# 确保在项目目录
cd ~/mongo-clickhouse

# 生成 KeyFile（副本集节点间认证）
openssl rand -base64 756 > init-scripts/mongodb-keyfile

# 设置严格的权限（必须是 400）
chmod 400 init-scripts/mongodb-keyfile

# 验证 KeyFile
ls -la init-scripts/mongodb-keyfile
# 应该显示: -r-------- 1 <user> <group> 1024 ... mongodb-keyfile
```

**说明**:
- KeyFile 用于 MongoDB 副本集节点间的内部认证
- 必须是 400 权限（仅所有者可读），否则 MongoDB 拒绝启动
- 副本集模式是 CDC（Change Data Capture）的前提

### 步骤 8: 启动所有服务

**目的**: 启动 MongoDB, ClickHouse, RabbitMQ 容器

```bash
# 启动所有服务
docker compose up -d

# 查看容器状态
docker compose ps
```

**预期输出**:
```
NAME                IMAGE                         STATUS
mongodb             mongo:8.0.15                  Up (healthy)
clickhouse          clickhouse-server:24.3        Up (healthy)
clickhouse-tabix    tabix-web-client:latest       Up
rabbitmq            rabbitmq:3.12-management      Up (healthy)
```

**说明**:
- 共 4 个容器，分别提供数据库、消息队列和分析能力
- 业务服务需要单独部署（消费 RabbitMQ 消息并写入 ClickHouse）

### 步骤 3: 初始化 MongoDB 副本集

**目的**: 将单节点 MongoDB 初始化为副本集模式，启用 Change Stream（CDC 的基础）

```bash
# 初始化副本集
docker exec mongodb mongosh -u admin -p admin --authenticationDatabase admin \
  --eval "rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'mongodb:27017'}]})"
```

**预期输出**:
```json
{ "ok": 1 }
```

**如果看到 "already initialized"**: 说明副本集已经初始化过了，跳过此步骤。

### 步骤 4: 验证副本集状态

**目的**: 确认副本集初始化成功，节点状态为 PRIMARY

```bash
# 等待副本集稳定
sleep 15

# 查看副本集状态
docker exec mongodb mongosh -u admin -p admin --authenticationDatabase admin \
  --eval "rs.status()" | grep -E "stateStr|health"
```

**预期输出**:
```
"stateStr" : "PRIMARY"
"health" : 1
```

**说明**:
- `PRIMARY`: 表示节点是主节点，可以读写
- `health: 1`: 表示节点健康

### 步骤 5: 查看所有服务日志

**目的**: 检查各服务是否有错误，确认启动成功

```bash
# 查看所有服务日志
docker compose logs

# 查看特定服务日志（最后 50 行）
docker compose logs --tail=50 mongodb
docker compose logs --tail=50 clickhouse
docker compose logs --tail=50 rabbitmq

# 实时跟踪日志
docker compose logs -f
```

**成功标志**:
- MongoDB: `Waiting for connections on port 27017`
- ClickHouse: `Ready for connections`
- RabbitMQ: `Server startup complete`

## 服务访问信息

部署成功后，可以通过以下地址访问各服务：

| 服务 | 访问地址 | 用户名 | 密码 | 说明 |
|------|---------|--------|------|------|
| MongoDB | `mongodb://服务器IP:27017` | admin | admin | 数据库连接 |
| ClickHouse HTTP | `http://服务器IP:8123` | admin | admin | HTTP 接口 |
| ClickHouse Native | `服务器IP:9000` | admin | admin | 原生 TCP 接口 |
| RabbitMQ Management | `http://服务器IP:15672` | admin | admin | 消息队列管理 |
| ClickHouse Tabix | `http://服务器IP:8124` | admin | admin | 数据库 Web 管理 |

### MongoDB 远程连接配置

#### 从 Windows 使用 MongoDB Compass 连接

**连接字符串**（假设 Ubuntu 虚拟机 IP 为 192.168.254.129）:

```
mongodb://admin:admin@192.168.254.129:27017/im_db?authSource=admin&replicaSet=rs0
```

**或分开填写连接参数**:

- **Hostname**: `192.168.254.129` (虚拟机 IP)
- **Port**: `27017`
- **Authentication**: Username/Password
- **Username**: `admin`
- **Password**: `admin`
- **Authentication Database**: `admin`
- **Advanced Options** → **Replica Set Name**: `rs0`

#### 连接故障排查

如果遇到 `getaddrinfo ENOTFOUND mongodb` 错误，说明主机名无法解析。解决方案：

1. **使用 IP 地址而非主机名**: `mongodb` 是 Docker 内部服务名，外部无法解析
2. **检查虚拟机防火墙**: 确保 27017 端口开放

```bash
# 在 Ubuntu 虚拟机中检查防火墙
sudo ufw status

# 如果防火墙激活，开放 MongoDB 端口
sudo ufw allow 27017/tcp
sudo ufw reload
```

3. **验证端口监听**: 确认 MongoDB 端口正确映射到宿主机

```bash
# 检查端口监听状态
sudo netstat -tlnp | grep 27017
# 或
sudo ss -tlnp | grep 27017
```

4. **测试本地连接**: 在虚拟机内部先测试连接

```bash
docker exec mongodb mongosh -u admin -p admin --authenticationDatabase admin --eval "db.runCommand({ping: 1})"
```

5. **虚拟机网络模式**: 确保虚拟机使用桥接或 NAT 模式，而非仅主机模式

## 业务服务集成说明

部署完成后，需要开发业务服务来消费 RabbitMQ 消息并写入 ClickHouse。

### 数据流示意

```
业务应用 → MongoDB (存储业务数据)
             ↓
          CDC / 手动投递
             ↓
          RabbitMQ (消息队列)
             ↓
     业务服务消费者 (Spring Boot)
       - 消费 RabbitMQ 消息
       - 执行业务逻辑
       - 写入 ClickHouse
             ↓
         ClickHouse (数据分析)
```

## 服务管理命令

```bash
# 查看所有容器状态
docker compose ps

# 启动所有服务
docker compose up -d

# 停止所有服务
docker compose stop

# 重启特定服务
docker compose restart mongodb
docker compose restart clickhouse
docker compose restart rabbitmq

# 删除所有容器（保留数据）
docker compose down

# 删除所有容器和数据（谨慎使用！）
docker compose down -v

# 查看资源使用情况
docker stats

# 进入容器
docker exec -it mongodb bash
docker exec -it clickhouse bash
docker exec -it rabbitmq bash

# RabbitMQ 管理命令
# 查看队列列表
docker exec rabbitmq rabbitmqctl list_queues

# 查看交换机
docker exec rabbitmq rabbitmqctl list_exchanges

# 查看绑定关系
docker exec rabbitmq rabbitmqctl list_bindings

# 查看连接
docker exec rabbitmq rabbitmqctl list_connections
```

## 数据备份

```bash
# 备份 MongoDB
docker exec mongodb mongodump --out /tmp/backup -u admin -p admin --authenticationDatabase admin
docker cp mongodb:/tmp/backup ./mongodb-backup-$(date +%Y%m%d)

# 备份 ClickHouse
docker exec clickhouse clickhouse-client --user admin --password admin \
  --query "BACKUP DATABASE im_analytics TO Disk('default', 'backup')"

# 备份 RabbitMQ 配置
docker exec rabbitmq rabbitmqctl export_definitions /tmp/rabbitmq-definitions.json
docker cp rabbitmq:/tmp/rabbitmq-definitions.json ./rabbitmq-backup-$(date +%Y%m%d).json

# 备份数据目录（直接复制宿主机目录）
tar -czf backup-$(date +%Y%m%d).tar.gz ~/workspace/docker/mongo-clickhouse/
```

## 完全卸载

如果需要完全移除所有服务和数据：

```bash
# 1. 停止并删除所有容器
cd ~/mongo-clickhouse
docker compose down -v

# 2. 删除项目目录
rm -rf ~/mongo-clickhouse

# 3. 删除数据目录
rm -rf ~/workspace/docker/mongo-clickhouse

# 4. 删除 Docker 镜像（可选）
docker rmi 10.100.6.129:8987/mongo:8.0.15
docker rmi 10.100.6.129:8987/clickhouse/clickhouse-server:24.3
docker rmi 10.100.6.129:8987/rabbitmq:3.12-management
docker rmi 10.100.6.129:8987/spoonest/clickhouse-tabix-web-client:latest
```

## 技术栈版本

| 组件 | 版本 | 说明 |
|------|------|------|
| MongoDB | 8.0.15 | 最新稳定版，副本集模式 |
| ClickHouse | 24.3 LTS | 长期支持版本 |
| RabbitMQ | 3.12 with Management | 包含 Web 管理插件 |
| Docker Compose | 3.7+ | 容器编排 |

## 参考资料

- [MongoDB 8.0 文档](https://www.mongodb.com/docs/v8.0/)
- [ClickHouse 24.3 文档](https://clickhouse.com/docs/en/intro)
- [RabbitMQ 文档](https://www.rabbitmq.com/documentation.html)
- [Spring AMQP 文档](https://spring.io/projects/spring-amqp)
- [ClickHouse JDBC 驱动](https://github.com/ClickHouse/clickhouse-java)

## 许可证

MIT License

---

**注意**: 本项目针对 Ubuntu 环境优化，使用 Docker Compose 单节点部署，适合开发、测试和中小规模生产环境。生产环境部署请参考 DEPLOY.md 进行安全加固和性能优化。
