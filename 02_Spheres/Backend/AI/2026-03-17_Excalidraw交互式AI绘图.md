---
title: Excalidraw 交互式 AI 绘图
date: 2026-03-17
tags: [AI, Excalidraw, Obsidian, idea]
status: idea
---

# Excalidraw 交互式 AI 绘图

## 核心 Idea

通过本地大模型 + 自建中间层服务，实现在浏览器里与 AI 多轮对话来创建和修改 Excalidraw 图表，最终输出 Obsidian 兼容的 `.excalidraw.md` 格式。

---

## 使用场景

1. **图生图**：把历史的 PlantUML / ProcessOn 截图，让视觉模型识别并转换为 Excalidraw JSON
2. **文生图**：用自然语言描述图表，模型生成初始 Excalidraw JSON
3. **多轮修改**：在已有图的基础上，用文字指令增量修改（"加一条双向箭头"、"把这个框移到右边"）

---

## 技术架构

### 文生图链路

```
用户文字描述
  ↓
qwen2.5:32b 生成 PlantUML 代码   ← LLM 最擅长，训练数据充分
  ↓
PlantUML 渲染成图片               ← 布局引擎保证坐标合理，无需 LLM 猜位置
  ↓
qwen2.5-vl:32b 读图 → Excalidraw JSON
```

### 图生图链路（历史图片）

```
已有图片（PlantUML截图 / ProcessOn截图）
  ↓
qwen2.5-vl:32b 读图 → Excalidraw JSON   ← 直接从这步开始
```

### 多轮修改 + 输出链路

```
终端对话（用户输入修改指令）
  ↓
编排脚本（维护当前 JSON 状态）
  └── qwen2.5:32b + 当前 JSON + 指令 → 新 JSON
  ↓
中间层服务 POST /diagram（存储 JSON + 推送变更）
  ↓
浏览器 Excalidraw（WebSocket 监听 → 自动刷新渲染）
  ↓
确认后 → 转换为 Obsidian .excalidraw.md 压缩格式
```

### 为什么先生成 PlantUML 再转图

主流 AI 画图工具（Whimsical、Eraser.io 等）都用 Mermaid/PlantUML 而不是直接生成 Excalidraw，原因是 Excalidraw JSON 包含坐标，LLM 直接生成坐标不稳定。

通过 PlantUML 作为中间格式，让每一层只做自己最擅长的事：
- LLM → 逻辑结构（PlantUML 代码）
- PlantUML 渲染引擎 → 布局坐标
- 视觉模型 → 格式转换（图片 → JSON）

---

## 关键设计点

**为什么 Excalidraw 容器不够用**：
Excalidraw 官方容器是纯静态 React App，没有接收 JSON 的 API，需要在前面加一个中间层服务才能实现程序化控制。

**中间层职责**：
- 存储当前图表 JSON 状态
- 暴露 `POST /diagram` 接口接收新 JSON
- 通过 WebSocket 通知浏览器刷新

**多轮交互的核心**：
每轮模型拿到的是完整的当前 JSON 状态 + 用户指令，做增量修改而非从零生成，保证上下文连贯。

**Obsidian 格式转换**：
Obsidian Excalidraw 插件使用压缩的 `.excalidraw.md` 格式，需要脚本将标准 JSON 转换，有现成 Python 工具可处理。

---

## 依赖组件

| 组件 | 用途 | 状态 |
|------|------|------|
| Ollama + qwen2.5:32b | 文字指令 → JSON | 待部署 |
| Ollama + qwen2.5-vl:32b | 图片 → JSON | 待部署 |
| Excalidraw 容器 | 可视化验证 | 待部署 |
| 中间层服务（自建）| JSON 状态管理 + 推送 | 待开发 |
| 转换脚本 | 标准 JSON → Obsidian 格式 | 待开发 |

---

## 前置条件

- Ollama 本地部署完成（已完成）
- qwen2.5:32b 和 qwen2.5-vl:32b 模型下载完成
- 对 Excalidraw JSON 格式有基本了解
