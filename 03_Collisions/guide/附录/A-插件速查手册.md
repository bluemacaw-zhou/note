---
title: 插件速查手册
subtitle: Obsidian 常用插件快速参考
stage: 附录
order: A
author: 戴跃辉
date: 2026-03-06
tags: [插件, 速查手册]
---

# 插件速查手册

Obsidian 常用插件快速参考指南。

---

## 📋 目录

- [核心基础设施](#核心基础设施)
- [可视化与绘图](#可视化与绘图)
- [项目与任务管理](#项目与任务管理)
- [编辑增强与效率](#编辑增强与效率)
- [内容组织与展示](#内容组织与展示)
- [媒体与数据处理](#媒体与数据处理)

---

## 核心基础设施

### obsidian-git
**用途**：Git 版本控制
**安装**：社区插件市场搜索 "obsidian-git"
**配置**：
```yaml
Auto commit interval: 30
Auto-push interval: 60
Auto-pull interval: 30
```
**文档**：[05-Git版本控制](../07-团队协作/04-Git版本控制.md)

### templater-obsidian
**用途**：高级模板系统
**安装**：社区插件市场搜索 "Templater"
**配置**：
```yaml
Template folder location: templates
Trigger on new file creation: true
```
**文档**：[03-Templater模板系统](../05-效率工具/06-Templater模板系统.md)

### dataview
**用途**：数据查询和展示
**安装**：社区插件市场搜索 "Dataview"
**查询示例**：
````dataview
TABLE file.name, tags
FROM ""
WHERE tags
````
**文档**：[02-Dataview数据查询](../04-项目管理/02-Dataview数据查询.md)

---

## 可视化与绘图

### obsidian-excalidraw-plugin
**用途**：手绘风格绘图
**安装**：内置插件
**文档**：[07-Excalidraw手绘指南](../03-可视化工具/03-Excalidraw手绘指南.md)

### advanced-canvas
**用途**：Canvas 白板增强
**安装**：社区插件市场搜索 "Advanced Canvas"

### obsidian-mindmap-nextgen
**用途**：思维导图生成
**安装**：社区插件市场搜索 "Mindmap"

### obsidian-charts
**用途**：图表生成
**安装**：社区插件市场搜索 "Charts"

---

## 项目与任务管理

### obsidian-projects
**用途**：项目管理
**安装**：社区插件市场搜索 "Projects"

### obsidian-kanban
**用途**：看板管理
**安装**：社区插件市场搜索 "Kanban"

### calendar
**用途**：日历视图
**安装**：社区插件市场搜索 "Calendar"

### obsidian-task-progress-bar
**用途**：任务进度条
**安装**：社区插件市场搜索 "Task Progress Bar"

---

## 编辑增强与效率

### easy-typing-obsidian
**用途**：中英文自动排版
**安装**：社区插件市场搜索 "EasyTyping"
**文档**：[01-EasyTyping自动排版](../05-效率工具/01-EasyTyping自动排版.md)

### emoji-shortcodes
**用途**：Emoji 快捷输入
**安装**：社区插件市场搜索 "Emoji Shortcodes"
**文档**：[02-Emoji快捷输入](../05-效率工具/02-Emoji快捷输入.md)

### image-converter
**用途**：图片转换
**安装**：社区插件市场搜索 "Image Converter"

### sheet-plus
**用途**：电子表格
**安装**：社区插件市场搜索 "SheetPlus"
**文档**：[03-SheetPlus电子表格](../03-可视化工具/04-SheetPlus电子表格.md)

---

## 内容组织与展示

### obsidian-style-settings
**用途**：样式设置
**安装**：社区插件市场搜索 "Style Settings"
**文档**：[01-StyleSettings配置](../06-样式与美化/01-StyleSettings配置.md)

### obsidian-icon-folder
**用途**：文件夹图标
**安装**：社区插件市场搜索 "Icon Folder"
**文档**：[02-图标与标签](../06-样式与美化/02-图标与标签.md)

### highlightr-plugin
**用途**：内容高亮
**安装**：社区插件市场搜索 "Highlightr"
**文档**：[03-高亮与提示块](../06-样式与美化/03-高亮与提示块.md)

### colored-tags
**用途**：彩色标签
**安装**：社区插件市场搜索 "Colored Tags"

### obsidian-admonition
**用途**：提示块
**安装**：社区插件市场搜索 "Admonition"

---

## 媒体与数据处理

### pdf-plus
**用途**：PDF 阅读增强
**安装**：社区插件市场搜索 "PDF++"
**文档**：[05-PDF与导入工具](../05-效率工具/05-PDF与导入工具.md)

### obsidian-importer
**用途**：内容导入器
**安装**：社区插件市场搜索 "Importer"

### media-extended
**用途**：媒体扩展
**安装**：社区插件市场搜索 "Media Extended"

### copilot
**用途**：AI 助手
**安装**：社区插件市场搜索 "Copilot"
**文档**：[01-Copilot配置指南](../08-AI集成/01-Copilot配置指南.md)

---

## 快速查找

### 按功能分类

**版本控制**：
- obsidian-git

**模板系统**：
- templater-obsidian
- quickadd

**数据查询**：
- dataview

**项目管理**：
- obsidian-projects
- obsidian-kanban
- calendar

**绘图工具**：
- obsidian-excalidraw-plugin
- advanced-canvas
- obsidian-mindmap-nextgen

**编辑增强**：
- easy-typing-obsidian
- emoji-shortcodes
- sheet-plus

**样式美化**：
- obsidian-style-settings
- obsidian-icon-folder
- colored-tags
- highlightr-plugin

**PDF/导入**：
- pdf-plus
- obsidian-importer
- image-converter

**AI 集成**：
- copilot

---

**文档版本**：v2.0
**最后更新**：2026-03-06
