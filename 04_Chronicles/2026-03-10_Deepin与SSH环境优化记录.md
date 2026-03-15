---
title: Deepin 环境与 SSH/VPN 深度排障与优化日志
date: 2026-03-10
tags: [排障记录, Deepin, SSH, OpenVPN, 运维]
---

# Deepin 环境与 SSH/VPN 深度排障与优化日志

本日志记录了在受限环境下（Deepin 无 root），通过阿里云跳板机打通家庭 Mac Mini 的全过程。重点在于还原解决“连接卡死”和“VPN 配置不生效”的排查思路。

## 1. 初始需求与环境
- **需求**：在公司 Deepin 虚拟机（无 root 权限）上，实现一键直连家里的 Mac Mini（位于阿里云 OpenVPN 拨号后的内网）。
- **环境架构**：`Deepin Client -> Aliyun Server (OpenVPN Server) -> Mac Mini (OpenVPN Client)`。

## 2. 核心问题点：SSH 跳转卡死
- **现象描述**：配置 `ProxyJump` 后，执行 `ssh macmini` 时在输入完阿里云密码后长时间卡死，无报错。
- **排查过程**：
    1. **详细模式诊断**：执行 `ssh -v macmini`，发现连接停留在 `debug1: channel 0: new [direct-tcpip]`。
    2. **初步分析**：说明 SSH 已经成功进入阿里云，但在阿里云尝试通过 VPN 内网 IP 拨号 Mac Mini 时，网络不通。
    3. **现状确认**：在阿里云上直接 `ping 10.8.0.x` (Mac IP) 失败，确认 VPN 链路断开。

## 3. 深度排障：为何 VPN 频繁断开且配置不生效？
这是本次优化的技术难点，经历了多次“假设-验证”：

- **第一阶段：端口误判**
    - **现象**：服务端配置文件显示 `port 1193`，但客户端无论如何都连不上。
    - **排查**：在阿里云执行 `netstat -tunlp | grep openvpn`。
    - **发现**：真实监听端口竟然是 **1194**。说明服务端根本没在跑预期的配置。

- **第二阶段：配置文件路径错位 (真凶)**
    - **现象**：修改了 `/etc/openvpn/server.conf` 为 1193 端口并重启，`netstat` 依然显示 1194。
    - **排查**：执行 `ps aux | grep openvpn` 查看进程详细参数。
    - **重大发现**：进程加载参数为 `--config server.conf`（相对路径），其工作目录在 `/etc/openvpn/server/`。
    - **结论**：系统里存在两份 `server.conf`。用户改的是 `/etc/openvpn/server.conf`，但 systemd 启动的是 `/etc/openvpn/server/server.conf`。

- **第三阶段：保活机制失效**
    - **问题**：即使连上，几分钟后也会失联。
    - **分析**：由于之前加载了错误的配置文件，`keepalive 10 60` 实际并未生效，且 `redirect-gateway` 未注释，导致 Mac 全局流量被拉扯到阿里云，网络极其不稳定。

## 4. 解决方案与最终配置
针对上述排查结果，执行了以下闭环操作：
1. **同步配置**：将正确的配置覆盖至 `/etc/openvpn/server/server.conf`。
2. **强制重启**：`sudo systemctl restart openvpn-server@server`。
3. **对齐端口**：将服务端和客户端统一回 **1194** (或 1193，需保持一致)。
4. **注入保活**：
    - **OpenVPN**：设置 `keepalive 10 60`。
    - **SSH**：在 Deepin 端配置 `ServerAliveInterval 30`。
    - **Mac 端**：开启 `pmset -a womp 1` 并在终端长跑 `ping 10.8.0.1` 物理保活。

## 5. 最终成果
1. **一键直达**：通过 `ProxyJump` 实现了从 Deepin 到 Mac Mini 的秒连。
2. **稳定性**：解决了因空闲导致的 VPN 闪断，SSH 链路具有极强的容错性。
3. **舒适度**：深度优化了 Deepin 终端的 **24-bit TrueColor** 显示效果，彻底告别单色模式。

## 6. 深度排障：Clash Verge 与 OpenVPN/SSH 的冲突解决

在 Mac Mini 作为客户端的环境下，引入 Clash Verge 后出现了新的 SSH 断连问题。以下是详细的排查与精确优化记录：

### 6.1 问题现象
- **报错**：`Read from remote host 10.8.0.1: Connection reset by peer`。
- **特征**：SSH 连接在一段时间后（或传输大流量时）必然断开，即使 OpenVPN 显示连接正常。

### 6.2 核心冲突点分析 (Q&A)
- **Q: 为什么开启 Clash 后 SSH 会断开？**
  - **A**: Clash Verge 的 TUN 模式会创建虚拟网卡并接管系统流量。如果未配置绕过，它会劫持发往 VPN 内网（10.8.0.1）的流量。由于两个虚拟网卡（Clash 的 `utun` 和 OpenVPN 的 `utun4`）在争夺路由，导致 SSH 心跳包被错误拦截或重置。
- **Q: 为什么会提示 Connection reset by peer？**
  - **A**: 这是典型的 **MTU (最大传输单元)** 冲突。VPN 隧道有额外的封装开销，如果 MTU 保持默认的 1500，SSH 的大包在经过隧道时会因超过物理链路限制而被丢弃或分片失败。

### 6.3 精确优化方案
针对上述问题，实施了以下三个维度的精确修改：

#### 1. Clash Verge 避让规则 (Bypass)
在 **设置 -> 系统代理 -> 绕过列表** 以及 **TUN 模式 -> 排除自定义网段** 中精确添加：
- `10.8.0.0/24` (OpenVPN 内网段)
- `47.116.161.91/32` (阿里云公网 IP)
**覆写配置 (Override)** 强制直连：
```yaml
rules:
  - IP-CIDR,10.8.0.0/24,DIRECT
  - IP-CIDR,47.116.161.91/32,DIRECT
```

#### 2. OpenVPN MTU 强制约束 (核心修复)
在客户端 `config.ovpn` 中添加以下参数，解决大流量断连：
```text
tun-mtu 1400
mssfix 1360
```
*验证：连接后执行 `ifconfig utun4` 确认 MTU 已降至 1400。*

#### 3. SSH 客户端精确保活
在 Mac 本地 `~/.ssh/config` 中为 VPN 网段设置高频心跳：
```bash
Host 10.8.0.*
    ServerAliveInterval 15
    ServerAliveCountMax 3
    TCPKeepAlive yes
```

### 6.4 最终验证结果
- **路径验证**：`traceroute -n 10.8.0.1` 第一跳直接到达目标，证明 Clash 绕过成功。
- **MTU 验证**：`ping -D -s 1360 10.8.0.1` 确认大包不分片且 0 丢包通过。
- **稳定性预期**：配合 macOS 的休眠优化（防止自动睡眠），SSH 连接可实现跨昼夜不断开。

---
*记录人：Gemini CLI & 用户 (2026-03-10 23:50)*
