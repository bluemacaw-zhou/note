---
title: Bases 数据库
subtitle: Obsidian 内置数据库功能
stage: 第二阶段-核心插件
order: 02
author: 戴跃辉
date: 2026-03-06
tags: [核心插件, Bases, 数据库]
prerequisites: 01-基础入门/03-markdown扩展语法
next: 03-Obsidian Query语法
---

# Bases 数据库

Obsidian 内置的数据库功能，类似 Notion Database。

---

## 📋 目录

- [功能简介](#功能简介)
- [创建数据库](#创建数据库)
- [数据类型](#数据类型)
- [视图类型](#视图类型)
- [实用案例](#实用案例)

---

## 功能简介

**Bases** 是 Obsidian 1.5+ 版本引入的核心功能，无需安装插件。

**核心特性**：
- 创建数据库视图
- 多种视图类型（表格、看板、日历等）
- 基于 frontmatter 的数据源
- 实时数据同步

---

## 创建数据库

### 创建 Base 文件

**方法1：命令面板**
```
1. Ctrl/Cmd + P 打开命令面板
2. 输入 "Create a new base"
3. 选择数据源文件夹
4. 配置字段和视图
```

**方法2：手动创建**
```markdown
<!-- 创建 .base 文件 -->
```yaml
type: base
datasource: 路径/到/文件夹
fields:
  - name: title
    type: text
  - name: status
    type: select
    options: [待办, 进行中, 已完成]
```
```

---

## 数据类型

### 支持的字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| text | 文本 | 标题、描述 |
| number | 数字 | 优先级、进度 |
| select | 单选 | 状态、类别 |
| multi-select | 多选 | 标签 |
| date | 日期 | 截止日期 |
| checkbox | 复选框 | 完成标记 |
| list | 列表 | 子任务 |

---

## 视图类型

### 1. 表格视图

默认视图，类似电子表格。

### 2. 看板视图

按状态分列显示。

### 3. 日历视图

按日期展示。

### 4. 画廊视图

卡片式展示。

---

## 实用案例

### 案例1：任务追踪

```markdown
<!-- tasks.base -->
```yaml
type: base
datasource: Tasks
fields:
  - name: 任务名称
  - name: 状态
    type: select
    options: [待办, 进行中, 已完成]
  - name: 优先级
    type: select
    options: [高, 中, 低]
  - name: 截止日期
    type: date
```
```

### 案例2：项目管理

```markdown
<!-- projects.base -->
```yaml
type: base
datasource: Projects
fields:
  - name: 项目名称
  - name: 负责人
  - name: 进度
    type: number
  - name: 状态
    type: select
    options: [规划, 开发, 测试, 上线]
```
```

---

## 与 Dataview 对比

| 功能 | Bases | Dataview |
|------|-------|----------|
| 类型 | 核心功能 | 插件 |
| 数据源 | .base 文件 | 任意 markdown |
| 查询 | 可视化配置 | 查询语言 |
| 灵活性 | 中等 | 高 |

---

## 最佳实践

> [!tip] 使用建议
> 1. **明确数据源**：指定清晰的数据文件夹
> 2. **字段规范**：使用一致的字段名称
> 3. **视图管理**：创建多种视图满足不同需求
> 4. **定期维护**：清理无效数据

---

**文档版本**：v2.0
**最后更新**：2026-03-06
