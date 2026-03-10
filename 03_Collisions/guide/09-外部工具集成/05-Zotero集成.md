---
title: Zotero 集成
subtitle: 学术文献管理集成
stage: 第九阶段-外部工具集成
order: 05
author: 戴跃辉
date: 2026-03-06
tags: [外部工具, Zotero, 文献管理]
prerequisites: 01-基础入门/05-附件与媒体管理
next: 附录/A-插件速查手册
---

# Zotero 集成

将 Zotero 文献管理工具与 Obsidian 集成，高效管理学术文献。

---

## 📋 目录

- [Zotero 简介](#zotero-简介)
- [Obsidian Zotero 插件](#obsidian-zotero-插件)
- [安装配置](#安装配置)
- [使用方法](#使用方法)
- [实践案例](#实践案例)

---

## Zotero 简介

**Zotero** 是免费的文献管理工具。

**核心功能**：
- 文献收集
- 元数据提取
- 引用管理
- PDF 注释
- 团队协作

---

## Obsidian Zotero 插件

**插件名称**：Zotero Integration

**功能特性**：
- 从 Zotero 导入文献
- 自动创建笔记
- 同步元数据
- PDF 集成
- 引用管理

---

## 安装配置

### 安装 Zotero

**下载安装**：
```
官网：https://www.zotero.org
支持：Windows, macOS, Linux
```

### 安装 Obsidian 插件

**步骤**：
1. 设置 → 社区插件 → 浏览
2. 搜索 "Zotero Integration"
3. 安装并启用

### 配置连接

**基本配置**：
```yaml
Zotero Integration:
  Import PDFs: true         # 导入 PDF
  Import Notes: true        # 导入注释
  Auto Create Note: true     # 自动创建笔记
```

---

## 使用方法

### 1. 导入文献

**从 Zotero 导入**：
```
1. 在 Zotero 中选择文献
2. 右键 → Export to Obsidian
3. 选择目标文件夹
4. 导入笔记
```

### 2. 创建笔记

**自动创建**：
```
1. 配置模板
2. 选择文献
3. 自动生成文献笔记
4. 包含元数据和引用
```

### 3. 引用管理

**插入引用**：
```markdown
---
citation: [作者, 年份]
zotero: item_id
---

相关文献：[[文献标题]]
```

---

## 实践案例

### 案例1：学术论文

**文献笔记模板**：
```markdown
---
title: {{title}}
authors: {{authors}}
year: {{year}}
publication: {{publicationType}}
zotero: {{key}}
---

# {{title}}

## 作者
{{authors}}

## 发表信息
- 期刊：{{publicationTitle}}
- 年份：{{year}}
- 卷期：{{volume}}{{issue}}

## 摘要
{{abstractNote}}

## 核心观点


## 研究方法


## 个人思考


## 引用格式
> [cite:key]

## 相关文献
```

### 案例2：文献综述

**综述笔记**：
```markdown
# 主题文献综述

## 研究背景

## 主要文献
- [[文献1]]
- [[文献2]]
- [[文献3]]

## 研究进展

## 待解决问题

## 参考文献
```

---

## 最佳实践

> [!tip] 文献管理
> 1. **统一命名**：使用一致的文献命名
> 2. **标签分类**：按主题或项目添加标签
> 3. **定期同步**：定期同步 Zotero 数据
> 4. **备份重要**：备份文献数据库

> [!tip] 笔记整理
> 1. **及时记录**：阅读后立即做笔记
> 2. **标注重点**：使用高亮和注释
> 3. **建立链接**：在相关文献间建立链接
> 4. **定期回顾**：定期回顾文献笔记

---

## 常见问题

### Q1：Zotero 连接失败？

**A**：
- 确认 Zotero 已启动
- 检查 Zotero 插件是否启用
- 验证端口配置

### Q2：PDF 导入失败？

**A**：
- 检查 PDF 文件路径
- 确认 Zotero 有读取权限
- 尝试手动导入

### Q3：元数据缺失？

**A**：
- 使用 Zotero 的元数据提取功能
- 手动补充缺失信息
- 使用 DOI 自动获取

---

## 相关资源

**Zotero 官网**：https://www.zotero.org

**插件地址**：https://github.com/aidenlx/obsidian-zotero-plugin

**相关文档**：
- [01-Obsidian Web Clipper](./01-Obsidian Web Clipper.md)
- [05-PDF与导入工具](../05-效率工具/05-PDF与导入工具.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
