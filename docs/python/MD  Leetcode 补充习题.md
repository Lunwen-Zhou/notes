# Leetcode 补充习题

## 哈希表

### 387 字符串中的第一个唯一字符

给定一个字符串 `s` ，找到 *它的第一个不重复的字符，并返回它的索引* 。如果不存在，则返回 `-1`

```
输入: s = "leetcode"
输出: 0
输入: s = "loveleetcode"
输出: 2
输入: s = "aabb"
输出: -1
```

```
1 <= s.length <= 10^5
s 只包含小写字母
```

```python
class Solution:
    def firstUniqChar(self, s: str) -> int:
        mp = {}
        n = len(s)
        for ch in s:
            mp[ch] = mp.get(ch,0) + 1
        for i,ch in enumerate(s):
            if mp[ch] == 1:
                return i
        return -1
```

**公司**：美的机考（25-08经验贴）



## 双指针

### 264 丑数 II

给你一个整数 `n` ，请你找出并返回第 `n` 个 **丑数** 

**丑数** 就是质因子只包含 `2`、`3` 和 `5` 的正整数

```
输入：n = 10
输出：12
输入：n = 1
输出：1
```

```
1 <= n <= 1690
```

```python
class Solution:
    def nthUglyNumber(self, n: int) -> int:
        dp = [0] * n
        dp[0] = 1
        
        p2, p3, p5 = 0, 0, 0
        
        for i in range(1, n):
            next2 = dp[p2] * 2
            next3 = dp[p3] * 3
            next5 = dp[p5] * 5
            
            next_ugly = min(next2, next3, next5)
            dp[i] = next_ugly
            
            if next_ugly == next2:
                p2 += 1
            if next_ugly == next3:
                p3 += 1
            if next_ugly == next5:
                p5 += 1
                
        return dp[n - 1]
```

**解法 2**：我原本的解法，过 456 / 596

```python
class Solution:
    def nthUglyNumber(self, n: int) -> int:
        res = [1,2]
        if n <= 2:
            return res[n-1]
        num = 3
        while len(res) < n:
            tmp = num
            for p in [2, 3, 5]:
                while tmp % p == 0:
                    tmp //= p
            if tmp == 1:
                res.append(num)
            num += 1
        return res[-1]
```



## 二分查找

### 69 x 的平方根 

给你一个非负整数 `x` ，计算并返回 `x` 的 **算术平方根** 

由于返回类型是整数，结果只保留 **整数部分** ，小数部分将被 **舍去 **

**注意：**不允许使用任何内置指数函数和算符，例如 `pow(x, 0.5)` 或者 `x ** 0.5` 

```
输入：x = 4
输出：2
入：x = 8
输出：2
```

```
0 <= x <= 2^31 - 1
```

**解法 1**：二分查找

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        left = 0
        right = x + 1
        while left < right:
            mid = (left + right) // 2
            if mid*mid <= x:
                left = mid + 1
            else:
                right = mid
        return left - 1
```

本题需要找到一个满足 $t^2 >x$ 的整数 $t$，再返回 $t-1$。因此 `if` 引导的部分为不成立的情况，所以需要使用 $\text{mid}^2\leq x$

**解法 2**：个人，可通过

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        i = 1
        while True:
            if i*i > x:
                return i-1
            else:
                i+=1
```

**解法 3**：牛顿迭代法

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0
        t = x
        next_t = 0.5*(t+ x/t)
        while abs(t-next_t) >= 1e-2:
            t = next_t
            next_t = 0.5*(t+ x/t)
        return int(next_t)
```

牛顿迭代法更新公式为
$$
t_{n+1} = t_n - \frac{f(t_n)}{f'(t_n)} = \frac{1}{2}\left(t_n + \frac{x}{t_n}\right)
$$
推导过程：

> 设上一步得到的迭代点为 $(x_n, f(x_n))$，在曲线 $y=f(x)$ 上作该点的切线方程，得
> $$
> y - f(x_n) = f'(x_n)(x - x_n)
> $$
> 令 $y=0$，求出的 $x$ 记为 $x_{n+1}$，即得上述公式



## 栈

### 85 最大矩形

给定一个仅包含 `0` 和 `1` 、大小为 `rows x cols` 的二维二进制矩阵，找出只包含 `1` 的最大矩形，并返回其面积。

例：
$$
\begin{array}{|c|c|c|c|c|}
\hline
1 & 0 & 1 & 0 & 0 \\
\hline
1 & 0 & \mathbf{1} & \mathbf{1} & \mathbf{1} \\
\hline
1 & 1 & \mathbf{1} & \mathbf{1} & \mathbf{1} \\
\hline
1 & 0 & 0 & 1 & 0 \\
\hline
\end{array}
$$

```
输入：matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
输出：6
输入：matrix = [["0"]]
输出：0
输入：matrix = [["1"]]
输出：1
```

```
1 <= rows, cols <= 200
matrix[i][j] 为 '0' 或 '1'
```

*leecode 84 柱状图中最大的矩形，直接应用*

```python
class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        data = [0] * n
        ans = 0

        def maxTriangle(nums):
            nums = [0] + nums + [0]
            n = len(nums)
            res = 0
            stack = []
            for i in range(n):
                while stack and nums[stack[-1]] > nums[i]:
                    j = stack.pop()
                    res = max(res,nums[j]*(i-stack[-1]-1))
                stack.append(i)
            return res

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == "1":
                    data[j] += 1
                else:
                    data[j] = 0
            ans = max(ans, maxTriangle(data))
        return ans
```



## 图论

### 130 被围绕的区域

给你一个 `m x n` 的矩阵 `board` ，由若干字符 `'X'` 和 `'O'` 组成，**捕获** 所有 **被围绕的区域**：

- **连接：**一个单元格与水平或垂直方向上相邻的单元格连接
- **区域：连接所有** `'O'` 的单元格来形成一个区域
- **围绕：**如果一个区域中的所有 `'O'` 单元格都不在棋盘的边缘，则该区域被包围。这样的区域 **完全** 被 `'X'` 单元格包围

通过 **原地** 将输入矩阵中的所有 `'O'` 替换为 `'X'` 来 **捕获被围绕的区域**。你不需要返回任何值

```
输入：board = [['X','X','X','X'],['X','O','O','X'],['X','X','O','X'],['X','O','X','X']]
输出：[['X','X','X','X'],['X','X','X','X'],['X','X','X','X'],['X','O','X','X']]
解释见下图
```

$$
\begin{array}{|c|c|c|c|}
\hline
X & X & X & X \\
\hline
X & \mathbf{O} & \mathbf{O} & X \\
\hline
X & X & \mathbf{O} & X \\
\hline
X & \mathbf{O} & X & X \\
\hline
\end{array}
\quad \Longrightarrow \quad
\begin{array}{|c|c|c|c|}
\hline
X & X & X & X \\
\hline
X & X & X & X \\
\hline
X & X & X & X \\
\hline
X & \mathbf{O} & X & X \\
\hline
\end{array}
$$

```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m = len(board)
        n = len(board[0])
        visited = [[False]*n for _ in range(m)]
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        q = deque()
        
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O' and not visited[i][j]:
                    q.append((i,j))
                    change = True
                    visited[i][j] = True
                    area = []
                    while q:
                        r,c = q.popleft()
                        area.append([r,c])
                        if r in (0,m-1) or c in (0,n-1):
                            change = False
                        for dr,dc in directions:
                            nr = r+dr
                            nc = c+dc
                            if 0<=nr<=m-1 and 0 <= nc <= n-1 and board[nr][nc] == 'O' and not visited[nr][nc]:
                                visited[nr][nc] = True
                                q.append((nr,nc))
                    if change:
                        for r,c in area:
                            board[r][c] = 'X'
```



## 贪心算法

### 135 分发糖果

`n` 个孩子站成一排。给你一个整数数组 `ratings` 表示每个孩子的评分

你需要按照以下要求，给这些孩子分发糖果：

- 每个孩子至少分配到 `1` 个糖果
- 相邻两个孩子中，评分更高的那个会获得更多的糖果

请你给每个孩子分发糖果，计算并返回需要准备的 **最少糖果数目** 

```
n == ratings.length
1 <= n <= 2 * 10^4
0 <= ratings[i] <= 2 * 10^4
```

```python
class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        left = [1]*n
        right = [1]*n
        ans = 0
        for i in range(1,n):
            if ratings[i] > ratings[i-1]:
                left[i] = left[i-1]+1
        for i in range(n-2,-1,-1):
            if ratings[i] > ratings[i+1]:
                right[i] = right[i+1] + 1
        for i in range(n):
            ans += max(left[i],right[i])
        return ans
```

容易看出，这种解法是符合题目要求。下面证明它是最优的方案

设任意一个合法的分配方案为 $c_0,c_1,\dots,c_{n-1}$，我们算法构造的方案为 
$$
d_i=\max(left[i],right[i]),\quad i = 0,1,\ldots,n-1
$$
下面证明：对任意合法方案 $c$，有 $c_i \ge d_i(i=1,\ldots,n-1)$，从而
$$
\sum_i c_i \ge \sum_i d_i
$$
**Proof**：

① **性质**：任意合法方案 $c$ 满足 $c_i \geq left[i]$

用数学归纳法证明：

- $i=0$ 时。$c_0 \ge 1 = left[0]$

- 设对 $i-1$ 有 $c_{i-1} \geq left[i-1]$。现在考虑 $c_i$ 与 $left[i]$ 的关系：

  - 若 $ratings[i] > ratings[i-1]$：
    $$
    c_i \ge c_{i-1}+1 \ge left[i-1]+1 = left[i]
    $$

  - 若 $ratings[i] \leq ratings[i-1]$：

    此时 $left[i] = 1$，显然 $c_i >= left[i]$

  故 $c_i\geq left[i]$

- $c_i \geq left[i],i=0,1,\ldots,n-1$

② 同理有 $c_i \geq right[i],i=0,1,\ldots,n-1$

③ 因此 $c_i \ge \max(left[i],right[i]) = d_i$ $\quad \square$



## 技巧

1014 最佳观光组合

给你一个正整数数组 `values`，其中 `values[i]` 表示第 `i`个观光景点的评分，并且两个景点 `i` 和 `j` 之间的 **距离**为 `j - i`

一对景点（`i < j`）组成的观光组合的得分为 `values[i] + values[j] + i - j` ，也就是景点的评分之和 **减去** 它们两者之间的距离

返回一对观光景点能取得的最高分

```
输入：values = [8,1,5,2,6]
输出：11
输入：values = [1,2]
输出：2
```

```
2 <= values.length <= 5 * 10^4
1 <= values[i] <= 1000
```

```python
class Solution:
    def maxScoreSightseeingPair(self, values: List[int]) -> int:
        ans = float('-inf')
        best_left = values[0] + 0
        n = len(values)
        for j in range(1,n):
            ans = max(ans, best_left + values[j] - j)

            best_left = max(best_left, values[j] + j)
        return ans
```

