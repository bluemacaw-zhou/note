---
title: Dataview 数据查询
subtitle: 让知识库动起来
stage: 第四阶段-项目管理
order: 02
author: 戴跃辉
date: 2026-03-06
tags: [Dataview, 查询, 数据, 插件]
prerequisites: 01-基础入门/04-双链与标签系统
plugin: https://github.com/blacksmithgu/obsidian-dataview
---

# Dataview 数据查询

Dataview 是 Obsidian 最强大的插件之一，它将您的 Markdown 笔记变成**可查询的数据库**。通过 Dataview，您可以：

- 自动生成目录和索引
- 追踪任务和项目进度
- 统计和分析数据
- 创建动态仪表盘

---

## 📋 目录

- [1. 插件安装与配置](#1-插件安装与配置)
- [2. 基础查询语法](#2-基础查询语法)
- [3. 常用查询示例](#3-常用查询示例)
- [4. 高级查询技巧](#4-高级查询技巧)
- [5. 实战案例](#5-实战案例)
- [6. 与其他插件集成](#6-与其他插件集成)

---

## 1. 插件安装与配置

### 1.1 安装步骤

1. 打开 `设置` → `第三方插件`
2. 搜索 `Dataview`
3. 安装并启用

### 1.2 基础配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| **Enable JavaScript Queries** | ✅ 启用 | 支持更强大的查询 |
| **Render Inline Queries** | ✅ 启用 | 在行内渲染查询结果 |
| **Automatic View Refresh** | ✅ 启用 | 自动刷新查询结果 |
| **Pretty Render Inline Fields** | ✅ 启用 | 美化行内字段显示 |

### 1.3 Dataview 语法

有两种语法模式：

**Dataview 查询语言**（推荐新手）：
````markdown
```dataview
TABLE file.ctime as "创建时间"
FROM #项目
SORT file.ctime DESC
```
````

**Dataview JS**（高级用户）：
````markdown
```dataviewjs
dv.table(["文件", "标签"],
  dv.pages("#project")
    .sort(p => p.file.ctime, "desc")
    .map(p => [p.file.link, p.tags])
)
```
````

> [!tip] 选择建议
> - **简单查询**：用 Dataview 查询语言
> - **复杂逻辑**：用 Dataview JS

---

## 2. 基础查询语法

### 2.1 TABLE 查询

**基础语法**：
````markdown
```dataview
TABLE file.name, file.ctime, tags
FROM #项目
```
````

**自定义列名**：
````markdown
```dataview
TABLE
  file.name as "文件名",
  file.ctime as "创建时间",
  tags as "标签"
FROM #项目
```
````

**无 ID 列**：
````markdown
```dataview
TABLE without id
  file.link as "文档",
  status as "状态",
  priority as "优先级"
FROM #需求
```
````

### 2.2 LIST 查询

**简单列表**：
````markdown
```dataview
LIST
FROM #项目
```
````

**带元数据的列表**：
````markdown
```dataview
LIST status, file.ctime
FROM #项目
SORT file.ctime DESC
```
````

**嵌套列表**：
````markdown
```dataview
LIST rows.file.link
FROM #项目
GROUP BY file.folder
```
````

### 2.3 TASK 查询

**查询所有任务**：
````markdown
```dataview
TASK
FROM #Sprint23
```
````

**未完成任务**：
````markdown
```dataview
TASK
WHERE !completed
FROM #Sprint23
```
````

**按优先级分组**：
````markdown
```dataview
TASK
WHERE !completed
FROM #Sprint23
GROUP BY priority
SORT due ASC
```
````

**逾期任务**：
````markdown
```dataview
TASK
WHERE due < date(today) AND !completed
FROM #任务
SORT due ASC
```
````

---

## 3. 常用查询示例

### 3.1 项目统计

**项目进度追踪**：
````markdown
```dataview
## 📊 项目进度

TABLE without id
  sumCompleted as "已完成",
  sumTotal as "总数",
  round((sumCompleted / sumTotal) * 100) as "%完成率"
FROM #Sprint23
WHERE completed >= date(today) - dur(7 days)
GROUP BY true
```
````

### 3.2 文档索引

**所有需求文档**：
````markdown
```dataview
## 📋 需求文档索引

TABLE without id
  file.link as "文档",
  status as "状态",
  priority as "优先级",
  file.ctime as "创建日期"
FROM #类型/需求
SORT priority DESC, file.ctime DESC
```
````

**最近更新的文档**：
````markdown
```dataview
## 🕐 最近更新

LIST file.mtime + " 📝 " + status
FROM -"templates"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```
````

### 3.3 任务管理

**今日任务**：
````markdown
```dataview
## 📅 今日任务

TASK
WHERE due = date(today)
GROUP BY priority
SORT due ASC
```
````

**本周任务**：
````markdown
```dataview
## 📆 本周任务

TASK
WHERE due >= date(today) AND due <= date(today) + dur(6 days)
GROUP BY file.folder
SORT due ASC
```
````

**按负责人分组**：
````markdown
```dataview
## 👥 任务分配

TABLE without id
  rows.text as "任务"
FROM #任务
WHERE !completed
GROUP BY author
SORT author ASC
```
````

### 3.4 标签统计

**标签使用统计**：
````markdown
```dataview
## 🏷️ 标签统计

TABLE without id
  rows.file.link as "文档"
FROM ""
FLATTEN file.tags as tag
GROUP BY tag
SORT length(rows) DESC
```
````

---

## 4. 高级查询技巧

### 4.1 WHERE 条件

**日期查询**：
````markdown
```dataview
TABLE file.link
WHERE file.ctime > date("2026-01-01")
```
````

**标签查询**：
````markdown
```dataview
TABLE file.link
WHERE contains(tags, "项目")
```
````

**字段查询**：
````markdown
```dataview
TABLE file.link
WHERE status = "进行中" AND priority = "高"
```
````

**组合条件**：
````markdown
```dataview
TABLE file.link
WHERE (status = "进行中" OR status = "待办")
AND priority = "高"
```
````

### 4.2 SORT 排序

**单字段排序**：
````markdown
```dataview
TABLE file.link, file.ctime
SORT file.ctime DESC
```
````

**多字段排序**：
````markdown
```dataview
TABLE file.link, priority, status
SORT priority DESC, file.ctime ASC
```
````

### 4.3 GROUP BY 分组

**按文件夹分组**：
````markdown
```dataview
TABLE rows.file.link
GROUP BY file.folder
```
````

**按标签分组**：
````markdown
```dataview
TABLE rows.file.link
FROM #项目
FLATTEN file.tags as tag
GROUP BY tag
```
````

**按字段分组**：
````markdown
```dataview
TABLE without id
  rows.file.link as "任务",
  length(rows) as "数量"
FROM #任务
GROUP BY status
```
````

### 4.4 常用函数

**日期函数**：
````markdown
```dataview
TABLE
  date(today) as "今天",
  date(now) as "现在",
  file.ctime as "创建时间",
  file.mtime as "修改时间"
```
````

**字符串函数**：
````markdown
```dataview
TABLE
  upper(file.name) as "大写",
  lower(file.name) as "小写",
  substring(file.name, 0, 5) as "前5字符"
```
````

**数学函数**：
````markdown
```dataview
TABLE without id
  sum(rows.amount) as "总计",
  average(rows.amount) as "平均",
  length(rows) as "数量"
FROM #财务
GROUP BY category
```
````

---

## 5. 实战案例

### 5.1 项目仪表盘

**项目主页**：
````markdown
---
tags: [项目, 用户中心]
status: 进行中
---

# 用户中心项目

## 📊 项目概览

| 项目 | 内容 |
|------|------|
| **状态** | [状态](状态.md) |
| **进度** | 🟡 65% |
| **开始时间** | 📅 2026-03-01 |
| **预计完成** | 📅 2026-06-30 |

## 📋 需求追踪

```dataview
TABLE without id
  file.link as "需求",
  status as "状态",
  priority as "优先级"
FROM [用户中心项目](用户中心项目.md) AND #类型/需求
SORT priority DESC
```

## 🚀 开发进度

```dataview
TABLE without id
  file.link as "任务",
  status as "状态",
  due as "截止日期"
FROM [用户中心项目](用户中心项目.md) AND #任务
WHERE !completed
SORT due ASC
```

## 📈 统计数据

```dataview
TABLE without id
  length(filter(rows, (r) => r.status = "已完成")) as "已完成",
  length(filter(rows, (r) => r.status = "进行中")) as "进行中",
  length(rows) as "总数"
FROM [用户中心项目](用户中心项目.md)
GROUP BY true
```
````

### 5.2 学习笔记索引

**主题学习页面**：
````markdown
---
tags: [主题索引, SpringBoot]
---

# SpringBoot 学习笔记

## 📚 学习资源

```dataview
LIST
FROM #SpringBoot AND #学习笔记
SORT file.ctime DESC
```

## 🗂️ 核心概念

```dataview
TABLE without id
  file.link as "概念",
  summary as "摘要"
FROM #SpringBoot AND #核心概念
SORT file.name ASC
```

## 💡 实战案例

```dataview
TABLE without id
  file.link as "案例",
  difficulty as "难度",
  tags as "相关技术"
FROM #SpringBoot AND #实战
SORT difficulty DESC
```

## 📝 学习记录

```dataview
TABLE without id
  dateformat(file.ctime, "yyyy-MM-dd") as "日期",
  file.link as "笔记",
  tags as "标签"
FROM #SpringBoot
SORT file.ctime DESC
```
````

### 5.3 会议记录管理

**会议索引**：
````markdown
---
tags: [会议索引]
---

# 会议记录索引

## 📅 最近的会议

```dataview
TABLE without id
  dateformat(date, "yyyy-MM-dd") as "日期",
  file.link as "会议",
  attendees as "参会人员",
  action_items as "行动项"
FROM #会议记录
WHERE date >= date(today) - dur(30 days)
SORT date DESC
```

## 👥 按参会人查找

```dataview
LIST
FROM #会议记录
WHERE contains(attendees, "张三")
SORT date DESC
```

## ⚠️ 待办事项

```dataview
TASK
FROM #会议记录
WHERE contains(tags, "待办")
GROUP BY file.link
```
````

---

## 6. 与其他插件集成

### 6.1 与 Tasks 插件集成

**查询 Tasks 任务**：
````markdown
```dataview
TASK
WHERE !completed
GROUP BY priority
SORT due ASC
```
````

**高级任务查询**：
````markdown
```dataview
TASK
WHERE !completed
AND due < date(today) + dur(7 days)
AND contains(tags, "紧急")
GROUP BY file.folder
```
````

### 6.2 与 Kanban 集成

**统计看板数据**：
````markdown
```dataview
## 看板统计

TABLE without id
  length(filter(rows, (r) => contains(r, "待办"))) as "待办",
  length(filter(rows, (r) => contains(r, "进行中"))) as "进行中",
  length(filter(rows, (r) => contains(r, "已完成"))) as "已完成"
FROM ""
WHERE file.path = this.file.path
GROUP BY true
```
````

### 6.3 与 Calendar 集成

**今日任务**（从 Calendar 日记）：
````markdown
```dataview
TASK
WHERE file.path = this.file.path
WHERE due = date(today)
```
````

**本周总结**：
````markdown
```dataview
TABLE without id
  dateformat(date, "yyyy-MM-dd") as "日期",
  summary as "摘要",
  mood as "心情"
FROM "📅 日志"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```
````

---

## 7. Dataview JS 高级用法

### 7.1 基础 JS 查询

**Hello World**：
````markdown
```dataviewjs
dv.paragraph("Hello, Dataview JS!");
```
````

**简单表格**：
````markdown
```dataviewjs
dv.table(["文件", "标签"],
  dv.pages("#项目")
    .limit(10)
    .map(p => [p.file.link, p.tags])
)
```
````

### 7.2 数据处理

**过滤和排序**：
````markdown
```dataviewjs
const pages = dv.pages("#项目")
  .where(p => p.status === "进行中")
  .sort(p => p.priority, "desc")

dv.table(["项目", "优先级"],
  pages.map(p => [p.file.link, p.priority])
)
```
````

**数据统计**：
````markdown
```dataviewjs
const tasks = dv.pages("#任务").where(t => !t.completed);

dv.header(3, "任务统计");
dv.paragraph(`总计：${tasks.length} 个未完成任务`);
dv.paragraph(`高优先级：${tasks.filter(t => t.priority === "高").length} 个`);
```
````

### 7.3 可视化

**进度条**：
````markdown
```dataviewjs
const completed = dv.pages("#任务").where(t => t.completed).length;
const total = dv.pages("#任务").length;
const percent = Math.round((completed / total) * 100);

dv.paragraph(`完成进度：${percent}%`);
dv.progress(percent, 100);
```
````

---

## 8. 常见问题

### Q1：Dataview 查询很慢怎么办？

**A**：优化建议
- 限制查询范围：用 `FROM` 指定文件夹
- 使用 `LIMIT` 限制结果数量
- 避免复杂的嵌套查询
- 考虑使用 Dataview JS

### Q2：如何查询嵌套标签？

**A**：
````markdown
```dataview
// 查询 #技术栈/后端
TABLE file.link
WHERE contains(tags, "#技术栈/后端")
```
````

### Q3：如何在查询中使用当前文件？

**A**：
````markdown
```dataview
TABLE file.link
WHERE file.path = this.file.path
```
````

### Q4：Dataview 和 Templater 如何配合？

**A**：
- **Templater**：创建时动态生成内容
- **Dataview**：实时查询当前状态

**示例**：
```markdown
---
date: {{date}}
---

## 当日任务
```dataview
TASK
WHERE due = {{date}}
```
```
````

---

## 9. 性能优化

### 9.1 查询优化

**❌ 低效查询**：
````markdown
```dataview
TABLE *
FROM ""
```
````

**✅ 高效查询**：
````markdown
```dataview
TABLE file.link, status
FROM #项目
LIMIT 50
```
````

### 9.2 缓存策略

- Dataview 自动缓存查询结果
- 修改笔记后自动刷新
- 大量查询可能影响性能

---

## 10. 下一步学习

- [02-核心插件/03-Templater模板系统](02-核心插件/03-Templater模板系统.md) - 学习模板系统
- [../02-核心插件/01-Canvas白板完全指南](../02-核心插件/01-Canvas白板完全指南.md) - 可视化数据
- [04-项目管理/04-任务追踪系统](04-项目管理/04-任务追踪系统.md) - 深入任务管理

---

**文档版本**：v2.0
**最后更新**：2026-03-06
**相关文档**：[../01-基础入门/04-双链与标签系统](../01-基础入门/04-双链与标签系统.md) | [02-核心插件/03-Templater模板系统](02-核心插件/03-Templater模板系统.md)
