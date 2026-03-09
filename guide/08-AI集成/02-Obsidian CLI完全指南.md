---
title: Obsidian CLI 完全指南
subtitle: 命令行工具完整使用手册
stage: 第九阶段-外部工具集成
order: 02
author: 戴跃辉
date: 2026-03-06
tags: [外部工具, CLI, 命令行]
prerequisites: 09-外部工具集成/01-Obsidian Web Clipper
next: 03-自动化脚本集成
---

# Obsidian CLI 完全指南

使用命令行工具管理和操作 Obsidian vault。

---

## 📋 目录

- [CLI 简介](#cli-简介)
- [安装配置](#安装配置)
- [核心命令](#核心命令)
- [实战案例](#实战案例)

---

## CLI 简介

**Obsidian CLI** (obsidian-cli) 是官方命令行工具。

**主要功能**：
- 管理多个 vault
- 创建和编辑笔记
- 搜索内容
- 插件管理
- 自动化脚本

**适用场景**：
- 自动化工作流
- CI/CD 集成
- 批量操作
- 远程管理

---

## 安装配置

### 安装 CLI

**通过 npm 安装**：
```bash
npm install -g obsidian-cli
```

**验证安装**：
```bash
obsidian-cli --version
# 或
obsidian --version
```

### 基础配置

**配置文件**：
```yaml
~/.obsidian-cli/config.yaml
```

**常用配置**：
```yaml
vaults:
  default: /path/to/vault
  work: /path/to/work/vault

editor:
  command: code
  args: ["--wait"]

open:
  command: open
```

---

## 核心命令

### 1. Vault 管理

**列出所有 vault**：
```bash
obsidian vault list
```

**打开 vault**：
```bash
obsidian vault open /path/to/vault
```

**获取 vault 信息**：
```bash
obsidian vault info /path/to/vault
```

### 2. 笔记操作

**创建笔记**：
```bash
obsidian new /path/to/vault "笔记标题"
# 或指定路径
obsidian new /path/to/vault "文件夹/笔记标题"
```

**编辑笔记**：
```bash
obsidian edit /path/to/vault "笔记标题"
```

**删除笔记**：
```bash
obsidian delete /path/to/vault "笔记标题"
```

### 3. 搜索功能

**搜索笔记**：
```bash
obsidian search /path/to/vault "搜索关键词"
```

**高级搜索**：
```bash
obsidian search /path/to/vault \
  --tag "工作" \
  --created-after "2026-03-01" \
  --sort-by "created"
```

**搜索内容**：
```bash
obsidian search /path/to/vault \
  --content "特定内容"
```

### 4. 插件管理

**列出插件**：
```bash
obsidian plugin list /path/to/vault
```

**启用插件**：
```bash
obsidian plugin enable /path/to/vault dataview
```

**禁用插件**：
```bash
obsidian plugin disable /path/to/vault dataview
```

**重新加载插件**：
```bash
obsidian plugin reload /path/to/vault
```

---

## 实战案例

### 案例1：自动化日报

**脚本**：
```bash
#!/bin/bash
# daily_report.sh

VAULT_PATH="/path/to/vault"
DATE=$(date +%Y-%m-%d)
TITLE="日报-$DATE"
CONTENT="# $DATE\n\n## 今日工作\n\n## 明日计划\n"

obsidian new "$VAULT_PATH" "$TITLE"
echo -e "$CONTENT" >> "$VAULT_PATH/$TITLE.md"
obsidian edit "$VAULT_PATH" "$TITLE"
```

**使用**：
```bash
chmod +x daily_report.sh
./daily_report.sh
```

### 案例2：批量导入

**Python 脚本**：
```python
#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

VAULT_PATH = "/path/to/vault"
SOURCE_DIR = "/path/to/files"

def import_files():
    for file in Path(SOURCE_DIR).glob("*.md"):
        title = file.stem
        content = file.read_text()

        # 创建笔记
        subprocess.run([
            "obsidian", "new",
            VAULT_PATH, title
        ])

        # 写入内容
        note_path = f"{VAULT_PATH}/{title}.md"
        with open(note_path, 'w') as f:
            f.write(content)

        print(f"Imported: {title}")

if __name__ == "__main__":
    import_files()
```

### 案例3：备份脚本

**Shell 脚本**：
```bash
#!/bin/bash
# backup_vault.sh

VAULT_PATH="/path/to/vault"
BACKUP_DIR="/path/to/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份
tar -czf "$BACKUP_DIR/vault_$DATE.tar.gz" \
  -C "$VAULT_PATH" .

# 保留最近 7 天的备份
find "$BACKUP_DIR" -name "vault_*.tar.gz" \
  -mtime +7 -delete

echo "Backup completed: vault_$DATE.tar.gz"
```

### 案例4：链接检查

**Python 脚本**：
```python
#!/usr/bin/env python3
import re
from pathlib import Path
import subprocess

VAULT_PATH = "/path/to/vault"

def find_broken_links():
    md_files = list(Path(VAULT_PATH).rglob("*.md"))
    broken_links = []

    for file in md_files:
        content = file.read_text()
        # 查找 wiki 链接
        links = re.findall(r'\[\[([^\]]+)\]\]', content)

        for link in links:
            link_path = Path(VAULT_PATH) / f"{link}.md"
            if not link_path.exists():
                broken_links.append({
                    'file': str(file.relative_to(VAULT_PATH)),
                    'link': link
                })

    return broken_links

if __name__ == "__main__":
    broken = find_broken_links()
    if broken:
        print("Broken links found:")
        for item in broken:
            print(f"  {item['file']}: [[{item['link']}]]")
    else:
        print("No broken links!")
```

---

## 高级用法

### 1. 集成到 CI/CD

**Jenkins Pipeline**：
```groovy
pipeline {
    agent any
    stages {
        stage('Test Links') {
            steps {
                sh 'python scripts/check_links.py'
            }
        }
        stage('Generate Docs') {
            steps {
                sh '''
                    obsidian export /path/to/vault \
                      --format pdf \
                      --output ./docs/
                '''
            }
        }
    }
}
```

### 2. Git Hooks

**Pre-commit Hook**：
```bash
#!/bin/bash
# .git/hooks/pre-commit

# 检查链接
python scripts/check_links.py
if [ $? -ne 0 ]; then
  echo "存在失效链接，请修复后再提交"
  exit 1
fi

# 格式化 frontmatter
python scripts/format_frontmatter.py
```

### 3. 定时任务

**Crontab**：
```bash
# 每天早上 9 点创建日报
0 9 * * * /path/to/daily_report.sh

# 每小时备份
0 * * * * /path/to/backup_vault.sh

# 每周日凌晨 2 点检查链接
0 2 * * 0 /path/to/check_links.py
```

---

## 最佳实践

> [!tip] 使用建议
> 1. **脚本化**：将常用操作编写成脚本
> 2. **错误处理**：添加错误处理和日志
> 3. **权限控制**：注意脚本执行权限
> 4. **测试验证**：在生产使用前充分测试

---

## 常见问题

### Q1：命令找不到？

**A**：
- 确认已全局安装
- 检查 PATH 环境变量
- 尝试重启终端

### Q2：权限问题？

**A**：
```bash
# Linux/Mac
chmod +x script.sh

# Windows
# 以管理员身份运行
```

### Q3：路径包含空格？

**A**：
```bash
# 使用引号
obsidian new "/path/with spaces/vault" "title"
```

---

## 相关资源

**项目地址**：https://github.com/obsidianmd/obsidian-cli

**相关文档**：
- [01-Obsidian Web Clipper](../09-外部工具集成/01-Obsidian Web Clipper.md)
- [03-自动化脚本集成](../09-外部工具集成/03-自动化脚本集成.md)
- [04-第三方工具集成](../09-外部工具集成/04-第三方工具集成.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
