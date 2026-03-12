---
type: experiment
status: completed
source: 突发任务: SSH 环境下无法使用 Claude Code
started: 2026-03-12
updated: 2026-03-12
tags: [Claude Code, SSH, macOS, Keychain]
---

# SSH 环境下 Claude Code 登录问题排查

## 背景

有一台安装了 Claude Code 的远程 Mac 机器（通过两跳 SSH 到达），直接执行 `claude` 命令提示需要登录，但 SSH 环境下无法打开浏览器完成 OAuth 授权流程。

网络约束：
- 本地机器：无法访问 claude.ai（无代理）
- 远程机器：有代理可访问 claude.ai，但无 GUI 浏览器

---

## 排查过程

### 思路一：curl 模拟 OAuth 流程

最初想法：用 curl 在远程机器上模拟浏览器完成整个 OAuth 授权码流程。

**否定原因：** OAuth PKCE 流程需要完整的浏览器会话（cookie、登录态），curl 模拟过于复杂，且有现成方案可绕过。

---

### 思路二：API Key 方案

```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

设置环境变量后 Claude Code 跳过 OAuth，直接走 API Key 认证。

**问题：** API Key 与 Claude.ai 套餐是两套独立计费体系，会产生额外费用。

---

### 思路三：SSH 端口转发

OAuth 回调地址是 `http://localhost:PORT`，通过 SSH 本地端口转发，把本地浏览器的请求转发到远程机器的监听端口：

```bash
ssh -L PORT:localhost:PORT user@remote-host
```

**否定原因：** 本地机器无法访问 claude.ai，浏览器打不开授权 URL，流程在第一步就断了。

---

### 思路四：复制 ~/.claude/ 凭证目录

既然远程机器已经登录过，直接把凭证目录 scp 到需要的机器。

```bash
scp -r ~/.claude/ user@target:~/.claude/
```

**发现真正问题：** 远程机器 `~/.claude/` 目录存在，用户也是同一个（michael），但执行 `claude` 时显示 "Welcome back michael!" 之后输入内容仍然报 `Not logged in`，并提示：

```
Run in another terminal: security unlock-keychain
```

---

## 根本原因

**macOS Keychain 锁定。**

Claude Code 在 Mac 上将真正的 auth token 存储在系统 Keychain 中，而非 `~/.claude/` 目录。GUI 登录会话下 Keychain 自动解锁，但 SSH 连接进来时 Keychain 处于锁定状态，导致 Claude Code 读不到 token。

---

## 解决方案

SSH 进入机器后，手动解锁 Keychain：

```bash
security unlock-keychain ~/Library/Keychains/login.keychain-db
# 输入该用户的登录密码
```

解锁后 `claude` 即可正常使用。

---

## 遗留问题

每次 SSH 连接都需要手动解锁，较为繁琐。后续可考虑：
- 写入 SSH 登录初始化脚本自动执行
- 或改用 `ANTHROPIC_API_KEY` 彻底绕开 Keychain（接受单独计费）
