---
title: QuickAdd 自动化
subtitle: 快速添加和宏自动化
stage: 第五阶段-效率工具
order: 07
author: 戴跃辉
date: 2026-03-06
tags: [效率工具, QuickAdd, 自动化, 宏]
prerequisites: 01-基础入门/03-markdown扩展语法
next: 04-编辑器增强插件
---

# QuickAdd 自动化

QuickAdd 是一个强大的自动化插件，可以快速创建笔记和执行宏。

---

## 插件简介

**核心功能**：
- 快速创建笔记
- Macro 宏自动化
- Choice 选择菜单
- 模板集成
- 用户输入捕获

---

## 安装配置

**安装**：
```
设置 → 社区插件 → 浏览 → 搜索 "QuickAdd" → 安装启用
```

**基本配置**：
```yaml
QuickAdd:
  Auto-launch: true       # 自动启动
  Show in menu: true      # 在菜单显示
```

---

## 快速开始

### 创建 Choice

**步骤**：
1. QuickAdd → Manage Choices
2. Create new choice
3. 选择类型（Template/Macro/Capture）
4. 配置选项

### 模板 Choice

**配置示例**：
```yaml
Name: 每日笔记
Type: Template
Template: 每日笔记模板.md
File Name Format: {{date:YYYY-MM-DD}}
Create in: 日记/
```

### Macro Choice

**步骤序列**：
1. 创建笔记
2. 插入模板
3. 打开文件
4. 移动光标

---

## 宏脚本

### 基础 Macro

**每日日报**：
```javascript
// 创建文件
const fileName = `日报-${tp.date.now("YYYY-MM-DD")}`;
await tp.file.create_new(fileName, "日报/", "日报模板内容");

// 打开文件
await tp.file.open(fileName);
```

### 用户输入

**捕获输入**：
```javascript
// 获取标题
const title = await quickadd.input("请输入标题");

// 选择类型
const type = await quickadd.suggester(
  ["任务", "笔记", "会议"],
  ["task", "note", "meeting"]
);
```

---

## 实用示例

### 快速任务

**一键创建任务**：
```yaml
Choice: 新建任务
Type: Macro
Steps:
  - Create note in Tasks/
  - Use task template
  - Open in new pane
```

### 会议记录

**快速记录**：
```yaml
Choice: 会议记录
Type: Template
Template: 会议模板.md
File Name: {{title}}-{{date:YYYYMMDD}}
Folder: 会议记录/
```

---

## 与 Templater 对比

| 功能 | QuickAdd | Templater |
|------|----------|-----------|
| 主要用途 | 自动化流程 | 模板系统 |
| 学习曲线 | 中等 | 较高 |
| 宏功能 | 强大 | 支持 |
| 脚本能力 | 完整 | 完整 |

---

## 简单使用建议

> [!tip] 快速上手
> 1. **从简单开始**：先创建基本 Choice
> 2. **逐步添加**：慢慢增加宏步骤
> 3. **测试验证**：每个步骤都要测试
> 4. **保存备份**：重要配置要备份

---

## 更多资源

**插件地址**：https://github.com/chhoumann/quickadd

**相关文档**：
- [06-Templater模板系统](06-Templater模板系统.md)
- [03-自动化工作流](../07-团队协作/03-自动化工作流.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
