---
title: Button 按钮演示
subtitle: 最小可用 Buttons 示例
---

# Button 按钮演示

本页提供可直接使用的 Buttons 插件示例（语法完整、可点击执行）。

## 1. 新建项目按钮（可用）


```button
name 新建项目笔记
type note(00-示例和演示/项目管理/10-新项目.md)
templater false
```

## 2. 快速打开示例笔记（可用）

```button
name 打开 Dataview 演示
type note(00-示例和演示/03-Dataview查询演示.md)
templater false
```

```button
name 打开性能优化项目
type note(00-示例和演示/项目管理/03-性能优化.md)
templater false
```

## 3. 编辑命令按钮（可用）

```button
name 切换加粗
type command
action Editor: Toggle bold
icon bold
```

```button
name 切换斜体
type command
action Editor: Toggle italic
icon italic
```

## 4. 使用说明

- 需要安装并启用社区插件 `Buttons`。
- `type note(完整路径.md)`：点击后创建或打开对应文件（本页示例全部使用该方式）。
- `type command`：执行 Obsidian 命令面板中的命令。

---

**文档版本**：v3.0  
**最后更新**：2026-03-06
