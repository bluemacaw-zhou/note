---
title: Bases 数据库管理
subtitle: 项目中的数据库应用
stage: 第四阶段-项目管理
order: 04
author: 戴跃辉
date: 2026-03-06
tags: [项目管理, Bases, 数据库]
prerequisites: 02-核心插件/02-Bases数据库
next: 02-Dataview数据查询
---

# Bases 数据库管理

在项目管理中使用 Bases 数据库。

---

## 📋 目录

- [项目数据库](#项目数据库)
- [任务管理](#任务管理)
- [进度追踪](#进度追踪)
- [实践案例](#实践案例)

---

## 项目数据库

### 创建项目 Base

**结构设计**：
```yaml
type: base
datasource: Projects
fields:
  - name: 项目名称
  - name: 状态
    type: select
    options: [规划, 开发, 测试, 上线, 归档]
  - name: 优先级
    type: select
    options: [P0, P1, P2, P3]
  - name: 负责人
    type: text
  - name: 开始日期
    type: date
  - name: 截止日期
    type: date
  - name: 进度
    type: number
```

---

## 任务管理

### 任务 Base

**字段设置**：
```yaml
fields:
  - name: 任务标题
  - name: 描述
    type: text
  - name: 状态
    type: select
    options: [待办, 进行中, 已完成, 已取消]
  - name: 类型
    type: select
    options: [功能, Bug, 优化, 文档]
  - name: 优先级
    type: select
    options: [紧急, 高, 中, 低]
  - name: 指派给
    type: text
  - name: 截止日期
    type: date
```

### 视图配置

**看板视图**：
- 按状态分列
- 拖拽更新状态

**日历视图**：
- 按截止日期展示
- 快速查看时间线

---

## 进度追踪

### 项目进度 Base

```yaml
fields:
  - name: 里程碑
  - name: 完成度
    type: number
  - name: 状态
    type: select
    options: [未开始, 进行中, 已完成, 延期]
  - name: 负责人
  - name: 计划日期
    type: date
  - name: 实际日期
    type: date
```

---

## 实践案例

### 案例1：敏捷开发项目

**项目 Base**：
```markdown
<!-- agile-projects.base -->
- 查看所有冲刺（Sprint）
- 跟踪用户故事
- 管理任务分配
```

### 案例2：产品路线图

**路线图 Base**：
```markdown
<!-- roadmap.base -->
- 时间线视图
- 功能规划
- 版本管理
```

---

## 与 Dataview 结合

**优势互补**：
- **Bases**：可视化管理，拖拽操作
- **Dataview**：复杂查询，数据分析

**配合使用**：
```markdown
<!-- Bases 管理日常任务 -->
<!-- Dataview 生成报表和统计 -->
```

---

## 最佳实践

> [!tip] 使用建议
> 1. **字段统一**：使用统一的字段命名
> 2. **数据规范**：建立数据输入规范
> 3. **定期维护**：清理无效数据
> 4. **备份重要**：定期备份数据

---

**文档版本**：v2.0
**最后更新**：2026-03-06
