---
title: PDF 与导入工具
subtitle: PDF++ 和 Importer 插件使用指南
stage: 第五阶段-效率工具
order: 05
author: 戴跃辉
date: 2026-03-06
tags: [效率工具, PDF, 导入]
prerequisites: 01-基础入门/05-附件与媒体管理
next: 06-样式与美化/01-StyleSettings配置
---

# PDF 与导入工具

PDF 阅读增强和内容导入工具，丰富知识库内容来源。

---

## 📋 目录

- [PDF++ 增强阅读](#pdf-增强阅读)
- [Importer 内容导入](#importer-内容导入)
- [Image Converter 图片转换](#image-converter-图片转换)
- [实践案例](#实践案例)

---

## PDF++ 增强阅读

### 插件简介

**PDF++** 是 Obsidian 最强大的 PDF 阅读插件，支持高亮、注释、OCR 等功能。

**核心功能**：
- PDF 内嵌阅读
- 高亮和注释
- 文本提取和 OCR
- 双页显示
- 深色模式

### 安装配置

```yaml
# 安装
设置 → 社区插件 → 浏览 → 搜索 "PDF++" → 安装启用

# 基本配置
PDF++:
  Default Page: single       # 单页/双页
  Dark Mode: true           # 深色模式
  Auto Extract: true        # 自动提取文本
```

### 基础用法

**嵌入 PDF**：
```markdown
![[文件名.pdf]]
```

**高亮文本**：
1. 在 PDF 中选中文本
2. 选择高亮颜色
3. 自动保存到笔记

**添加注释**：
1. 点击注释工具
2. 在 PDF 任意位置添加
3. 输入注释内容

### 高级功能

**1. 高亮提取**

```markdown
<!-- 自动生成高亮摘录 -->
## PDF 高亮

原文：这是原文内容...

来源：[[文档.pdf]] 第 5 页
```

**2. OCR 识别**

```yaml
# OCR 设置
OCR:
  Language: chi_sim+eng    # 中英文混合
  Auto OCR: false         # 手动触发
```

**3. 双链引用**

```markdown
<!-- 链接到特定页面 -->
![[文档.pdf#page=15]]

<!-- 链接到高亮 -->
![[文档.pdf#highlight=3]]
```

---

## Importer 内容导入

### 插件简介

**Importer** 可以从各种来源导入内容到 Obsidian。

**支持格式**：
- Notion
- Evernote
- Bear
- HTML 网页
- Markdown 文件
- Roam Research

### 安装配置

```yaml
# 安装
设置 → 社区插件 → 浏览 → 搜索 "Importer" → 安装启用
```

### 导入方式

**1. Notion 导入**

```yaml
步骤：
1. 导出 Notion 页面为 HTML/Markdown
2. Obsidian 中：Importer → Import Files
3. 选择导出的文件
4. 配置导入选项
5. 开始导入
```

**2. Evernote 导入**

```yaml
步骤：
1. 导出 Evernote 笔记为 .enex 文件
2. Importer → 选择 Evernote
3. 上传 .enex 文件
4. 选择目标文件夹
5. 导入
```

**3. 网页导入**

```markdown
<!-- 直接导入网页 -->
命令：Importer: Import from URL
输入：https://example.com/article
格式：Markdown
```

### 导入配置

```yaml
Importer:
  # 文件夹结构
  Folder Format: "{{date}}/{{title}}"
  # 附件处理
  Attachment Folder: attachments/{{date}}
  # 标签转换
  Tag Format: "#{{tag}}"
```

---

## Image Converter 图片转换

### 插件简介

**Image Converter** 自动转换和优化图片格式。

**功能**：
- PNG ↔ WebP 转换
- 图片压缩
- 格式统一
- 批量处理

### 配置使用

```yaml
# 安装
设置 → 社区插件 → 浏览 → 搜索 "Image Converter" → 安装启用

# 配置
Image Converter:
  Output Format: webp       # 输出格式
  Quality: 80               # 质量
  Max Width: 1920           # 最大宽度
  Convert On Paste: true    # 粘贴时自动转换
```

---

## 实践案例

### 案例1：学术研究笔记

```markdown
# 论文阅读笔记

## 论文信息
**标题**：深度学习在自然语言处理中的应用
**来源**：[[paper.pdf]]
**日期**：2026-03-06

## 重要摘录

> 核心观点：Transformer 架构改变了 NLP 的范式
> 来源：paper.pdf 第 3 页

## 个人思考
...

## 相关链接
- [[相关论文2.pdf]]
- [[笔记-Transformer.md]]
```

### 案例2：网页内容收集

```markdown
<!-- Importer 导入后自动生成 -->
---
source: https://blog.example.com/article
imported: 2026-03-06
tags: [技术博客, 前端]
---

# 文章标题

[原文链接](https://blog.example.com/article)

## 摘要
导入的文章内容...

## 笔记
...
```

### 案例3：图片管理

```yaml
# 图片优化流程
1. 截图/复制图片
2. 粘贴到 Obsidian
3. Image Converter 自动：
   - 转换为 WebP
   - 压缩质量 80%
   - 限制宽度 1920px
4. 保存到 attachments/
```

---

## 最佳实践

> [!tip] PDF 阅读
> 1. **建立文件夹结构**：按主题或项目分类 PDF
> 2. **统一命名规范**：`作者-标题-年份.pdf`
> 3. **及时做笔记**：阅读时同步记录想法
> 4. **使用双链**：在笔记和 PDF 之间建立链接

> [!tip] 内容导入
> 1. **先整理后导入**：清理无关内容
> 2. **检查格式**：确认导入后的格式正确
> 3. **补充元数据**：添加来源、日期等信息
> 4. **后续整理**：导入后及时归类

---

## 常见问题

### Q1：PDF++ 显示空白？

**A**：
- 检查 PDF 文件是否损坏
- 尝试重新安装插件
- 查看控制台错误信息

### Q2：导入后格式混乱？

**A**：
- 使用格式化工具清理
- 手动调整重点内容
- 考虑使用 Pandoc 预处理

### Q3：图片转换失败？

**A**：
- 检查原始图片格式
- 确认磁盘空间充足
- 尝试手动转换

---

## 相关资源

**插件地址**：
- PDF++: https://github.com/alviner/obsidian-pdf-plus
- Importer: https://github.com/obsidianmd/obsidian-importer
- Image Converter: https://github.com/ozntel/obsidian-image-converter

**相关文档**：
- [04-编辑器增强插件](04-编辑器增强插件.md)
- [01-附件与媒体管理](../01-基础入门/05-附件与媒体管理.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
