# 优化理论笔记

## 近端算子

给定函数 $f$ 和步长 $\lambda>0$，近端算子定义为

$$
\operatorname{prox}_{\lambda f}(v)
=
\arg\min_x\left\{
 f(x)+\frac{1}{2\lambda}\lVert x-v\rVert_2^2
\right\}.
$$

## 软阈值算子

当 $f(x)=\lVert x\rVert_1$ 时，近端算子是逐元素软阈值：

$$
\operatorname{soft}(z,\tau)
=
\operatorname{sign}(z)\max(|z|-\tau,0).
$$
