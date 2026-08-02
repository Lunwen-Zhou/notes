# DLF 论文笔记

DLF 在每一层中同时建模低阶显式交互、高阶显式交互和隐式交互，再通过注意力融合各个交互分支。

## 低阶交互示例

$$
S=\frac{QK^\top}{\sqrt d},\qquad
A=\operatorname{Softmax}(S),\qquad
Z=AV.
$$

对应的 TensorFlow 代码通常包含三个线性映射：

```python
seed_q = linear(low_order_seed, rank)
current_k = linear(current, rank)
current_v = linear(current, units)
weights = masked_softmax(tf.matmul(seed_q, current_k, transpose_b=True), mask)
out = tf.matmul(weights, current_v)
```
