# 知识流转系统 · AI 分类指南

本文件描述该笔记库的核心架构与流转规则。
**当你（AI）被要求对一条笔记、一段对话或一个想法进行分类归档时，遵循本文件的规则。**

---

## 目录结构

```
01_Curiosities/   好奇心兴趣池
02_Spheres/       生命圈职责域
03_Collisions/    碰撞实验
04_Chronicles/    知识蒸馏
```

---

## 每个目录的本质

### 01_Curiosities · 兴趣种子池
- **本质**：灵感迸发的捕获层，无压力、非功利
- **内容形态**：一个想法、一个问题、一个触动点，不要求完整
- **判断标准**：只要触动了好奇心，不管能否变现、是否"有用"，都归这里
- **当前活跃兴趣点**：AI、Emacs、UML、K8s、Mac、Apple Pencil、Obsidian、3D打印、文艺复兴大师
- **注意**：01 与 02 可以覆盖相同主题，不冲突——同一主题在01是灵感状态，在02是结构化学习状态

### 02_Spheres · 周期履责日志
- **本质**：付费购买的结构化知识的学习记录，周期性履行的身份职责
- **内容形态**：独立的日记条目，时间戳 + 本次内容 + 本次感悟，不追求连贯上下文
- **判断标准**：有明确的学习计划或周期节奏的内容归这里
- **三个圈层**：
  - `Backend`：Java / Go / 操作系统 / AI工程课程
  - `Investor`：每周宏观课、科技公司分析课、霍华德·马克斯备忘录
  - `Life`：海缸维护记录、孩子教育观察与思考

### 03_Collisions · 碰撞实验
- **本质**：知识积压到一定程度后，产生实践冲动，开启验证性实验
- **触发机制**：两种来源——①学习中自然产生"这该怎么应用？"的冲动；②突发性任务（工作需求、临时问题、外部事件驱动）
- **内容形态**：有明确目标、持续推进、记录完整过程（包括报错、弯路、犹豫）
- **判断标准**：有具体的验证目标、需要动手实操的内容归这里
- **强制要求**：必须有始有终。完成 / 阶段性成果 / 写明终止原因，三选一

### 04_Chronicles · 知识蒸馏
- **本质**：03实验或02学习积累之后，主动分配时间进行蒸馏，去掉过程噪音，留下私人洞见
- **内容形态**：精简、高密度，用自己的话，不保留实验过程细节
- **判断标准**：是已经消化过的结论和洞见，不是原始过程记录
- **回流规则**：04的精华会更新01对应兴趣点的认知——当一个兴趣点进入新阶段，或产生了新的兴趣分支，01会引用04的条目

---

## 完整流转图

```
外部输入（文章/课程/对话/灵感）
        │
        ├─ 随机灵感、弱信号、好奇心种子
        │         ↓
        │    01_Curiosities（无压力存入，等待萌芽）
        │
        └─ 付费课程、结构化学习、周期性职责
                  ↓
             02_Spheres（日记形式，周期履责）

01 / 02 知识积压 → 产生实践冲动（"这该怎么用？"）
        ↓                                           ↑
   03_Collisions（开启实验，动手验证）← 突发性任务直接触发
        ↓
   实验完成 / 归档
        ↓（主动分配时间蒸馏，这本身也是02的任务）
   04_Chronicles（精华，去噪后的私人洞见）
        ↓
   认知升级，某个兴趣进入新阶段
        ↓
   01_Curiosities 引用 04 条目，完成闭环
```

---

## AI 分类决策树

收到一条需要归档的内容时，按顺序判断：

```
1. 这是一个随机的想法 / 灵感 / 好奇心触动？
   → YES → 01_Curiosities

2. 这是某个付费课程的学习笔记 / 周期性职责的记录？
   → YES → 02_Spheres / [Backend|Investor|Life]

3. 这是一个正在进行的、有明确目标的动手实验？
   → YES → 03_Collisions

4. 这是已经消化过的结论、洞见、蒸馏后的知识？
   → YES → 04_Chronicles

5. 以上都不明确？
   → 默认进入 01_Curiosities，等待进一步判断
```

---

## 文档 Frontmatter 规范

每类文档使用不同的 frontmatter，**`type` 字段必须存在**，让 AI 第一眼判断文档性质。
废弃字段（一律不使用）：`stage`、`order`、`prerequisites`、`next`、`marp`、`theme`、`backgroud-color`、`addons`

### 01_Curiosities
```yaml
---
type: curiosity
topic: AI          # 对应哪个活跃兴趣点
date: 2026-03-10
tags: [RAG, 向量数据库]
---
```

### 02_Spheres
```yaml
---
type: journal
sphere: Backend    # Backend | Investor | Life
date: 2026-03-10
tags: [Java, JVM]
---
```

### 03_Collisions
```yaml
---
type: experiment
status: active     # active | blocked | completed | archived
source: AI兴趣 × Backend职责   # 或写"突发任务: 描述"
started: 2026-03-09
updated: 2026-03-10
tags: [MCP, GitHub]
---
```

### 04_Chronicles
```yaml
---
type: chronicle
source: 03_Collisions/2026-03-09_MCP记录AI问答.md
distilled: 2026-03-10
tags: [MCP, GitHub API]
flows-to: AI       # 回流更新哪个 01 兴趣点
---
```

---

## Tags 打标规则

tags 用于内容检索，必须是**概念词**，不是描述词。

### 来源规则（按优先级）

1. **目录层级** — 文件所在的每一层子目录名自动成为 tag
   - `02_Spheres/Backend/java/mongodb/xxx.md` → `["Backend", "java", "mongodb"]`

2. **文件名提取** — 从文件名中提取核心概念词，去掉描述性词语
   - 去掉：`是什么 / 基本概念 / 基本操作 / 常用命令 / 使用方法 / 安装 / 指南 / 概述 / 入门` 等
   - 保留：技术名词、产品名、人名等实体词
   - `gpt是什么.md` → `"gpt"`；`mongodb基本概念.md` → `"mongodb"`

3. **内容读取（不确定时必须）** — 文件名为英文且含连字符/空格时，不能机械拆分，需读内容确认
   - `client-server-interaction.md` → 读内容后确认是 IM 系统图 → `["IM", "PlantUML"]`
   - `maven-dependency-management-guide.md` → `["maven", "dependency management"]`

### 禁止出现的 tag

- 版本号：`"24.04"`、`"3.12"` 等
- 单个汉字或虚词：`"的"`、`"与"` 等
- 过长的短语（超过 6 个字的中文词组）：拆开或取核心词
- 文件名原文（如 `"gpt是什么"`、`"docker-compose常用命令"`）
- 大小写重复：`"mac"` 和 `"Mac"` 只保留一个，以先出现的为准

---

## 资源文件规范

### 图片 / 附件
每个主目录下统一放 `assets/` 子文件夹：
```
01_Curiosities/assets/
02_Spheres/assets/
03_Collisions/assets/
04_Chronicles/assets/
```

**从属图片**（某篇 md 的插图）命名格式与 Excalidraw 一致：
```
{父md文件名}-{序号}-{图的描述}.{ext}
```

示例：
```
01_Curiosities/assets/
└── NLP vs NLU vs NLG-01-概念对比.png   ← 属于 NLP vs NLU vs NLG.md
```

**独立图片**（无从属 md）：直接描述性命名，放对应 `assets/`。

### Excalidraw 文件
Excalidraw 不进 `assets/`，直接放在对应目录下。

**独立图**（本身就是内容，无从属 md）：正常命名，放对应目录。

**从属图**（某篇 md 的插图）：使用同名约定，格式：
```
{父md文件名}-{序号}-{图的描述}.excalidraw
```

示例：
```
03_Collisions/
├── 2026-03-09_MCP记录AI问答.md
├── 2026-03-09_MCP记录AI问答-01-系统架构.excalidraw
├── 2026-03-09_MCP记录AI问答-02-数据流.excalidraw
└── 2026-03-09_MCP记录AI问答-03-时序图.excalidraw
```

移动或删除 md 时，搜索同名前缀即可找到所有关联文件（图片 + Excalidraw）。

### 安装配置类文件（docker-compose 等）
配置文件（yml、sql、js、sh 等）保留原始格式存放，不转为 md。
每个服务对应两个 md 文件：

- `xxx安装.md` — 只放核心 yml 代码块
- `xxx安装说明.md` — 记录完整安装流程（前置准备、启动命令、服务端口等）

```
service/
├── xxx安装.md          ← 核心 yml 代码块
├── xxx安装说明.md      ← 安装流程说明
└── init-scripts/       ← 原始配置/初始化脚本，保留不动
    ├── init.sql
    └── init.js
```

---

## 分类时的注意事项

- **01 和 02 主题重叠是正常的**，不要因为"AI已经在02里"就拒绝把AI相关灵感放进01
- **02 的条目是独立的**，不要试图把它们串联成连贯的知识体系
- **03 的过程噪音要保留**，不要在03里做精简——精简是04的工作
- **04 不是搬运**，是蒸馏。如果内容还有大量过程细节，它还属于03，尚未到达04的阶段
- **不确定时优先归01**，01是最宽容的容器
