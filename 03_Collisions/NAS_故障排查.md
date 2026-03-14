---
type: experiment
status: active
tags: [NAS, 故障排查, docker, jellyfin]
---

# NAS 故障排查记录

> 关联文档：[[NAS搭建]] · [[2026-03-13_NAS媒体服务实践记录]]
> 记录格式：现象 → 定位过程 → 根因 → 解法

---

## 坑 1：qBittorrent 临时密码每次重启变化

**现象**：服务启动后无法用已知密码登录。
**根因**：linuxserver 镜像每次容器重启生成新的随机临时密码，不持久化。
**解法**：首次启动后立即通过 API 固定密码：
```bash
# 临时密码从容器日志获取
docker logs media-qbittorrent 2>&1 | grep -i password

# 登录拿 session cookie
curl -c /tmp/qb.cookie 'http://localhost:8080/api/v2/auth/login' \
  --data 'username=admin&password=<临时密码>'

# 修改为固定凭据
curl -b /tmp/qb.cookie 'http://localhost:8080/api/v2/app/setPreferences' \
  --data 'json={"web_ui_username":"michael","web_ui_password":"michael"}'
```

---

## 坑 2：Jackett 多个 indexer 不可用

**现象**：Sonarr 搜索时，Jackett 代理 EZTV 返回 400，1337x 完全无法访问。
**根因**：
- EZTV：Jackett 的 `tvsearch` 实现与 EZTV 最新 API 不兼容
- 1337x：站点启用了 Cloudflare 保护，需要 headless browser 绕过
**解法**：整体换用 Prowlarr，不再使用 Jackett。Prowlarr 维护更活跃，原生集成 Sonarr/Radarr。

---

## 坑 3：Prowlarr 中 EZTV 仍然 429 + Cloudflare 超时

**现象**：换成 Prowlarr 后，EZTV 返回 429 Too Many Requests 和 Cloudflare challenge timeout。
**根因**：EZTV 对公开访问做了频率限制且启用了 Cloudflare。
**解法**：弃用 EZTV，改用 LimeTorrents（TV）和 YTS（电影）。

---

## 坑 4：LimeTorrents 不暴露电影分类

**现象**：Prowlarr 添加 LimeTorrents 后，Radarr 搜索电影无结果。
**定位**：检查 LimeTorrents Torznab 暴露的分类，发现只有通用/TV 类，无 2000 系列（电影分类）。
**根因**：LimeTorrents 的 Prowlarr 适配器未正确映射电影分类，Radarr 按分类过滤后无匹配。
**解法**：用 YTS 替代，YTS 正确暴露 2040（HD Movies）、2045（x265）、2060（3D）分类。

---

## 坑 5：添加剧集/电影报 400 "Path must not be empty"

**现象**：通过 Ruddarr 或 API 添加内容时返回 400。
**根因**：Sonarr/Radarr 未配置 Root Folder，不知道整理后的文件放哪里。
**解法**：
```bash
# Sonarr
curl -X POST http://localhost:8989/api/v3/rootfolder \
  -H "X-Api-Key: c5d25520a69c428bbe5209908bbafcaf" \
  -H "Content-Type: application/json" \
  -d '{"path":"/media/tv"}'

# Radarr
curl -X POST http://localhost:7878/api/v3/rootfolder \
  -H "X-Api-Key: 8a9b154e4d10498c971ff4551a562116" \
  -H "Content-Type: application/json" \
  -d '{"path":"/media/movies"}'
```

---

## 坑 6：Ruddarr 提示 "Upgrade to Sonarr v4.0.5 or newer"

**现象**：Ruddarr 连接 Sonarr 时提示版本过低，无法使用。
**根因**：`latest` 标签在拉取时获取到的是 v3 镜像，Ruddarr 要求 v4+。
**解法**：
```bash
docker compose pull sonarr && docker compose up -d sonarr
```

---

## 坑 7：Sonarr 下载完成后未自动导入

**现象**：qBittorrent 下载完成，文件在 `/downloads/completed/` 中，Sonarr 未自动整理。
**定位**：检查 qBittorrent 中该任务的 category，发现未打 `sonarr` tag。
**根因**：Sonarr 只认领 category 为 `sonarr` 的任务，category 不对则不处理。
**解法**：通过手动导入 API 触发（用 `seriesId` 参数而非路径，路径参数有编码问题）：
```bash
# 获取 seriesId
curl http://localhost:8989/api/v3/series -H "X-Api-Key: <key>"

# 触发手动导入
curl -X POST "http://localhost:8989/api/v3/manualimport?seriesId=<id>" \
  -H "X-Api-Key: <key>"
```

---

## 坑 8：Jellyfin 无法转码，播放黑屏（ffmpeg 路径为空）

**现象**：播放时黑屏，日志无转码输出或报 ffmpeg 找不到。
**定位**：检查 `~/nas/config/jellyfin/config/encoding.xml`，发现 `EncoderAppPath` 字段为空。
**根因**：首次启动时 Jellyfin 只写入了 `EncoderAppPathDisplay`，`EncoderAppPath`（实际用于调用的字段）未写入，值为空。
**解法**：手动编辑 `encoding.xml`，添加：
```xml
<EncoderAppPath>/usr/lib/jellyfin-ffmpeg/ffmpeg</EncoderAppPath>
```
然后重启容器：`docker compose restart jellyfin`

---

## 坑 9：播放黑屏（转码启动后 5 秒被杀）

**现象**：日志出现 ffmpeg 启动后很快出现 "Stopping ffmpeg process with q command" 然后 "Deleting partial stream file(s)"。
**定位**：确认 ffmpeg 确实启动（有转码命令日志），但被 Jellyfin 主动终止。
**根因**：Jellyfin session 管理检测到客户端未及时消费 HLS 分片，判断会话空闲，主动终止进程。实际原因是 VPN 高延迟导致客户端启动缓慢。
**解法**：等待 10-15 秒让缓冲建立，不要在黑屏后立即退出。如果是 VPN 场景，降低码率（设置 RemoteClientBitrateLimit）可改善。

---

## 坑 10：macOS SSH 状态误判

**现象**：执行 `launchctl list | grep sshd` 返回空，误判 SSH 未启动。
**根因**：macOS 使用 socket activation 机制，sshd 只在有连接时才出现在 launchctl 列表，空闲时不显示。
**正确检查方式**：
```bash
sudo systemsetup -getremotelogin
# 返回 "Remote Login: On" 即为已启用
```

---

## 坑 11：多语言 MKV 默认音轨选错

**现象**：含 Ita/Eng/Spa 三条音轨的 MKV，播放时只有意大利语。
**定位过程**：
1. 查 ffprobe 确认文件有三条音轨（stream 0:1 = ita，0:2 = eng，0:3 = spa）
2. 查 Jellyfin 转码日志，发现 `-map 0:1`（意大利语）
3. 尝试 Jellyfin 用户配置 `AudioLanguagePreference: eng` + `PlayDefaultAudioTrack: false` → 无效
4. 用 `mkvpropedit` 修改文件 default flag，触发媒体库重新扫描 → 最终生效，转码命令变为 `-map 0:2`

**最终解法**：mkvpropedit 修改默认轨 + Jellyfin 重新扫描该 item：
```bash
mkvpropedit <file> --edit track:a1 --set flag-default=0 \
                   --edit track:a2 --set flag-default=1

# 触发 Jellyfin 重新扫描
curl -X POST "http://localhost:8096/Items/<itemId>/Refresh?MetadataRefreshMode=FullRefresh" \
  -H "Authorization: MediaBrowser Token=<token>"
```

---

## 坑 12：Swiftfin 播放无声音

**现象**：Swiftfin 播放有画面无声音，无音量控制选项。
**定位过程**：
1. 确认服务端转码正常（日志有 `-codec:a:0 libfdk_aac`）
2. VLC 本地打开文件有声音 → 文件本身无问题
3. Mac 浏览器通过 Jellyfin Web 播放有声音 → 服务端无问题
4. 安装 Infuse，局域网播放有声音 → Swiftfin 特有问题
5. 官方 Jellyfin iOS app 局域网播放有声音 → 确认是 Swiftfin bug

**结论**：Swiftfin 存在音频渲染 bug，弃用，改用 Jellyfin 官方 iOS app。

---

## 坑 13：VPN 播放持续缓冲无法启动

**现象**：通过 OpenVPN（阿里云 ECS 3Mbps 带宽）播放时，Jellyfin 客户端一直转圈。
**定位**：Jellyfin 默认转码码率 7-8Mbps，阿里云 ECS 3Mbps 带宽扣除 VPN 开销后实际可用约 2.5Mbps，严重不足。
**解法**：设置服务端远程码率上限：
```bash
# 通过 API 设置 RemoteClientBitrateLimit = 2Mbps
TOKEN=$(curl -s -X POST "http://localhost:8096/Users/AuthenticateByName" \
  -H "Content-Type: application/json" \
  -H "Authorization: MediaBrowser Client=\"curl\", Device=\"cli\", DeviceId=\"cli001\", Version=\"1.0.0\"" \
  -d '{"Username":"michael","Pw":"michael"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['AccessToken'])")

# 读取当前配置，修改后写回
curl -s "http://localhost:8096/System/Configuration" \
  -H "Authorization: MediaBrowser Token=\"$TOKEN\"" -o /tmp/jf_config.json
python3 -c "
import json
c=json.load(open('/tmp/jf_config.json'))
c['RemoteClientBitrateLimit']=2000000
print(json.dumps(c))
" > /tmp/jf_config_new.json
curl -X POST "http://localhost:8096/System/Configuration" \
  -H "Authorization: MediaBrowser Token=\"$TOKEN\"" \
  -H "Content-Type: application/json" \
  -d @/tmp/jf_config_new.json
```
**效果**：VPN 场景降级为 720p，基本可流畅播放（取决于当时实际带宽）。
