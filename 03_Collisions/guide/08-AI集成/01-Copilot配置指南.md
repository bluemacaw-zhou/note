---
title: Copilot 配置指南
subtitle: AI 助手完整配置
stage: 第八阶段-AI集成
order: 01
author: 戴跃辉
date: 2026-03-06
tags: [AI, Copilot, 配置]
prerequisites: 02-核心插件/02-Dataview数据查询
next: 02-AI工作流设计
---

# Copilot 配置指南

配置和使用 Obsidian Copilot AI 助手。

---

## 📋 目录

- [插件简介](#插件简介)
- [安装配置](#安装配置)
- [API 密钥配置](#api-密钥配置)
- [使用方法](#使用方法)
- [最佳实践](#最佳实践)

---

## 插件简介

**Copilot** 是 Obsidian 的 AI 助手插件，支持多种 AI 模型。

**核心功能**：
- 智能问答
- 内容生成
- 文本摘要
- 代码解释
- 翻译辅助

**支持的 AI 模型**：
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Azure OpenAI
- 本地模型 (Ollama)

---

## 安装配置

### 安装步骤

1. **安装插件**
   - 设置 → 社区插件 → 浏览
   - 搜索 "Copilot"
   - 安装并启用

2. **打开设置**
   - 设置 → Copilot
   - 配置 API 密钥

### 基础配置

```yaml
Copilot:
  # 模型选择
  Model: gpt-4-turbo-preview

  # 语言设置
  Language: 中文

  # 温度参数
  Temperature: 0.7

  # 最大 Token
  Max Tokens: 2000
```

---

## API 密钥配置

### OpenAI 配置

**获取 API 密钥**：
1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 创建 API 密钥
4. 复制密钥

**配置 Copilot**：
```yaml
设置 → Copilot → API Key
输入: sk-xxxxxxxxxxxxxxxxxxxxx
```

### Anthropic Claude 配置

**获取 API 密钥**：
1. 访问 https://console.anthropic.com
2. 注册/登录账号
3. 创建 API 密钥

**配置**：
```yaml
设置 → Copilot → Model
选择: Claude 3 Sonnet

API Key: sk-ant-xxxxxxxxxxxxxxxx
```

### 本地模型 (Ollama)

**安装 Ollama**：
```bash
# 下载安装
https://ollama.ai

# 拉取模型
ollama pull llama2
```

**配置 Copilot**：
```yaml
设置 → Copilot
Model: ollama/llama2
API Base: http://localhost:11434
```

---

## 使用方法

### 1. 智能问答

**命令面板**：
```
Ctrl/Cmd + P → Copilot: Ask AI
```

**侧边栏对话**：
```
点击 Copilot 图标 → 输入问题 → 发送
```

### 2. 内容生成

**生成文本**：
```markdown
<!-- 选中提示词 -->
请生成一篇关于 Obsidian 的介绍文章，包括：
1. 核心功能
2. 使用场景
3. 最佳实践
```

**续写内容**：
```markdown
<!-- 写开头 -->
Obsidian 是一个强大的知识管理工具...

<!-- Copilot 续写 -->
选中内容 → Copilot: Complete
```

### 3. 文本摘要

**摘要当前笔记**：
```
命令：Copilot: Summarize current note
```

**摘要选中内容**：
```
选中内容 → Copilot: Summarize selection
```

### 4. 代码解释

**解释代码**：
````markdown
````javascript
function hello() {
  console.log("Hello World");
}
````

<!-- Copilot 解释 -->
选中代码 → Copilot: Explain code


### 5. 翻译辅助

**翻译文本**：
```
选中英文 → Copilot: Translate to Chinese
选中中文 → Copilot: Translate to English
```

---

## 最佳实践

> [!tip] 使用建议
> 1. **明确指令**：提供清晰详细的提示词
> 2. **分步提问**：复杂问题拆分成多个小问题
> 3. **验证结果**：AI 生成内容需要人工验证
> 4. **保护隐私**：不要输入敏感信息

> [!tip] 提示词工程
> 1. **角色设定**：指定 AI 的角色和背景
> 2. **任务描述**：清楚说明要完成的任务
> 3. **输出格式**：指定期望的输出格式
> 4. **示例参考**：提供参考示例

### 示例提示词

**内容生成**：
```
你是一位技术写作专家，请撰写一篇关于 Git 的技术文章：
- 目标读者：初中级开发者
- 字数要求：800-1000 字
- 包含示例代码
- 语气友好且专业
```

**文档审阅**：
```
请审阅以下文档，检查：
1. 语法错误
2. 逻辑清晰度
3. 格式规范
4. 提供改进建议
```

**知识问答**：
```
根据我的知识库内容，回答以下问题：
[问题内容]

请提供：
1. 直接答案
2. 相关笔记链接
3. 参考来源
```

---

## 常见问题

### Q1：API 调用失败？

**A**：
- 检查 API 密钥是否正确
- 确认账户有足够额度
- 检查网络连接
- 查看控制台错误信息

### Q2：生成质量不佳？

**A**：
- 调整 Temperature 参数（0.1-1.0）
- 改进提示词表达
- 尝试不同的模型
- 增加上下文信息

### Q3：使用成本控制？

**A**：
```yaml
# 成本优化
Model: gpt-3.5-turbo      # 更便宜
Max Tokens: 1000          # 限制长度
Temperature: 0.5          # 降低随机性
```

---

## 相关资源

**插件地址**：https://github.com/logancyang/obsidian-copilot

**API 文档**：
- OpenAI: https://platform.openai.com/docs
- Anthropic: https://docs.anthropic.com

**相关文档**：
- [02-AI工作流设计](./02-AI工作流设计.md)
- [03-Excalidraw MCP集成](./03-Excalidraw MCP集成.md)

---

**文档版本**：v2.0
**最后更新**：2026-03-06
