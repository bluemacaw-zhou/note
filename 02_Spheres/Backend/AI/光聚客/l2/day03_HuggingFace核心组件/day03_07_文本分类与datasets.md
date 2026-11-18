---
type: journal
sphere: Backend
date: 2026-11-18
tags: [Backend, AI, 光聚客, 文本分类, datasets]
---

# 文本分类与 datasets

> 总览 [[day03_00_总览|day03]] · ← [[day03_06_特征空间与词向量|词向量]] · 终点

**为什么需要**：生成只是一种任务。同样是「分词 → 向量 → Transformer」，把最后的输出头从「21128 选 1」换成「N 个类别选 1」，就能做分类。

## 生成与分类只差一个输出头

| | 文本生成（04） | 文本分类 |
|---|---|---|
| 模型类 | `AutoModelForCausalLM` | `AutoModelForSequenceClassification` |
| 输出 | 下一个字在 21128 个字上的概率 | 整句话在 N 个类别上的概率 |
| pipeline | `pipeline("text-generation")` | `pipeline("text-classification")` |

## 课程分类示例的两个陷阱

**陷阱一：test03 的分类头是随机的**

`test03.py` 用 `BertForSequenceClassification` 加载 `bert-base-chinese`。但 `bert-base-chinese` 只做过**预训练**，从来没有学过分类：

- 加载时，transformers 会警告 `classifier.weight` 和 `classifier.bias` 是新初始化的（newly initialized）；
- 输出的 `LABEL_0` / `LABEL_1` 和它们的分数都来自随机权重，**没有任何含义**。

要做分类，有两条路：拿它在自己的标注数据上**微调**，或者直接找一个已经微调好的分类模型。

**陷阱二：资料示例用错了模型**

资料用 `uer/roberta-base-finetuned-cluener2020-chinese` 做 `sentiment-analysis`（情感分析）。但 CLUENER2020 是**命名实体识别**（NER）数据集，这个模型是给每个字标「人名、地名、机构」等实体标签的，不是判断整句话的情感。

- 想做中文情感分析，要选在情感数据上微调过的模型，例如 `uer/roberta-base-finetuned-jd-binary-chinese`（京东评论正面 / 负面）。
- 选模型时，要先看模型卡上写的**任务类型**和**训练数据集**。

## datasets：两个核心方法

```python
from datasets import load_dataset, load_from_disk

dataset = load_dataset("glue", "mrpc")       # 从 Hub 下载
dataset = load_from_disk("./my_dataset")     # 读本地，对应 dataset.save_to_disk(...) 保存的目录
```

- `load_dataset` 返回 `DatasetDict`，已经按 train / validation / test 划分好，对应 day01_11 的数据集划分。
- MRPC 是一个句子对任务：判断两句话是否同义。它天然是一个二分类数据集，正好可以拿来微调上面那个分类头。

**这一天的落点**：会**用**现成的模型之后，下一步就是在自己的数据上**微调**。到那时，day01、day02 的训练循环就派上用场了。
