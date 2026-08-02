# TensorFlow 1.x 代码笔记

## `tf.variable_scope`

```python
def input_layer(self, inputs, units, name):
    with tf.variable_scope(
        name,
        reuse=tf.AUTO_REUSE,
        partitioner=self.partitioner
    ):
        return self.linear_func(inputs, units, "trans_inputs")
```

`with` 创建上下文。代码块内部新建的变量会自动带上对应的变量域前缀。

## 常见张量形状

在推荐模型中，第一个维度通常表示 Batch：

$$
X\in\mathbb R^{B\times S\times D},
$$

其中 $B$ 是批大小，$S$ 是序列长度，$D$ 是特征维度。
