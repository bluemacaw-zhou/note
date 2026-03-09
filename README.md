# Obsidian Template

使用 Obsidian 管理文档的知识库模板仓库，包含完整的学习文档和最佳实践配置。

==仓库创建后，可将此文档修改为仓库的 README 说明==

## 知识库管理

- 采用 **PARA 方法** 进行管理：`Project（项目）、Area（领域）、Resource（资源）、Archive（归档）`
- `guide/` 目录包含完整的 Obsidian 学习文档
- `00-示例和演示/` 目录提供各种功能的实战示例

### 使用方法

1. `fork` 到自己的项目下
2. 使用 Obsidian 打开仓库
3. 参考 `guide/` 目录下的文档学习使用

---

## 默认目录

| 目录名称 | 说明 | 使用 |
|---------|------|------|
| `templates` | 文档模板目录 | 按 `/` 或 `Ctrl+P` 调用模板功能 |
| `copilot-custom-prompts` | Copilot AI Prompts 目录 | 在 AI Chat 窗口通过 `/` 调用 |
| `attachments` | 默认附件目录，存放图片等 | 自动保存插入的图片和附件 |

> 配置目录可通过相应插件进行更改

---

## 学习路径 (guide 目录)

| 阶段 | 目录 | 内容 |
|------|------|------|
| **基础入门** | `01-基础入门/` | Obsidian 基本概念、双链标签、Markdown 扩展语法 |
| **核心插件** | `02-核心插件/` | Canvas 白板、Bases 数据库、Query 语法 |
| **可视化工具** | `03-可视化工具/` | 思维导图、图表可视化、Excalidraw 手绘、SheetPlus 表格 |
| **项目管理** | `04-项目管理/` | Projects 插件、Dataview 查询、Kanban 看板、Bases 管理 |
| **效率工具** | `05-效率工具/` | EasyTyping 排版、Emoji 输入、编辑器增强、模板系统、QuickAdd 自动化 |
| **样式美化** | `06-样式与美化/` | Style Settings 配置、图标标签、高亮提示块 |
| **团队协作** | `07-团队协作/` | 知识库架构设计、Git 版本控制、自动化工作流 |
| **AI 集成** | `08-AI集成/` | Copilot 配置、AI 工作流设计、MCP 集成 |
| **外部工具** | `09-外部工具集成/` | Web Clipper、Obsidian CLI、脚本集成、Zotero 集成 |
| **附录** | `附录/` | 插件速查手册、快捷键大全、常见问题 FAQ、学习资源 |

---

## 核心插件与功能

### 📚 基础功能

| 功能 | 插件/特性 | 说明 |
|------|----------|------|
| 双向链接 | 内置功能 | `[[笔记名]]` 创建知识网络 |
| 图谱视图 | 内置功能 | 可视化笔记关系 |
| 标签系统 | 内置功能 | `#标签` 组织内容 |

### 🎨 可视化与绘图

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| 无限白板 | Canvas, Advanced Canvas | 头脑风暴、知识整理 |
| 手绘绘图 | Excalidraw | 流程图、示意图 |
| 思维导图 | Mind Map | 信息组织与理解 |
| 统计图表 | Charts | 数据可视化（可与 Dataview 联动） |
| 电子表格 | Sheet Plus | 类 Excel 的数据整理 |
| 演示文稿 | Advanced Slide | 将笔记转换为 PPT |

### 📊 项目与数据管理

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| 项目管理 | Projects | 任务分解、进度跟踪 |
| 数据库 | Bases | 表格/卡片/日历视图 |
| 数据查询 | Dataview | 按目录、时间、标签生成表格和列表 |
| 看板管理 | Kanban | 可视化工作流、任务分配 |
| 日程管理 | Calendar | 时间管理、计划制定 |

### ⚡ 效率与编辑

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| 自动排版 | Easy Typing | 标点符号、中英文空格自动处理 |
| Emoji 输入 | Emoji ShortCodes | 快速插入表情符号 |
| 编辑增强 | Editing Toolbar | 括号配对、快速选中文本 |
| 模板系统 | Templater, QuickAdd | 动态模板、自动化工作流 |
| 提示块 | Admonition | 彩色引用块 |
| 彩色标签 | Colored Tags | 标签颜色分类 |

### 🤖 AI 与自动化

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| AI 助手 | Copilot | 文档润色、流程图生成、知识库问答 |
| 向量搜索 | Copilot + Embedding | 实现对知识库的语义搜索 |
| 自动化 | QuickAdd, Templater | 自动创建笔记、日期变量等 |
| 脚本执行 | Obsidian Scripts, Shell commands | 批量处理、自动化任务 |

### 👥 团队协作

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| 版本控制 | Obsidian Git, Remote Save | Git 自动提交/推送/拉取 |
| 知识库同步 | Obsidian Sync / Git | 团队协作、多设备同步 |

### 🎯 其他工具

| 功能 | 插件名称 | 用途 |
|------|----------|------|
| PDF 编辑 | PDF++ | 直接编辑和注释 PDF |
| 样式自定义 | Style Settings | 字体、颜色、布局个性化 |
| 首页 | Homepage | 指定打开时自动显示的文件 |
| Web 剪藏 | Obsidian Web Clipper | 保存网页内容到笔记 |
| Zotero 集成 | Zotero Integration | 文献管理 |

---

## 示例与演示

`00-示例和演示/` 目录包含可直接运行的示例：

- `01-Homepage演示.canvas` - 首页白板示例
- `02-Kanban任务演示.md` - 看板任务管理示例
- `03-Dataview查询演示.md` - Dataview 查询语法示例
- `04-Bases数据库演示.base` - Bases 数据库视图示例
- `05-Button按钮演示.md` - Buttons 插件示例
- `06-高亮与脚注演示.md` - 高亮语法和 Markdown 脚注示例
- `项目管理/` - 完整的项目管理示例数据

---

## 快速开始

1. **安装 Obsidian**：访问 [obsidian.md](https://obsidian.md) 下载
2. **克隆仓库**：`git clone <仓库地址>`
3. **用 Obsidian 打开**：选择仓库文件夹
4. **开始学习**：从 `guide/000-Obsidian教程导航.md` 开始
