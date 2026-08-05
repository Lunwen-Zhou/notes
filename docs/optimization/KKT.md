## KKT

*本部分内容 优先参考《非线性最优化理论与方法》第 7 章*

### 凸优化 KKT 充要性

设 $f: \mathbb{R}^n \to (-\infty, \infty]$ 为一个**proper**、**下半连续**、**凸函数**。考虑问题：
$$
\begin{equation}
\begin{aligned}
\min_{x \in \mathbb{R}^n} \quad & f(x) \\
\text{s.t.} \quad & g_i(x) \leq 0, \quad i = 1, \dots, m, \\
& h_j(x) = 0, \quad j = 1, \dots, p.
\end{aligned}
\end{equation}
$$
其中：

- 每个 $g_i : \mathbb{R}^n \to \mathbb{R}$ 是**凸函数**；

- 每个 $h_j : \mathbb{R}^n \to \mathbb{R}$ 是**仿射函数**。

假设该问题满足 **Slater 条件**

>  即存在某个点 $\tilde{x}$ 使得
>  $$
>  \begin{aligned}
>  & g_i(\tilde{x}) < 0, \quad i = 1, \dots, m, \\
>  & h_j(\tilde{x}) = 0, \quad j = 1, \dots, p.
>  \end{aligned}
>  $$



**结论**：在上述条件下，一个点 $x^\star \in \text{dom}(f)$ 是原问题的**全局最优解**，当且仅当存在拉格朗日乘子
$$
\begin{aligned}
& \lambda_i^\star \geq 0, \quad i = 1, \dots, m,
 \\
& \mu_j^\star \in \mathbb{R}, \quad j = 1, \dots, p
\end{aligned}
$$
使得以下 **KKT 条件** 同时成立：

1. **一阶最优性** Stationarity
   $$
   0 \in \partial f(x^\star) + \sum_{i=1}^{m} \lambda_i^\star \partial g_i(x^\star) + \sum_{j=1}^{p} \mu_j^\star \nabla h_j(x^\star)
   $$

2. **原始可行性** Primal feasibility
   $$
   \begin{aligned}
   & g_i(x^\star) \leq 0, \quad i = 1, \dots, m,\\
   & h_j(x^\star) = 0, \quad j = 1, \dots, p
   \end{aligned}
   $$

3. **对偶可行性** Dual feasibility
   $$
   \lambda_i^\star \geq 0, \quad i = 1, \dots, m
   $$

   > 等式约束的乘子 $\mu_j^\star$ 没有正负限制

4. **互补松弛性** Complementary slackness

   不等式约束与其对应的乘子的乘积必须为 0
   $$
   \lambda_i^\star g_i(x^\star) = 0, \quad i = 1, \dots, m
   $$

- 该定理条件下，是 KKT 条件是充要条件

- 若 $f$ 严格凸且可行域为凸集，则满足 KKT 条件的解 $x^*$ 是唯一的（但 $\lambda^*,\mu^*$ 不一定）

  即唯一性来自
  $$
  f \text{ 严格凸} + \text{可行域凸}
  \Longrightarrow
  \text{最优解唯一}
  $$

- 若**仅含等式约束**，KKT 条件退化为
  $$
  \begin{aligned}
  0 &\in \partial_x L(x^\star, \lambda^\star, \mu^\star), \\
  0 &\in \partial f(x^\star) + \sum_{i=1}^{m} \lambda_i^\star \partial g_i(x^\star) + \sum_{j=1}^{p} \mu_j^\star \nabla h_j(x^\star)
  \end{aligned}
  $$

- $x \notin \text{dom} (f)$ 时，$f(x) = +\infty$，此时讨论最优解（认为不是可行点）、次梯度都没有意义



### 例题

（研一 《最优化理论与方法》 期末考试）

求下述优化问题的 KKT 条件并由此求出优化问题的最优解，其中 $c \in \mathbb{R}^n$ 为常量
$$
\begin{equation}
\begin{aligned}
\min_{x} \quad & c^T x + \sum_{i=1}^{n} x_i \ln x_i \\
\text{s.t.} \quad & \sum_{i=1}^{n} x_i = 1
\end{aligned}
\end{equation}
$$
**Sol**：

> $f(x) = c^T x + \sum_{i=1}^{n} x_i \ln x_i$ 是 proper
>
> **严格凸性**
> $$
> \nabla^2 f(x) = \begin{bmatrix} \frac{1}{x_1} & 0 & \cdots & 0 \\ 0 & \frac{1}{x_2} & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & \frac{1}{x_n} \end{bmatrix}\succ 0
> $$
> 故严格凸
>
> 约束条件 $h_1(x) = \sum_{i=1}^{n} x_i - 1=x^T \mathbf{1} - 1$ 是仿射函数（只有一个约束），$h_1 : \mathbb{R}^n \to \mathbb{R}$
>
> ① 一阶最优性，Stationarity
>
> 由$\frac{\partial f}{\partial x_i} = c_i + \ln x_i + 1$，得
> $$
> \nabla f(x) = \begin{pmatrix} \frac{\partial f}{\partial x_1} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{pmatrix} = \begin{pmatrix} c_1 + \ln x_1 + 1 \\ \vdots \\ c_n + \ln x_n + 1 \end{pmatrix} \text{}
> $$
> $\nabla h(x) = \mathbf{1}$，由
> $$
> \mathbf{0} = \nabla f(x^\star) + \mu^\star \nabla h(x^\star)
> $$
> 可得
> $$
>  \begin{pmatrix} c_1 + \ln x_1 + 1 \\ \vdots \\ c_n + \ln x_n + 1 \end{pmatrix} + \mu^\star \begin{pmatrix} 1 \\ \vdots \\ 1 \end{pmatrix} = 0 \text{}
> $$
> 等价于
> $$
> c_i + \ln x_i^\star + 1 + \mu^\star = 0 \quad i = 1, \dots, n
> $$
> 即
> $$
> x_i^\star = e^{-c_i-1-\mu^\star}
> $$
> ② 原始可行性，Primal feasibility
>
> 由 $h(x^\star) = 0$，得
> $$
> \sum_{i=1}^{n} x_i^\star = 1
> $$
> 即
> $$
> \begin{align}
> e^{\mu^\star} &= \sum_{i=1}^{n}  e^{-c_i-1}\\  
> x_i^\star &=  \frac{e^{-c_i}}{\sum_{j=1}^{n} e^{-c_j}}
> \end{align}
> $$
>
> $\square$

