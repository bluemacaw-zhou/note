---
title: Templater 模板系统
subtitle: 高级模板与自动化
stage: 第五阶段-效率工具
order: 06
author: 戴跃辉
date: 2026-03-06
tags: [效率工具, Templater, 模板, 自动化]
prerequisites: 01-基础入门/03-markdown扩展语法
next: 07-QuickAdd自动化
---

# Templater 模板系统

Templater 是一个强大的模板插件，提供动态模板功能。

---

## 插件简介

**核心功能**：
- 动态变量
- JavaScript 脚本
- 用户函数
- 命令执行

---

## 安装配置

**安装**：
```
设置 → 社区插件 → 浏览 → 搜索 "Templater" → 安装启用
```

**基础配置**：
```yaml
Template folder location: templates
Trigger Templater on new file creation: true
```

---

## 快速开始

### 基础模板

```markdown
---
title: {{title}}
date: {{date}}
---

# {{title}}

创建时间：{{time}}
```

### 动态变量

```markdown
<%*
// 当前日期
const today = tp.date.now("YYYY-MM-DD");
t`日期：${today}`;
*%>
```

---

## 常用功能

**文件名变量**：
- `{{title}}`：笔记标题
- `{{date}}`：当前日期

**日期格式**：
- `{{date:YYYY-MM-DD}}`：格式化日期

**用户输入**：
```javascript
<% await tp.system.prompt("请输入标题") %>
```

---

## 简单示例

### 每日笔记

```markdown
---
date: {{date:YYYY-MM-DD}}
weekday: {{date:dddd}}
---

# {{date:YYYY-MM-DD}} {{date:dddd}}

## 今日工作


## 明日计划


---
```

### 会议记录

```markdown
---
title: {{title}}
date: {{date}}
attendees: <% await tp.system.prompt("参会人员") %>
---

# {{title}}

## 参会人员
<% attendees.split(",").forEach(p => { %>
- <% p %>
<% }) %>

## 议程


## 讨论内容


## 行动项
| 任务 | 负责人 | 截止日期 |
|------|--------|----------|
|      |        |          |

---
```

---

## 更多资源

**插件地址**：https://github.com/SilentVoid13/Templater

**相关文档**：
- [07-QuickAdd自动化](07-QuickAdd自动化.md)
- [03-自动化工作流](../07-团队协作/03-自动化工作流.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
