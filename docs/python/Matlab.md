# Matlab 笔记本

## 基本

### 添加所有文件夹

`addpath(genpath(pwd));` 自动添加当前目录下所有子文件夹

---

### find 寻找 true 元素的索引

`find` 用于返回非零元素（或 true 元素）的索引，`find(condition)`

```matlab
a = [1 5 3 8 2];
b = 3;

a > b
```

```
ans =

     0     1     0     1     0
```

若用 `find(a > b)`

```
ans =
     2     4
```

完整语法：`find(condition, k, direction)`

`k`：返回多少个索引

`direction`：从前还是从后找，只有 `'first'`、`'last'`

在上例中，如用 `x = find(a > b, 1, 'last')`，则输出 4

若没有满足条件，则输出 `[]`

#### a > b 的应用

应用：区间约束，将向量 `x` 投影到 $[0, U]^n$ 集合

```matlab
x = [-3, -1, 0.5, 2, 5]; 
U = 3;

x(x < 0) = 0; % 将所有小于 0 的元素统一改为 0
x(x > U) = U; % 将所有大于 U 的元素统一改为 U
```

结果：`0  0  0.5  2  3`

## 函数

### max

`[M, I] = max(A, [], dim)` 

dim = 2时，就是一行一行取最大，结果放在 `M`，位置在 `I`

`[]` 用于占位，避免 `max(A,B)` 这样被认为是两个元素或矩阵的比较

#### 连用max(max())

`sum(sum(A))`

其中 $A$ 为矩阵，第一步求和默认先按**列**，`sum(A)` 结果是**行向量**

---

### 随机

#### randn

`W = randn(L, L);`   会生成 $L \times L$ 的**实数矩阵** $W$，且每一个元素 $W(i, j)$ **独立同分布（i.i.d.）**，即
$$
W(i, j) \sim \mathcal{N}(0, 1)
$$
**i.i.d.** Independent and Identically Distributed

----

### 抽象函数

也称：**匿名函数**

形式：`f = @(input) expression`   

即使 `input` 没有内容，也还是要加括号

例 $f(x) = x^2 + y^2$ ，计算 $f(1,1)$

```matlab
f = @(x,y) x^2 + y^2;
result = f(1,1)
```

该例中，改为 `x.^2 + y.^2;` ，则可以计算向量，如计算 `f([1 2],[4 5])` ，此时逐元素运算
$$
x.^2 = [1,4], \qquad
y.^2 = [16,25]
$$
相加得 $[17,29]$

----



## 数组、向量

### arrayfun 对数组执行函数

`B = arrayfun(func, A)`

`func`: 函数句柄（可以是匿名函数或内置函数）

例： $x^2+1$ 与内置 $\sqrt x$ 函数

```matlab
A = [1, 2, 3];
B = arrayfun(@(x) x^2 + 1, A)
C = arrayfun(@sqrt, A)
```

也可以先在前面定义匿名函数 `f` ，改为 `arrayfun(f, A)`

---

### 排序 ascend

```matlab
a = [1 2 3]';
b = [-1 7]';
sort([a;b], "ascend")
```

`ascend` 默认从小到大，输出

```
ans =
    -1
     1
     2
     3
     7
```



##  矩阵

### diag

设 A 为方阵，`diag(A)` 得到的是列向量

---

### numel 统计元素个数

计算矩阵 / 向量的元素个数，方式是符合直觉的

---

### repmat 复制矩阵

`repmat(A, m, n)`：将矩阵 $A$ 按块复制成 $m\times n$ 个副本，即 $\text{repmat}(A,m,n) \in \mathbb{R}^{mp \times nq}$

若 $A$ 是 $N \times 1$ 维，`repmat(A,1,K)` 将其变成 $N \times K$ 维，形式上：
$$
\begin{bmatrix}
a_1 \\
a_2 \\
\vdots \\
a_N
\end{bmatrix}
\quad\Longrightarrow\quad
\begin{bmatrix}
a_1 & a_1 & \cdots & a_1 \\
a_2 & a_2 & \cdots & a_2 \\
\vdots & \vdots & & \vdots \\
a_N & a_N & \cdots & a_N
\end{bmatrix}
$$
例：将矩阵按行分块后，求出行向量的 $\ell_2$ 范数，再横向复制三遍

```matlab
X = [1 2 3;
     4 5 6];
row_norms = sqrt(sum(X.^2,2)); % 求模
repmat(row_norms,1,3)
```

输出：

```
ans =
    3.7417    3.7417    3.7417
    8.7750    8.7750    8.7750
```

设
$$
X=
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
\in \mathbb{R}^{2\times 3}
$$

`X.^2`：
$$
X.^2=
\begin{bmatrix}
1 & 4 & 9 \\
16 & 25 & 36
\end{bmatrix}
$$
`sum(X.^2,2)`：`2` 表示每一行求和（1为按列）
$$
\sum_{j}X_{ij}^2
=
\begin{bmatrix}
1+4+9 \\
16+25+36
\end{bmatrix}
=
\begin{bmatrix}
14\\
77
\end{bmatrix}
$$
`sqrt(sum(X.^2,2));`
$$
\text{row\_norms}
=
\begin{bmatrix}
\sqrt{14}\\
\sqrt{77}
\end{bmatrix}
=
\begin{bmatrix}
3.7417\\
8.7750
\end{bmatrix}
$$
然后再横向复制3遍


---

### 广播

设 $X$ 是 $N \times K$ 维的，如果想让矩阵的每一行元素都依次乘 $1, 2,\dots,K$，即
$$
\text{ans} = \left[ \begin{matrix}
   {{x}_{11}}\cdot 1 & {{x}_{12}}\cdot 2 & \cdots  & {{x}_{1K}}\cdot K  \\
   {{x}_{21}}\cdot 1 & {{x}_{22}}\cdot 2 & \cdots  & {{x}_{2K}}\cdot K  \\
   \vdots  & \vdots  & \ddots  & \vdots   \\
   {{x}_{N1}}\cdot 1 & {{x}_{N2}}\cdot 2 & \cdots  & {{x}_{NK}}\cdot K  \\
\end{matrix} \right]
$$

```
ans = X .* (1:K)
```

---

### 特征值

#### eig

通用求解器，计算**所有**特征值，慢

时间复杂度：$O(n^3)$

`e = eig(A);` 仅计算特征值，返回列向量

`[V, D] = eig(A);` 同时计算特征向量和特征值，返回**两个矩阵**

例：（求最小特征值）

配合 `full(w)`，可将系数存储矩阵变成普通矩阵（在很多算法中矩阵 $W$ 通常是按**稀疏矩阵**的方式存储，所以先用full转为普通矩阵，再用通用特征值算法）

```matlab
lambda_min = min(eig(full(W)));
```

如果矩阵很大，例如 $n > 1000$，更好的方法是

```matlab
lambda_min = eigs(W,1,'smallestreal');
```

---

#### eigs

专门为**稀疏矩阵**设计，利用迭代法只算其中几个特征值，速度快，可能会有报错

```matlab
[v, lambda] = eigs(A, 1, 'smallestreal', opts)
```

`1`：个数 

`smallestreal`：提取**实部最小**的特征值

`opts`：结构体对象，规模不大的话可以不带上

**opts的设置**

```matlab
opts.disp = 0;
```

`disp = 0`：关闭求解过程中的诊断信息输出，保持命令行整洁

---

### sub2ind 矩阵转为线性引索

```matlab
Idx_linear = sub2ind(Size, Row_subs, Col_subs)
```

`Idx_linear`：计算出的线性索引（用于直接访问内存）

注意得到的是整数，**列优先**（Column-major order）

例：希望存储下述矩阵的最大值的位置为 $(i,j)$ 形式
$$
A = \begin{bmatrix} 0.1 & \mathbf{0.9} \\ \mathbf{0.8} & 0.2 \\ 0.3 & \mathbf{0.7} \end{bmatrix}
$$

```matlab
A = [0.1 0.9;
     0.8 0.2;
     0.3 0.7];
     
[N, K] = size(A); 
[~, I] = max(A, [], 2); % I 是列向量, 每个元素记录该行的位置
R = (1:N)'; 

L = sub2ind([N, K], R, I)
```

这里 `R` 与 `I` 会拼出 $(1,2),(2,1),(3,2)$

```matlab
I =

     2
     1
     2

L =

     4
     2
     6
```

#### 用线性索引修改矩阵元素

```matlab
A = zeros(3,3);

idx = sub2ind(size(A), [1 3 2], [2 1 3])

A(idx) = 10
```

```
idx =

     4     3     8

A =

     0    10     0
     0     0    10
    10     0     0
```

---

### 对角矩阵 blkdiag

`blkdiag(A,B)` 会生成**块对角矩阵**（block diagonal matrix），即
$$
\text{blkdiag}(A,B)=
\begin{bmatrix}
A & 0 \\
0 & B
\end{bmatrix}
$$
如果有多个矩阵，`blkdiag(A,B,C)` 表示
$$
\begin{bmatrix}
A & 0 & 0\\
0 & B & 0\\
0 & 0 & C
\end{bmatrix}
$$
例：$H\in\mathbb{R}^{2K\times 2K}$
$$
H=
\begin{bmatrix}
\frac{1}{\alpha} I_K & \mathbf{0}_K \\
\mathbf{0}_K & \mathbf{0}_K
\end{bmatrix}
$$

```matlab
H = blkdiag((1/alpha) * eye(K), zeros(K));
```



## 凸优化

### 二次规划求解器 quadprog

需要 Optimization Toolbox

`quadprog` 用于求解**光滑二次规划问题**，其标准形式为
$$
\begin{aligned}
\min_{\tilde{x}} \quad & \frac{1}{2}\tilde{x}^{\top}H\tilde{x}+f^{\top}\tilde{x}\\
\text{s.t.}\quad & A\tilde{x}\le b,\\
& A_{\mathrm{eq}}\tilde{x}=b_{\mathrm{eq}} .
\end{aligned}
$$
要求：目标函数是**光滑二次函数**、线性约束、通常 $H \succeq 0$（以保证凸性）

---

#### 例 NNLS 非负最小二乘

（Jack Xin等 稀疏高光谱结混）

考虑问题

$$
\min_{x\ge 0} \frac12\|Ax-b\|^2
$$

其中 $A \in \mathbb{R}^{m \times n} $，$x \in \mathbb{R}^n$，$b \in \mathbb{R}^m$，展开平方：

$$
\frac12\|Ax-b\|^2
=
\frac12 x^T A^TA x - b^TAx + \frac12 b^Tb
$$

略去常数项：

$$
\min_x
\frac12 x^T (A^TA)x
+
(-A^Tb)^T x
$$

故 $H=A^TA$，$f=-A^Tb$，约束写成 quadprog 形式 $-x\le0$，即 $A=-I$，$b=0$

```matlab
% problem size
m = 50;
n = 10;

% random data
A = randn(m,n);
b = randn(m,1);

% quadprog parameters
H = A'*A;
f = -A'*b;

% inequality constraint  x >= 0
Aineq = -eye(n);
bineq = zeros(n,1);

x = quadprog(H,f,Aineq,bineq);

% display result
disp('solution x:')
disp(x)

% residual
res = norm(A*x-b);
disp('||Ax-b|| =')
disp(res)
```

```
找到满足约束的最小值。

优化已完成，因为目标函数沿
可行方向在最优性容差值的范围内呈现非递减，
并且在约束容差值范围内满足约束。
```

说明：算法检测到 KKT 最优条件已经在数值容差内满足，因此停止

