---
title: Git 版本控制
subtitle: Obsidian Git 集成与协作
stage: 第七阶段-团队协作
order: 04
author: 戴跃辉
date: 2026-03-06
tags: [Git, 版本控制, 协作, 插件]
plugin: https://github.com/denolehev/obsidian-git
prerequisites: markdown扩展语法
next: 06-Homepage主页配置
---

# Git 版本控制

Obsidian Git 插件让您的知识库具备完整的版本控制能力，实现自动备份、团队协作和历史追溯。

---

## 📋 目录

- [1. Git 版本控制简介](#1-git-版本控制简介)
- [2. 插件安装与配置](#2-插件安装与配置)
- [3. 基础使用](#3-基础使用)
- [4. 团队协作](#4-团队协作)
- [5. 高级功能](#5-高级功能)
- [6. 常见问题](#6-常见问题)

---

## 1. Git 版本控制简介

### 1.1 为什么使用 Git

**核心价值**：

- ✅ **版本追溯**：查看每次修改历史
- ✅ **自动备份**：推送到远程仓库
- ✅ **团队协作**：多人共享知识库
- ✅ **分支管理**：独立开发不影响主线
- ✅ **冲突解决**：合并不同版本

### 1.2 Obsidian Git 插件

**主要功能**：

- 自动提交更改
- 定时推送到远程
- 可视化查看差异
- 一键拉取更新
- 冲突解决辅助

---

## 2. 插件安装与配置

### 2.1 安装插件

**步骤**：

1. 设置 → 第三方插件
2. 浏览市场搜索 "Obsidian Git"
3. 安装并启用

### 2.2 基础配置

**配置路径**：设置 → Obsidian Git

#### 自动提交设置

```yaml
# 自动备份间隔（分钟）
Auto commit interval: 30

# 自动提交前保存
Auto-save before commit: true

# 提交信息格式
Commit message: "vault backup: {{date}}"
```

#### 推送设置

```yaml
# 自动推送
Auto-push interval: 60

# 拉取间隔
Auto-pull interval: 30

# 拉取前提交
Commit before pull: true
```

#### 同步行为

```yaml
# 自动拉取后提交
Commit & push after pull: true

# 同步设置
Sync method: merge  # merge | rebase | squash
```

### 2.3 Git 仓库初始化

**首次设置**：

1. **初始化 Git 仓库**

```bash
# 在知识库根目录
cd D:/workspace/wfg-dev-wiki
git init
```

2. **创建 .gitignore**

```gitignore
# .gitignore 内容
.obsidian/
.obsidian-plugins/
.trash/
.DS_Store
Thumbs.db
*.tmp
*.log
```

3. **首次提交**

```bash
git add .
git commit -m "Initial commit"
```

4. **连接远程仓库**

```bash
# Gitea 示例
git remote add origin https://git.wind.com.cn/username/wiki.git

# GitHub 示例
git remote add origin https://github.com/username/wiki.git
```

5. **首次推送**

```bash
git push -u origin main
```

---

## 3. 基础使用

### 3.1 插件界面

**Obsidian Git 界面**：

```
┌─────────────────────────────────────┐
│ Obsidian Git                        │
├─────────────────────────────────────┤
│ Source Control                      │
│ ├─ Changes (3)                      │
│ │  ├─ M 笔记.md                     │
│ │  ├─ A 新文档.md                   │
│ │  └─ D 旧文档.md                   │
│ │                                   │
│ ├─ Staged Changes                  │
│ │  └─ M 笔记.md                     │
│ │                                   │
│ ├─ Commit message                  │
│ │  └─ [_________________]           │
│ │                                   │
│ └─ [Commit] [Push] [Pull]          │
│                                     │
│ General                             │
│ ├─ Last commit: 2 minutes ago      │
│ ├─ Last pull: 5 minutes ago        │
│ └─ Branch: main                    │
└─────────────────────────────────────┘
```

### 3.2 日常操作

#### 提交更改

**方式一：命令面板**

1. `Ctrl/Cmd + P`
2. 输入 "Obsidian Git"
3. 选择 "Create backup"

**方式二：快捷键**

```
Ctrl/Cmd + S  →  自动保存
Auto commit    →  自动提交
```

#### 推送到远程

**命令**：

1. `Ctrl/Cmd + P`
2. "Obsidian Git: Push"

#### 拉取更新

**命令**：

1. `Ctrl/Cmd + P`
2. "Obsidian Git: Pull"

### 3.3 查看更改

**查看文件差异**：

1. 在 Source Control 中点击文件
2. 查看修改对比
3. 选择接受或拒绝更改

**差异视图示例**：

```
┌─────────────────────────────────────┐
│ 文件差异：笔记.md                   │
├─────────────────────────────────────┤
│ ← Old  │  New →                    │
│ ───────┼────────────────────────────│
│ - 旧内容                              │
│ + 新内容                              │
│   保留内容                            │
└─────────────────────────────────────┘
```

---

## 4. 团队协作

### 4.1 协作流程

**标准工作流**：

```
┌─────────┐
│ 开始工作 │
└────┬────┘
     │
     ↓
┌─────────┐
│ 拉取更新 │ ← Pull (获取最新)
└────┬────┘
     │
     ↓
┌─────────┐
│ 编辑笔记 │
└────┬────┘
     │
     ↓
┌─────────┐
│ 提交更改 │ ← Commit (本地提交)
└────┬────┘
     │
     ↓
┌─────────┐
│ 推送远程 │ ← Push (同步到服务器)
└────┬────┘
     │
     ↓
┌─────────┐
│ 重复循环 │
└─────────┘
```

### 4.2 多人协作最佳实践

**协作规则**：

> [!warning] 协作注意事项
> 1. **工作前先拉取**：确保获取最新更改
> 2. **小步提交**：频繁提交，避免大量冲突
> 3. **明确提交信息**：描述清楚修改内容
> 4. **及时推送**：提交后尽快推送到远程
> 5. **冲突沟通**：遇到冲突及时沟通

**提交信息规范**：

```bash
# 格式：[类型] 简短描述

feat: 新增用户登录功能
fix: 修复链接错误
docs: 更新 README
refactor: 重构目录结构
style: 修正错别字
test: 添加测试用例
chore: 更新依赖
```

### 4.3 冲突解决

**冲突示例**：

```
<<<<<<< HEAD
# 标题 A
内容 A
=======
# 标题 B
内容 B
>>>>>>> origin/main
```

**解决步骤**：

1. **识别冲突**
   - Git 会标记冲突区域
   - `=======` 分隔符区分两个版本

2. **选择保留内容**
   - 保留 HEAD（你的版本）
   - 保留 origin/main（远程版本）
   - 或者手动合并两者

3. **解决冲突**

```markdown
<!-- 解决后 -->
# 标题 A（合并版）
内容 A + 内容 B
```

4. **提交解决**

```bash
git add .
git commit -m "resolve: 解决文档冲突"
```

### 4.4 分支协作

**创建功能分支**：

```bash
# 创建并切换分支
git checkout -b feature/new-docs

# 或在 Obsidian Git 中
# 命令面板 → Create new branch
```

**分支工作流**：

```
main (主线)
  │
  ├─ feature/user-guide (用户文档分支)
  ├─ feature/api-docs (API 文档分支)
  └─ hotlink/fix-links (紧急修复分支)
```

**合并分支**：

```bash
# 切换到主线
git checkout main

# 拉取最新
git pull

# 合并分支
git merge feature/user-guide

# 推送
git push
```

---

## 5. 高级功能

### 5.1 自定义提交信息

**动态提交信息**：

```yaml
# 插件设置
Commit message: |
  {{date}} - {{time}}

  Files changed:
  {{files}}

  Author: {{author}}
```

**提交信息模板**：

```
vault backup: 2026-03-06 14:30

Files changed:
- M: 笔记.md
- A: 新文档.md
- D: 旧文档.md

Author: 戴跃辉
```

### 5.2 自动同步设置

**不同场景配置**：

**个人使用**：

```yaml
Auto commit interval: 30
Auto-push interval: 60
Auto-pull interval: 0  # 不自动拉取
```

**团队协作**：

```yaml
Auto commit interval: 15
Auto-push interval: 30
Auto-pull interval: 10  # 频繁拉取
Sync method: merge
```

**移动设备**：

```yaml
Auto commit interval: 5
Auto-push interval: 10
Auto-pull interval: 5
Commit before pull: true
```

### 5.3 Git 钩子

**配置 Git 钩子**：

**提交前检查**：

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 检查是否有大文件
git diff --cached --name-only | xargs ls -la | awk '$5 > 10485760 {print $9}' | while read file; do
  echo "Error: $file is too large (>10MB)"
  exit 1
done
```

**提交后通知**：

```bash
# .git/hooks/post-commit
#!/bin/bash

# 发送通知
echo "Backup completed: $(date)" >> .git/backup.log
```

### 5.4 与 Gitea 集成

**配置 Gitea Webhook**：

1. **在 Gitea 设置 Webhook**

```
URL: https://your-server/obsidian-sync
Secret: your-secret-key
Events: Push events
```

2. **自动同步脚本**

```bash
#!/bin/bash
# Webhook 处理脚本

cd /path/to/obsidian-vault
git pull origin main

# 可选：通知用户
notify-send "Obsidian" "知识库已同步"
```

---

## 6. 常见问题

### Q1：自动提交不工作？

**A**：检查以下几点

1. **确认 Git 已安装**

```bash
git --version
```

2. **确认仓库已初始化**

```bash
git status
```

3. **检查插件设置**

- Auto commit interval 是否 > 0
- Git path 是否正确

### Q2：推送失败怎么办？

**A**：常见原因和解决

**原因1：认证失败**

```bash
# 解决：配置 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 将公钥添加到 Gitea/GitHub
```

**原因2：远程仓库不存在**

```bash
# 解决：添加远程仓库
git remote add origin <repository-url>
```

**原因3：网络问题**

```bash
# 解决：检查网络连接
ping git.wind.com.cn
```

### Q3：如何处理大量冲突？

**A**：使用策略

**策略1：使用远程版本**

```bash
git pull --strategy=theirs origin main
```

**策略2：使用本地版本**

```bash
git pull --strategy=ours origin main
```

**策略3：手动合并**

```bash
git fetch origin
git merge origin/main
# 手动解决冲突
```

### Q4：如何回滚到之前的版本？

**A**：使用 Git 历史回滚

**查看历史**：

```bash
git log --oneline
```

**回滚到指定版本**：

```bash
# 方式1：软回滚（保留更改）
git reset --soft <commit-hash>

# 方式2：硬回滚（丢弃更改）
git reset --hard <commit-hash>

# 方式3：回滚并推送
git revert <commit-hash>
```

### Q5：如何优化大仓库性能？

**A**：性能优化建议

1. **浅克隆**

```bash
git clone --depth 1 <repository-url>
```

2. **稀疏检出**

```bash
git sparse-checkout init
git sparse-checkout set "重要目录"
```

3. **定期清理**

```bash
git gc --aggressive
```

---

## 7. 快捷键速查

| 快捷键 | 功能 |
|--------|------|
| `Ctrl/Cmd + P` → "Create backup" | 创建备份 |
| `Ctrl/Cmd + P` → "Pull" | 拉取更新 |
| `Ctrl/Cmd + P` → "Push" | 推送远程 |
| `Ctrl/Cmd + P` → "View diff" | 查看差异 |

---

## 8. 下一步学习

- [06-Homepage主页配置](../附录/A-插件速查手册.md) - 主页配置
- [07-团队协作/01-知识库架构设计](01-知识库架构设计.md) - 团队协作实践
- [09-外部工具集成/04-第三方工具集成](../09-外部工具集成/04-第三方工具集成.md) - Gitea 集成详解

---

**文档版本**：v2.0
**最后更新**：2026-03-06
**相关文档**：[04-双链与标签系统](../01-基础入门/04-双链与标签系统.md) | [07-团队协作/01-知识库架构设计](01-知识库架构设计.md)
