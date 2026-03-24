# Clash Verge 规则模式失效排查记录

**日期**：2026-03-11
**环境**：macOS / Clash Verge (verge-mihomo 内核) / 订阅：龙猫云 TotoroCloud
**现象**：规则模式下无法访问 Google，切换到全局模式正常

---

## 一、问题描述

用户无意中关闭了 Clash Verge 的一个后台服务，之后发现：

- **全局模式**：可以正常访问 Google
- **规则模式**：无法访问 Google，连接超时

---

## 二、排查过程

### 2.1 确认进程状态

```bash
ps aux | grep -i clash
```

结果：两个核心进程均在运行

```
clash-verge        # UI 进程 (Tauri)
verge-mihomo       # 代理内核进程
```

结论：进程层面无异常。

---

### 2.2 检查系统代理设置

```bash
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
networksetup -getsocksfirewallproxy Wi-Fi

networksetup -getwebproxy Ethernet
networksetup -getsecurewebproxy Ethernet
networksetup -getsocksfirewallproxy Ethernet
```

| 接口 | HTTP 代理 | HTTPS 代理 | SOCKS 代理 |
|------|-----------|------------|------------|
| Wi-Fi | ❌ 未设置 | ❌ 未设置 | ❌ 未设置 |
| Ethernet | ✅ 127.0.0.1:7897 | ✅ 127.0.0.1:7897 | ✅ 127.0.0.1:7897 |

当前活跃网络接口为 `en0`（Ethernet），系统代理设置正确。

---

### 2.3 确认当前运行模式

通过 Clash API 查询：

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/configs
```

返回 `"mode": "global"`——用户已手动切换到全局模式作为临时绕过方案。

---

### 2.4 检查 DNS 是否正常

```bash
dig www.google.com @127.0.0.1
```

返回 `198.18.0.4`（fake-ip 段地址），说明 DNS 劫持和 fake-ip 模式工作正常。

---

### 2.5 检查代理节点和规则

**代理节点状态：**

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/proxies/...
```

| 代理组 | 当前节点 | 状态 |
|--------|----------|------|
| 龙猫云 - TotoroCloud | 美国 06 | ✅ 在线，延迟 ~600ms |
| GLOBAL | 美国 07 | ✅ 在线 |

节点均正常。

---

### 2.6 检查已加载的规则数量（关键发现）

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/rules | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('Total rules loaded:', len(data['rules']))
"
```

**输出：`Total rules loaded: 2`**

正常情况下应有数百条规则，结果只有 2 条：

```
IP-CIDR,10.8.0.0/24,DIRECT
IP-CIDR,47.116.161.91/32,DIRECT
```

---

### 2.7 核对历史日志（还原现场）

查看问题发生时段（21:58）的 sidecar 日志：

```
[WARNING] dial DIRECT --> www.google.com:443 error: connect failed: dial tcp 31.13.94.37:443: i/o timeout
[INFO]    127.0.0.1:53865 --> mozilla-ohttp.fastly-edge.com:443 doesn't match any rule using DIRECT
[INFO]    127.0.0.1:53879 --> www.baidu.com:443 doesn't match any rule using DIRECT
```

关键特征：**几乎所有流量都显示 `doesn't match any rule using DIRECT`**，说明规则引擎运行正常，但规则集为空，所有流量都 fallback 到 DIRECT 直连。Google 等境外域名直连在国内自然超时。

---

### 2.8 定位配置文件问题（根本原因）

检查 verge-mihomo 实际读取的生成配置文件：

```bash
grep -n "^rules:" clash-verge.yaml
# 找到 rules 段后查看内容
```

**`clash-verge.yaml` 的 rules 段只有 2 条**，与 API 查询结果一致。

再对比订阅文件（`RU1rdZTHoTwv.yaml`，614 行），其中包含完整的规则集（google、geosite、geoip 等），但这些规则完全没有被合并进去。

追查原因，发现 merge 配置文件 `mJt0v35QdWYg.yaml` 内容如下：

```yaml
# Profile Enhancement Merge Template for Clash Verge

rules:
  - IP-CIDR,10.8.0.0/24,DIRECT
  - IP-CIDR,47.116.161.91/32,DIRECT
```

---

## 三、根本原因

**Clash Verge merge 配置中 `rules:` 与 `prepend-rules:` 的行为差异：**

| 键名 | 行为 |
|------|------|
| `rules:` | **完全替换**订阅的规则集 |
| `prepend-rules:` | 在订阅规则**前面追加** |
| `append-rules:` | 在订阅规则**后面追加** |

`mJt0v35QdWYg.yaml` 使用了 `rules:` 键，导致本来用于"给局域网地址走直连"的 2 条辅助规则，把订阅里几百条规则全部覆盖掉。

**为什么之前没出问题？**

用户关闭后台服务导致内核重启，Clash Verge 重新生成 `clash-verge.yaml`。这次重新生成时，merge 配置的 `rules:` 覆盖行为才真正暴露出来（此前可能内核未完全重启，内存中的规则仍有效）。

---

## 四、修复方案

将 `mJt0v35QdWYg.yaml` 中的 `rules:` 改为 `prepend-rules:`：

```yaml
# 修改前
rules:
  - IP-CIDR,10.8.0.0/24,DIRECT
  - IP-CIDR,47.116.161.91/32,DIRECT

# 修改后
prepend-rules:
  - IP-CIDR,10.8.0.0/24,DIRECT
  - IP-CIDR,47.116.161.91/32,DIRECT
```

**修复后操作步骤：**

1. 打开 Clash Verge 界面
2. 进入"订阅"页面，重新激活当前订阅（或在设置里点击"重启内核"）
3. 切回规则模式

**验证命令：**

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/rules | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('Rules loaded:', len(d['rules']))"
# 正常应显示数百条
```

---

## 五、经验总结

1. **全局模式能用、规则模式不能用** → 优先检查规则是否正确加载，而不是节点或 DNS
2. **Clash Verge merge 配置** 中 `rules:` 会覆盖订阅规则，局部添加规则应使用 `prepend-rules:` 或 `append-rules:`
3. **内核重启是照妖镜** → 平时运行正常的错误配置，在内核重启后重新生成配置时才会暴露
4. **排查路径**：进程 → 系统代理 → DNS → 节点状态 → 规则加载数量 → 配置文件对比
