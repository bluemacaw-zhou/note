---
type: curiosity
topic: Mac
date: 2026-03-12
tags: [git, SSH]
---

# Git SSH 免密提交配置指南

## 背景

默认使用 HTTPS 协议的 Git 仓库每次推送都需要输入账号和 token，通过配置 SSH Key 可以实现完全免密提交。

---

## 一、生成 SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- 一路回车（默认路径 `~/.ssh/id_ed25519`）
- 可选设置 passphrase（留空则完全免密）

---

## 二、将公钥添加到 GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出内容，粘贴到：

> GitHub → Settings → SSH and GPG keys → New SSH key → 粘贴 → Add SSH key

---

## 三、将仓库 remote 从 HTTPS 切换为 SSH

**查看当前 remote 地址：**

```bash
git remote -v
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)
```

**修改为 SSH 地址：**

```bash
git remote set-url origin git@github.com:username/repo.git
```

> HTTPS 地址格式：`https://github.com/username/repo.git`
> SSH 地址格式：`git@github.com:username/repo.git`
> 转换规则：去掉 `https://github.com/`，替换为 `git@github.com:`

**验证修改结果：**

```bash
git remote -v
# origin  git@github.com:username/repo.git (fetch)
# origin  git@github.com:username/repo.git (push)
```

---

## 四、验证 SSH 连接

```bash
ssh -T git@github.com
# Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

出现上述提示说明配置成功。

---

## 五、测试推送

```bash
git push
# 不再提示输入密码，直接推送成功
```

---

## 常见问题

### ssh-add 问题（macOS/Linux）

如果设置了 passphrase，每次开机需要运行：

```bash
ssh-add ~/.ssh/id_ed25519
```

macOS 可以配置 `~/.ssh/config` 永久记住：

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

### Windows 上 SSH Agent 未启动

```powershell
# 以管理员身份运行 PowerShell
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent
ssh-add ~/.ssh/id_ed25519
```

### 多个 GitHub 账号

在 `~/.ssh/config` 中配置别名：

```
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal

Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
```

然后 remote 地址使用别名：

```bash
git remote set-url origin git@github-personal:username/repo.git
```
