---
type: journal
sphere: Backend
date: 2026-11-12
tags: [Backend, AI, 光聚客, PyTorch, 自动求导]
---

# PyTorch 与手写训练对照

> 总览 [[day01_00_总览|day01]] · ← [[day01_11_训练流程与常用术语|训练流程]] · 终点

**为什么需要**：前面每一步都能手写，但网络一大，求导和参数管理就写不过来了。

## 框架演进

![[procreate/深度学习框架演进.png]]

**读图**：每个框架名下面的小字是关键词，红圈标出 PyTorch。演进主线是计算图：Theano 首创自动微分，TensorFlow 用声明式的静态图（先定义整张图，再执行），PyTorch 用命令式的动态图（边执行边建图），TF 2.0 再把两者合并。

**PyTorch 的特点**：

- 动态计算图：边执行边建图，调试方便；
- 反向模式自动求导；
- 支持 GPU。

## 一一对应

课程的 `test04.py` 对比 [[02_Spheres/Backend/AI/子牙/2026-10-29_手写ChatGPT_专题一_线性模型与训练闭环|专题一]] 的 linear-demo：

| 步骤 | PyTorch | 手写 |
|---|---|---|
| 模型 | `nn.Linear(1, 1)`，放在 `nn.Module` 里 | `tool/linear.py` 的 `Linear` |
| 损失 | `nn.MSELoss()` | `np.mean(error ** 2)` |
| 优化器 | `torch.optim.SGD(params, lr)` | `tool/sgd.py` 的 `SGD` |
| 清零 | `optimizer.zero_grad()` | `SGD.zero_grad()` |
| 求梯度 | `loss.backward()`，**自动** | `Linear.backward()`，**手写链式法则** |
| 更新 | `optimizer.step()` | `SGD.step()` |

**唯一的本质区别**在求梯度：PyTorch 根据计算图自动算，其余步骤的结构完全相同。

## 数据怎么送进循环

课程 `test02.py` 用到两个类：

- `Dataset`：定义「第 i 条数据是什么」；
- `DataLoader`：负责分批、打乱，按 mini-batch 把数据交给训练循环。
