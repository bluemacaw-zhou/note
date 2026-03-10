---
title: Obsidian Query 语法
subtitle: 内置查询语言完全指南
stage: 第二阶段-核心插件
order: 03
author: 戴跃辉
date: 2026-03-06
tags: [核心插件, Query, 查询]
prerequisites: 02-核心插件/02-Bases数据库
next: 03-可视化工具/01-思维导图工具
---

# Obsidian Query 语法

Obsidian 内置的查询语言，用于筛选和展示笔记。

---

## 📋 目录

- [语法基础](#语法基础)
- [查询类型](#查询类型)
- [常用示例](#常用示例)
- [实践案例](#实践案例)

---

## 语法基础

### 基本结构

````markdown
```query
文件路径
标签
条件
```
````

### 简单查询

**按路径**：
````markdown
```query
path:"Projects/"
```
````

**按标签**：
````markdown
```query
tag:#重要
```
```

**按文件名**：
````markdown
```query
file:"会议"
```
```

---

## 查询类型

### 1. 组合查询

**AND 条件**：
````markdown
```query
path:"Projects/" tag:#进行中
```
````

**OR 条件**：
````markdown
```query
tag:#重要 OR tag:#紧急
```
````

**NOT 条件**：
````markdown
```query
path:"Projects/" -tag:#已完成
```
````

### 2. 高级查询

**按时间**：
````markdown
```query
created:2026-03-01..
```
````

**按内容**：
````markdown
```query
"关键词"
```
````

---

## 常用示例

### 示例1：查找项目笔记

````markdown
```query
path:"Projects/" file:"项目"
```
````

### 示例2：查找待办任务

````markdown
```query
task:"TODO"
```
````

### 示例3：查找本周笔记

````markdown
```query
created:2026-03-01..
```
````

---

## 实践案例

### 案例1：快速查找

**查找重要未完成任务**：
````markdown
```query
path:"Tasks/" tag:#重要 -file:"已完成"
```
````

### 案例2：项目管理

**查找当前进行中的项目**：
````markdown
```query
path:"Projects/" tag:#进行中
```
````

---

## 与 Dataview 对比

| 功能 | Obsidian Query | Dataview |
|------|---------------|----------|
| 类型 | 内置功能 | 插件 |
| 语法 | 简单 | 复杂 |
| 查询能力 | 基础 | 强大 |
| 学习曲线 | 低 | 高 |

---

## 最佳实践

> [!tip] 使用建议
> 1. **从简单开始**：先掌握基本查询
> 2. **逐步组合**：使用 AND/OR 组合条件
> 3. **保存常用查询**：在模板中保存常用查询
> 4. **结合使用**：与 Bases 和 Dataview 配合使用

---

**文档版本**：v2.0
**最后更新**：2026-03-06
