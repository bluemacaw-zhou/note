---
type: journal
sphere: Backend
date: 2026-10-29
tags: [Backend, AI, 子牙, Tokenizer, Embedding, Transformer, LM Head, 自回归]
---

# 手写 ChatGPT · 开篇：预测 Token 的推理链路

**一句话**：大模型预测 token = **预测下一个 token + 自回归**。内部做的事情是：让「下一个 token 的 ID」在一个长度为 V 的概率向量里取最大值。

## 1. 一条链路，追踪形状

课程的教学模型：`context_len T = 6`，`embed_dim D = 4`，词表 `V = 273`。问「你是谁」，期望下一个 token 是「我」（ID = 53）。

```text
"你是谁…"                  文本
  ↓ Tokenizer              (1, 6)      6 个 token ID
  ↓ Embedding 查表         (1, 6, 4)   每个 ID 取一行 4 维向量
  ↓ + Position Embedding   (1, 6, 4)   逐位置相加
  ↓ Transformer Blocks     (1, 6, 4)   形状不变，数值融合了上下文
  ↓ LM Head (y = Wx + b)   (1, 273)    给词表里每个候选打分
  ↓ Softmax                (1, 273)    第 53 项 ≈ 0.99999 最大
  ↓ argmax + decode        "我"
```

| 模块 | 职责 | 关键参数 |
|---|---|---|
| Tokenizer | 文本 ↔ ID | 词表（不训练） |
| Embedding | ID → 初始向量 | 表 `(V, D)`，可训练 |
| Position Embedding | 注入「第几个位置」 | 表 `(T, D)`，可训练 |
| Transformer Block | 结合上下文变换表示 | Q/K/V、FFN、LayerNorm |
| LM Head | 隐藏状态 → V 个分数 | W、b，可训练 |
| Softmax | 分数 → 概率 | 无参数 |

**狭义的「大模型」只指 Transformer Block 堆叠**；Tokenizer、Embedding、LM Head、Softmax 是包在它外面的输入输出层。

**例子**：课程文章里，LM Head 把 `(1, 6, 4)` 拍平成 24 维，用 `W: (24, 273)` 映射到词表。当前项目代码已改为只取最后一个位置的 `(1, 4)` 映射。两种都是「隐藏状态 → 词表分数」，只是取法不同。

## 2. 三种「向量」的区别

最容易混的一组概念：

| | Token ID | 初始 Embedding | Hidden State |
|---|---|---|---|
| 本质 | 词表里的编号 | 查表得到的可训练向量 | 经过 Transformer 后的向量 |
| 是否含语义 | 否，53 不比 2「大」 | 训练后才有，同一 ID 永远同一行 | 有，且随上下文变化 |
| 例子 | 「苹果」= 某个 ID | 两句话里的「苹果」向量相同 | 「苹果很好吃」和「苹果手机」里的不同 |

维度上 `hidden_dim = embed_dim = 4`，但数值和信息不同。子牙的比喻：初始 Embedding 是蒙灰的旧照片，Transformer 把灰擦掉，再结合场景认出照片里的人。

## 3. Transformer 内部：先知道位置，不求细节

开篇把 Transformer 当黑盒，只记三个约束：

- **多头整除**：`D = H × D_h`。比如 `D = 4`、2 个头，每头 2 维；`D = 5` 就无法等分成 2 头。
- **因果掩码**：位置 i 只能看到自己和之前的位置，不能偷看后面的 token。
- **FFN 中间层**：通常是 `4 × hidden_dim`。

Block 内的组件：Masked Multi-Head Attention → Add & Norm → FFN → Add & Norm。细节留到专题七之后。

## 4. 从概率到一句话：自回归

```text
"你是谁"         → argmax → "我"
"你是谁我"       → argmax → "是"
"你是谁我是"     → …
…                → <EOS>  → 停止
```

- 每次只取最后 `context_len` 个 token 作为输入，窗口不会无限变长。
- `<EOS>` 是训练数据里人为加的结束符，模型学会预测它，就会停下；程序另设最大长度兜底。
- 一直取最大值是**贪心解码**，此外还有采样策略。

**引出的问题**：ChatGPT 的词表有 10 万以上，所以最后一步是 `(1, 10w+)` 的向量。这个计算量就是 Weight Tying、KV Cache 等技术要解决的问题。

## 5. 各模块的技术演进（只记主线）

| 模块 | 演进主线 | 本课实现 |
|---|---|---|
| Tokenizer | 字符 → 词 → 子词（BPE / WordPiece / SentencePiece）→ Byte-level BPE → tiktoken → 多模态 | 字符级 |
| Embedding | One-Hot → 可训练表 → Word2Vec / GloVe（静态）→ BERT / GPT（上下文化）→ 句向量（RAG） | One-Hot → 可训练表 |
| 位置编码 | 可学习绝对位置 → Sinusoidal → 相对位置 → RoPE（旋转 Q/K）→ ALiBi | 可学习绝对位置，相加 |
| 优化器 | SGD → Momentum → AdaGrad / RMSProp → Adam → AdamW | SGD |

一句话：**Tokenizer 决定世界被切成哪些单位，Embedding 决定这些单位在向量空间中的位置。**

## 来源

- 语雀：《【笔记】开篇：带你透彻理解大模型底层》及其子篇（视频笔记、tokenizer 技术、embedding 技术、优化器技术）。
- 视频：`2、尝鲜：带你透彻理解大模型底层工作机制.mp4`（字幕已核对）。
- 代码对照：`/Users/michael/workspace/ziya-chatgpt-3/pytorch/Model.py`。
