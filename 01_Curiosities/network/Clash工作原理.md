---
type: curiosity
topic: Network
date: 2026-03-12
tags: [Clash, 代理, 网络协议, TUN, Shadowsocks, Xray]
---

# Clash 工作原理

## 1. Clash 是什么

Clash 是一个基于规则的网络代理客户端，核心职责是：**拦截本机流量 → 按规则判断 → 转发到对应出口**。

它本身不是协议，而是一个流量调度引擎，支持多种底层代理协议。

---

## 2. 流量拦截：两种模式

### 2.1 系统代理模式（HTTP/SOCKS5 Proxy）
- Clash 在本机监听一个端口（默认 7890）
- 将系统的 HTTP/HTTPS 代理指向该端口
- **局限**：只有主动感知代理的应用才会走代理（浏览器可以，很多 CLI 工具不行）

### 2.2 TUN 模式（虚拟网卡）
- Clash 创建一个虚拟网卡（utun），将系统路由表中的流量全部导入
- 所有 TCP/UDP 流量都会被接管，包括 kubectl、curl 等命令行工具
- **这就是为什么 kubectl 会被代理拦截的根本原因**

> 你遇到的 kubectl 超时问题，是因为 TUN 或系统代理把发往 `0.0.0.0:54903` 的流量转发给了 Clash，而 Clash 尝试通过远端代理服务器去访问本地地址，自然超时。解决方案就是配置 `no_proxy`。

---

## 3. 规则引擎

Clash 拦截流量后，按优先级匹配规则：

```
DOMAIN-SUFFIX,google.com,Proxy      # 域名后缀匹配
DOMAIN-KEYWORD,youtube,Proxy        # 域名关键字匹配
IP-CIDR,192.168.0.0/16,DIRECT       # IP 段直连
GEOIP,CN,DIRECT                     # 中国 IP 直连
MATCH,Proxy                         # 兜底规则
```

出口类型：
- `DIRECT`：直接连接，不走代理
- `REJECT`：丢弃，用于广告过滤
- `Proxy`：转发到代理服务器（或策略组）

---

## 4. 底层传输协议

Clash 只是调度层，真正负责"翻墙"的是底层协议，流量最终通过这些协议加密后发往 VPS：

| 协议 | 特点 |
|------|------|
| **Shadowsocks** | 最经典，轻量，流量特征较明显 |
| **VMess** | V2Ray 设计，混淆能力强，头部有时间戳验证 |
| **VLESS** | VMess 的精简版，性能更好 |
| **Trojan** | 伪装成 HTTPS 流量，极难识别 |
| **Hysteria2** | 基于 QUIC/UDP，适合高丢包网络 |

---

## 5. 完整链路

```
本机应用
   ↓ (系统代理 or TUN 网卡)
Clash 本地监听
   ↓ (规则匹配)
   ├── DIRECT → 直接出站
   └── Proxy  → 加密封装（VMess/Trojan 等）
                   ↓
              VPS 服务器（境外）
                   ↓
              目标网站
```

---

## 6. 为什么本地流量也会被拦截

Clash 的规则从上到下匹配，如果没有为 `127.0.0.1`、`localhost` 配置 `DIRECT` 规则，这些流量同样会走代理。

正确的配置应在规则顶部加上：
```yaml
- IP-CIDR,127.0.0.0/8,DIRECT
- IP-CIDR,10.0.0.0/8,DIRECT
- IP-CIDR,172.16.0.0/12,DIRECT
- IP-CIDR,192.168.0.0/16,DIRECT
```

或者在 shell 中配置 `no_proxy` 环境变量绕过代理。
