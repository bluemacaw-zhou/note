---
title: Dataview 查询演示
subtitle: 基于项目管理示例的可运行查询
---

# Dataview 查询演示

本页所有示例都基于目录：`guide/00-示例和演示/项目管理`。

## 1. 基础项目查询

```dataview
TABLE 项目名称, 状态, 优先级, 负责人, 进度, 截止日期
FROM "guide/00-示例和演示/项目管理"
SORT 优先级 ASC, 截止日期 ASC
```

## 2. P0/P1 在进行项目

```dataview
TABLE 项目名称, 负责人, 进度, 截止日期
FROM "guide/00-示例和演示/项目管理"
WHERE (优先级 = "P0" OR 优先级 = "P1") AND 状态 != "归档"
SORT 截止日期 ASC
```

## 3. FLATTERN（FLATTEN）按人拆分任务演示

说明：Dataview 正确关键字是 `FLATTEN`。这里按你要求做“FLATTERN 语法拆分”的任务演示，即把每个项目里的 checklist 任务展开后，再按 `负责人` 聚合。

### 3.1 展开后查看每条任务

```dataview
TABLE 负责人, file.link AS 项目, task.text AS 任务, choice(task.completed, "已完成", "未完成") AS 完成状态
FROM "guide/00-示例和演示/项目管理"
FLATTEN file.tasks AS task
WHERE task.text
SORT 负责人 ASC, file.name ASC
```

### 3.2 按负责人分组查看未完成任务

```dataview
LIST task.text + "（" + file.link + "）"
FROM "guide/00-示例和演示/项目管理"
FLATTEN file.tasks AS task
WHERE task.text AND !task.completed
GROUP BY 负责人
SORT 负责人 ASC
```

### 3.3 按负责人统计未完成任务数量

```dataview
TABLE length(rows) AS 未完成任务数
FROM "guide/00-示例和演示/项目管理"
FLATTEN file.tasks AS task
WHERE task.text AND !task.completed
GROUP BY 负责人
SORT length(rows) DESC
```

## 4. 近期截止项目

```dataview
TABLE 项目名称, 负责人, 状态, 截止日期
FROM "guide/00-示例和演示/项目管理"
WHERE 截止日期 >= date(2026-03-01) AND 截止日期 <= date(2026-03-31)
SORT 截止日期 ASC
```

---

**文档版本**：v3.0  
**最后更新**：2026-03-06
