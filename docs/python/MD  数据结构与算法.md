# 数据结构与算法

# 基本理论

## 算法基础

### 复杂度

#### 空间复杂度

空间复杂度看的是 **占用的峰值**，而不是 **操作的次数**

#### 时间复杂度

用于描述一个算法随着 **输入规模** $n$ 增大，其运行时间增长速度的指标

**定义**：设 $n$ 为算法的输入规模，算法的执行的基本操作次数为 $T(n)$，$f(n)$ 是一个描述 $n$ 增长数量级的函数。称算法的 **时间复杂度**为 $O(f(n))$，当存在 $c>0$、$n_0$，使得 $n>n_0$ 时，恒有
$$
T(n) \leq cf(n)
$$

## 数学基础

**性质**：对任意 **整数** $x$ 有
$$
x=\left\lfloor \frac{x}{2} \right\rfloor +\left\lceil \frac{x}{2} \right\rceil
$$
- 该性质 $\forall x \in \mathbb{R}$ 并不一定成立

  取 $x=\frac{3}{2}$，此时原性质等号左侧不是整数，右侧是整数，肯定不相等

**Proof**：

> 可将 $x$ 分为偶数、奇数讨论：
>
> ① 若 $x$ 为偶数，则存在 $k\in \mathbb{Z}$ 使得 $x=2k$。此时 $\frac{x}{2} = k$
> $$
> \left\lfloor \frac{x}{2} \right\rfloor=\left\lfloor k \right\rfloor=k
> $$
>
> $$
> \left\lceil \frac{x}{2} \right\rceil
> =
> \left\lceil k \right\rceil
> =k
> $$
>
> $$
> \left\lfloor \frac{x}{2} \right\rfloor+\left\lceil \frac{x}{2} \right\rceil=k+k=2k=x
> $$
>
> ② 若 $x$ 为奇数，则存在 $k\in \mathbb{Z}$ 使得 $x=2k+1$。此时 $\frac{x}{2} = k+\frac{1}{2}$
> $$
> \left\lfloor \frac{x}{2} \right\rfloor=k
> $$
>
> $$
> \left\lceil \frac{x}{2} \right\rceil=k+1
> $$
>
> $$
> \left\lfloor \frac{x}{2} \right\rfloor+\left\lceil \frac{x}{2} \right\rceil=k+(k+1)=2k+1=x
> $$
>
> $\square$
>



# 排序

基于 **比较** 的排序算法（如快排、归并排序、堆排序等）其时间复杂度下限是 $O(n \log n)$

### 冒泡排序

时间：$O(n^2)$

基本算法

```python
def bubble_sort(nums):
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums
```

如果在某一轮中没有发生交换，那么可以提前停止

> 如 `[1, 2, 3, 4, 5]` 第1轮：没有发生交换，但原本的写法会继续跑第2轮、第3轮……

```python
for i in range(n):
    swapped = False

    for j in range(0, n - i - 1):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            swapped = True

    if not swapped:
        break
```

---

### 归并排序

核心思想：分治（Divide & Conquer），大问题排序 = 两个子问题排序 + 合并两个有序数组

首先需要用到两个单增数组，合并成一个单增数组

```python
def merge(nums1: list[int], nums2: list[int]) -> list[int]:
    l1 = len(nums1)
    l2 = len(nums2)
    left = 0
    right = 0
    ans = []
    while left < l1 and right < l2:
        if nums1[left] < nums2[right]:
            ans.append(nums1[left])
            left += 1
        else:
            ans.append(nums2[right])
            right += 1

    if left < l1:
        while left < l1:
            ans.append(nums1[left])
            left += 1

    if right < l2:
        while right < l2:
            ans.append(nums2[right])
            right += 1

    return ans
```

```python
def merge_sort(nums: list[int]) -> list[int]:
    n = len(nums)
    if n <= 1: # 1个的时候默认是有序的，base case
        return nums

    mid = n // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    return merge(left,right)
```

递归为
$$
\text{merge\_sort}(\text{nums}) =
\begin{cases}
\text{nums}, & |\text{nums}| \le 1 \\
\text{merge}(\text{merge\_sort}(L),\ \text{merge\_sort}(R)), & \text{otherwise}
\end{cases}
$$


# 线性结构

Linear Structures

## 链表

### def 链表

链表（Linked list）是一种常用的 **数据结构**，由一系列 **节点** 组成，每个节点包含 **数据域** 和指针域。指针域存储了下一个节点的 **地址**，从而建立起各 **节点 **之间的线性关系

通过类来表示数据的节点

### 垃圾收集器

GC（Garbage Collection）用于自动管理内存并回收不再使用的对象所占用的资源。



# 树结构

## 二叉树

**二叉树**（Binary Tree）是一种每个节点最多有两个子节点的树形数据结构，其中每个节点的子节点，称为**左子节点**（Left Child）、**右子节点**（Right Child）

在 python 中，用**类**表示二叉树

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```



### 遍历

#### 先序遍历

（Pre-order Traversal）

先序遍历顺序是：根 -> 左 -> 右

```python
def preorderTraversal(root):
    ans = []
    def backtrack(node):
        if not node:
            return

        ans.append(node.val)
        backtrack(node.left)
        backtrack(node.right)

    backtrack(root)
    return ans
```

#### 中序遍历

左 -> 根 -> 右

例：

```
    1
   / \
  2   3
 / \
4   5
```

结果为 `[4 2 5 1 3]`

### 二叉搜索树

对于任意一个节点：左子树所有值 < 当前节点 < 右子树所有值（**默认严格不等号**）

中序查找时，得到一个单调增的序列

### 其他二叉树

#### 平衡二叉树

每个节点的左右子树高度差的绝对值不超过 1

#### 完全二叉树

（Complete Binary Tree）

**定义**：除了最后一层，上面所有层都 **完全填满** 了。最后一层，**必须从左往右连续地有节点**，不能“跳着空”

设 $x$ 为节点在数组中的下标索引，**从 0 开始编号 **时：一个完全二叉树的某个节点 $x$，它的左儿子一定是 $2x + 1$，右儿子一定是 $2x + 2$，父节点为 $\left \lfloor \frac{x-1}{2} \right \rfloor$

---



## 堆

### 最小堆 heapq

heapq 是 Python 的最小堆实现

可以理解成一种特殊 **数组**

堆顶永远是最小值，`heap[0]`

可以当成 list 来使用，但是不能随便改，一改就会破坏

每次堆操作的时间复杂度：$O(k)$（假设最小堆有 $k$ 个元素）

**有重复时**：不会被去重

**元组的比较**：(a,b) 按照字典顺序去比较

创建堆、如堆、出堆：

```python
import heapq

heap = []

# 把 x 加入堆
heapq.heappush(heap, x)

# 出堆
heapq.heappop(heap)

# 查看堆元素个数
len(heap)
```

不是完全排序， ≠ 排序数组。只是保证：`heap[0]` 是最小的

**模拟最大堆**：用负号，取出来再负回来

---



# 图论

## 并查集

（Union-Find Set）

并查集：处理“动态合并集合”问题的标准工具



# 算法

## DFS、BFS

 是图/树上的**遍历算法**

### 深度优先搜索算法

DFS，Depth-First Search

一路向下（用递归/栈）

### 广度优先搜索算法

BFS，Breadth-First Search

一层一层（用队列）

---



## 递归

术语：

- **剪枝**

  提前终止了 **不可能产生合法解 **的搜索路径，避免无谓递归

- **终止条件**（base case）

  递归必须停止的“合法终点状态”



## 动态规划

**判断是否是动态规划**

1. 递归结构

   本质：**问题可以拆成更小的同类问题**，如可以写出类似下述的递推关系：

   ```
   f(n) = f(n-1) + f(n-2)
   dp[i] = min(dp[i-1], dp[i-2]) + cost[i]
   dp[i][j] = ... dp[i-1][j] ... dp[i][j-1]
   ```

   此时说明：**有递归结构**

2. 重复子问题的可记忆化

   本质：**同一个子问题会被反复计算**，如 Fibonacci 数列：

   ```
   f(5)
   ├── f(4)
   │   ├── f(3)
   │   └── f(2)
   └── f(3)
       ├── f(2)
       └── f(1)
   ```

   `f(3)` 被算了两次，`f(2)` 被算了三次，这就是重复子问题



## 贪心算法

（Greedy Algorithm）

**定义**：在问题求解过程中，每一步都做出当前最优（局部最优）的选择，并希望通过这些局部最优选择，最终得到全局最优解
