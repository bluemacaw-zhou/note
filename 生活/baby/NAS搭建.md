# NAS 完整搭建指南

> 适用场景：家庭媒体服务器 + 文件备份 + 智能下载 + 全屋代理

---

## 目录

1. [NAS 是什么](#1-nas-是什么)
2. [硬件：x86 软路由小主机](#2-硬件x86-软路由小主机)
3. [操作系统：Ubuntu Server](#3-操作系统ubuntu-server)
4. [网络层：透明代理](#4-网络层透明代理)
5. [容器平台：Docker](#5-容器平台docker)
6. [媒体下载：qBittorrent + Sonarr + Radarr](#6-媒体下载qbittorrent--sonarr--radarr)
7. [资源索引：Jackett](#7-资源索引jackett)
8. [媒体服务：Jellyfin](#8-媒体服务jellyfin)
9. [电视端访问：Redmi 电视](#9-电视端访问redmi-电视)
10. [智能控制：QQ Bot + OpenClaw + Claude](#10-智能控制qq-bot--openclaw--claude)
11. [完整架构总览](#11-完整架构总览)
12. [采购清单](#12-采购清单)
13. [部署顺序建议](#13-部署顺序建议)

---

## 1. NAS 是什么

NAS（Network Attached Storage，网络附加存储）是一台**永远开着的、挂在局域网上的文件服务器**。

核心价值：
- **24 小时开机**：随时可访问，后台自动下载
- **大容量存储**：集中存放电影、照片、文档
- **网络可访问**：局域网内所有设备共享资源
- **服务运行平台**：跑 Docker 容器，部署各种服务

与普通外接硬盘的区别：
- 外接硬盘需要插电脑才能用
- NAS 独立运行，手机/电视/电脑都能直接访问
- NAS 可以主动下载、自动整理、主动推送通知

---

## 2. 硬件：x86 软路由小主机

**一台机器搞定路由器 + NAS + 容器平台**，比"成品 NAS + 独立路由器"方案省约 900 元，性能还更强。

### 为什么选 x86 小主机

- **性能强**：N100 处理器，完整跑 Docker 无压力
- **内存大**：16GB，跑十几个容器不卡
- **存储灵活**：SATA 接口直连机械硬盘，速度远比 USB 快
- **多网口**：4 个 2.5G 网口，一进一出做路由，天然适合软路由
- **低功耗**：整机 10~20W，24 小时运行月电费约 15~30 元

### 推荐型号

| 型号 | CPU | 内存 | 网口 | 参考价 |
|------|-----|------|------|--------|
| 倍控 N5105 | N5105 | 8GB | 4口 | ~800 元 |
| **倍控 N100** | **N100** | **16GB** | **4口** | **~1000 元** ⭐ |
| 畅网 N6005 | N6005 | 16GB | 6口 | ~1500 元 |

**推荐倍控 N100：**
- N100 核显支持 Jellyfin 硬件解码，4K 视频转码流畅
- 16GB 内存跑全套服务绰绰有余
- 性价比最优

### 硬盘

选 **NAS 专用机械硬盘**，不要用普通桌面盘，专为 24 小时连续运转设计：

| 品牌 | 型号 | 容量 | 特点 |
|------|------|------|------|
| 西数 | WD Red Plus | 4TB / 6TB | 最常见，稳定 |
| 希捷 | IronWolf | 4TB / 6TB | 性能稍好 |

推荐：**4TB × 2 组 RAID 1**，双盘互备，实际可用 4TB，单盘损坏数据不丢。

---

## 3. 操作系统：Ubuntu Server

x86 小主机直装 **Ubuntu Server**，标准 Linux 环境，原生支持 Docker，所有操作都是熟悉的命令行。

Ubuntu 原生可以实现完整的路由器功能，无需额外的路由器操作系统：

| 功能 | 实现方式 |
|------|---------|
| 路由转发 | `iptables` + 开启 `ip_forward` |
| DHCP / DNS | `dnsmasq` |
| 透明代理 | `Mihomo` + `iptables` |
| 防火墙 | `ufw` / `nftables` |
| OpenVPN 客户端 | `openvpn` 包 |
| 容器平台 | `Docker` + `docker-compose` |

---

## 4. 网络层：透明代理

### 核心概念

ClashX 装在单台电脑上，只代理那台电脑的流量。Ubuntu 软路由做的是**透明代理**，全屋所有设备流量都经过它，设备本身完全无感知，不需要任何配置：

```
手机 / 电视 / 电脑（无需任何配置）
        ↓ 所有流量
Ubuntu 软路由（Mihomo）
        ↓ 按规则判断
国内 IP / 域名  →  直连
国外 IP / 域名  →  代理节点
广告域名        →  拦截
```

### Mihomo 规则

Mihomo 通过域名规则和 GeoIP 数据库两种方式判断国内外：

```yaml
rules:
  - DOMAIN-SUFFIX,google.com,PROXY
  - DOMAIN-SUFFIX,youtube.com,PROXY
  - DOMAIN-SUFFIX,baidu.com,DIRECT
  - DOMAIN-SUFFIX,taobao.com,DIRECT
  - GEOIP,CN,DIRECT      # 中国 IP 全部直连
  - MATCH,PROXY          # 其余走代理
```

域名规则由社区维护，覆盖几万个域名，每天更新，直接订阅使用即可。

### iptables 流量劫持

将所有设备的流量劫持给 Mihomo 处理：

```bash
# 新建链
iptables -t nat -N MIHOMO

# 私有 IP 不代理（局域网 + 阿里云内网直接放行）
iptables -t nat -A MIHOMO -d 0.0.0.0/8    -j RETURN
iptables -t nat -A MIHOMO -d 127.0.0.0/8  -j RETURN
iptables -t nat -A MIHOMO -d 192.168.0.0/16 -j RETURN
iptables -t nat -A MIHOMO -d 10.0.0.0/8   -j RETURN

# 其余 TCP 流量转给 Mihomo 透明代理端口
iptables -t nat -A MIHOMO -p tcp -j REDIRECT --to-port 7892

# 应用到所有入站流量
iptables -t nat -A PREROUTING -p tcp -j MIHOMO
```

### 与 OpenVPN 的分工

三者完全不冲突，各管各的：

```
流量进入软路由
        ↓
iptables 判断
        ├── 阿里云内网 IP  →  RETURN（走 OpenVPN 隧道）
        ├── 私有 IP 段     →  RETURN（局域网直连）
        └── 其余流量       →  转给 Mihomo
                                ├── 国内  →  直连
                                └── 国外  →  代理节点
```

**注意**：OpenVPN 服务端配置不要加 `redirect-gateway`，只推送内网路由段，否则会和 Mihomo 抢默认路由。

---

## 5. 容器平台：Docker

### 为什么用 Docker

- 安装/卸载干净，不污染系统
- `docker-compose up` 一键启动所有服务
- 和日常开发环境完全一致，无学习成本

### 基础 docker-compose.yml

```yaml
version: "3"
services:
  jellyfin:
    image: jellyfin/jellyfin
    ports:
      - "8096:8096"
    volumes:
      - /data/media:/media
    restart: unless-stopped

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent
    ports:
      - "8080:8080"
    volumes:
      - /data/downloads:/downloads
    restart: unless-stopped

  sonarr:
    image: lscr.io/linuxserver/sonarr
    ports:
      - "8989:8989"
    volumes:
      - /data/media:/media
      - /data/downloads:/downloads
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr
    ports:
      - "7878:7878"
    volumes:
      - /data/media:/media
      - /data/downloads:/downloads
    restart: unless-stopped

  jackett:
    image: lscr.io/linuxserver/jackett
    ports:
      - "9117:9117"
    restart: unless-stopped
```

### K8s 部署（Mac Mini 验证阶段）

用 Mac Mini 验证整套方案时，按 Namespace 隔离：

```
Namespace: media   # Jellyfin / qBittorrent / Sonarr / Radarr / Jackett
Namespace: bot     # NapCatQQ / Spring Boot Bot
Namespace: ai      # OpenClaw（沙箱隔离）
```

---

## 6. 媒体下载：qBittorrent + Sonarr + Radarr

### qBittorrent

**下载执行器**，负责实际的 BT 下载任务。提供 HTTP API，可被 Sonarr / Radarr 自动调用。

- Web UI 端口：`8080`

### Sonarr

**自动追剧系统**，专门管理电视剧和动画的自动下载。一次添加，永久自动追更：

```
添加"小猪佩奇"
        ↓
每天自动扫描 Indexer
        ↓
发现新集 → 自动推给 qBittorrent 下载
        ↓
下载完成 → 自动整理文件命名
        ↓
Jellyfin 自动识别新内容
```

- Web UI 端口：`8989`

### Radarr

**自动追电影系统**，功能与 Sonarr 相同，专门针对电影。

- Web UI 端口：`7878`

---

## 7. 资源索引：Jackett

### 种子网络原理

种子网站本身**不存储视频**，只存索引信息（文件名、大小、校验码）。实际文件分散在全球用户硬盘上，下载时从多个用户同时获取，拼成完整文件。

### Jackett 的作用

各种子网站 API 格式不同，Jackett 作为**聚合适配器**，对上层提供统一接口：

```
Sonarr / Radarr
        ↓ 统一 Torznab 协议
      Jackett
        ↓ 各自适配
动漫花园 / NyaaSi / 1337x / ...
```

- Web UI 端口：`9117`
- 添加一次 Jackett，Sonarr 就能搜索所有配置的站点

### 推荐 Indexer

| 站点 | 类型 | 适合内容 |
|------|------|---------|
| 动漫花园 (dmhy.org) | 公开 | 中文动画、日漫字幕组 ⭐ |
| NyaaSi | 公开 | 日文原版动画 |
| 1337x | 公开 | 英文电影电视 |
| 馒头 (MTeam) | 私有 PT 站 | 全品类高质量，旧资源长期做种 |

### 旧资源问题

七龙珠等旧动画可能遇到**无人做种**（种子失效）的问题，推荐两种解决方式：

- **PT 站**：馒头等私有站有人长期做种，旧资源最全，需要邀请码加入
- **网盘分享**：阿里云盘 / 夸克搜索，用 Alist 工具挂载后 Jellyfin 可直接识别播放

---

## 8. 媒体服务：Jellyfin

### 是什么

Jellyfin 是完全**免费开源**的媒体服务器，把本地文件整理成类似 Netflix 的界面。

### 核心功能

- **自动刮削**：识别电影/剧集，自动下载封面、简介、评分
- **多端访问**：电视、手机、电脑、平板统一界面
- **硬件解码**：N100 核显完整支持，4K 视频硬件转码不卡
- **字幕管理**：自动搜索匹配字幕
- **用户管理**：多用户权限控制，适合家庭使用

### 与下载器的联动

```
qBittorrent 下载完成
        ↓
文件移入 Jellyfin 媒体库目录
        ↓
Jellyfin 自动扫描 → 刮削封面简介
        ↓
电视端直接播放
```

- Web UI 端口：`8096`

---

## 9. 电视端访问：Redmi 电视

### 第一步：电脑通过 ADB 连接电视

ADB（Android Debug Bridge）是 Google 官方的**安卓调试工具**，可以让电脑通过局域网直接控制安卓设备，无需 USB 线。

**电视端开启无线调试：**
```
设置 → 关于 → 连续点击"系统版本"7次
→ 出现开发者选项
→ 开启"USB 调试"或"无线调试"
→ 记下电视的局域网 IP 地址
```

**电脑安装 ADB：**
```bash
# macOS
brew install android-platform-tools

# Ubuntu
apt install adb

# Windows：下载 Android SDK Platform Tools，解压后加入环境变量
```

**连接电视：**
```bash
# 电脑和电视需在同一局域网
adb connect 192.168.1.xxx:5555

# 验证连接
adb devices
# 显示：192.168.1.xxx:5555  device  表示连接成功
```

### 第二步：安装 Jellyfin

下载 **Android TV 版本** APK，TV 版针对遥控器操作优化，体验远好于普通 Android 版。

下载地址：`jellyfin.org → Downloads → Android TV`

```bash
# 通过 ADB 直接安装，无需 U 盘
adb install jellyfin-androidtv.apk
```

**配置连接 Jellyfin 服务器：**
```
打开 Jellyfin
→ 输入服务器地址，例如：http://192.168.1.100:8096
→ 登录账号
→ 完成
```

如果安装后主屏幕找不到图标：
```
设置 → 应用管理 → 找到 Jellyfin → 打开
```

### 第三步：关闭广告（可选）

非必须，但能明显改善日常使用体验。通过 ADB 禁用广告相关系统应用，无需刷机，`disable` 是禁用而非删除，随时可恢复：

```bash
# 关闭开机广告
adb shell pm disable-user --user 0 com.miui.systemAdSolution

# 安装 FLauncher 替换默认主界面，去除广告推荐
adb install flauncher.apk
```

---

## 10. 智能控制：QQ Bot + OpenClaw + Claude

### 为什么选 QQ

- 国内最普及，手机常驻，消息即时
- 不需要额外安装 App，家人也能直接用
- 国内网络稳定，不依赖代理

### 整体链路

```
手机 QQ："帮我下载小猪佩奇全集"
        ↓
NapCatQQ 接收消息（OneBot 协议）
        ↓
Spring Boot Bot 服务
        ↓
OpenClaw → Claude API 解析意图
→ { title: "小猪佩奇", season: "all", type: "animation" }
        ↓
调用 Sonarr API 添加下载任务
        ↓
QQ 回复："已添加，预计 2 小时完成"
        ↓
下载完成 → Jellyfin 自动整理 → 电视直接播放
```

### QQ Bot 框架：NapCatQQ

QQ 官方不提供 Bot API，NapCatQQ 基于 QQ NT 内核模拟客户端，对外实现 **OneBot 协议**（统一的 HTTP / WebSocket API）。Spring Boot 只需对接 OneBot 协议，不耦合具体框架实现：

```
NapCatQQ（模拟 QQ 客户端）
        ↓ OneBot 协议
Spring Boot Bot 服务
        ↓
OpenClaw / Sonarr / Radarr API
```

### OpenClaw 沙箱隔离

部署在独立 K8s Namespace，通过 NetworkPolicy 限制只能访问 Claude API，无法横向访问内网其他服务：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  namespace: ai
spec:
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            name: bot
  egress:
    - to:
      - ipBlock:
          cidr: 0.0.0.0/0  # 出口只允许访问 api.anthropic.com
```

### Spring Boot Bot 核心逻辑

```java
@RestController
public class QQBotController {

    @PostMapping("/qq/event")
    public void handleMessage(@RequestBody QQEvent event) {
        String text = event.getMessage();

        // 调用 OpenClaw 解析自然语言意图
        MediaIntent intent = openClawClient.parse(text);

        // 根据类型路由到对应服务
        switch (intent.getType()) {
            case "animation", "series" -> sonarrClient.addSeries(intent);
            case "movie"               -> radarrClient.addMovie(intent);
        }

        // 回复 QQ
        qqClient.sendMessage(event.getGroupId(),
            "已添加下载任务：" + intent.getTitle());
    }
}
```

### 没有 AI 也能远程控制

AI 是锦上添花，不是必须的。通过 OpenVPN 连回家后，手机浏览器直接操作各服务的 Web UI：

| 服务 | 地址 | 功能 |
|------|------|------|
| Sonarr | `nas-ip:8989` | 添加追剧任务 |
| Radarr | `nas-ip:7878` | 添加电影下载 |
| qBittorrent | `nas-ip:8080` | 查看下载进度 |
| Jellyfin | `nas-ip:8096` | 直接看片 |

---

## 11. 完整架构总览

```
┌──────────────────────────────────────────────────────┐
│                      家庭网络                          │
│                                                      │
│  x86 软路由小主机（倍控 N100）                           │
│  ├── Ubuntu Server                                   │
│  │   ├── Mihomo          全屋透明代理                  │
│  │   │                   国内直连 / 国外走代理节点        │
│  │   ├── OpenVPN 客户端   接入阿里云内网                 │
│  │   ├── dnsmasq          DHCP + DNS                 │
│  │   ├── iptables         流量劫持规则                  │
│  │   └── Docker Compose                              │
│  │       ├── Jellyfin          :8096                 │
│  │       ├── qBittorrent       :8080                 │
│  │       ├── Sonarr            :8989                 │
│  │       ├── Radarr            :7878                 │
│  │       ├── Jackett           :9117                 │
│  │       ├── NapCatQQ                                │
│  │       └── Spring Boot Bot                         │
│  │                                                   │
│  └── SATA 硬盘：西数红盘 4TB × 2（RAID 1）              │
│                                                      │
│  Redmi 电视                                           │
│  └── Jellyfin Android TV（ADB 安装）                  │
│                                                      │
└──────────────────────────────────────────────────────┘

外部依赖：
├── 阿里云 ECS（OpenVPN 服务端 + 出口节点）
├── QQ（消息通道）
└── Anthropic Claude API（意图解析）
```

---

## 12. 采购清单

| 设备 | 型号 | 价格 |
|------|------|------|
| x86 小主机 | 倍控 N100（16GB，4口 2.5G） | ~1000 元 |
| 硬盘 × 2 | 西数红盘 4TB WD Red Plus | ~600 元/块 |
| **合计** | | **~2200 元** |

### 先用 Mac Mini 验证（零成本）

购买小主机前，用现有的 Mac Mini 先把整套软件跑通，确认没问题再采购：

```
Mac Mini
├── Docker Desktop / K8s
│   ├── Jellyfin / qBittorrent / Sonarr / Radarr / Jackett
│   ├── NapCatQQ
│   └── Spring Boot Bot
└── 外接移动硬盘（临时存储）
```

---

## 13. 部署顺序建议

分阶段部署，每步独立验证，避免问题堆积难以排查。

### 第一阶段：媒体服务跑通

```
目标：能在电视上播放内容

1. Docker 部署 qBittorrent + Jellyfin
2. 手动下载一个测试文件
3. ADB 连接 Redmi 电视，安装 Jellyfin APK
4. 验证电视能正常播放
```

### 第二阶段：自动下载跑通

```
目标：添加一部剧能自动下载

1. Docker 部署 Jackett，添加动漫花园
2. Docker 部署 Sonarr，对接 Jackett + qBittorrent
3. 添加"小猪佩奇"，验证自动下载全流程
```

### 第三阶段：远程访问

```
目标：出门在外也能控制

1. 确认 OpenVPN 组网正常
2. 手机连 VPN，访问 Sonarr Web UI
3. 验证远程添加下载任务
```

### 第四阶段：透明代理

```
目标：全屋设备无感翻墙

1. Ubuntu 安装配置 Mihomo
2. 配置 iptables 流量劫持规则
3. 验证全屋设备国内直连、国外走代理
4. 验证与 OpenVPN 不冲突
```

### 第五阶段：QQ Bot + AI 控制

```
目标：QQ 发一句话触发下载

1. Docker 部署 NapCatQQ，登录 QQ
2. Spring Boot Bot 对接 OneBot 协议
3. 硬编码测试：收到消息 → 调用 Sonarr API
4. 接入 OpenClaw + Claude API，替换硬编码意图解析
5. K8s 部署，配置 NetworkPolicy 沙箱隔离
```

### 第六阶段：迁移到 x86 小主机

```
目标：Mac Mini 还给开发用

1. 购买 x86 小主机 + 硬盘
2. 安装 Ubuntu Server
3. 配置网络层（Mihomo + iptables + OpenVPN + dnsmasq）
4. 迁移 docker-compose 配置
5. 迁移数据到机械硬盘
6. 验证所有服务正常
```

---

*文档生成时间：2026年3月*
*适用版本：Ubuntu 24.04 LTS / Jellyfin 10.x / Sonarr v4 / Radarr v5 / Jackett 0.21.x / NapCatQQ latest*
