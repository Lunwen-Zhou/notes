# MMoE 基础

对于第 $i$ 个专家，记其输出为 $E_i(x)$。任务 $t$ 的 Gate 产生权重

$$
\mathbf g^{(t)}(x)
=
\operatorname{Softmax}\left(\operatorname{MLP}^{(t)}_G(x)\right).
$$

任务 $t$ 得到的混合表示为

$$
\mathbf h^{(t)}
=
\sum_{i=1}^{N}g_i^{(t)}(x)E_i(x).
$$

不同任务使用不同 Gate，因此可以按照各自目标选择专家。
