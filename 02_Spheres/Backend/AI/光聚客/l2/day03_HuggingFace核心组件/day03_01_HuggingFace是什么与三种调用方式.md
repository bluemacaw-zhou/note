---
type: journal
sphere: Backend
date: 2026-11-18
tags: [Backend, AI, 光聚客, HuggingFace, Inference API]
---

# HuggingFace 是什么与三种调用方式

> 总览 [[day03_00_总览|day03]] · 下一块 → [[day03_02_模型下载与本地加载|下载与加载]]

**为什么需要**：从零训练一个语言模型，需要海量数据和算力。HuggingFace 把别人训练好的模型集中起来，下载一个就能直接用。

## 四个组件

| 组件 | 管什么 | 类比 |
|---|---|---|
| Hub（网站） | 托管模型、数据集，可以按任务、框架、语言筛选 | 模型界的 GitHub |
| `transformers` | 加载模型和分词器，运行推理 | 运行时 |
| `tokenizers` | 分词（见 [[day03_03_分词与索引\|03]]） | — |
| `datasets` | 加载数据集（见 [[day03_07_文本分类与datasets\|07]]） | — |

安装：`pip install transformers datasets tokenizers`，前提是已经装好 PyTorch。

## 三种调用方式

| 方式 | 代码 | 模型跑在哪 | 适合 |
|---|---|---|---|
| 匿名调用 API | `requests.post(API_URL, json={"inputs": ...})` | HuggingFace 的服务器 | 快速试一下，限额很低 |
| 带 Token 调用 API | 再加一个请求头 `Authorization: Bearer <token>` | HuggingFace 的服务器 | 正式调用在线模型 |
| 下载到本地 | `from_pretrained` + `pipeline` | 自己的机器 | 离线运行、可以微调，day03 的主线 |

## 课程代码的三个问题

| 问题 | 说明 |
|---|---|
| 请求体的键名写错 | `api_test01.py` 写的是 `{"input": ...}`，应为 `{"inputs": ...}`。资料和 `api_test02.py` 写的都是 `inputs` |
| 接口地址已经过时 | 课程用的 `api-inference.huggingface.co/models/...` 已经被 HuggingFace 的 `router.huggingface.co` 取代。我在 `huggingface-demo/API_test/api_test.py` 中改成了 OpenAI 兼容的 `/v1/chat/completions` 接口 |
| **Token 写死在代码里** | `api_test02.py` 直接写了一个真实的 `hf_...` Token，随课程资料一起分发出去了。正确的做法是从环境变量读取（`os.environ.get("HF_TOKEN")`），日志里也要把 Token 打码，我的改写版就是这样做的 |

**引出下一块**：选择下载到本地，模型文件下载到了哪里，又该怎么加载？
