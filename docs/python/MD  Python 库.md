# Python 库

例子直接使用自己实际遇到的工程、科研代码即可。一开始的版本不用很完美，日后如果再次用到，再去完善即可

## math

### factorial

`factorial(n)`：计算 $n!$



## Numpy

基本用法 `import numpy as np`

以元组形式作为元素的二维数组（矩阵），`data = [(x1,x2,x3), ...]`，可以转换为矩阵

`X = np.array(data)`

不会修改原来的 `data`，是“拷贝 + 转换”，不是引用

转换之后还可以修改，如 `X[0,0] = 100`



### 基本线性代数

全1矩阵：`X = np.ones((m,n))`

横向拼接：`np.hstack((A,B))`

（horizontal stack）

转置：已经用 np 建好矩阵后， `X.T` 表示转置



线性方程组：求解
$$
Ax = b
$$

```
np.linalg.solve(A, b)
```

linalg = linear algebra



求逆矩阵

`np.linalg.inv()`



### reshape

行向量变列向量：

```
y = [1, 2, 3]
y = np.array(y)
y = y.reshape(-1, 1)
```

`-1` 表示自动推断行数

默认按 **行优先** 填充

```python
a = np.array([1,2,3,4,5,6])
b = a.reshape(2,3)
```

会得到

```python
b = [[1,2,3],
     [4,5,6]]
```



### tile

`np.tile(B, (m,n))` 等价于
$$
\text{kron}(\mathbf{1}_{m\times n}, B)
$$


横向将一个行向量复制 3 次：

```python
import numpy as np

a = np.array([1,2,3])

b = np.tile(a, 3)
```

得到 `b = [1 2 3 1 2 3 1 2 3]`

```
b = np.tile(a, (2,3))
```

得到 b = 

```
[[1 2 3 1 2 3 1 2 3]
 [1 2 3 1 2 3 1 2 3]]
```



### mean

```python
X_train = np.array([[1, 2, 3],
                    [4, 5, 6]])
mu = np.mean(X_train, axis=0)
```

得到的 mu 相当于 `array([2.5, 3.5, 4.5])`

`axis=0` 表示按列



### std 计算标准差

```python
sigma = np.std(X, axis=0, ddof=0)
```

表示对矩阵的每一列计算标准差

ddof：Delta Degrees of Freedom（自由度的增量）

`ddof = 0`：（总体标准差）
$$
\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2}
$$
`ddof = 1`：（样本标准差，无偏估计）
$$
s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (x_i - \bar{x})^2}
$$




### 应用

#### 给矩阵围一圈常数

```python
import numpy as np

matrix = np.array([[1, 2],
                   [3, 4]])

# 在四周填充一圈 0
padded = np.pad(matrix, pad_width=1, mode='constant', constant_values=0)
print(padded)
print(type(padded))

padded = padded.tolist()

print(padded) 
print(type(padded))
```

输出结果为

```python
[[0 0 0 0]
 [0 1 2 0]
 [0 3 4 0]
 [0 0 0 0]]
<class 'numpy.ndarray'>
[[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
<class 'list'>
```

或者也可以简单地用下面的方式

```python
matrix = [[1,2],[3,4],[5,6]]
m = len(matrix)
n = len(matrix[0])
wid = 1
matrix_pad = [[0] *(n+2*wid) for _ in range(m + 2*wid)]
for i in range(m):
    for j in range(n):
        matrix_pad[i+wid][j+wid] = matrix[i][j]
print(matrix_pad)
```



## collections

### Counter

统计每个字符出现次数

```python
S = "AABBCC"
cnt = Counter(S)
```

得到 `cnt = {'A': 2, 'B': 2, 'C': 2}`



## json

打印 json 数组

```python
import json

data = {
    "name": "Tom",
    "age": 18,
    "scores": [90, 80, 85]
}

print(json.dumps(data))
```

输出（字符串格式）

```
{"name": "Tom", "age": 18, "scores": [90, 80, 85]}
```

导入

```python
string = '{"name": "Tom", "age": 18, "scores": [90, 80, 85]}'

data = json.loads(string)

name = data["name"]
age = data["age"]
scores = data["scores"]
```

如果是从读入，可以写 `data = json.loads(sys.stdin.read())`





## pathlib

### Path

导入

```python
from pathlib import Path
```

专门用来处理 **文件路径**

`/` 用于拼接路径，如：

```python
INTERACTIONS_PATH = PROJECT_ROOT / "users_interactions.csv
```

其中 `PROJECT_ROOT` 需要是 Path 对象



即使导入了 Path，也不可以

```python
"/Users/zhoulunwen/project" / "users_interactions.csv"
```

因为第一个是字符串，字符串不能拼接。只能

```python
Path("/Users/zhoulunwen/project") / "users_interactions.csv"
```

可以 `Path("A") / "B" / "C"`，不可以 `"A" \ Path("B")`，字符串就是不能用拼接

简记

```python
Path(...) / "..."      # 可以
Path(...) / Path(...)  # 可以
"..." / Path(...)      # 不可以
"..." / "..."          # 不可以
```



```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
```

首先 `Path(__file__).resolve()` 得到目前文件的绝对目录：

`/Users/zhoulunwen/Documents/推荐算法/article_recommender/src/config.py`

然后 `parents[1]` 表示网上两层，得到

`/Users/zhoulunwen/Documents/推荐算法/article_recommender`

最后不带 `/`



## Pandas

DataFrame 是 pandas 中最核心的数据结构，可以理解为 **一张带行和列的二维表格**（类似 Excel 

表），如

| personId | contentId | eventType |
| :------: | :-------: | :-------: |
|    U1    |    A1     |   VIEW    |
|    U2    |    A3     |   LIKE    |
|    U1    |    A2     | BOOKMARK  |

```python
import pandas as pd

df = pd.read_csv("users_interactions.csv")
```

这里的 `df` 是一个 DataFrame



|      |   Series    |       DataFrame        |      |
| :--: | :---------: | :--------------------: | :--: |
| 维度 |    一维     |          二维          |      |
| 类比 |  一列数据   |       Excel表格        |      |
| 组成 | 索引 + 数据 | 行索引 + 列索引 + 数据 |      |



### groupby

```python
import pandas as pd

# 原始数据 df
df = pd.DataFrame({
    "personId": ["A", "A", "A", "B", "B", "B", "C"],
    "contentId": [101, 101, 102, 101, 102, 102, 103],
    "event_weight": [1.0, 4.0, 2.5, 5.0, 1.5, 3.0, 2.0]
})

print(df)
# 默认情况（as_index=True）
result_true = df.groupby(["personId", "contentId"]).agg(strength_sum=('event_weight', 'sum'))
print(result_true)

# 保持为普通列（as_index=False）
result_false = df.groupby(["personId", "contentId"], as_index=False).agg(strength_sum=('event_weight', 'sum'))
print(result_false)

# 只按 personId 相同进行聚合
result_user_only = df.groupby(["personId"], as_index=False).agg(
    strength_sum=('event_weight', 'sum')
)
print(result_user_only)
```

输出

```
  personId  contentId  event_weight
0        A        101           1.0
1        A        101           4.0
2        A        102           2.5
3        B        101           5.0
4        B        102           1.5
5        B        102           3.0
6        C        103           2.0
                    strength_sum
personId contentId              
A        101                 5.0
         102                 2.5
B        101                 5.0
         102                 4.5
C        103                 2.0
  personId  contentId  strength_sum
0        A        101           5.0
1        A        102           2.5
2        B        101           5.0
3        B        102           4.5
4        C        103           2.0
  personId  strength_sum
0        A           7.5
1        B           9.5
2        C           2.0
```

因此需要 `as_index=False`

上述聚合中，有的是需要 personId、contentId 都相同时才聚合，最后是只需要 personId 相同就聚合

在新生成的表格中，原本的列（event_weight）就不在了



```python
interactions_agg = interactions_agg.sort_values(
        ["personId", "last_timestamp"]
    ).reset_index(drop=True)
```

`drop=True `如果不加 ，`pandas` 会把乱掉的旧行号做成一个叫 `index` 的新列保留在表格里。加上该语句后，旧行号会被彻底扔掉



```python
for _, user_df in interactions_agg.groupby("personId", sort=False):
```

由于不关心用户被处理的顺序，所以 `sort=False`，如果不加，Pandas 在内部会多做一步“前置准备”，进行排序

取出来的两个元素：

- 第一个元素（键）：personId，但不需要，所以用 `_`
- 第二个元素（值）：一个独立的子 DataFrame，里面**只包含**当前这个用户的所有交互数据



```python
train_df.groupby("personId")["contentId"].apply(lambda x: set(x.tolist())).to_dict()
```

假设原数据为

```python
import pandas as pd

train_df = pd.DataFrame({
    "personId": [1, 1, 1, 2, 2, 3],
    "contentId": [101, 102, 101, 201, 202, 301]
})
```

此时 train_df 为

```
   personId  contentId
0         1        101
1         1        102
2         1        101
3         2        201
4         2        202
5         3        301
```

第一步 `train_df.groupby("personId")`

逻辑上变为（实际上不是这样，是 DataFrameGroupBy 类型）

```
用户 1 这一组：
101
102
101

用户 2 这一组：
201
202

用户 3 这一组：
301
```

第二步 `train_df.groupby("personId")["contentId"]`，分组后，每组只取 `contentId` 这一列

第三步 `.apply(lambda x: set(x.tolist()))`

`apply` 对每一个分组后的 `contentId` 列，执行一次自定义函数

对于用户 1，`x` 是一个 Series

```
0    101
1    102
2    101
Name: contentId, dtype: int64
```

然后转为 list 为 `[101, 102, 101]`，再变为哈希集合

```
personId
1    {101, 102}
2    {201, 202}
3         {301}
Name: contentId, dtype: object
```

再转为 Python 字典

```
{
    1: {101, 102},
    2: {201, 202},
    3: {301}
}
```





### sort_values

```python
user_df = user_df.sort_values("last_timestamp")
```

表示按照 DataFrame 中的 `"last_timestamp"` 这一列进行**升序排序**。排序时是**整行一起移动**，不会只改变 `"last_timestamp"` 这一列，每一行中的其他字段仍然对应，类似 Excel



### iloc

```python
train_parts.append(user_df.iloc[:-1])
test_parts.append(user_df.iloc[-1:])
```

`iloc` 是 pandas 里按**整数位置**取数据的方法，按第几行取，而不是按标签名取

`user_df.iloc[:-1]` 取除了最后一行以外的所有行

`user_df.iloc[-1:]` 取最后一行，结果仍为 DataFrame 格式



### concat

```python
train_df = pd.concat(train_parts, ignore_index=True)
```

pandas 里用来**拼接多个 DataFrame** 的函数

把 train_parts 列表里的多个小 DataFrame，纵向拼接成一个大 DataFrame

