# Python 笔记本

## 环境配置

### pip

#### 工位 windows

解释器：python 3.12.9

ModuleNotFoundError: No module named 'numpy'

当前运行解释器为：D:\1 Software\python 3.12.9\python.exe

需在cmd中运行：

"D:\1 Software\python 3.12.9\python.exe" -m pip install numpy

## 报错

IndentationError：缩进错误，看一下缩进能解决



## 通用

### 基础数学运算

**除法并且向下取整**：`//` ： “地板除” (Floor Division)

**Python 最大值**：`float('inf')` 表示正无穷大，是一个特殊的**浮点数**，比任何其他数字都大

**取余**：`a % b`

负数情况，如 `(-2) % 4` 会被调整为正数，输出 2

---



### 运算顺序

```python
water += min(post[i],pre[i]) - height[i]
```

等价于

```python
water = water + (min(post[i], pre[i]) - height[i])
```

因此原本表达式中，无需在右侧写一个大的括号



### 基本

#### 制表符

tab character

`\t`，如 `a = "x\ty"`，打印 `a` 会得到 `x	y`



### 逻辑词

#### or

```python
A = B or set()
```

如果 B 是非空容器，则 `A = B`，否则 `A = set()`



### 循环

#### range

如果 `range(a,b)` 中 $a\geq b$，程序还是可以运行，只是 `for i in range(a,b)` 这个循环**不执行**

---



### 交换两数

```python
a = 1
b = 2
a,b = b,a
```

---



### 二分查找

 `bisect` 模块所有函数都假设列表是**升序排列**，否则结果是错误的，且不会报错

#### bisect.bisect_left

用之前需要import：`import bisect`

查找插入位置

```python
a = [1, 3, 5, 7]
bisect.bisect_left(a, 4)
```

返回：2

元素已存在，返回最左的索引

```python
a = [1, 3, 3, 3, 7]
print(bisect.bisect_left(a, 3))
```

返回：1

---



### 单引号与双引号

是完全相同的，以下两式相同：

```
# 写法 A：使用双引号
sentence_list = ["g", "o", "o", "d", "!"]

# 写法 B：使用单引号
sentence_list = ['g', 'o', 'o', 'd', '!']
```

python 这样设计为了方便处理本身带引号的句子，只看两侧的匹配

---



### pass

占位符（Placeholder）

Python 的语法规定，函数、类或循环的内部**不能为空**，很多代码框架里都会先写一个 `pass`，等以后想好逻辑了再回来填，如

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 这里后续再完善代码
        pass
```

---



### 本地测试

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 在这里粘贴你写的逻辑
        pass


if __name__ == "__main__":
    sol = Solution()

    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    expected = [3, 3, 5, 5, 6, 7]

    result = sol.maxSlidingWindow(nums, k)
    print(f"预期为: {expected}")
    print(f"result = {result}")
```

`sol = solution()` 为**实例化对象**

例2（实现类 climbStairs）

```python
def main():
    n = int(sys.stdin.readline().strip())
    sol = Solution()
    ans = sol.climbStairs(n) 
    print(ans)

if __name__ == "__main__":
    main()
```

---



### 打印

**同一行间隔打印**：`print(a, end = "\t")`

---



### 深拷贝与浅拷贝

- 浅拷贝（Shallow Copy）

  给原链表里的每个节点复印了一张“名片”

  名片是新的，但上面的地址（指针）还是指向原来的老房子

- 深拷贝（Deep Copy）

  按照原链表的图纸，在另一块空地上盖了一座一模一样的新房子

  创造 $n$ 个新节点，它们的内存地址必须和原节点不同

对于数组、对象（类）、指针等，复制时传递的是地址，才有浅、深的区别。

对于基础数据类型（如整数 `int`、浮点数 `float`、布尔值 `bool`），它们在内存中通常存储在**栈（Stack）**上。 执行 `a = b` 时，系统会直接把 `b` 的值复制一份给 `a`

对于数组、对象（类）、指针等，它们的数据体量通常较大，为了节省内存和提高效率，系统往往只在栈里存一个**地址（指针）**，而把真实的大量数据存在**堆（Heap）**里



### exit

`exit(0)`：立即终止程序运行，并返回状态码 0

`exit(1)` → 异常结束（一般不用）



### 局部变量

在下例中

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.ans = float('-inf')
        def backtrack(node): 
            if not node:
                return 0

            lm = backtrack(node.left)
            rm = backtrack(node.right)

            self.ans = max(self.ans, node.val + max(lm, 0) + max(rm, 0))

            return node.val + max(lm, rm, 0)

        backtrack(root)
        return self.ans
```

在 backtrack 函数外部定义的 `ans`，在其内部使用时，是会报错的，解决方法：

① 使用 `self.ans`

② 在函数内部声明 `nonlocal ans`



## 数据

### Python 数据类型

- 数字（Numbers）

  包括三种子类型：`int`、`float`、`complex`：如 `1+2j`, `3j`

- 字符串（str）

  不可变

- 布尔值（bool）

  所有对象在布尔上下文中均有真值

  `True`：非零数、非空容器

  `False`：`0`、`""`、`[]`、`None` 等

- 列表（list）

  有序、**可变**的序列容器，可包含任意类型的元素（支持嵌套）

  用方括号 `[]` 定义

- 元组（tuple）

  有序、**不可变**的序列容器（与列表类似，但一旦创建不能修改）

  用圆括号 `()` 定义

  **单元素**：需加逗号：`(x,)`

- 集合（set）

  无序、**不重复**的元素集合

  用花括号 `{}` 或 `set()` 构造

  支持数学集合运算：并集 `|`、交集 `&`、差集 `-`、对称差 `^`

  元素必须是**可哈希（hashable）** 的（即不可变类型，如 `int`, `str`, `tuple`；不可用 `list`, `dict`）

- 字典（dict）

  无序的**键值对（key-value pairs）** 集合





### 可变对象

python中不可变对象：字符串

可变对象（mutable）：列表

---



### optional

类型提示（type hint）

如 `Optional[TreeNode]` 等价于 `Union[TreeNode, None]`，可以是TreeNode，也可以是None

这种写法在处理二叉树、链表等可能为空的数据结构时比较常见

例子：

```python
def function(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
```

表示函数接收一个参数 `root`，它的类型 可能是 `TreeNode`，也可能是 `None`，同理函数的返回值

**新的写法**：

`-> Optional[TreeNode]:` 可写成 `-> 'TreeNode | None':`（对于Python ≥ 3.10）

`' '` 不是必须的，只有前向引用才需要，如

```python
class A:
    def f(self) -> 'B':  # B 还没定义
        ...
```



## 元组

`tuple`



## 数组

### 基本

#### 子序列与子串

**子序列**：可以删掉一些字符，但不能改变剩余字符的相对顺序

**子串**：**必须连续**

---



### 技巧

检查布尔数组中是否有 $\geq 1$ 个 `False`

```python
status_list = [True, False, False]

if not any(status_list):
    print("数组里全都是 False")
```

any 本身只处理一维的可迭代对象，矩阵不能简单使用

---



### 等号赋值传递地址

```python
s = [1, 2, 3]
s1 = s

print(id(s))
print(id(s1))
print(s is s1)
```

输出

```
4375677440
4375677440
True
```

例如修改 `s[0] = -1` 那么 `print(s1)` 会输出 `[-1, 2, 3]`

---



### 创建数组

填充相同值

```python
n = 5
arr = [0] * n  # 结果: [0, 0, 0, 0, 0]
```

**用 `for x,y in List[1:]` 同时取出内部数组多个元素**

例1：用 `[1:]` 来指定数组的某一部分 

```python
data = [["Header", "Score"], ["A", 95], ["B", 88], ["C", 92]]

for name, score in data[1:]:
    print(f"学生 {name} 考了 {score} 分")
```

输出：

```
学生 A 考了 95 分
学生 B 考了 88 分
学生 C 考了 92 分
```

`for x,y in List[1:]` 可以将外层数组中每个元素（也是数组）`x,y` 中x,y提取出来

如果 `["A", 95]` 有三个元素，但是接着它的只有 `name, score` 两个，会**报错** 

**三个时**：`for x,y,z in List[1:]` 

---



### enumerate

enumerate 切片后会从下标 0 开始计数，也就是先把字符串切出来后，当成一个新的字符串

```python
s = ['a', 'b', 'c', 'd', 'e']
n = len(s)
for i in range(1,n):
    print(i)
for i,ch in enumerate(s[1:n]):
    print(f"i = {i}, ch = {ch}")
```

```
1
2
3
4
i = 0, ch = b
i = 1, ch = c
i = 2, ch = d
i = 3, ch = e
```



#### start

```python
for a, b in enumerate(["A", "B", "C"], start=1):
    print(a, b)
```

输出

```
1 A
2 B
3 C
```

---



### zip

```python
labels = [1, 0, 1]
scores = [0.8, 0.2, 0.7]
```

此时 `for label, score in zip(labels, scores):` 会变成：

```python
(1, 0.8)
(0, 0.2)
(1, 0.7)
```

即 `zip([a1, a2, a3], [b1, b2, b3])` $\iff$ `[(a1, b1), (a2, b2), (a3, b3)]`

使用 `data = list(zip(scores, labels))` 会得到

```python
[(0.8, 1),
 (0.2, 0),
 (0.7, 1)]
```

是一个 list

长度不一致会按短的那个截断





---

### 切片

在 Python 中，对列表（ `list` ）使用切片操作（如 `path[:]`）会返回一个 **浅拷贝** 的新列表对象

```python
path = [1, 2, 3]
new_path = path[:]
print(new_path is path)  # False → 是不同的对象
```

- 因此对于回溯算法 `ans.append(path[:])` 无需 `copy()`

  但这只对于 `path` 中的元素都是**不可变对象**（如 `int`, `str`, `tuple`）时完全安全

  如果 `path` 包含可变对象，内部元素仍然为引用

  ```python
  path = [[1], [2]]
  ans = path[:] # 浅拷贝
  path[0].append(3)
  print(ans)  # [[1, 3], [2]] → 内部列表被修改了！
  ```

  如果需要完全独立的副本，使用 **深拷贝**

  ```python
  import copy
  path = [[1], [2]]
  ans = copy.deepcopy(path)
  path[0].append(3)
  print(ans)  # [[1], [2]]
  ```

切片不会引发 IndexError，如字符串 `s` 的长度为5，直接调用 `s[5]` 是会报错的，但是 `s[0:100]` 是合法的

性质：**左闭右开**

```python
s = [1,2,3]
s1 = s[0:1]
```

此时 `s1 = [1]`

---



### append

用于数组，增加一个元素，如 [1] 变为 [1, 2]

---



### sorted

排序，升序

用法：`sorted_nums = sorted(nums)` ，可将 $[4, 2, 7]$ 变为 $[2,4,7]$

用的不是快排，用的是 **Timsort**

一种归并排序（Merge Sort） + 插入排序（Insertion Sort）的混合算法

**不用快排的原因**

1. 最坏情况太差

   快排最坏：$O(n^2)$

2. 不稳定

   有些场景需要稳定排序

3. 工程上不如 Timsort

   Timsort 能利用“部分有序”的数据（现实数据很常见）

   如 `nums = [1,2,3,7,6,5,4]`，Timsort 会发现 `[1,2,3,7]` 是有序的，`[6,5,4]` 也是一段有序的（逆序会处理），比普通排序要更快

**Timsort 的复杂度**

最坏：$O(n \log n)$

平均：$O(n \log n)$

最好（几乎有序）：$O(n)$

但算法分析通常取 $O(n \log n)$

#### 用于字符串

会将字符串拆解为单个字母，如 `sorted("eat")` 返回 `['a', 'e', 't']`

字符串本身是不可变（immutable）对象，因此不能做 `st[0] = 'a'`，不能原地修改顺序

sorted 并不是修改 st，而且将其当成一个序列，排序后生成一个**新的列表**

一般要和 `join` 连用，就得到一个排序后的字符串

```python
sort_ch = "".join(sorted(ch))
```

此时输出 `aelpp`

---



### sort

对于 list 类型使用，对字符串会返回 `None`，不能 `sort(list)`，不是全局函数，只是 list 的一个方法

 `.sort()`：原地排序。`sorted()`：生成新列表

注意与 `sorted` 使用的 **位置** 不同



**sort 的原地含义**

`print(arr.sort())` 这样的写法会输出 None（这个函数本身不返回内容），因为 sort 是原地修改

正确是先直接在外面计算 `arr.sort()`，然后再打印为 `print(arr)`，这就是**原地**的含义



例：面积从大到小排序

```python
a = [[1,3], [3,4], [1,2], [2,4]] # 现在要从大到小排序
# [[3, 4], [2, 4], [1, 3], [1, 2]]
a.sort(key=lambda p:p[0]*p[1], reverse=True)
```

`p:p[0]*p[1]` 相当于定义了一个匿名函数



按第二个元素降序

```
a = [(1, 10), (3, 5), (2, 8), (4, 2)]
b = sorted(a, key=lambda p:-p[1])

# 得到: b = [(1, 10), (2, 8), (3, 5), (4, 2)] 
```



按第一个元素升序，但是第二个元素降序

```
a = [(1, 10), (1, 5), (2, 8), (2, 3), (1, 8)]
b = sorted(a, key=lambda p:(p[0], -p[1]))

# 得到: b = [(1, 10), (1, 8), (1, 5), (2, 8), (2, 3)]
```

有第一关键字和第二关键字之分：`key = (第一关键字, 第二关键字, ...)`



## 矩阵

### 基本

**获取维度**：行数 `len(matrix)`   列数 `len(matrix[0])`

**leetcode 去掉空矩阵的情况**：去掉空列表 [] 、里面装了空列表的列表 [[]] （此时认为外面是有装东西的）

```python
if not matrix or not matrix[0]:
	return list() 
```

若 `A = []` ，则 `if A:` 不会执行

若 `A = [[]]` ，则 `if A:` **会执行**（此时认为 A 并不是空的）



**矩阵复制**

为了不影响函数外部传入的原始矩阵，可以先对 grid 做一层拷贝：

```python
grid = [row[:] for row in grid]
```

之后在函数内部修改 grid，不会影响外部的原始矩阵

---



### 初始化

```python
rows, cols = 3, 4
matrix = [[0 for _ in range(cols)] for _ in range(rows)]
matrix = [[0] * cols for _ in range(rows)]
```

---



### 一维索引

把一个矩阵拉平后，一维索引转化为坐标：

```python
matrix = [
    [10, 20, 30],
    [40, 50, 60]]
n = 3
index = 4
row = index // n
col = index % n
```

列是关键



## 链表

### 单链表

（Singly-linked list）

在 leetcode 中的存储方式为

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
```





## 字符串

### 基本

**不区分字符与字符串**

很多其他编程语言（如 C, C++），单引号包裹的单个字符（如 `'a'` ）是 `char` 类型，而双引号包裹的是 `String` 类型

但python不区分

**字符串与列表的区别：**

字符串有**不可变性**，不能append，要用 `+` 重新拼接成一个新的字符串：

```python
sentence = "good !"
sentence = sentence + "?" 
print(sentence)
```

输出：`good !?`

`sentence[-1]` 可以输出栈顶 `?`

如果存储为列表：

```python
# 把字符串转成列表
sentence_list = ["g", "o", "o", "d", "!"]
# 往列表末尾添加元素
sentence_list.append("?")  
# 把列表拼回字符串
new_sentence = "".join(sentence_list) 
```

得到：`good !?`

---



### 字典顺序

从左到右逐字符比较，如果一直相同，短的字符串更小

如：`"apple" < "banana" `

`"abc" < "abcd"`

`"abc" < "abd"`，因为 `"c" < "d"`

---



### 数组拼成字符串 "".join

例：把分散的字母拼回单词，得到**字符串**

```python
letters = ['y', 'e', 's']
word = "".join(letters)
print(word) 
```

输出 `yes`



**如果希望拼接时中间有空格**

```python
A = ["a", "b", "c"]
s1 = " ".join(A)  # 得到: "a b c"
s2 = ",".join(A)  # 得到: "a,b,c"
```





## 队列

### deque 双端队列

double-ended queue

需要import：`from collections import deque`

**参数需可迭代**（iterable）

正确实例，iterable

```python
deque([1,2])
deque((1,2))
deque("ab")
deque(range(3))
```

```
[1,2]
[1,2]
['a','b']
[0,1,2]
```

但 `deque(1,2)` 不是 iterable

下面的写法，与 `q = deque([(1, 2)])` 是相同的，如果要把(1,2)作为一个整体，在初始化时要加 `[]`

```python
q = deque()
q.append((1, 2))
```



**一个元素时的初始化**

如果要数字 1 初始化，要写成 `q = deque([1])`，不能写成 `deque(1)`，因为**列表是可迭代对象**，但是数字不是。同理 `q = deque([root])`，这里 `root` 为二叉树根节点



**应用**：在BFS（广度优先搜索）中需要**先进先出**（FIFO）

流程为：加入节点 → 处理节点 → 再加入新节点，如

```
队列: [(0,0)]

取出 (0,0)
加入 (0,1) (1,0)

队列: [(0,1),(1,0)]

取出 (0,1) ...
```

若用 `list`，时间复杂度为 $O(n)$，需要整体移动数组

```python
q = []
q.append((i,j))
q.pop(0)
```

用 `deque`

```python
q = deque()
q.append((i,j))
q.popleft()
```

**左右端出队**

`pop()` 右端出队

`popleft()` 左端出队



## 哈希表

### 字典

`dict`（字典）基于哈希表（hash table）实现，其插入（insert）、查找（lookup）、删除（delete）
在平均情况（average case）下的时间复杂度都是 $O(1)$

表示：`mp = {}`

list 不能放进 set（不可 hash），可以考虑转为 tuple 来替代



**同时遍历字典的 key、value**

`for key, value in mp.items():`



数字（1-26）对应字母的字典

```python
mp = {chr(ord('a')+i): i+1 for i in range(26)}
```

大写对应小写

```python
mp = {chr(ord('A')+i):chr(ord('a')+i) for i in range(26)}
```



#### 例子

**例（学生信息）**

```python
user_info["name"] = "Kevin"
user_info["role"] = "Graduate Student"
print(user_info)
```

输出：`{'name': 'Kevin', 'role': 'Graduate Student'}` 

这里 `"name"` 是 key， `"kevin"` 是 value

**例（水果价格）**

```python
prices = {
    "apple": [1,2],   # 注意为数组
    "banana": 3,
    "orange": 4
}
print(list(prices.values()))
print(prices["apple"]) # 通过 Key 获取 Value
```

输出： `[[1, 2], 3, 4]` 和 `[1, 2]`	

如果不加list，输出"字典值形式"：`dict_values([[1, 2], 3, 4])`

因此需要加list强制转为列表

**例 单词的字符统计**

```python
counts = {}
text = "matha"

for char in text:
    if char not in counts:
        counts[char] = 1  # 第一次见到，初始化为1
    else:
        counts[char] += 1 # 再次见到，累加

print(counts)
```

输出：`{'m': 1, 'a': 2, 't': 1, 'h': 1}`



#### 没有 key，赋值时会自动创建

```python
map = {}

# 场景 1：如果键不存在 —— 自动创建
map['a'] = 0
print(map)

# 场景 2：如果键已存在 —— 覆盖更新
map['a'] = 10
print(map)

# 场景 3：在循环中动态处理
chars = ['x', 'y', 'x']
for i, char in enumerate(chars):
    map[char] = i
    print(f"i =  {i}, 处理字符 '{char}', 最新字典为 {map}")
```

结果

```
{'a': 0}
{'a': 10}
i =  0, 处理字符 'x', 最新字典为 {'a': 10, 'x': 0}
i =  1, 处理字符 'y', 最新字典为 {'a': 10, 'x': 0, 'y': 1}
i =  2, 处理字符 'x', 最新字典为 {'a': 10, 'x': 2, 'y': 1}
```

**对 value 进行 append 时要先保证是list**

要先新建一个空列表[]，再用append，注意这并不违反前面的规则

```python
mp = {}
if "a" not in mp:
    mp["a"] = []
mp["a"].append("eat")
mp["a"].append("yes")
print(mp)
```

输出：`{'a': ['eat', 'yes']}`



#### 安全的取值方式 get

```python
mp.get(key, default)
```

如果 `key` 在字典里，返回对应的值

若不然，返回 `default`

---



#### defaultdict

`defaultdict(int)` 访问不存在的 key 会**自动创建一个默认值**，不会报错。用法

```python
from collections import defaultdict

d = defaultdict(factory)
```

`int` → 默认值 0

`list` → 默认值 []

`set` → 默认值 set()



### Set

**Set 和 Dict 的区别**

`set` 和 `dict` 在 Python 中底层都是基于哈希表（hash table）实现的，从**数据结构**上讲，它们都属于哈希表这一大类

`dict` 是 **键值对**（key-value）的哈希表

`set` 是 **仅键**（key-only）的哈希表（可以理解为只存 key、不存 value 的 dict）

用花括号写，自动就是set

**例（快速判断id是否在名单）**

```python
# 模拟一个巨大 ID 列表
ids = [1001, 1005, 2020, 1001, 3030, 1005]

id_set = set(ids)

if 2020 in id_set:
    print("Found it!") # 该步瞬间完成，不需要遍历整个列表
```

`set(ids) ` ：将列表转换为集合，自动去重，且建立哈希表

可以直接写成 `ids_set = {1001, 1005, 2020, 1001, 3030, 1005}`，会自动去重



#### 添加元素

- 单个元素

  `add`：`A_set.add(1)`，将 1 添加到 A_set 中

- 多个元素，update

  ```python
  A_set = set()
  A_set.update(i for i in range(10))
  
  B = [1, 2, 3, 4]
  A_set.update(B)
  ```



#### 删除元素

**三种**删除方法

- **remove()**

  `id_set.remove(2020)`

  ✔ 如果元素存在 → 删除

  ❌ 如果不存在 → 报错（KeyError）

- **discard()**（更安全，推荐）

  `id_set.discard(2020)`

  ✔ 存在就删

  ✔ 不存在也不会报错

- pop()

  随机删一个元素

---



### 交集

```python
A_set = {1, 2, 3, 4}
B_set = {3, 4, 5, 6}

result = A_set & B_set # 结果为 {3, 4}
```

自动去重，**不修改原集合**（返回一个新的集合）

支持多个集合取交集

如果交集为空，**会生成 `set()`，而非 `{}`，因为这是字典**



## 指针

就是数组的下标， 没有C语言那样可以加减运算的“物理指针”

### 单指针

如找负数的下标

```python
nums = [10, 20, -5, 30, -10]
pointer = 0
```

找到后，指针为 `pointer` ，对应数字 `nums[pointer]`

---



### 双指针

**例 检查回文联**

```python
s = "racecar"
left = 0           # 指向开头
right = len(s) - 1 # 指向末尾

while left < right:
    if s[left] == s[right]:
        left += 1  # 左指针往右走
        right -= 1 # 右指针往左走
    else:
        print("不是回文")
        break
else:
    print("是回文")
```



# 算法理论

### 空间复杂度

空间复杂度看的是**占用的峰值**，而不是**操作的次数**

---



### 时间复杂度

#### 排序算法

基于**比较**的排序算法（如快排、归并排序、堆排序等）其时间复杂度下限是 $O(n \log n)$



## 图论

一般在算法题或图论建模中，如 $x$ 需要 $y$ 才能进行，会画成 $y \rightarrow x$，类似 $y$ 推出 $x$
