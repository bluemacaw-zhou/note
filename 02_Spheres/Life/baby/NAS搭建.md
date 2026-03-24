---
type: journal
sphere: Life
date: 2026-03-10
updated: 2026-03-14
tags: ["Life", "baby", "NAS搭建", "媒体服务"]
---

# NAS 媒体服务：理论与架构

> 当前运行环境：Mac Mini + OrbStack Docker（验证阶段）
> 实践记录：[[2026-03-13_NAS媒体服务实践记录]] · 故障排查：[[2026-03_NAS故障排查]] · 未来规划：[[2026-03-13_NAS未来规划]]

---

## 一、是什么，为什么做

NAS（Network Attached Storage）是一台**永远开着的局域网文件服务器**，核心价值在于：
- 24 小时开机，后台自动下载，不依赖手动操作
- 存储集中，手机/电视/电脑统一访问
- 运行容器服务，实现自动化媒体管理

本方案的目标：**一句话添加，自动下载，自动整理，电视/手机直接播放**。

---

## 二、组件全景

### 2.1 当前实际运行的组件

```
┌─────────────────── Mac Mini ─────────────────────┐
│                                                    │
│  OrbStack Docker (name: media)                     │
│  ├── Jellyfin      :8096   媒体服务器               │
│  ├── qBittorrent   :8080   种子下载执行器            │
│  ├── Sonarr        :8989   剧集自动化管理            │
│  ├── Radarr        :7878   电影自动化管理            │
│  └── Prowlarr      :9696   Indexer 聚合器           │
│                                                    │
│  宿主机文件系统                                      │
│  └── ~/nas/media/          最终媒体文件              │
│      ├── tv/               剧集                    │
│      └── movies/           电影                    │
│                                                    │
└────────────────────────────────────────────────────┘

客户端
├── iPhone → Jellyfin 官方 App（播放）
├── iPhone → Ruddarr（管理下载任务）
└── 红米电视 → Jellyfin for Android TV（播放）

远程访问
└── 手机 → 阿里云 ECS → OpenVPN 隧道 → Mac Mini (10.8.0.2)
```

### 2.2 各组件职责

| 组件              | 职责                               | 类比         |
| --------------- | -------------------------------- | ---------- |
| **Jellyfin**    | 媒体服务器，管理媒体库、刮削元数据、按需转码、对外串流      | 私有 Netflix |
| **qBittorrent** | 种子协议下载执行器，接受上层推送的磁链/种子，完成实际下载    | 迅雷         |
| **Sonarr**      | 剧集生命周期管理：追踪更新、搜索资源、推送下载、整理命名     | 自动追剧机器人    |
| **Radarr**      | 电影生命周期管理，功能与 Sonarr 相同但针对电影      | 自动追电影机器人   |
| **Prowlarr**    | Indexer 聚合器，统一适配各种子站为 Torznab 协议 | 种子搜索引擎中间层  |
| **Ruddarr**     | iPhone 端 Sonarr + Radarr 管理客户端   | 移动控制台      |

---

## 三、设计思考

### 3.1 为什么用 Docker 而不是 K8s

媒体服务有两个特点：**有状态**（大量配置数据库）+ **依赖大存储卷**（几百 GB 的媒体文件）。

K8s 的优势是网络隔离（NetworkPolicy）和弹性调度，这对媒体服务没有价值。Docker Compose 更直接，存储挂载更简单，也没有 K8s 的 overhead。

K8s 层留给真正需要网络隔离的服务（如 NapCatQQ + AI Bot 沙箱）。

### 3.2 为什么用 Prowlarr 而不是 Jackett

最初计划用 Jackett，实际使用中发现：
- Jackett 的部分 indexer 实现有 API 兼容问题（EZTV 返回 400）
- 部分站点需要额外的 FlareSolverr 组件绕过 Cloudflare
- Prowlarr 原生集成 Sonarr/Radarr（自动同步，无需手动填 Torznab URL）
- Prowlarr 社区更活跃，indexer 维护更好

结论：Prowlarr 是 Jackett 的直接替代者，使用体验更好。

### 3.3 为什么 Sonarr/Radarr 和 qBittorrent 要共享同一套卷

Sonarr/Radarr 下载完成后需要把文件从 `/downloads` 整理到 `/media`。如果两个目录在不同的物理设备上，整理是**复制**（耗时、占双倍空间）；如果在同一个卷上，整理是**hardlink**（瞬间完成、不占额外空间）。

三个容器挂载同一份宿主机目录就是为了保证 hardlink 可行。

### 3.4 为什么需要 Prowlarr 这一层而不是直接搜种子

Sonarr/Radarr 只支持标准的 **Torznab 协议**。各种子站（dmhy、YTS、1337x 等）各自有不同的 API 格式。Prowlarr 统一适配，让 Sonarr/Radarr 无需关心底层种子站的差异。

---

## 四、网络流量

### 4.1 下载流（从添加到入库）

```
用户（Ruddarr）添加剧集/电影
        ↓
Sonarr/Radarr 发起 Torznab 搜索 → Prowlarr
        ↓
Prowlarr 代理访问对应种子站（dmhy / YTS），返回资源列表
        ↓
Sonarr/Radarr 按质量规则选定资源，推送磁链给 qBittorrent
        ↓
qBittorrent 通过 BT 协议（:6881）从 Peer 网络下载
  → 落盘到 ~/nas/downloads/completed/<category>/
        ↓
Sonarr/Radarr 检测到下载完成，hardlink 整理到 ~/nas/media/tv/ 或 /movies/
  → 按 "剧名/Season X/SxxExx - 标题.mkv" 命名规范
        ↓
Jellyfin 定期扫描媒体库，自动识别新文件，刮削封面/简介/评分
```

### 4.2 播放流（从点击到画面）

```
用户打开 Jellyfin App，点击播放

Jellyfin 判断：客户端是否支持直接播放该格式？
  ├── 支持 → Direct Play：直接传输原始文件（无 CPU 消耗）
  └── 不支持 → 转码：
        ffmpeg 读取源文件
        → 视频重编码为 H264（libx264）
        → 音频重编码为 AAC（libfdk_aac）
        → 封装为 HLS fMP4 分片
        → 客户端通过 HTTP 拉取分片播放

iPhone 场景：MKV + HEVC 10bit → 必须转码（iPhone 不支持 MKV 容器）
电视场景：多数格式可 Direct Play（Android 原生支持 HEVC、MKV、AC3）
```

### 4.3 远程访问流

```
家庭局域网访问：
手机/电视 ──局域网──→ Mac Mini :8096

远程 VPN 访问：
手机 → OpenVPN Connect
     → 阿里云 ECS（VPN 服务端，client-to-client 已开启）
     → OpenVPN 隧道
     → Mac Mini (VPN IP: 10.8.0.2)
     → 容器内网
     → Jellyfin/Sonarr/Radarr 各服务

注意：阿里云 ECS 带宽 3Mbps，VPN 实际可用 ~2.5Mbps。
Jellyfin 已设置 RemoteClientBitrateLimit = 2Mbps，远程播放降码率适配。
```

---

## 五、未来规划

> 详细规划、硬件选型、AI 探索、资源站追踪见 [[2026-03-13_NAS未来规划]]。
