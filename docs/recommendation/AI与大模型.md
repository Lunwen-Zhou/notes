# AI 与大模型

## 大模型

### 参数

模型中需要被学习的变量

- **优化中**

  设优化形式 $\min_{\theta} f(\theta)$，这里 $\theta = (\theta_1, \theta_2, \dots, \theta_n) \in \mathbb{R}^n$ 是一个**向量参数**，每一个 $\theta_i$ 都是一个参数

- **机器学习中**
  - 线性模型：$y = w_1 x_1 + w_2 x_2 + b$，参数为 $\theta = (w_1, w_2, b)$
  - 神经网络：一个简单 **全连接层** 为 $y = Wx + b$，参数为 权重矩阵 $W$、偏置 $b$

---



### Softmax

把得分向量归一成概率分布：各分量非负且和为 1

具体算法：（数值稳定版本）设输入的向量为 $z$，先减最大值再指数归一化，保证数值稳定：
$$
p_i = \frac{e^{z_i - \max z}}{\sum_j e^{z_j - \max{z}}}
$$
**代码**（假设传入的是 Pyhton 的 list 类型 `scores`）

```python
import torch

def softmax(scores: list[float]) -> torch.Tensor:
    scores = torch.tensor(scores, dtype=torch.float32)
    
    max_score = torch.max(scores)
    exp_scores = torch.exp(scores - max_score)
    sum_exp_scores = torch.sum(exp_scores)
    
    return exp_scores / sum_exp_scores
```

- **具体例子**

  > 设 `scores = [1, 2, 3]`。首先经过 def 内的第一行，`scores` 变为 `tensor([1., 2., 3.])`
  >
  > `max_score` 为 `tensor(3.)`，接下来 `scores - max_score` 会 **广播**，具体来说为
  >
  > ```
  > tensor([1., 2., 3.]) - tensor(3.)
  > ```



### K - Means

迭代过程中，衡量样本点 **归属** 的核心准则是：**到质心的欧氏距离最小**

---



### SmoothQuant

SmoothQuant 通过等价变换，把量化难度从 activation 迁移到 weight，本质上是将 activation 的 **scale** 吸收到**权重**中

---



### LayerNorm

可视为一个算子 $\mathrm{LN}(\cdot):\mathbb{R}^d \to \mathbb{R}^d$，$x \mapsto y = \mathrm{LN}(x)$

LN 可在一定程度上避免 **梯度消失** 或 **梯度爆炸** 的问题，**增强模型的泛化能力**

**计算流程**：

1. 计算均值
   $$
   \mu = \frac{1}{d}\sum_{i=1}^d x_i
   $$

2. 计算方差
   $$
   \sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2
   $$

3. 归一化
   $$
   \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
   $$

4. 缩放 + 平移
   $$
   y_i = \gamma \hat{x}_i + \beta
   $$

即：先减均值 → 再除方差 → 再仿射变换



#### Post-LN

原始 Transformer

先做子层计算 Sublayer ，再加残差 $x$  ，再做 LayerNorm
$$
y = \mathrm{LN}(x + \mathrm{Sublayer}(x))
$$

- $\mathrm{Sublayer}(x)$：可以是以下两种

  - Attention
    $$
     \mathrm{softmax}(xW_Q (xW_K)^\top) xW_V
    $$

  - MLP
    $$
    W_2 \sigma(W_1 x + b_1) + b_2
    $$
    

#### Pre-LN

现在的主流。先对输入做 LN，结构为
$$
y = x + \mathrm{Sublayer}(\mathrm{LN}(x))
$$
---



### RMSNorm

#### 均方根

RMS：Root Mean Square，均方根。均方根可以看成是一个向量的”平均大小“

普通的均值
$$
\frac{1}{d}\sum x_i
$$
会正负抵消。而均方根
$$
\sqrt{\frac{1}{d}\sum x_i^2}
$$
更加稳定



**流程**

1. 计算均方
   $$
   \text{RMS} = \sqrt{\frac{1}{d}\sum_{i=1}^d x_i^2 + \varepsilon}
   $$

2. 归一化
   $$
   \hat{x}_i = \frac{x_i}{\text{RMS}}
   $$

3. 缩放（通常没有偏置）
   $$
   y_i = \gamma \hat{x}_i
   $$
   

---



### FNN：前馈神经网络

Feedforward Neural Network

对于一个样本 $x$：


$$
y = f(Wx + b)
$$


多层就是不断复合：


$$
x \to f_1 \to f_2 \to \cdots \to f_L
$$


本质：静态映射（static mapping）

没有记忆，不知道前一个数据是什么

适合：图象分类、表格数据、回归任务



### RNN：循环神经网络

有“记忆”（hidden state），每一步都：

① 接收当前输入 $x_t$

② 同时利用“过去的信息” $h_{t-1}$

公式：
$$
h_t = f(W_h h_{t-1} + W_x x_t)
$$

$$
y_t = g(W_y h_t)
$$

是一个**推进系统**：
$$
h_t = T(h_{t-1}, x_t)
$$
是**动态系统 / 序列优化问题**

#### 与前馈神经网络对比

|     特性     | 前馈网络 |        RNN         |
| :----------: | :------: | :----------------: |
|  是否有记忆  |    无    |         有         |
| 输入是否独立 |    有    |         无         |
| 是否建模时间 |    无    |         有         |
|     结构     |   DAG    | 有环（展开后是链） |

---



### RMSprop

RMSprop 会对每个参数维护一个“历史梯度平方的指数加权平均”：


$$
v_t = \beta v_{t-1} + (1-\beta) g_t^2
$$


更新时：


$$
\theta \leftarrow \theta - \frac{\eta}{\sqrt{v_t} + \epsilon} g_t
$$

这里 $\eta$ 是一开始定下来的

属于**自适应学习率**方法

> $\frac{1}{\sqrt{v_t}}$：每个参数都有自己的 $v_t$，所以：
>
> 梯度大的维度 → $v_t$ 大 → 步长变小
>
> 梯度小的维度 → $v_t$ 小 → 步长变大

步长：$\frac{\eta}{\sqrt{v_t} + \epsilon}$

---



### KV Cache

在 Transformer 推理时，每一层都会产生：Key（K）、Value（V）

这些东西会被 **缓存下来（Cache）**，因为后面的 token 会反复用到前面所有 token 的 K、V

所以 KV Cache 是一个 **不断增长的大矩阵**（随序列长度增长



量化 KV Cache 的原因：用低精度（INT8 / INT4）存储 → 省内存 + 提速

工业标准做法：

- 存：INT4 / INT8（省内存）
- 用：反量化 → FP16（保证精度）

---



### NPU

在大模型训练中的核心作用

1. 高效执行张量/矩阵运算

   大模型训练的核心是大量**高维张量运算**（如 Transformer 中的**QKV 注意力机制**、**全连接层**等）

   NPU 内置专用硬件单元（如张量核心），能并行、低延迟地完成这些操作，显著提升训练吞吐量

2. 支持混合精度训练

3. 降低训练能耗与成本



早期 NPU 主要用于**推理（inference）**，但随着架构演进（如支持梯度计算、反向传播优化），**新一代 NPU 已具备大模型训练能力**



NPU、GPU、CPU 在大模型训练中的对比

| 特性           | CPU                  | GPU                             | NPU                                 |
| -------------- | -------------------- | ------------------------------- | ----------------------------------- |
| **通用性**     | 高（适合控制流）     | 中（适合并行计算）              | 低（专用于 AI）                     |
| **并行能力**   | 弱（核心少）         | 强（数千 CUDA 核）              | 极强（专为张量并行设计）            |
| **能效比**     | 低                   | 中                              | **高**                              |
| **训练适用性** | 不适合               | 主流（如 A100/H100）            | **越来越适合**（尤其推理+部分训练） |
| **编程生态**   | 成熟（C/C++/Python） | 成熟（CUDA/TensorFlow/PyTorch） | 正在完善（需厂商工具链支持）        |

---





### 张量 Swap

一种“显存不够，内存来凑”的智能调度策略，核心目标是：在有限硬件资源下，最大化模型规模或序列长度的支持能力



需要张量 Swap 的原因：

**GPU 显存有限**（如 80GB A100）

KV Cache 占用巨大

**激活值（Activations）随序列长度线性增长**，训练时显存压力极大



当显存不足时，系统必须做出选择：

1. ❌ 直接 OOM（Out-Of-Memory）崩溃
2. ✅ **Swap 出部分张量** → 腾出显存 → 继续运行

---



### 互信息

定义：
$$
I(X;Y) = H(Y) - H(Y \mid X)
$$

- 含义：知道 $X$ 之后，$Y$ 的不确定性减少了多少

在特征工程的特征选择（Feature Selection）过程中，当我们怀疑特征 X 与目标变量 Y 之间存在复杂的非线性相关性（例如 $Y=X^2$ 或周期性关系），且 $X$ **并不服从正态分布**时，在评估特征重要性时最为准确且稳健的是**互信息**

不需要正态分布、不要求线性

---



## Transformer

Transformer 是一种用 **Self-Attention** 来建模 token 与 token 之间关系的模型

> 如：
>
> ```
> 我 喜欢 机器 学习
> ```
>
> Transformer 不只是按顺序读，而是会让每个词去“看”这句话里的其他词，判断哪些词对自己更重要

而 RNN 特点：按顺序处理

**缺点**：

- 长句子中，前面的信息传到后面会衰减

- 不能很好并行，因为必须一个词一个词处理；

- 长距离依赖不好建模

Transformer：不再按顺序一步步读，而是让所有 token 同时互相“看一遍”，即为“Self-Attention”



假设一句话有 4 个 token：

```text
我，喜欢，机器，学习
```

每个 token 先被表示成向量：$x_1,x_2,x_3,x_4$。组成一个矩阵：

$$
X=
\begin{bmatrix}
- & x_1 & -\\
- & x_2 & -\\
- & x_3 & -\\
- & x_4 & -
\end{bmatrix}
\in \mathbb R^{4\times d}
$$

- 4 表示有 4 个 token
- $d$ 表示每个 token 的 embedding 维度（是 token 原始输入向量维度，hidden size 维度）

Self-Attention 对每一个 token，重新生成一个新的向量，这个新向量会 **融合** 句子中其他 token 的信息

>  比如对于“学习”这个 token，它可能会重点关注“机器”，因为“机器学习”是一个整体概念

三个重要的向量

```
Query  查询向量     # 我想找什么信息
Key    被查询向量   # 我能提供什么线索
Value  信息向量     # 我真正携带的信息
```

对于每个 token 向量 $x_i$，都会通过三个矩阵变换得到
$$
q_i=x_iW_Q, \quad k_i=x_iW_K, \quad v_i=x_iW_V
$$
即
$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V
$$

- $Q \in \mathbb R^{n \times d_k}$：$n$ 个 Query 向量组成的矩阵
- $K \in \mathbb R^{m \times d_k}$：$m$ 个 Key 向量组成的矩阵
- $V \in \mathbb R^{m \times d_v}$：$m$ 个 Value 向量组成的矩阵



**Attention 的标准公式**
$$
\boxed{
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}
\left(
\frac{QK^\top}{\sqrt{d_k}}
\right)V}
$$
$QK^\top\in \mathbb R^{n\times n}$ 中的元素 $s_{ij}$ 表示第 $i$ 个 token 对第 $j$ 个 token 的关注程度。在 Self-Attention 中，Query 和 Key 来自同一序列，故 $n=m$。此时 $s_{ij}$ 可理解为第 $i$ 个 token 对第 $j$ 个 token 的关注程度

$d_k$ 是 Key 或 Query 向量的维度，当 $d_k$ 较大时，点积 $QK^\top$ 的方差会增大，导致 softmax 梯度变得很小。分别取查询矩阵 $Q$ 和键矩阵 $K$ 的某一行 $q,k\in \mathbb{R}^{d_k}$，则有下述关系
$$
\text{Var} (q\cdot k) = d_k
$$
由 $\text{Var}(c\cdot x) = c^2 \text{Var} (x)$，故
$$
\text{Var}\left( \frac{q\cdot k}{\sqrt{d_k}}\right) = 1
$$
即这是在将方差归一化为 1。设

$$
A=
\operatorname{softmax}
\left(
\frac{QK^\top}{\sqrt{d_k}}
\right)
$$
这里 softmax 是按行来做的

最后 $Z=AV$，相当于把不同 token 的 Value 向量加权求和



参数：模型中 **真正需要训练的** 是生成 $Q,K,V$ 的三个线性变换矩阵：
$$
W_Q, \quad W_K, \quad W_V
$$
具体例子：

> 以 BERT-base 的一个 attention head（注意力头）为例：$d_{\text{model}}=768$，$d_k=d_v=64$
>
> 则
> $$
> W_Q\in \mathbb R^{768\times 64},\quad W_K\in \mathbb R^{768\times 64}, \quad W_V\in \mathbb R^{768\times 64}
> $$
> 参数总量
> $$
> 3\times 768\times 64 = 147456
> $$
> 如果考虑偏置，每一个线性层还有一个偏置向量：
> $$
> b_Q, b_K,b_V \in \mathbb{R}^{64}
> $$
> 加上偏置后的参数总量为
> $$
> 147456 + 3\times 64 = 147648
> $$
> 

### Cross-Attention

假设机器翻译，整个过程是（英文翻译为中文）

```
英文句子
   ↓
Encoder
   ↓
英文语义表示
   ↓
Decoder
   ↓
中文句子
```

Encoder 的作用：把输入语言转换成机器能够理解的语义表示。如输入 I love machine learning，先经过分词，转为 `[I, love, machine, learning]`，每个 token 变为 embedding：
$$
X=
\begin{bmatrix}
x_1\\
x_2\\
x_3\\
x_4
\end{bmatrix}
$$
经过 Encoder $H=\operatorname{Encoder}(X)$，得到：
$$
H=
\begin{bmatrix}
h_1\\
h_2\\
h_3\\
h_4
\end{bmatrix}
$$
这里 $h_i$ 不仅有本身单词的含义，还融合了上下文（eg：经过 Encoder 后，某个 $h_{\text{machine}}$ 不只是“机器”之义，还知道了后面有“学习”，所以理解成“机器学习” ）

Encoder 本质在做“词 → 待上下文的语义表示”

Decoder 的作用：根据 Encoder 提供的信息，一个一个生成目标语言



具体例子：

> Encoder 输入：（3 个 token）
>
> ```
> I love AI
> ```
>
> Decoder 当前生成
>
> ```
> 我 喜欢
> ```
>
> 此时 Decoder 产生 Query $Q \in \mathbb{R}^{2 \times d_k}$，Encoder 产生 Key $K \in \mathbb R^{3 \times d_k}$，此时 $QK^\top \in \mathbb R^{2 \times 3}$，即
> $$
> \begin{bmatrix}
> s_{11}&s_{12}&s_{13}\\
> s_{21}&s_{22}&s_{23}
> \end{bmatrix}
> $$
> 含义：
>
> - 第一行：“我”这个 Query 看英文三个 token 的程度
> - 第二行：“喜欢”这个 Query 看英文三个 token 的程度

---



## 线性代数

### SVD 分解

#### 紧凑 SVD 形式

设 $X \in \mathbb{R}^{m\times n}$，则
$$
X = U \Sigma V^T =\sum_{i=1}^{r} \sigma_i u_i v_i^T
$$
其中 $U \in \mathbb{R}^{m\times r}$，满足 $U^T U = I_r$（列正交规范）

$V \in \mathbb{R}^{n\times r}$，满足 $V^T V = I_r$

$\Sigma = \mathrm{diag}(\sigma_1, \dots, \sigma_r)$（奇异值）

$\sigma_i$：第 $i$ 个奇异值（$\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_r$）

$u_i$：左奇异向量（列向量）

$v_i$：右奇异向量（列向量）

- $\sigma_i u_i v_i^T$ 是一个秩为 1 的矩阵（rank-1 matrix）

这个分解可以理解为：
$$
X = (\text{最重要结构}) + (\text{次重要}) + \cdots
$$
如果我们不是加完 $r$ 个结构，而是前 $k$ 个，可以得到如下的 rank-$k$ 近似



#### 最佳 rank-$k$ 近似

$X_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T$，只保留前 $k$ 个最重要的结构。写成矩阵形式：
$$
X_k = U_k \Sigma_k V_k^T
$$
其中：

$U_k = [u_1,\dots,u_k] \in \mathbb{R}^{m\times k}$

$V_k = [v_1,\dots,v_k] \in \mathbb{R}^{n\times k}$

$\Sigma_k = \mathrm{diag}(\sigma_1,\dots,\sigma_k)$

满足：（Eckart–Young 定理）
$$
X_k = \arg\min_{\mathrm{rank}(Y)\le k} \|X - Y\|_F^2
$$
误差来源：
$$
\|X - X_k\|_F^2 = \sum_{i=k+1}^{r} \sigma_i^2
$$


#### 完整 SVD

设 $X \in \mathbb{R}^{m\times n}$，则存在分解
$$
X = U \Sigma V^T
$$
其中 $U \in \mathbb{R}^{m\times m}\ ,V \in \mathbb{R}^{n\times n}$ 为正交矩阵

> 即 $U^T U = UU^T = I_m$，$V^T V = VV^T = I_n$

$\Sigma \in \mathbb{R}^{m\times n}$，具体为
$$
\Sigma = 
\begin{bmatrix}
\sigma_1 & & & \\
& \ddots & & \\
& & \sigma_r & \\
& & & 0 \\
& & & & \ddots
\end{bmatrix}
 =
\begin{bmatrix}
\Sigma_r & 0_{r\times (n-r)} \\
0_{(m-r)\times r} & 0_{(m-r)\times (n-r)}
\end{bmatrix}
\in \mathbb{R}^{m\times n}
$$
$\Sigma_r = \mathrm{diag}(\sigma_1,\dots,\sigma_r) \in \mathbb{R}^{r\times r}$



**应用**

- 图象去噪

  图像本质是一个矩阵（像素矩阵），用 SVD 提取主要结构、去掉噪声

- 文本主题建模

  词-文档矩阵。如

  |      | 文档1 | 文档2 | 文档3 |
  | :--: | :---: | :---: | :---: |
  | 词1  |   3   |   0   |   1   |
  | 词2  |   0   |   2   |   1   |
  | 词3  |   5   |   1   |   0   |

- 推荐系统

  用户-电影评分矩阵，如

  |       | 电影1 | 电影2 | 电影3 |
  | :---: | :---: | :---: | :---: |
  | 用户A |   5   |   ?   |   3   |
  | 用户B |   4   |   2   |   ?   |
  | 用户C |   ?   |   5   |   4   |

决策树则不行，因为没有矩阵结构



## 概率论

### 期望

$$
\operatorname{Var}(X)=E[X^2]-(E[X])^2
$$

$\operatorname{Var}(X)\geq 0$ 恒成立，因此上式右侧 $\geq 0$ 恒成立



设 $X, Y$ 是两个随机变量，且 **相互独立**，并且相关期望存在，则有


$$
\mathbb{E}[XY] = \mathbb{E}[X] \cdot \mathbb{E}[Y]
$$

---



### 协方差

设有 $n$ 个样本，每个样本是 $d$ 维向量。记 $x_i \in \mathbb{R}^d,\quad i=1,\dots,n$

> 标准的做法是每一行一个样本

$$
X =
\begin{bmatrix}
- & x_1^\top & - \\
- & x_2^\top & - \\
& \vdots & \\
- & x_n^\top & -
\end{bmatrix}
\in \mathbb{R}^{n \times d}
$$

$$
\mu = \frac{1}{n}\sum_{i=1}^n x_i \in \mathbb{R}^d
$$

$$
\Sigma = \frac{1}{n} (X - \mathbf{1}\mu^\top)^\top(X - \mathbf{1}\mu^\top)
$$

例：给定二维数据集，包含三个样本 $\left\{(0,0), (1,1), (2,2)\right\}$，求其**协方差矩阵**

构造矩阵
$$
X =
\begin{bmatrix}
0 & 0 \\
1 & 1 \\
2 & 2
\end{bmatrix}
$$
求中心
$$
\mu = \begin{bmatrix}
\dfrac{0+1+2}{3}\\
\dfrac{0+1+2}{3}
\end{bmatrix} = 
\begin{bmatrix}
1\\
1
\end{bmatrix}
$$

> $$
> \mu = \frac{1}{n}\sum_{i=1}^n x_i \in \mathbb{R}^d
> $$
>
> 这里
> $$
> x_1 = (0,0)^\top\quad x_2 = (1,1)^\top \quad x_3=(2,2)^\top
> $$

中心化数据
$$
X - \mathbf{1}\mu^\top =
\begin{bmatrix}
-1 & -1 \\
0 & 0 \\
1 & 1
\end{bmatrix}
$$

$$
\Sigma = \frac{1}{n} (X - \mathbf{1}\mu^\top)^\top (X - \mathbf{1}\mu^\top) = \frac{1}{3} \cdot
\begin{bmatrix}
2 & 2 \\
2 & 2
\end{bmatrix}
=
\begin{bmatrix}
\frac{2}{3} & \frac{2}{3}\\
\frac{2}{3} & \frac{2}{3}
\end{bmatrix}
$$





## 数值分析

### 插值多项式

插值多项式在节点处的函数值一定等于给定函数值



对于给定的 $n+1$ 个互异节点，次数不超过 $n$ 的插值多项式存在且唯一

比如，2个点就可以唯一确定一条直线

$\Longrightarrow$ Lagrange 插值法和 Newton 插值法构造的插值多项式是相同的



高次插值多项式**并不一定**能更好地逼近原函数，具体见下面的 Runge 现象

#### Runge 现象

在区间 $[-1,1]$ 上，用等距节点插值
$$
f(x)=\frac{1}{1+25x^2}
$$
随着次数增加：


- 中间逼近变好
- **两端剧烈振荡（发散）**

结论：高次多项式插值 **不一定更好，甚至可能更差**

---



### 三次样条插值

要求插值函数在**节点处**一阶和二阶导数连续，以保证光滑性

在每个子区间上用三次多项式逼近函数

相比于高次多项式，三次样条能避免 Runge 现象
