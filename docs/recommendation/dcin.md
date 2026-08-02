# DCIN 论文笔记

## 1. 问题背景

传统方法可能把多个历史页面中的商品直接展平成一个长序列，从而丢失页面边界以及页内决策上下文。DCIN 的目标是利用历史页面内商品之间的关系，更准确地建模用户兴趣。

## 2. CIU

设第 $i$ 个历史页面为

$$
\mathbf P_i\in\mathbb R^{P\times D_s},
$$

点击商品为 $\mathbf x_i^c\in\mathbb R^{D_s}$。定义

$$
Q_i=\mathbf x_i^cW^Q,\qquad
K_i=\mathbf P_iW^K,\qquad
V_i=\mathbf P_iW^V.
$$

注意力输出可写为

$$
\operatorname{CIU}_i
=
\operatorname{Softmax}\left(
\frac{Q_iK_i^\top}{\sqrt d}+f_i
\right)V_iW^O+\mathbf x_i^c.
$$

其中 $f_i$ 是相关性 Mask，被屏蔽商品在 Softmax 后的权重为 $0$。

## 3. 工程映射

在项目中可把历史序列从 `[B, 60, D]` 改为 `[B, 3, 20, D]`，从而保留“三个历史页面、每页二十个商品”的结构。
