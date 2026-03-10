---
title: Emoji 快捷输入
subtitle: Emoji 表情符号快速输入
stage: 第五阶段-效率工具
order: 02
author: 戴跃辉
date: 2026-03-06
tags: [效率工具, Emoji, 快捷输入]
prerequisites: 01-基础入门/03-markdown扩展语法
next: 03-SheetPlus电子表格
---

# Emoji 快捷输入

通过简写快速输入 Emoji 表情符号，提升笔记表现力。

---

## 📋 目录

- [插件简介](#插件简介)
- [安装配置](#安装配置)
- [常用代码](#常用代码)
- [自定义配置](#自定义配置)
- [使用场景](#使用场景)

---

## 插件简介

**Emoji Shortcodes** 插件允许使用简写代码快速输入 Emoji，无需记忆复杂的 Unicode 或频繁复制粘贴。

**主要优势**：
- 类似 GitHub 的 Emoji 简写语法
- 自动补全支持
- 可自定义映射关系
- 轻量级，无性能影响

---

## 安装配置

### 安装步骤

1. **搜索安装**
   - 设置 → 社区插件 → 浏览
   - 搜索 "Emoji Shortcodes"
   - 安装并启用

2. **基本配置**
   ```yaml
   # 默认配置
   Emoji Shortcodes:
     Trigger: :       # 触发符号
     Auto Complete: true
   ```

---

## 常用代码

### 文档相关

| 代码 | Emoji | 说明 |
|------|-------|------|
| `:memo:` | 📝 | 备忘录 |
| `:clipboard:` | 📋 | 剪贴板 |
| `:pencil:` | ✏️ | 铅笔 |
| `:book:` | 📖 | 书籍 |
| `:bookmark:` | 🔖 | 书签 |
| `:page_facing_up:` | 📄 | 文档 |
| `:file_folder:` | 📁 | 文件夹 |

### 状态标识

| 代码 | Emoji | 说明 |
|------|-------|------|
| `:white_check_mark:` | ✅ | 完成 |
| `:x:` | ❌ | 错误/关闭 |
| `:warning:` | ⚠️ | 警告 |
| `:no_entry:` | ⛔ | 禁止 |
| `:rotating_light:` | 🚨 | 紧急 |
| `:grey_question:` | ❓ | 疑问 |

### 进度标识

| 代码 | Emoji | 说明 |
|------|-------|------|
| `:rocket:` | 🚀 | 启动/快速 |
| `:construction:` | 🚧 | 施工中 |
| `:wrench:` | 🔧 | 工具/维修 |
| `:hammer:` | 🔨 | 锤子/开发 |
| `:gear:` | ⚙️ | 设置 |

### 学习相关

| 代码 | Emoji | 说明 |
|------|-------|------|
| `:graduation_cap:` | 🎓 | 毕业 |
| `:school:` | 🏫 | 学校 |
| `:books:` | 📚 | 书籍集合 |
| `:bulb:` | 💡 | 想法/灯泡 |
| `:thinking:` | 🤔 | 思考 |
| `:brain:` | 🧠 | 大脑 |

### 项目管理

| 代码 | Emoji | 说明 |
|------|-------|------|
| `:calendar:` | 📅 | 日历 |
| `:date:` | 📆 | 日历（撕页） |
| `:alarm_clock:` | ⏰ | 闹钟 |
| `:hourglass:` | ⏳ | 沙漏/等待 |
| `:checkered_flag:` | 🏁 | 终点/完成 |

---

## 自定义配置

### 添加自定义映射

**设置路径**：设置 → Emoji Shortcodes → Custom Shortcodes

```yaml
# 自定义示例
Custom Shortcodes:
  - shortcode: ":obsidian:"
    emoji: "🔷"
  - shortcode: ":git:"
    emoji: "📦"
  - shortcode: ":todo:"
    emoji: "☐"
  - shortcode: ":done:"
    emoji: "☑️"
```

### 使用场景示例

```markdown
# 项目状态
:construction: 进行中
:white_check_mark: 已完成
:x: 已取消

# 优先级
:rocket: 紧急
:warning: 重要
:grey_exclamation: 普通

# 文档类型
:memo: 笔记
:clipboard: 模板
:bookmark: 收藏
```

---

## 使用场景

### 场景1：任务清单

```markdown
## 今日任务

- [ ] :rocket: 完成项目文档
- [x] :white_check_mark: 代码审查
- [ ] :wrench: 修复 Bug #123
- [ ] :bulb: 技术调研
```

### 场景2：文档分类

```markdown
# :folder: 项目文档

## :memo: 需求文档
...

## :gear: 技术方案
...

## :books: 参考资料
...
```

### 场景3：状态标记

```markdown
| 任务 | 状态 | 优先级 |
|------|------|--------|
| 登录功能 | :white_check_mark: | :rocket: |
| 支付接口 | :construction: | :warning: |
| 数据优化 | :hourglass: | :grey_exclamation: |
```

---

## 高级技巧

### 1. 配合模板使用

**Templater 模板**：
```markdown
---
title: {{title}}
date: {{date}}
status: :construction:
priority: :warning:
---

# :memo: {{title}}
```

### 2. 结合 Dataview

```dataview
TABLE file.name, status, priority
FROM "Tasks"
WHERE !completed
```

### 3. 自动触发规则

```yaml
# 自动补全设置
Auto Complete Trigger:
  Minimum Characters: 2      # 最少输入字符
  Delay: 100                # 延迟(ms)
  Show In Menu: true        # 在菜单显示
```

---

## 常见问题

### Q1：输入简写后没有转换？

**A**：检查配置
- 确认插件已启用
- 检查触发符号是否为 `:`
- 尝试重启 Obsidian

### Q2：如何查看所有可用代码？

**A**：
- 查看 GitHub 项目文档
- 使用内置自动补全功能
- 参考官方 Emoji 列表

### Q3：与系统 Emoji 输入法冲突？

**A**：
- 修改触发符号（如改为 `;;`）
- 调整输入法优先级
- 禁用系统 Emoji 快捷键

---

## 相关资源

**插件地址**：https://github.com/obsidian-community/obsidian-emoji-shortcodes

**Emoji 参考**：
- [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet)
- [Unicode Emoji](https://unicode.org/emoji/charts/full-emoji-list.html)

**相关文档**：
- [01-EasyTyping自动排版](01-EasyTyping自动排版.md)
- [03-SheetPlus电子表格](../03-可视化工具/04-SheetPlus电子表格.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
