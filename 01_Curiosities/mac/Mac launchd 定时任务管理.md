---
type: curiosity
date: 2026-05-15
tags: [mac, launchd, cron-job]
---

# Mac launchd 定时任务管理

本机定时任务统一归档在 `~/cron-job/`。每个任务一个目录，脚本、plist、日志和说明文档都放在对应任务目录内。

`~/Library/LaunchAgents/` 只保留供 macOS launchd 发现任务的入口文件，不再作为任务文件的主维护目录。

## 背景

原本由 openclaw cron 管理的 `dl-progress` 和 `whisper-srt` 已迁移到 macOS 原生 launchd。它们本质上只是定时执行 Python 脚本，不需要大模型参与；迁移后可避免 openclaw cron 在 `lightContext` 下误判路径和持续消耗 token。

阿里云 DDNS 任务也已纳入同一套 `~/cron-job/<task>/` 归档规范。

## 当前任务

| 任务 | Label | 间隔 | 任务目录 |
|------|-------|------|----------|
| 阿里云 DDNS | `top.bluwmacaw.ddns` | 300 秒 | `~/cron-job/ddns-aliyun/` |
| 下载进度播报 | `com.michael.dl-progress` | 600 秒 | `~/cron-job/dl-progress/` |
| 自动字幕生成 | `com.michael.whisper-srt` | 600 秒 | `~/cron-job/whisper-srt/` |

## 文件布局

### DDNS

| 类型 | 路径 |
|------|------|
| 脚本 | `~/cron-job/ddns-aliyun/ddns-aliyun.sh` |
| plist | `~/cron-job/ddns-aliyun/top.bluwmacaw.ddns.plist` |
| 标准日志 | `~/cron-job/ddns-aliyun/ddns-aliyun.log` |
| 错误日志 | `~/cron-job/ddns-aliyun/ddns-aliyun.err` |
| 说明文档 | `~/cron-job/ddns-aliyun/ddns-setup.md`、`~/cron-job/ddns-aliyun/ddns-check.md` |

### dl-progress

| 类型 | 路径 |
|------|------|
| 脚本 | `~/cron-job/dl-progress/dl-progress.py` |
| plist | `~/cron-job/dl-progress/com.michael.dl-progress.plist` |
| 标准日志 | `~/cron-job/dl-progress/com.michael.dl-progress.log` |
| 错误日志 | `~/cron-job/dl-progress/com.michael.dl-progress.err.log` |

### whisper-srt

| 类型 | 路径 |
|------|------|
| 脚本 | `~/cron-job/whisper-srt/whisper-srt.py` |
| plist | `~/cron-job/whisper-srt/com.michael.whisper-srt.plist` |
| 标准日志 | `~/cron-job/whisper-srt/com.michael.whisper-srt.log` |
| 错误日志 | `~/cron-job/whisper-srt/com.michael.whisper-srt.err.log` |

## LaunchAgents 入口

`~/Library/LaunchAgents/` 下需要保留以下入口：

| 入口 | 指向 |
|------|------|
| `~/Library/LaunchAgents/top.bluwmacaw.ddns.plist` | `~/cron-job/ddns-aliyun/top.bluwmacaw.ddns.plist` 的硬链接 |
| `~/Library/LaunchAgents/com.michael.dl-progress.plist` | `~/cron-job/dl-progress/com.michael.dl-progress.plist` 的符号链接 |
| `~/Library/LaunchAgents/com.michael.whisper-srt.plist` | `~/cron-job/whisper-srt/com.michael.whisper-srt.plist` 的符号链接 |

不要删除这些入口，否则登录后 launchd 无法自动发现任务。

## 常用命令

### 查看任务状态

```bash
launchctl print gui/$(id -u)/top.bluwmacaw.ddns
launchctl print gui/$(id -u)/com.michael.dl-progress
launchctl print gui/$(id -u)/com.michael.whisper-srt
```

重点看：

```text
program
stdout path
stderr path
last exit code
run interval
```

### 立即触发

```bash
launchctl kickstart -k gui/$(id -u)/top.bluwmacaw.ddns
launchctl kickstart -k gui/$(id -u)/com.michael.dl-progress
launchctl kickstart -k gui/$(id -u)/com.michael.whisper-srt
```

### 查看日志

```bash
tail -f ~/cron-job/ddns-aliyun/ddns-aliyun.log
tail -f ~/cron-job/ddns-aliyun/ddns-aliyun.err

tail -f ~/cron-job/dl-progress/com.michael.dl-progress.log
tail -f ~/cron-job/dl-progress/com.michael.dl-progress.err.log

tail -f ~/cron-job/whisper-srt/com.michael.whisper-srt.log
tail -f ~/cron-job/whisper-srt/com.michael.whisper-srt.err.log
```

### 修改 plist 后重新加载

```bash
launchctl bootout gui/$(id -u) ~/cron-job/ddns-aliyun/top.bluwmacaw.ddns.plist
launchctl bootstrap gui/$(id -u) ~/cron-job/ddns-aliyun/top.bluwmacaw.ddns.plist

launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.michael.dl-progress.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.michael.dl-progress.plist

launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.michael.whisper-srt.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.michael.whisper-srt.plist
```

说明：`dl-progress` 和 `whisper-srt` 通过 `~/Library/LaunchAgents/` 下的符号链接加载更稳定；DDNS 当前通过任务目录中的 plist 加载，`~/Library/LaunchAgents/` 下保留硬链接用于登录发现。

### 校验 plist

```bash
plutil -lint ~/cron-job/ddns-aliyun/top.bluwmacaw.ddns.plist
plutil -lint ~/cron-job/dl-progress/com.michael.dl-progress.plist
plutil -lint ~/cron-job/whisper-srt/com.michael.whisper-srt.plist
```

## 新增任务规范

1. 在 `~/cron-job/<task-name>/` 创建任务目录。
2. 把脚本、plist、日志、说明文档都放入该目录。
3. plist 中的 `ProgramArguments` 和日志路径必须指向该任务目录。
4. 在 `~/Library/LaunchAgents/` 下创建入口链接。
5. 使用 `launchctl bootstrap gui/$(id -u) <plist>` 加载。
6. 使用 `launchctl print gui/$(id -u)/<label>` 确认路径已经生效。

## 可删除与不可删除

可以删除旧的散落文件，但必须先确认任务已经改指向 `~/cron-job/<task>/`：

- 旧的 `~/bin/ddns-aliyun.sh`
- 旧的 `~/ddns-aliyun.log`、`~/ddns-aliyun.err`
- 旧的 `~/ddns-setup.md`、`~/ddns-check.md`
- 旧的 `~/Library/Logs/com.michael.*` 日志
- 旧的 `~/cron-job/launchd/` 共用 plist 目录

不可删除：

- `~/cron-job/<task>/` 下的任务文件
- `~/Library/LaunchAgents/` 下对应任务入口
- `~/.aliyun/config.json`，DDNS 依赖 aliyun CLI 的全局配置

## UI 工具

可以安装 LaunchControl 查看和编辑 launchd 任务：

```text
https://www.soma-zone.com/LaunchControl/
```

LaunchControl 会识别 `~/Library/LaunchAgents/` 下的入口文件。
