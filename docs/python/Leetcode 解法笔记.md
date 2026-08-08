# leetcode 解法笔记

### 说明

笔记每一个点最好提炼出一个主题，便于后续阅读

## 哈希表

### 1 两数之和	

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出 **和为目标值** *`target`* 的那 **两个** 整数，并返回它们的数组下标

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素

你可以按任意顺序返回答案

```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

```python
class Solution:
    def twoSum(self, nums, target):
        n = len(nums)
        mp = {}
        for i,num in enumerate(nums):
            val = target - nums[i]
            if val in mp:
                return [i,mp[val]]
            else:
                mp[num] = i
```

C++

```c++
class Solution{
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i=0; i < nums.size(); ++i){
            int val = target - nums[i];
            if (mp.find(val) != mp.end()) {
                return {i, mp[val]};
            } else{
                mp[nums[i]] = i;
            }

        }
        return {};
    }
};
```

如果用双循环，时间为 $O(n^2)$，这里用哈希表将其降为 $O(n)$

**出错**：最后的 `mp[num] = i`，不能写成 `mp[val] = i`，记录的是原始数据，而不是补数

---

### 49 字母异位词分组

给你一个字符串数组，请你将**字母异位词**组合在一起。可以按**任意顺序**返回结果列表

```
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
输入: strs = [""]
输出: [[""]]
输入: strs = ["a"]
输出: [["a"]]
```

```python
class Solution:
    def groupAnagrams(self, strs: List[str]):
        mp = {}
        for st in strs:
            key = "".join(sorted(st))
            if key not in mp:
                mp[key] = []
            mp[key].append(st)

        return list(mp.values())
```

- 设置 `if key not in mp:` 的原因

  `mp` 中没有 `key` 时，直接 append 会报错

  除非 `from collections import defaultdict`

- 最后 `list` 的作用

  输出的形式为 `[["bat"],["nat","tan"],["ate","eat","tea"]]`

  外面还有一层 `[]` 包裹

  字典 `mp` 的每一个 `value` 是一个列表，如

  ```python
  {
      "abt": ["bat"],
      "ant": ["nat", "tan"],
      "aet": ["ate", "eat", "tea"]
  }
  ```

  因此 `mp.value()` 得到

  ```
  dict_values(
      [["bat"], ["nat","tan"], ["ate","eat","tea"]]
  )
  ```

  再通过 `list` 转为 **真正** 的列表，把字典里所有的“值”（分好组的那些列表）打包装进一个**大的列表** `[ ]` 里

  也可以写成

  ```python
  ans = []
  for group in mp.values():
      ans.append(group)
  return ans
  ```

**出错**：最后的 `list(mp.values())` 没有转为 list

---

### 128 最长连续序列

给定一个未排序的整数数组 `nums` ，找出数字连续的最长序列（**不要求序列元素在原数组中连续**）的长度

时间复杂度：`O(n)`

```
输入：nums = [100,4,200,1,3,2]
输出：4
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
输入：nums = [1,0,1,2]
输出：3
```

```python
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        ans = 0
        num_set = set(nums)

        for num in num_set:
            if num - 1 not in num_set:
                cur_num = num # 不拿出来也可以，但是还是复制一份比较保险
                cur_length = 1

                while cur_num + 1 in num_set:
                    cur_num += 1
                    cur_length += 1

                ans = max(ans, cur_length)

        return ans
```

`if num - 1 not in num_set:` 寻找开头，如果不是开头的话就**直接跳过**

**出错**：`while cur_num + 1 in num_set:` 写成了 `cur_num` 没有加 + 1

---




## 双指针

### 283 移动零

给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序

必须在不复制数组的情况下原地对数组进行操作

```
输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
输入: nums = [0]
输出: [0]
```

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        left = 0
        n = len(nums)
        for i in range(n):
            if nums[i] != 0:
                nums[i],nums[left] = nums[left],nums[i]
                left += 1
```

---

### 11 盛最多水的容器

给定一个长度为 `n` 的整数数组 `height` 。有 `n` 条垂线，第 `i` 条线的两个端点是 `(i, 0)` 和 `(i, height[i])` 

找出其中的两条线，使得它们与 $x$ 轴共同构成的容器可以容纳最多的水

返回容器可以储存的最大水量

**说明：**你不能倾斜容器

```python
class Solution(object):
    def maxArea(self, height):
        n = len(height)
        left = 0
        right = n - 1
        ans = (right - left)* min(height[left] , height[right])
        while left < right:
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
            cur_ans = (right - left)* min(height[left] , height[right])
            ans = max(ans,cur_ans)
        return ans
```

> 始终移动较短的那一边，才有可能会新的最大值出现

**出错**：取两端min，写成了max

---

### 15 三数之和

给你一个整数数组 `nums` ，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k`，同时还满足 `nums[i] + nums[j] + nums[k] == 0` 。请你**返回**所有和为 `0` 且不重复的三元组

**注意：**答案中不可以包含重复的三元组

```
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
输入：nums = [0,1,1]
输出：[]  # 唯一可能的三元组和不为 0
输入：nums = [0,0,0]
输出：[[0,0,0]]
```

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        ans = []
        nums.sort()
        n = len(nums)

        for i in range(n - 2):
            first = nums[i]
            
            if i > 0 and first == nums[i - 1]:
                continue

            if first > 0:
                break

            target = 0 - first
            left = i + 1
            right = n - 1

            while left < right:
                total = nums[left] + nums[right]
                if total < target:
                    left += 1
                elif total > target:
                    right -= 1
                else:
                    second = nums[left]
                    third = nums[right]
                    ans.append([first, second, third])

                    while left < right and nums[left] == second: # 注1
                        left += 1

                    while left < right and nums[right] == third:
                        right -= 1

        return ans
```

- 要提前排序，这是双指针法的基础

- 注 1

  这里 `nums[left] == second:` 不能写成 `nums[left] == nums[left + 1]`

  因为 `while left < right` 这个循环如果要停止，必须要每次操作都至少移动了一下 `left` 或 `right` 指针。上面的写法中，前者一定可以移动，但后者未必可以移动

**出错**：① `two_sum = nums[left] + nums[right]` 要在循环内部开头算，每次循环 `left` 、`right` 是一定有变化的

② `second = nums[left]`、`third = nums[right]` 忘记写 `nums`

---

### 42 接雨水

给定 `n` 个非负整数表示每个宽度为 `1` 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水

```
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。 
输入：height = [4,2,0,3,2,5]
输出：9
```

```
n == height.length
1 <= n <= 2 * 10^4
0 <= height[i] <= 10^5
```

**解法**：前后缀最大值

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        pre = [0] * n
        pre[0] = height[0]
        for i in range(1,n):
            pre[i] = max(pre[i-1],height[i])
        
        post = [0] * n
        post[n-1] = height[n-1]
        for i in range(n-2,-1,-1):
            post[i] = max(post[i+1],height[i])

        water = 0
        for i in range(n):
            water += min(post[i],pre[i]) - height[i]
        
        return water
```



## 滑动窗口

### 3 无重复字符的最长子串

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长子串** 的长度

```
输入: s = "abcabcbb"
输出: 3 
输入: s = "bbbbb"
输出: 1
输入: s = "pwwkew"
输出: 3
```

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        left = 0  # 目前满足“不含有重复字符的”子串左端点下标, [left, i]
        mp = {}  # mp: {字符 : 索引}
        ans = 0

        for i, ch in enumerate(s):
            if ch in mp and mp[ch] >= left: # 检查ch是否在mp，是为了保护后面的mp[ch]
                left = mp[ch] + 1

            mp[ch] = i  # 共用的，每次都看一下这一次的子串长度
            ans = max(ans,i - left + 1)
        return ans 
```

`if ch in mp` 如果当前的字符不在里面，这样也避免了去取没有的 `mp`

**解法 2**

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if s == "": # 不特判也不影响
            return 0
        ch_set = set()
        left = 0
        n = len(s)
        ans = 0
        for i in range(n):
            ch = s[i]
            if ch not in ch_set:
                ch_set.add(ch)
                ans = max(ans, i - left + 1)
            else:
                while s[left] != ch:
                    ch_del = s[left]
                    ch_set.remove(ch_del)
                    left += 1
                left += 1
        return ans
```

---

### 438 找到字符串中所有字母异位词

给定两个字符串 `s` 和 `p`，找到 `s` 中所有 `p` 的 **异位词** 的子串，返回这些子串的起始索引

不考虑答案输出的顺序

```
输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
输入: s = "abab", p = "ab"
输出: [0,1,2]
```

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        m = len(s)
        n = len(p)
        if m < n:
            return []
        ans = []
        from collections import Counter
        p_count = Counter(p)

        win = {}
        for i in range(n):
            ch = s[i]
            if ch in p_count:
                win[ch] = win.get(ch,0)+1
        if win == p_count:
            ans.append(0)

        for i in range(n,m): # i是目前要加进来的元素
            ch_left = s[i-n]
            ch = s[i]

            if ch_left in p_count:
                win[ch_left] -= 1
            if ch in p_count:
                win[ch] = win.get(ch,0) + 1

            if win == p_count:
                ans.append(i-n+1)
        return ans
```

- 直接硬解，时间 $O(nm \log m)$，具体：

  目标字符串 $p$ 排序为 $O(m \log m)$

  遍历字符串 $s$，从索引 $i$ 到 $i+m-1$ 取出一个长度为 $m$ 的子串，对子串排序 $O(m \log m)$

  比较排序后的子串与排序后的目标字符串 $p$ 是否相等 $O(m)$

  总共会生成约 $n$ 个子串（$n-m+1$），因一般 $n >> m$，$O(n)$，从而总共 $O(nm \log m)$

- 本题用 $O(mn)$ 的方法也会超时间

---



## 子串

### 560 和为 K 的子数组

给你一个整数数组 `nums` 和一个整数 `k` ，请你统计并返回该数组中和为 `k` 的子数组的个数 

**子数组**：数组中元素的连续非空序列

```
输入：nums = [1,1,1], k = 2
输出：2
输入：nums = [1,2,3], k = 3
输出：2
```

```
1 <= nums.length <= 2 * 10^4
-1000 <= nums[i] <= 1000
-10^7 <= k <= 10^7
```

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        mp = {0:1} # 最核心 {前缀和 : 出现的次数}
        pre = 0
        ans = 0

        for i in range(n):
            pre += nums[i]
            ans += mp.get(pre - k,0)
            mp[pre] = mp.get(pre,0) + 1
        return ans 
```

（手算例子，*见notability*）

例：`nums = [3, 1, 2], k = 3`

遍历到 $i=0$ 时，如果 mp 没有记录 `0`，则 `ans += mp.get(pre - k,0)` 就记录不到 `[3]`（但这也是一个答案）

或者对于这个例子，但 `k=6`，要想记录到答案 `[3, 1, 2]`，也依赖于在 mp 中放一个 `{0:1}`

---

### 239 滑动窗口最大值

给你一个整数数组 `nums`，有一个大小为 `k` 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位

返回 *滑动窗口中的最大值*

```
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
输入：nums = [1], k = 1
输出：[1]
```

**解法**：单调队列

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        q = deque()
        ans = []
        for i in range(k):
            while q and q[-1] < nums[i]:
                q.pop()
            q.append(nums[i])
        ans.append(q[0])

        for i in range(k,n): # i是准备新加进来的，所以要考虑到n-1
            if nums[i-k] == q[0]:
                q.popleft()
            while q and q[-1] < nums[i]:
                q.pop()
            q.append(nums[i])
            ans.append(q[0])
        return ans
```

这里 `q[-1] < nums[i]` 是比较保守的写法，相同的最大值会被保留

**出错**：① `while q and q[-1] < nums[i]:` 用了 `if`

② 在循环中，要先考虑左边准备删除的数字，再去考虑新加入的数字

---

### 76 最小覆盖子串

给定两个字符串 `s` 和 `t`，长度分别是 `m` 和 `n`，返回 s 中的 **最短窗口 子串**，使得该子串包含 `t` 中的每一个字符（**包括重复字符**）。如果没有这样的子串，返回空字符串 `""`

测试用例保证答案唯一

**进阶：**你能设计一个在 $O(m+n)$ 时间内解决此问题的算法吗？

```
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。
输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。
```

```
1 <= m, n <= 10^5
s 和 t 由英文字母组成
```

优化切片的解法：时间 $O(m+n)$

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_count = {}
        for ch in t:
            t_count[ch] = t_count.get(ch, 0) + 1

        requires = len(t_count)  # requires 需要满足的字符类数
        win = {} # s中的滑动窗口

        left = 0
        satisfies = 0
        start = 0  # 用于记录答案所在的开始位置
        INF = float('inf')
        min_len = INF

        for i, ch in enumerate(s):  # i 为右端点
            if ch in t_count: # 因为ch不一定会在t_count中，直接使用后面的t_count[ch]可能出错
                win[ch] = win.get(ch, 0) + 1
                if win[ch] == t_count[ch]:
                    satisfies += 1

            while satisfies == requires:
                cur_len = i - left + 1
                if cur_len < min_len:
                    min_len = cur_len
                    start = left

                # 收缩可能会让satisfies变小
                ch_left = s[left]
                if ch_left in t_count:
                    win[ch_left] -= 1
                    if win[ch_left] < t_count[ch_left]:  #
                        satisfies -= 1
                left += 1

        return "" if min_len == INF else s[start:start + min_len]
```

- `left` 和 `start` 的区别：

  `left` 是当前滑动窗口的左端点，会随着算法不断移动

  `start` 是目前找到的最优答案的起始位置，只在发现更短合法窗口时更新

下面这个解法没有优化切片，时间为 $O(m^2 + n)$

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_count = {}
        for ch in t:
            t_count[ch] = t_count.get(ch, 0) + 1

        requires = len(t_count) 
        win = {}

        left = 0
        satisfies = 0
        ans = ""
        for i, ch in enumerate(s):
            if ch in t_count:
                win[ch] = win.get(ch, 0) + 1
                if win[ch] == t_count[ch]:
                    satisfies += 1

            while satisfies == requires:
                tmp_ans = s[left:i + 1]
                if ans == "" or len(tmp_ans) < len(ans): 
                    ans = tmp_ans

                ch_left = s[left]
                if ch_left in t_count:
                    win[ch_left] -= 1
                    if win[ch_left] < t_count[ch_left]:
                        satisfies -= 1
                left += 1
        return ans
```

- 时间复杂度 $O(m^2+n)$

  设 $m = |s|$，$n = |t|$。一开始处理 `t`：$O(n)$

  算法主体 `for i,ch in enumerate(s):` 为 $O(m)$

  `while satisfies == req:` 这里也还是 $O(m)$，因为左右端点都是单调走完一次 s

  但是切片 `tmp_ans = s[left:i+1]` 是瓶颈，最坏情况下窗口长度是 $O(m)$，因此这一部分为 $O(m^2)$

  总时间复杂度为 $O(n)+O(m)+O(m^2)=O(m^2+n)$

因此主要需要优化切片



## 数组

### 56 合并区间

以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]` 。请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间

```
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
输入：intervals = [[4,7],[1,4]]
输出：[[1,7]]
```

```
1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= start_i <= end_i <= 10^4
```

注：即合并所有**有**重叠的闭区间（相切也算有重叠，即 $A \cap B \neq \varnothing$）

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        ans = [intervals[0]]

        for x,y in intervals[1:]:
            if x > ans[-1][-1]:
                ans.append([x,y])
            else:
                ans[-1][-1] = max(ans[-1][-1], y)

        return ans
```

---

### 189 轮转数组

给定一个整数数组 `nums`，将数组中的元素向右轮转 `k` 个位置，其中 `k` 是非负数

```
输入: nums = [1,2,3,4,5,6,7], k = 3
输出: [5,6,7,1,2,3,4]
输入：nums = [-1,-100,3,99], k = 2
输出：[3,99,-1,-100]
```

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n # 易错
        
        # 定义内部翻转函数
        def reverse(left:int,right:int) -> None:
            while left<right:
                nums[left],nums[right] = nums[right],nums[left]
                left += 1
                right -= 1
        
        reverse(0,n-1)
        reverse(0,k-1)
        reverse(k,n-1)
```

- 复杂度

  - 时间：$O(n)$

    第一次翻转约 $\frac{n}{2}$ 次交换，第二次约 $\frac{k}{2}$ 次，第三次约 $\frac{n-k}{2}$ 次，加起来约 $n$ 次，而每次的交换是常数次的

  - 空间：$O(1)$

    即使输入的 $n$ 很大，但是每次交换时，只用到了 `left`、`right`、`tmp`，申请的空间并不会随着$n$ 的变大而变大，也就是**即使计算机只有这几个空间也都能完成计算**，故为常数空间

**出错**：① 忘记取模

---

### 238 除了自身以外数组的乘积

给你一个整数数组 `nums`，返回 数组 `answer` ，其中 `answer[i]` 等于 `nums` 中除了 `nums[i]` 之外其余各元素的乘积

题目数据 **保证** 数组 `nums`之中任意元素的全部前缀元素和后缀的乘积都在 **32 位** 整数范围内

请 **不要使用除法**，且在 $O(n)$ 时间复杂度内完成此题

**进阶：**你可以在 $O(1)$ 的额外空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组 **不被视为** 额外空间）

```
输入: nums = [1,2,3,4]
输出: [24,12,8,6]
输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]
```

```
2 <= nums.length <= 10^5
-30 <= nums[i] <= 30
输入保证数组answer[i]在32位整数范围内
```

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        
        prefix = 1 # 前缀积
        for i in range(n):
            ans[i] = prefix
            prefix *= nums[i]
            
        postfix = 1 # 后缀积
        for i in range(n - 1, -1, -1):
            ans[i] *= postfix
            postfix *= nums[i]
            
        return ans
```

- 复杂度

  - 时间：$O(n)$

    约为 $2n$

  - 额外空间：$O(1)$

    输出数组 **不被视为** 额外空间定义的**额外变量**只有 `prefix`、`postfix`、`i`、`j`、`n`，不随 $n$ 变化，因此该程序是 $O(1)$ 额外空间算法

- 暴力解法

  时间 $O(n^2)$，因为每个 $i$ 要做 $O(n)$ 次乘法，总共 $n$ 个位置

  如果是先求整个数组的乘积，再除以自己，不符合题意说的**不能使用除法**

- 算法原理

  设数组是
  $$
  [ a_0, a_1, a_2, \dots, a_{n-1}]
  $$
  对于位置 $i$，除了 $a_i$ 以外的乘积就是
  $$
  a_0a_1\cdots a_{i-1}\cdot a_{i+1}\cdots a_{n-1}
  $$
  定义
  $$
  L[i] = \prod_{j=0}^{i-1} a_j, \quad R[i] = \prod_{j=i+1}^{n-1} a_j
  $$
  则答案是
  $$
  \text{ans}[i] = L[i]\cdot R[i]
  $$

---

### 41 缺失的第一个正数

给你一个未排序的整数数组 `nums` ，请你找出其中没有出现的最小的正整数

请你实现时间复杂度为 $O(n)$ 并且只使用常数级别额外空间的解决方案

```
输入：nums = [1,2,0]
输出：3
输入：nums = [3,4,-1,1]
输出：2
输入：nums = [7,8,9,11,12]
输出：1
```

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]: # 注意这里是while，要一直换
                target_idx = nums[i] - 1
                nums[i], nums[target_idx] = nums[target_idx], nums[i]
        
        for i in range(n):
            if nums[i] != i + 1:
                return(i + 1)
        
        return n+1
```

最简单的想法是用哈希表，但并不是常数额外空间

理想的下标：值 $n$ 应该放在 $n-1$ 的位置

`nums[nums[i] - 1] != nums[i]`：`nums[i] - 1` 是第 $i$ 个位置上的数 `nums[i]` 该去的地方，`nums[nums[i] - 1]` 是现在这上面的数，如果不是 `nums[i]` 就该换（有可能数组中有重复的数）



## 矩阵

### 73 矩阵置零

给定一个 `m x n` 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 **原地** 算法

例：
$$
\begin{array}{|c|c|c|}
\hline
1 & 1 & 1  \\
\hline
1 & \mathbf{0} & 1  \\
\hline
1 & 1 & 1  \\
\hline
\end{array}
\quad \Longrightarrow \quad
\begin{array}{|c|c|c|}
\hline
1 & \mathbf{0} & 1  \\
\hline
\mathbf{0} & \mathbf{0} & \mathbf{0}  \\
\hline
1 & \mathbf{0} & 1  \\
\hline
\end{array}
$$

```
输入：matrix = [[1,1,1],[1,0,1],[1,1,1]]
输出：[[1,0,1],[0,0,0],[1,0,1]]
```

```python
class Solution(object):
    def setZeroes(self, matrix):
        m = len(matrix)
        n = len(matrix[0])
        zero_row = [False]*m
        zero_col = [False]*n

        # 遍历矩阵一遍，统计0所在的位置
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    zero_row[i] = True
                    zero_col[j] = True
                    
        for i in range(m):
            for j in range(n):
                if zero_row[i] or zero_col[j]:
                	matrix[i][j] = 0
```

最后不用return，在类中已经修改了matrix

`if matrix[i][j] == 0:`  可换成 `if not matrix[i][j]:`

`if zero_row[i] == True:` 可换成 `if zero_row[i]:`

空间复杂度 $O(m + n)$

**易错**：将最后的 `matrix[i][j] = 0` 写成了 `==`

---

### 54 螺旋矩阵

给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 **顺时针螺旋顺序** ，返回矩阵中的所有元素

例：
$$
\begin{matrix}
1 & \rightarrow & 2 & \rightarrow & 3 \\
&             &   &             & \downarrow \\
4 & \rightarrow & 5 &             & 6 \\
\uparrow &      &   &             & \downarrow \\
7 & \leftarrow & 8 & \leftarrow & 9 
\end{matrix}
$$

```
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

```
1 <= m, n <= 10
-100 <= matrix[i][j] <= 100
```

```python
class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        m, n = len(matrix), len(matrix[0])
        left, right, up, down = 0, n-1, 0, m-1
        ans = []

        while True:
            for i in range(left, right + 1):
                ans.append(matrix[up][i])
            up += 1 
            if up > down:
                break

            for i in range(up, down + 1):
                ans.append(matrix[i][right])
            right -= 1
            if right < left:
                break

            for i in range(right, left - 1, -1):
                ans.append(matrix[down][i])
            down -= 1
            if down < up: 
                break

            for i in range(down, up - 1, -1):
                ans.append(matrix[i][left])
            left += 1 
            if left > right: 
                break

        return ans
```

`if not matrix` 检查**空列表** []

`or not matrix[0]` 检查空壳矩阵 [ [ ] ]，这是编写矩阵相关算法标准的**“防御性编程”边界检查**，当 `matrix = [[]]` 时，用 not matrix是会认为有东西的

注意下边界上移是 `up += 1`，矩阵里序号的特点是和直观反过来的

---

### 48 旋转图象

给定一个 `n × n` 的二维矩阵 `matrix` 表示一个图像。请你将图像**顺时针**旋转 90 度

你必须在 **原地** 旋转图像，这意味着你需要直接修改输入的二维矩阵。**请不要** 使用另一个矩阵来旋转图像。例：

<img src="Leetcode 解法笔记.assets/mat1.jpg" alt="mat1" style="zoom:48%;" />

```
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]
输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

```
n == matrix.length == matrix[i].length
1 <= n <= 20
-1000 <= matrix[i][j] <= 1000
```

```python
class Solution(object):
    def rotate(self, matrix):
        n = len(matrix)
        for i in range(n // 2):
            for j in range(n):
                matrix[n - 1 - i][j] , matrix[i][j] = matrix[i][j], matrix[n - 1 - i][j]

        for i in range(n):
            for j in range(i+1,n):
                matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]
```

---



## 链表

### 160 相交链表

给你两个单链表的头节点 `headA` 和 `headB` ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 `null` 

图示两个链表在节点 `c1` 开始相交：

<img src="Leetcode 解法笔记.assets/160_statement.png" alt="160_statement" style="zoom:48%;" />

题目数据 **保证** 整个链式结构中不存在环

**注意**，函数返回结果后，链表必须 **保持其原始结构** 

**评测系统说明**

> **评测系统** 的输入如下（你设计的程序 **不适用** 此输入）：
>
> - `intersectVal` - 相交的起始节点的值。如果不存在相交节点，这一值为 `0`
> - `listA` - 第一个链表
> - `listB` - 第二个链表
> - `skipA` - 在 `listA` 中（从头节点开始）跳到交叉节点的节点数
> - `skipB` - 在 `listB` 中（从头节点开始）跳到交叉节点的节点数
>
> 评测系统将根据这些输入创建链式数据结构，并将两个头节点 `headA` 和 `headB` 传递给你的程序。如果程序能够正确返回相交节点，那么你的解决方案将被 **视作正确答案** 

```
listA 中节点数目为 m
listB 中节点数目为 n
1 <= m, n <= 3 * 10^4
1 <= Node.val <= 10^5
0 <= skipA <= m
0 <= skipB <= n
如果 listA 和 listB 没有交点，intersectVal 为 0
如果 listA 和 listB 有交点，intersectVal == listA[skipA] == listB[skipB]
```

注：没有相交节点时，需要返回 `None`

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        p1 = headA
        p2 = headB

        while p1 != p2:
            p1 = p1.next if p1 else headB
            p2 = p2.next if p2 else headA
        return p1
```

**思路**：两个指针分别走 A 链 + B 链、B 链 + A 链，总路径长度相同，故必然在同一位置相遇

如果没有相交的相交的节点时，二者都会到 `None`，此时 `p1 = p2`，但返回的就是 `None`

---

### 206 反转链表

给你单链表的头节点 `head` ，请你反转链表，并返回反转后的链表

例：

<img src="Leetcode 解法笔记.assets/rev1ex1.jpg" alt="rev1ex1" style="zoom:52%;" />

```
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
输入：head = [1,2]
输出：[2,1]
输入：head = []
输出：[]
```

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head # 不去改变本来有的head，所以创建一个cur
        rev_head = None
        while cur:
            nxt = cur.next
            cur.next = rev_head
            rev_head = cur
            cur = nxt
        return rev_head
```

`cur = head` 非必须，这里是因为：使用额外指针遍历，避免混淆 head 的原始含义

---

### 234 回文链表

给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false`

```
输入：head = [1,2,2,1]
输出：true
输入：head = [1,2]
输出：false
```

```
链表中节点数目在范围[1, 10^5] 内
0 <= Node.val <= 9
```

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head.next: # 注意不是两层
            return True
        slow = head
        fast = head
        while fast and fast.next: # 奇数个节点: slow在正中间，偶数个在 n/2 + 1处
            slow = slow.next
            fast = fast.next.next

        rev_head = None # 反转从 slow到末尾的链表，并用rev_head记住其头结点
        cur = slow
        while cur:
            nxt = cur.next
            cur.next = rev_head
            rev_head = cur
            cur = nxt
        
        left = head
        right = rev_head
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True
```

- `while right:` 不能写成 left，因为 `left` 所在的这个链表是完整的，用它作while，肯定是会循环的次数更多，会到右半段所没有的长度，此时 `right.val` 取不出值，会出错

- 不用把左半段最后一个指向 `None`

  偶数时，例如 1 -> 2 -> 2 -> 1，左半段 1 -> 2，右半段 1 -> 2

  奇数时，例如 1 -> 2 -> 3 -> 2 -> 1，左半段 1 -> 2 -> 3，右半段 1 -> 2 -> 3

  虽然左半段的 3 下一个可能已经变成了其他，但并不需要用到

- 开头 `if not head.next:`，如果写成 `if not head.next.next:`

  对于例子 `head = [1, 2]`，真实答案为 `False`，但算法输出 `True`

  两个 `next` 时，会指向 `None`，此时为空，再 not 一下为真

- `if left.val != right.val:`

  不能写成 `if left != right:` 此时比较的是两个对象是否相同。即使其 val 相同，地址也是不相同的

---

### 141 环形链表

给你一个链表的头节点 `head` ，判断链表中是否有环

如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（索引从 0 开始）。**注意：`pos` 不作为参数进行传递** 。仅仅是为了标识链表的实际情况

*如果链表中存在环* ，则返回 `true` 。 否则，返回 `false`

**进阶：**你能用 $O(1)$（即，常量）内存解决此问题吗？

```
链表中节点的数目范围是 [0, 10^4]
-10^5 <= Node.val <= 10^5
pos 为 -1 或者链表中的一个 有效索引 。
```

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return Fasle
```

时间：$O(n)$，空间：$O(1)$

算法只用了**两个指针变量** `slow`、`fast`，不管链表多长，使用的内存是**常数级别**

`while fast and fast.next:` 如 `1 -> 2 -> 3 -> None`，如果 `fast` 在 3 处，此时 `fast` 非空，但是执行循环体内部时，`fast = fast.next.next` 会报错

不用担心 `fast` 跑太快会走的太远，若有环是没有终点的，`fast` 肯定可以追上 `slow`（相对速度为 1）

**法2**

简单的想法是用哈希表，把访问过的节点存起来，如果再次访问某节点，说明是有环的

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        vistied = set()
        cur = head
        while cur:
            if cur in vistied:
                return True
            else:
                vistied.add(cur)
                cur = cur.next
        return False
```

这里用 `set` 即可，不用 dict，因为无需用到值

时间：$O(n)$，空间：$O(n)$

---

### 142 环形链表 II

给定一个链表的头节点  `head` ，返回链表开始入环的第一个节点。 *如果链表无环，则返回 `null`*

**不允许修改** 链表

**进阶：**你是否可以使用 `O(1)` 空间解决此题？

**评测系统说明**：如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（**索引从 0 开始**）。如果 `pos` 是 `-1`，则在该链表中没有环。**注意：`pos` 不作为参数进行传递**，仅仅是为了标识链表的实际情况

```
链表中节点的数目范围在范围 [0, 10^4] 内
-10^5 <= Node.val <= 10^5
pos 的值为 -1 或者链表中的一个有效索引
```

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast: # 此时相遇
                p1 = slow
                p2 = head
                while p1 != p2:
                    p1 = p1.next
                    p2 = p2.next
                return p2
        return None 
```

**性质**：快慢指针相遇后，一个指针回到 head，两个指针一起走，再次相遇就是环入口

**Proof**：如下图所示，即证明：快慢指针第一次相遇于 $M$ 后，把一个指针放回 `head`，另一个留在 $M$，二者都每次走一步，它们会在环入口 $E$ 相遇

<img src="Leetcode 解法笔记.assets/ChatGPT Image 2026年7月16日 19_07_34.png" alt="ChatGPT Image 2026年7月16日 19_07_34" style="zoom:26%;" />

定义 $d(x,y)$ 为：从节点 $x$ 出发，沿着 `next` 走，**第一次** 到达 $y$ 所需要的 **步数**（至少需要 1 步）

设 $d(\text{head},E) = A$，$d(E,M) = B$，$d(M,E) = C$，则环长为 $R = B+C$。设相遇时，慢指针走了 $l_S$ 步，快指针走了 $l_F$ 步，慢指针完整走完的圈数为 $k$，则
$$
\begin{aligned}
l_S &= d(\text{head},M)  + kR\\
& = d(\text{head},E) +  d(E,M)+kR \\ 
& = A+ B +kR
\end{aligned}
$$
则 $l_F = 2l_S$。两指针在 $M$ 处相遇，设快指针比慢指针多走了 $n$ 圈，则
$$
\begin{aligned}
l_F - l_S & = nR \\
l_S & = nR \\
A+ B +kR &=nR 
\end{aligned}
$$
现在证明一个指针放回 `head`，一个指针在 $M$，两指针下一次相遇时，将位于 $E$，即位于 $M$ 指针走 $A$ 步时一定要走到 $E$（若能相遇，一定是二者第一次相遇的位置）
$$
l_S + A = 
$$

【注】这里的证明还在思考

**出错**：最后未考虑无环情况 `return None`

---

### 21 合并两个有序链表

将两个升序链表合并为一个新的 **升序** 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的

```
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
输入：l1 = [], l2 = []
输出：[]
输入：l1 = [], l2 = [0]
输出：[0]
```

```
两个链表的节点数目范围是 [0, 50]
-100 <= Node.val <= 100
l1 和 l2 均按 非递减顺序 排列
```

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        cur = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next # 易错，共用的
            
        if list1: 
            cur.next = list1 # list1现在指向的一定不是None，是有东西的，可以接过来
        if list2:
            cur.next = list2
        return dummy.next
```

---

### 2 两数相加

给你两个 **非空** 的链表，表示两个非负的整数。它们每位数字都是按照 **逆序** 的方式存储的，并且每个节点只能存储 **一位** 数字

请你将两个数相加，并以相同形式返回一个表示和的链表

你可以假设除了数字 0 之外，这两个数都不会以 0 开头

```
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
输入：l1 = [0], l2 = [0]
输出：[0]
输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]
```

```
每个链表中的节点数在范围 [1, 100] 内
0 <= Node.val <= 9
题目数据保证列表表示的数字不含前导零
```

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        cur = dummy
        carry = 0
        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            s = x + y + carry  # 和:sum
            carry = s // 10 # 进位
            
            cur.next = ListNode(s % 10)
            cur = cur.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next 

        return dummy.next
```

`cur = cur.next` 要记得把cur向后移动

**出错**：将整除 `//` 写成普通除法 `/`

---

### 19 删除链表的倒数第 N 个结点

给你一个链表，删除链表的**倒数**第 `n` 个结点，并且返回链表的头结点

**进阶：**你能尝试使用一趟扫描实现吗？

```
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
输入：head = [1], n = 1
输出：[]
输入：head = [1,2], n = 1
输出：[1]
```

```
链表中结点的数目为 sz
1 <= sz <= 30
0 <= Node.val <= 100
1 <= n <= sz
```

注：`sz` 并不能直接获得

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head) # dummy -> head
        fast = head
        slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        # 此时 slow 已经站在了要删的前一个节点上
        slow.next = slow.next.next
        return dummy.next
```

`dummy` 便于处理要删除的是头结点的情况

简单的想法是：先遍历一遍列表，记下来长度 $L$，要删除倒数第 $n$ 个，即删除正着数第 $L-n+1$ 个

`return dummy.next` 因为真正的头节点可能被删除，所以不能直接返回原来的 `head`

> 快在head，慢在dummy，快指针先走 $n$ 步，快慢再同速走，慢会停在删除的前1个

**出错**：返回不能写 `head`，当要删的刚好就是 head 时，会错

---

### 24 两两交换链表中的节点

给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）

```
输入：head = [1,2,3,4]
输出：[2,1,4,3]
输入：head = []
输出：[]
输入：head = [1]
输出：[1]
```

```
链表中节点的数目在范围 [0, 100] 内
0 <= Node.val <= 100
```

```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0,head)
        cur = dummy
        while cur.next and cur.next.next:
            node1 = cur.next
            node2 = cur.next.next
            nxt_node = cur.next.next.next

            cur.next = node2
            node2.next = node1
            node1.next = nxt_node
            cur = node1

        return dummy.next
```

---

### 25 K 个一组翻转链表

给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表

`k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序

你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换

```
输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]

输入：head = [1,2,3,4,5], k = 3
输出：[3,2,1,4,5]
```

```
1 <= k <= n <= 5000 # 链表中的节点数目为 n
0 <= Node.val <= 1000
```

```python
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next
            group_next = kth.next

            rev_head, rev_tail = self.reverse(group_prev.next, kth)
            
            # 接回原链表
            group_prev.next = rev_head
            rev_tail.next = group_next

            group_prev = rev_tail
        
   	def reverse(self, head, tail):
        tail.next = None
        rev_head = None
        rev_tail = head
        cur = head
        while cur:
            nxt = cur.next
            cur.next = rev_head
            rev_head = cur
            cur = nxt
        return rev_head, rev_tail
```

这道题是不难的，注意把翻转后的链表接回去即可

- 出错：`rev_head, rev_tail = self.reverse(group_prev.next, kth)` 这里传入的链表开头，写成了 `group_prev`，其实是需要再前进一个位置的

- 在 while 循环中，要先向前  `kth = kth.next`，再去判断 `kth` 是否为 `None`，如

  ```
   0 -> 1 -> 2 -> None   设 k = 3
   ↑
  kth
  ```

  需要从 0 的下一个开始，至少还有 3 个节点。如果是先判断 `kth` 是否为 `None`，有可能让 `kth` 刚好出于 `None` 的位置

---

### 138 随机链表的复制

给你一个长度为 `n` 的链表，每个节点包含一个额外增加的随机指针 `random` ，该指针可以指向链表中的任何节点或空节点

构造这个链表的 **深拷贝**。深拷贝应该正好由 `n` 个 **全新** 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 `next` 指针和 `random` 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。**复制链表中的指针都不应指向原链表中的节点**

例如，如果原链表中有 `X` 和 `Y` 两个节点，其中 `X.random --> Y` 。那么在复制链表中对应的两个节点 `x` 和 `y` ，同样有 `x.random --> y`

返回复制链表的头节点

你的代码 **只** 接受原链表的头节点 `head` 作为传入参数

```
0 <= n <= 1000
-10^4 <= Node.val <= 10^4
Node.random 为 null 或指向链表中的节点。
```

```python
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None

        cur = head
        mp = {}  # {原地址 : 新节点}
        while cur:
            mp[cur] = Node(cur.val)
            cur = cur.next  # 容易遗漏

        cur = head
        while cur:
            if cur.next:
                mp[cur].next = mp[cur.next]
            if cur.random:
                mp[cur].random = mp[cur.random]
            cur = cur.next

        return mp[head]
```

- 特判空的情况

  如果 `head = None`，那么前面的两个 `while cur:` 都不会执行，`mp` 仍然是空字典 `{}`

  此时最后的 `return mp[head]`，在字典中并没有 `None` 这个关键字

  也可以在字典中预存 `{None: None}` 来解决

**解法**：预存的写法

```python
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        mp = {None:None} # {原地址:新地址}
        cur = head
        while cur:
            value = cur.val
            mp[cur] = Node(value)
            cur = cur.next
        
        cur = head
        while cur:
            mp[cur].next = mp[cur.next]
            mp[cur].random = mp[cur.random]
            cur = cur.nex
            
        return mp[head]
```

---

### 148 排序链表

给你链表的头结点 `head` ，请将其按 **升序** 排列并返回 **排序后的链表*

```
链表中节点的数目在范围 [0, 5 * 10^4] 内
-10^5 <= Node.val <= 10^5
```

注：就是考**归并排序**

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:  # basecase一个时：默认有序
            return head
        dummy = ListNode(0)
        dummy.next = head
        slow = dummy
        fast = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        # 此时slow偶数在左半边最后一个，奇数在正中间

        mid = slow.next
        slow.next = None

        left = self.sortList(head)
        right = self.sortList(mid)

        return self.merge(left, right)

    def merge(self, l1, l2) -> Optional[ListNode]: 
        dummy = ListNode(0)
        cur = dummy
        while l1 and l2:
            if l1.val < l2.val:
                cur.next = l1
                l1 = l1.next
            else:
                cur.next = l2
                l2 = l2.next
            cur = cur.next

        if l1:
            cur.next = l1
        if l2:
            cur.next = l2

        return dummy.next
```

由于 sortList 函数是递归调用的，肯定要给出 basecase 的情况

出错：`cur.next = l1`、`cur.next = l2` 没有写 next

---

### 23 合并 K 个升序链表

给你一个链表数组，每个链表都已经按升序排列

请你将所有链表合并到一个升序链表中，返回合并后的链表

```
k == lists.length
0 <= k <= 10^4
0 <= lists[i].length <= 500
-10^4 <= lists[i][j] <= 10^4
lists[i] 按 升序 排列
lists[i].length 的总和不超过 10^4
```

**法1**：最小堆

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i,node in enumerate(lists):
            if node:
                heapq.heappush(heap,(node.val, i, node)) # i用来缓冲，避免node.val相同的情况
        dummy = ListNode(0)
        cur = dummy 
        while heap:
            _, i, node = heapq.heappop(heap) # 第一个参数不能用 node.val的形式来接收，但需要用到节点的值时，可以靠这种方式来计算

            cur.next = node
            cur = cur.next

            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
```

时间：$O(N \log k)$（$N$ 为数据总个数，$k$ 为链表个数），具体：

- 最多往堆里放 $k$ 个元素（每个链表的头节点）。每次 `heappush`：$O(\log k)$，共 $k$ 次。时间：$O(k \log k)$

- 对于每一个节点：

  - 被 `heappop` 一次
  - 并且如果有 `next`，会被 `heappush` 一次
  
  大约 $O(N)$，每次**堆操作**复杂度 $O(\log k)$，故 $O(N\log k)$

故 $O(k \log k) + O(N \log k) = O(N\log k)$

**出错**：`while heap` 内部的 cur 忘记向后移

**法2**：暴力解法

可以通过 leetcode

```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        l = len(lists)
        data = []
        for i in range(l):
            node = lists[i]
            cur = node
            while cur:
                data.append(cur.val)
                cur = cur.next

        data.sort()
        dummy = ListNode(0)
        cur = dummy
        for i in range(len(data)):
            cur.next = ListNode(data[i])
            cur = cur.next
        return dummy.next
```

时间：$O(N\log N)$（$N$ 为数据总个数）。具体：

- 遍历所有链表，把值收集到数组 `data` 中，会把每个节点访问一次，故 $O(N)$
- 对数组 `data` 排序， $O(N\log N)$
- 根据排好序的数组重新建一个新链表，又遍历一遍数组，故 $O(N)$

故 $O(N) + O(N\log N) + O(N) = O(N\log N)$

---

### 146 LRU 缓存

请你设计并实现一个满足 **LRU（最近最少使用）缓存** 约束的数据结构

实现 `LRUCache` 类：

- `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存
- `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1`
- `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字

函数 `get` 和 `put` 必须以 $O(1)$ 的平均时间复杂度运行

```
1 <= capacity <= 3000
0 <= key <= 10000
0 <= value <= 10^5
最多调用 2 * 10^5 次 get 和 put
```

```python
class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.mp = {} # 键:值

        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):# 将某一个节点删除
        next_node = node.next
        prev_node = node.prev
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node) -> None:# 注意顺序
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.mp:
            node = self.mp[key]
            self._remove(node)
            self._add_to_head(node)
            return node.val
        else:
            return -1
        

    def put(self, key: int, value: int) -> None:
        if key in self.mp:
            node = self.mp[key]
            node.val = value

            self._remove(node)
            self._add_to_head(node)
        else:
            node = Node(key,value)
            self._add_to_head(node)
            self.mp[key] = node

            if len(self.mp) > self.capacity:
                removed = self.tail.prev
                self._remove(removed)
                del self.mp[removed.key] # 易错


class Node:
    def __init__(self, key = 0, value = 0):
        self.key = key
        self.val = value
        self.prev = None
        self.next = None
```

`head` 没有prev， `tail` 没有next，都是None，并不是真的没有，只是不会用到这两个

`_add_to_head`、`_remove` 都是比较有必要额外去写的函数

**出错**：当插入新节点，超出容量后，没有删除最久没使用的节点

- 不删除最久没使用的节点导致的错误：

  ```
  输入
  ["LRUCache","put","put","get","put","get","put","get","get","get"]
  [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
  
  我的程序输出
  [null,null,null,1,null,2,null,1,3,4]
  
  预期输出
  [null,null,null,1,null,-1,null,-1,3,4]
  ```

  在前两次的 put 中，就已经达到了容量

  插入 key = 3 的节点时，虽然程序删掉了 tail 前面的节点。但是如果不在 `self.mp` 中也删除，还是能通过字典记住这个节点的，并且字典中是有节点 2 的

  

## 二叉树

### 94 二叉树的中序遍历

给定一个二叉树的根节点 `root` ，返回 *它的 **中序** 遍历* （注：返回的是装着 `val` 的数组）

**进阶:** 递归算法很简单，你可以通过迭代算法完成吗？

```
树中节点数目在范围 [0, 100] 内
-100 <= Node.val <= 100
```

**解法 1**：递归

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ans = []
        def backtrack(node):
            if not node:
                return 
            backtrack(node.left)
            ans.append(node.val)
            backtrack(node.right)
        backtrack(root)
        return ans
```

**解法 2**：迭代解法，可 AC

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        cur = root
        ans = []
        while cur or stack:
            while cur: 
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            ans.append(cur.val)
            cur = cur.right
        return ans
```

- `cur = stack.pop()` 一定要 pop 后才记录答案的原因

  由于 while 部分是 `while cur`，只要能存入 `stack` 就一定可以提取 `val`

  后续 `cur = cur.right` 只是调整为了右子树（可能为 `None`），但并没有存到 `stack` 中，后续还是要经过 `while cur` 来检查的（即使是右子树的根节点，也会被检查，while 循环部分就是从根节点开始检查的）

---

### 104 二叉树的最大深度

给定一个二叉树 `root` ，返回其最大深度

二叉树的 **最大深度** 是指从根节点到最远叶子节点的最长路径上的节点数

```
树中节点的数量在 [0, 10^4] 区间内
-100 <= Node.val <= 100
```

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        max_left = self.maxDepth(root.left)
        max_right = self.maxDepth(root.right)
        return max(max_left,max_right) + 1
```

---

### 226 翻转二叉树

给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点

```
下图
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

<img src="Leetcode 解法笔记.assets/image-20260714215428738.png" alt="image-20260714215428738" style="zoom:19%;" />

```
下图
输入：root = [2,1,3]
输出：[2,3,1]
```

<img src="Leetcode 解法笔记.assets/image-20260714215550616.png" alt="image-20260714215550616" style="zoom:18%;" />

```
输入：root = []
输出：[]
```

```
树中节点数目范围在 [0, 100] 内
-100 <= Node.val <= 100
```

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        self.invertTree(root.left)
        self.invertTree(root.right)
        root.left, root.right = root.right, root.left
        return root
```

- 递归没有用返回值，但二叉树仍可被修改

  因为二叉树节点是 **引用对象**，递归是在 **原地修改** 它（就是直接在改，并非复制出来一份新的来改）

- 对左、右子树分别运行 `invertTree` 后还需要交换节点值的原因

  `invertTree` 的定义是将 `root` 为根节点的二叉树翻转，因此本身是不需要处理根节点的（因为根节点只有一个点）

  当运行 `root.left` 和 `root.right` 之后，只能保证这两者作为根节点的二叉树是翻转了的

  但本身它们的翻转还需要处理（通过交换实现）

---

### 101 对称二叉树

给你一个二叉树的根节点 `root` ， 检查它是否轴对称

**进阶：**你可以运用 **递归** 和 **迭代** 两种方法解决这个问题吗？

```
树中节点数目在范围 [1, 1000] 内
-100 <= Node.val <= 100
```

**解法 1**：递归解法

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def backtrack(t1,t2):
            if not t1 and not t2:
                return True
            if not t1 or not t2:
                return False
            return backtrack(t1.left,t2.right) and backtrack(t1.right, t2.left) and (t1.val == t2.val)
        return backtrack(root.left,root.right)
```

**解法 2**：迭代解法

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        from collections import deque
        q = deque([(root.left, root.right)])
        while q:
            left_node, right_node = q.popleft()
            if not left_node and not right_node:
                continue
            if not left_node or not right_node:
                return False
            if left_node.val != right_node.val:
                return False
            q.append((left_node.left, right_node.right))
            q.append((left_node.right, right_node.left))
        return True
```

注意 deque 的初始化

---

### 543 二叉树的直径

给你一棵二叉树的根节点，返回该树的 **直径**

二叉树的 **直径** 是指树中任意两个节点之间最长路径的 **长度**。这条路径可能经过也可能不经过根节点 `root` 

两节点之间路径的 **长度** 由它们之间边数表示

```
下图中
输入：root = [1,2,3,4,5]
输出：3
```

<img src="Leetcode 解法笔记.assets/image-20260714220743286.png" alt="image-20260714220743286" style="zoom:14%;" />

```
输入：root = [1,2]
输出：1
```

```
树中节点数目在范围 [1, 10^4] 内
-100 <= Node.val <= 100
```

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.ans = 0
        def backtrack(node):
            if not node:
                return 0
            left_depth = backtrack(node.left)
            right_depth = backtrack(node.right)
            self.ans = max(self.ans, left_depth + right_depth)
            return max(left_depth, right_depth) + 1
        backtrack(root)
        return self.ans
```

- 算法原理

  过当前节点的最大路径（直径）是左子树深度加右子树深度

  在计算最大深度的同时，顺便计算出直径

- 使用全局变量 `self.ans` 的原因

  如果用 `ans`，在 `backtrack` 的内部，Python 会认为是这个函数里面的局部变量

  如果直接使用会认为这个变量还没有赋值，会报错

---

### 102 二叉树的层序遍历

给你二叉树的根节点 `root` ，返回其节点值的 **层序遍历**（即逐层地，从左到右访问所有节点）

```
树中节点数目在范围 [0, 2000] 内
-1000 <= Node.val <= 1000
```

**解法**：迭代算法

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        from collections import deque
        ans = []
        q = deque([root])
        while q:
            q_len = len(q)
            tmp = []
            for _ in range(q_len):
                node = q.popleft()
                tmp.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(tmp)
        return ans
```

---

### 108 将有序数组转换为二叉搜索树

给你一个整数数组 `nums` ，其中元素已经按 **升序** 排列，请你将其转换为一棵 **平衡** 二叉搜索树

```
1 <= nums.length <= 10^4
-10^4 <= nums[i] <= 10^4
nums 按 严格递增 顺序排列
```

注：要返回这颗平衡二叉树的根节点

**解法 1**：传下标

```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def build(left,right):
            if left > right:
                return None
            mid = (left + right) // 2
            node = TreeNode(nums[mid])
            node.left = build(left,mid - 1)
            node.right = build(mid + 1, right)
            return node
        
        return build(0,len(nums) - 1)
```

- 无需单独考虑 $\text{left} = \text{right}$

  此时设 $\text{mid} = \text{left} = \text{right} = a$，`node.left = build(a, a - 1)`、`node.right = build(a + 1,a)` 均会得到 `None`，实际只有 `node = TreeNode(nums[a])`

  这种情况下，等价于 `TreeNode(nums[a], None, None)`

**解法 2**：传切片

```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None

        mid = len(nums) // 2
        root = TreeNode(nums[mid])

        root.left = self.sortedArrayToBST(nums[:mid])
        root.right = self.sortedArrayToBST(nums[mid + 1:])

        return root
```

不用单独考虑 `n == 1`，此时后面的切片切不出来，就自动左、右子树为 `None`

---

### 98 验证二叉搜索树

给你一个二叉树的根节点 `root` ，判断其是否是一个有效的二叉搜索树

**有效** 二叉搜索树定义如下：

- 节点的左子树只包含 **严格小于** 当前节点的数
- 节点的右子树只包含 **严格大于** 当前节点的数
- 所有左子树和右子树自身必须也是二叉搜索树

```
树中节点数目范围在[1, 10^4] 内
-2^31 <= Node.val <= 2^31 - 1
```

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        nums = []
        def backtrack(node):
            if not node: # 剪枝
                return
            
            backtrack(node.left)
            nums.append(node.val)
            backtrack(node.right)

        backtrack(root)
        n = len(nums)
        for i in range(n-1):
            if nums[i] >= nums[i+1]:
                return False
        return True
```

中序遍历 + 检查答案是否是严格单调增即可

****

### 230 二叉搜索树中第 K 小的元素

给定一个二叉搜索树的根节点 `root` ，和一个整数 `k` ，请你设计一个算法查找其中第 `k` 小的元素（`k` 从 1 开始计数）

**进阶：**如果二叉搜索树经常被修改（插入/删除操作）并且你需要频繁地查找第 `k` 小的值，你将如何优化算法？

```
树中的节点数为 n 
1 <= k <= n <= 10^4
0 <= Node.val <= 10^4
```

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        nums = []
        def backtrack(node):
            if not node:
                return
            
            backtrack(node.left)
            nums.append(node.val)
            backtrack(node.right)

        backtrack(root)
        return nums[k-1]
```

---

### 199 二叉树的右视图

给定一个二叉树的 **根节点** `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值

```
二叉树的节点个数的范围是 [0,100]
-100 <= Node.val <= 100 
```

- BFS

```python
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        
        ans = []
        q = deque([root])
        while q:
            q_len = len(q)
            for i in range(q_len):
                node = q.popleft()
                if i == q_len - 1: # 到最后一个了
                    ans.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return ans
```

---

### 114 二叉树展开为链表

给你二叉树的根结点 `root` ，请你将它展开为一个单链表：

- 展开后的单链表应该同样使用 `TreeNode` ，其中 `right` 子指针指向链表中下一个结点，而左子指针始终为 `null` 
- 展开后的单链表应该与二叉树 **先序遍历** 顺序相同

**进阶：**你可以使用原地算法（$O(1)$ 额外空间）展开这棵树吗？

```
树中结点数在范围 [0, 2000] 内
-100 <= Node.val <= 100
```

```python
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        nodes = []
        def backtrack(node):
            if not node:
                return 
            nodes.append(node)
            backtrack(node.left)
            backtrack(node.right)
        
        backtrack(root)
        n = len(nodes)
        for i in range(n-1):
            cur = nodes[i]
            nxt = nodes[i+1]
            cur.left = None
            cur.right = nxt
```

- 时间：$O(n)$

  每个节点访问一次

- 空间：$O(n)$

  `nodes` 数组存了所有节点，空间为 $O(n)$

  递归栈取决于树的高度 h，平衡树 $O(\log n)$，最坏（链状树）$O(n)$，因此总空间复杂度 $O(h)+O(n) = O(n)$

---

### 105 从前序与中序遍历序列构造二叉树 

给定两个整数数组 `preorder` 和 `inorder` ，其中 `preorder` 是二叉树的**先序遍历**， `inorder` 是同一棵树的**中序遍历**，请构造二叉树并返回其根节点

```
1 <= preorder.length <= 3000
inorder.length == preorder.length
-3000 <= preorder[i], inorder[i] <= 3000
preorder 和 inorder 均 无重复 元素
inorder 均出现在 preorder
preorder 保证 为二叉树的前序遍历序列
inorder 保证 为二叉树的中序遍历序列
```

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
        
        # 至少有一个元素了
        root_val = preorder[0]
        root = TreeNode(root_val)

        root_index = inorder.index(root_val)

        i1 = inorder[:root_index]
        i2 = inorder[root_index + 1:]
        
        p1 = preorder[1:len(i1)+1] # 这里容易写错
        p2 = preorder[len(i1)+1:]

        root.left = self.buildTree(p1,i1)
        root.right = self.buildTree(p2,i2)
        
        return root
```

写题时，要很明确什么是前序、中序

---

### 437 路径总和 III

给定一个二叉树的根节点 `root` ，和一个整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 **路径** 的数目

**路径** 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）

```
二叉树的节点个数的范围是 [0,1000]
-10^9 <= Node.val <= 10^9
-1000 <= targetSum <= 1000 
```

```python
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        def count_from(node, target):
            if not node:
                return 0
            count = 1 if node.val == target else 0
            count += count_from(node.left, target - node.val)
            count += count_from(node.right, target - node.val)
            return count
        def backtrack(node): 
            if not node:
                return 0
            return count_from(node,targetSum) + backtrack(node.left) + backtrack(node.right)

        return backtrack(root)
```

- `def count_from(node, target):` 的定义

  统计从 `node` 开始（一定要从这个节点开始），向下形成的路径数

- `def backtrack(node):` 的定义

  以 `node` 为根节点的树，对其每一个节点均调用 count_from，统计路径和为 `targetSum` 的总数

---

### 236 二叉树的最近公共祖先

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（**一个节点也可以是它自己的祖先**）。”

```
树中节点数目在范围 [2, 10^5] 内
-10^9 <= Node.val <= 10^9
所有 Node.val 互不相同
p != q
p 和 q 均存在于给定的二叉树中
```

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left,p,q)
        right = self.lowestCommonAncestor(root.right,p,q)

        if left and right: # 左左右各有p和q，对于最外层来说只有这三个答案
            return root # 提交答案
        if left:
            return left
        else: # 不等价于if right，空的情况也往上传递了
            return right
```

---

### 124 二叉树中的最大路径和

二叉树中的 **路径** 被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中 **至多出现一次** 。该路径 **至少包含一个** 节点，且不一定经过根节点

**路径和** 是路径中各节点值的总和

给你一个二叉树的根节点 `root` ，返回其 **最大路径和**

```
输入：root = [1,2,3]
输出：6
输入：root = [-10,9,20,null,null,15,7]
输出：42
```

```
树中节点数目范围是 [1, 3 * 10^4]
-1000 <= Node.val <= 1000
```

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.ans = float('-inf')
        def backtrack(node):
            if not node:
                return 0
            left_max = max(0,backtrack(node.left))
            right_max = max(0, backtrack(node.right))

            self.ans = max(self.ans, node.val + left_max + right_max)
            return node.val + max(left_max,right_max)
        backtrack(root)
        return self.ans
```

- backtrack 的定义

  是从 node 出发向下不拐弯的单链，最优的结果（即一定要从 node 出发）

  在单链回溯的过程中，间接地把题目所需要的量算出来

- `self.ans = float('-inf')` 初值不能设为 0

  如果设为0，**全是负数的树**会出错

  如果整棵树都是负数，答案本来是其中最大的负数，把 `self.ans` 初值设成了 `0`，于是最后答案可能保留成 `0`

**出错**：忘记调用 `backtrack(root)`



## 图论

### 200 岛屿数量

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成

此外，你可以假设该网格的四条边均被水包围

 ```
 输入：grid = [
   ['1','1','1','1','0'],
   ['1','1','0','1','0'],
   ['1','1','0','0','0'],
   ['0','0','0','0','0']
 ]
 输出：1
 输入：grid = [
   ['1','1','0','0','0'],
   ['1','1','0','0','0'],
   ['0','0','1','0','0'],
   ['0','0','0','1','1']
 ]
 输出：3
 ```

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0
       	dire = [(1,0), (-1,0), (0,1), (0,-1)] 

        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    ans += 1
                    q = deque([(i, j)])
                    grid[i][j] = '0' # 注1

                    while q:
                        r, c = q.popleft()
                        for dr, dc in dire:
                            new_r = r + dr
                            new_c = c + dc
                            if 0 <= new_r <= m-1 and 0 <= new_c <= n-1 and grid[new_r][new_c] == '1':
                                grid[new_r][new_c] = '0'
                                q.append((new_r, new_c))

        return ans
```

- **BFS**，Breadth-First Search，广度优先搜索算法，一种图或网格的遍历算法

  从一个起点出发，**一层一层向外扩展**，先访问距离近的点，再访问距离远的点

- `q = deque([(i, j)])`

  一定要这样写，不能 `deque([i,j])`

- 注 1

  如果不立刻标记，别的相邻格子在检查邻居时，可能又会把它重复加入队列，造成重复访问

**出错**：① 没有加 `while q:` 没有把所有的岛屿都找完

② 加入四个方向的循环中，写成了 `grid[i][j] == '1'`

---

### 994 腐烂的橘子

在给定的 `m × n` 网格 `grid` 中，每个单元格可以有以下三个值之一：

- 值 `0` 代表空单元格
- 值 `1` 代表新鲜橘子
- 值 `2` 代表腐烂的橘子

每分钟，腐烂的橘子 **周围 4 个方向上相邻** 的新鲜橘子都会腐烂

返回 *直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 `-1`*

```
输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
输出：4
输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
输出：-1
解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个方向上。
输入：grid = [[0,2]]
输出：0
解释：因为 0 分钟时已经没有新鲜橘子了，所以答案就是 0 。
```

```
1 <= m, n <= 10
grid[i][j] 仅为 0、1 或 2
```

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        q = deque()
        fresh = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh += 1
                elif grid[i][j] == 2:
                    q.append((i, j))

        if fresh == 0:
            return 0
        minutes = 0

        while q and fresh > 0:
            q_len = len(q)
            for _ in range(q_len):
                r, c = q.popleft()  # 注意是popleft()，不是pop()
                for dr, dc in directions:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr <= m - 1 and 0 <= nc <= n - 1 and grid[nr][nc] == 1:
                        fresh -= 1
                        grid[nr][nc] = 2
                        q.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1
```

*与题200：岛屿数量，解法相同*，也用BFS，但要同时把所有 `1` 都放进去

- 循环用 q、fresh 两个条件的原因

  - 如果只写 `while q`

    可能所有橘子已经腐烂了，但由于 q 中还有元素，所以还会多跑一轮去清空。`minutes` 会多加一次。是

  - 如果只写 `while fresh > 0`

    在情况 `2 0 1` 中，有新鲜橘子，但它永远接触不到腐烂橘子，会**死循环**

**出错**：① 最后return没有考虑 fresh =0 的情况

② 1 2 写成了 `'1'`、`'2'`

③ 漏加 `fresh -= 1`

---

### 207 课程表

你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1`

在选修某些课程之前需要一些先修课程。 先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [ai, bi]`，表示如果要学习课程 `ai` 则 **必须** 先学习课程 `bi`

- 例如，先修课程对 `[0, 1]` 表示：想要学习课程 `0` ，你需要先完成课程 `1`

请你判断是否可能完成所有课程的学习？如果可以，返回 `true` ；否则，返回 `false`

```
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
```

```
1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= a_i, b_i < numCourses
prerequisites[i] 中的所有课程对 互不相同
```

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        indegree = [0] * numCourses
        graph = [[] for _ in range(numCourses) ]

        for x,y in prerequisites: #(x,y) y -> x
            indegree[x] += 1
            graph[y].append(x)
        
        q = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                q.append(i)
        
        count = 0
        while q:
            cur_node = q.popleft()
            count += 1
            for next_node in graph[cur_node]:
                indegree[next_node] -= 1
                if indegree[next_node] == 0:
                    q.append(next_node)
        return count == numCourses
```

- 有向图的拓扑排序（Kahn算法）

- 符号

  $(x,y)$ 表示 $y \rightarrow x$，课程 $x$ 的前置课程为 $y$。这样形成了一条有向的边 $(y,x)$

  `graph[y]` 表示：从节点 $y$ 出发能到达的所有节点。即
  $$
  graph[y] = \{ \text{所有把 $y$ 作为前置课程的课程}\}
  $$
  `indegree[i]` = 节点 $i$ 的入边数量 = 有多少前置课程

- 原理

  ```python
  for x, y in prerequisites:  # y -> x
  ```

  表示：想学课程 `x`，必须先学课程 `y`

  后面 `while q` 的部分，每次从队列里取出一个课程，并将其 “学掉”。如果所有的课程都能被学掉，就说明

- 例子

  假设依赖关系为

  ```
  0 -> 1
  1 -> 0
  ```

  此时 `prerequisites = [[1, 0], [0, 1]]`，`indegree = [1, 1]`，在下述代码中

  ```python
  q = deque()
  for i in range(numCourses):
      if indegree[i] == 0:
          q.append(i)
  ```

  并不能找到入度为 0 的点（也即无需任何前置课程的店），因此返回时，`return count == numCourses` 判断的是 `0 == 2`，为 `False`

  如果依赖关系为

  ```
  0 -> 1
  1 -> 0
  2 -> 1
  ```

  此时

  ```python
  indegree[0] = 1
  indegree[1] = 2
  indegree[2] = 0
  ```

  只有课程 2 是可以学的。最后返回时是 `1 == 3`，为 `False`

---

### 208 实现 Trie (前缀树)  

Trie（发音类似 "try"）或者说 **前缀树** 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查

请你实现 Trie 类：

- `Trie()` 初始化前缀树对象
- `void insert(String word)` 向前缀树中插入字符串 `word`
- `boolean search(String word)` 如果字符串 `word`在前缀树中，返回 `true`（即，在检索之前已经插入）；否则，返回 `false`
- `boolean startsWith(String prefix)` 如果之前已经插入的字符串 `word` 的前缀之一为 `prefix` ，返回 `true` ；否则，返回 `false`

```
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]
```

```
1 <= word.length, prefix.length <= 2000
word 和 prefix 仅由小写英文字母组成
insert、search 和 startsWith 调用次数 总计 不超过 3 * 10^4 次
```

```python
class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
        
class TrieNode():
    def __init__(self):
        self.children = {}
        self.is_end = False

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```



## 回溯

### 46 全排列

给定一个不含重复数字的数组 `nums` ，返回其 *所有可能的全排列* 。你可以 **按任意顺序** 返回答案

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
输入：nums = [0,1]
输出：[[0,1],[1,0]]
输入：nums = [1]
输出：[[1]]
```

```
1 <= nums.length <= 6
-10 <= nums[i] <= 10
nums 中的所有整数 互不相同
```

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        path = []
        def backtrack():
            if len(path) == n:
                ans.append(path[:])
                return
            for num in nums:
                if num in path:
                    continue
                path.append(num)
                backtrack() # 看一下加进来num行不行
                path.pop() # 看完了，该删掉num，看下一个num加进来怎么样
        
        backtrack()
        return ans
```

---

### 78 子集

给你一个整数数组 `nums` ，数组中的元素 **互不相同** 。返回该数组所有可能的子集（幂集）

解集 **不能** 包含重复的子集。你可以按 **任意顺序** 返回解集

```
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
输入：nums = [0]
输出：[[],[0]]
```

```
1 <= nums.length <= 10
-10 <= nums[i] <= 10
nums 中的所有元素 互不相同
```

本题标准解法的时间复杂度是 $O(n2^n)$

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        path = []
        def backtrack(start):
            ans.append(path[:])
            for i in range(start,n): # 以num[i]开头的子集
                path.append(nums[i]) # 首先应当要有nums[i]
                backtrack(i+1)
                path.pop() # 撤销
                
        backtrack(0)
        return ans 
```

- `backtrack(start)` 定义

  当前 `path` **已经是一个合法子集**，接下来只能从下标 $[start, n-1]$ 中继续选择元素

  `start` 表示下一次可选择元素的 **起始下标**

**法2**，时间复杂度 $O(n2^n)$，可通过

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        def backtrack(path, i): # 准备加入或不加入的下标为i
            if i == n:
                ans.append(path[:])
                return

            path.append(nums[i])
            backtrack(path, i+1)
            path.pop()

            backtrack(path, i+1)
        
        backtrack([], 0)
        return ans
```

- 时间复杂度 $O(n2^n)$

  一共有 $2^n$ 个子集，`ans.append(path[:])`，单次复制为 $O(n)$，故为 $O(n2^n)$

- backtrack 定义

  当前已经确定了前 $i$ 个元素是否选入子集

  `path` 保存当前已经选中的元素

  现在需要决定下标为 `i` 的元素选 or 不选

---

### 17 电话号码的字母组合

给定一个仅包含数字 `2-9` 的字符串，返回所有它能表示的字母组合。答案可以按 **任意顺序** 返回

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母

```
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
输入：digits = "2"
输出：["a","b","c"]
```

```
1 <= digits.length <= 4
digits[i] 是范围 ['2', '9'] 的一个数字。
```

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        n = len(digits)
        
        mp = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz"
        }

        ans = []
        path = []

        def backtrack(i):  # i表示准备确定的答案的下标
            if i == n:
                ans.append("".join(path[:]))
                return

            letters = mp[digits[i]]

            for ch in letters:
                path.append(ch)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return ans
```

- `backtrack(i)` 定义

  当前正在确定**结果字符串**中下标 $i$ 的字符（即有效答案的下标 $i$ 处）

- 用 `i == n` 记录答案的原因

  在执行 `backtrack(i + 1)` 时，若当前 $i=n-1$，那么在进入下一层递归之前，已经将最后一个字符加到了 `path`

  此时 backtrack 中，输入的参数为 $n$，而不是 $n-1$

**出错**：① `index == n` 写成 `index == n-1`，当最后一个字符被加入时，执行的是 `path.append(ch)`，此时再执行 `backtrack(index + 1)`，`path` 中是有 $n+1$ 个元素

② 如果 mp 中key用的是整数，那么后面的 `letters = mp[digits[index]]` 中要加 `int` 转为整数

---

### 39 组合总和

给你一个 **无重复元素** 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 **不同组合** ，并以列表形式返回。你可以按 **任意顺序** 返回这些组合

`candidates` 中的 **同一个** 数字可以 **无限制重复被选取** 。如果至少一个数字的被选数量不同，则两种组合是不同的

对于给定的输入，保证和为 `target` 的不同组合数少于 150 个

```
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]
输入: candidates = [2], target = 1
输出: []
```

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = []
        path = []
        n = len(candidates)
        def backtrack(i, total):
            if total == target:
                ans.append(path[:])
                return 
            if i >= n or total > target:
                return 

            # choice 1
            path.append(candidates[i])
            backtrack(i,total + candidates[i])
            path.pop()

            # choice 2
            backtrack(i+1,total)
        backtrack(0, 0)
        return ans 
```

backtrack 中 `i` 的定义：正在考虑第 $i$ 个元素

递归的分类是选与不选

`ans.append(path[:])` 中 `path[:]` 就是在拷贝一份新的数组放在 ans 中，后续对 path 的修改不会影响到 ans

---

### 22 括号生成

数字 `n` 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 **有效的** 括号组合

```
输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
输入：n = 1
输出：["()"]
```

```
1 <= n <= 8
```

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []
        def backtrack(left, right, path):
            if left == n and right == n:
                ans.append("".join(path))
                return 
            if left > n or right > left:
                return 
            
            path.append('(')
            backtrack(left + 1, right, path)
            path.pop()

            path.append(')')
            backtrack(left, right + 1, path)
            path.pop()
            
        backtrack(0, 0, [])
        return ans
```

- backtrack 无需维护 **已有符号个数** `i`

  如 `backtrack(left, right, i, path)`
  
  由于 `if left > n or right > left`，自然有
  $$
  \text{left} \leq n, \quad \text{right} \leq \text{left} \leq n
  $$
  因此无需控制 $i \leq 2n$

  不过下面这样也是可以通过的：
  
  ```python
  def backtrack(left, right, i, path):
      if left == n and right == n:
          ans.append("".join(path))
          return 
      if right > left or i >= 2*n: # 看这里
          return
  ```
  

---

### 79 单词搜索

给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word`。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false`

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用

**进阶：**你可以使用搜索剪枝的技术来优化解决方案，使其在 `board` 更大的情况下可以更快解决问题？

<img src="Leetcode 解法笔记.assets/word2.jpg" alt="word2" style="zoom:65%;" />

```
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCCED"
输出：true
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "SEE"
输出：true
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCB"
输出：false
```

```
m = board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board 和 word 仅由大小写英文字母组成
```

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])
        
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        visited = [[False]*n for _ in range(m)]
        
        def backtrack(i, j, k):
            if k == len(word):
                return True
            if i<0 or i>= m or j<0 or j>= n or visited[i][j] or board[i][j] != word[k]: # 第k+1个字符，在word中的写法是word[k]
                return False 

            visited[i][j] = True

            for dx,dy in directions:
                if backtrack(i+dx,j+dy,k+1):
                    return True
            
            visited[i][j] = False # 撤回

            return False # 本身和上下左右都找不到

        for i in range(m):
            for j in range(n):
                if backtrack(i,j,0):
                    return True
        return False
```

剪枝：越界、已访问过、当前字符不等于 `word[k]`

- `backtrack(i,j,k)` 的定义

  当前已经匹配成功 $k$ 个字符的情况下，从 $(i,j)$ 出发，去匹配第 $k+1$ 个字符 **直至结束**，是否能够成功

  由于已经考虑了匹配到底，所以在 `for dx,dy in directions:` 的循环中，一旦有 True 的就可以返回

---

### 131 分割回文串

给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 **回文串** 。返回 `s` 所有可能的分割方案

```
输入：s = "aab"
输出：[["a","a","b"],["aa","b"]]
输入：s = "a"
输出：[["a"]]
```

```
1 <= s.length <= 16
s 仅由小写英文字母组成
```

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        def is_sym(left,right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        ans = []
        path = []
        def backtrack(i): #本次切片的起始下标为i
            if i == n:
                ans.append(path.copy())
                return 
            for end in range(i,n):
                if is_sym(i,end):
                    path.append(s[i:end+1])
                    backtrack(end+1)
                    path.pop()
        backtrack(0)
        return ans
```

- `if i == n:` 用 $n$ 而非 $n-1$ 的原因

  `i` 表示**本次切片的起始下标**

  当已经把字符串全部切完时 `end = 1`，下一次切片的起始位置应该是 $end +1$，即 $n$，已经越过了最后一个字符

---

### 51 N 皇后

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子

**n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n×n` 的棋盘上，并且使皇后彼此之间不能相互攻击

给你一个整数 `n` ，返回所有不同的 **n 皇后问题** 的解决方案

每一种解法包含一个不同的 **n 皇后问题** 的棋子放置方案，该方案中 `'Q'` 和 `'.'` 分别代表了皇后和空位

```
输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
输入：n = 1
输出：[["Q"]]
```

```
1 <= n <= 9
```

```python
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        board = [['.'] * n for _ in range(n)]
        ans = []
        cols = set() # 出现过的列
        diag1 = set() # 主对角线 row - col
        diag2 = set() # 副对角线 row + col

        def backtrack(row): # 现在准备把皇后放在第 row 行（还没有放）
            if row == n: # 0 ~ n-1 都放好了
                ans.append(["".join(board[i]) for i in range(n)])
            
            for col in range(n): # 准备放在(row,col)处
                if col in cols or row-col in diag1 or row+col in diag2:
                    continue
                # 现在这是合法的位置了

                board[row][col] = 'Q'

                cols.add(col)
                diag1.add(row-col)
                diag2.add(row+col)
                backtrack(row+1)
        
                board[row][col] = '.' # 撤销
                cols.remove(col)
                diag1.remove(row-col)
                diag2.remove(row+col)

        backtrack(0)
        return ans
```

对角线约束：
$$
\begin{cases}
x - y = c_1 \quad (\text{主对角线}) \\
x + y = c_2 \quad (\text{副对角线})
\end{cases}
$$
每一种 $c_1,c_2$ 就分别代表了一种主、副对角线

row - col 控制 ↘ 方向，row + col 控制 ↙ 方向

**出错**：漏了递归 `backtrack(row+1)`



## 二分查找

### 35 搜索插入位置

**左边界搜索**

**左闭右开 $[a,b)$ 写法**：我现在主要用这个

```python
def lower_bound(nums, target) -> int:
    left = 0
    right = len(nums) # 取满，因右端点是开的，不满足题意的

    while left < right:  # 没有等号
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

本程序的目标是求：
$$
\min \{ i \mid \text{nums}[i] \geq \text{target} \}
$$
维护区间 $[\text{left},\text{right})$

> 找的是第一个 $\geq \text{target}$ 的位置

- `if nums[mid] < target` 设置的原因：

  目的是：找到**第一个** $\geq$ target 的位置

  这里在考察 `mid` 是否为可能满足这个要求的位置
  
  如果考虑不满足的情形，上式就要改为 $<$，因此将 `left` 取为 `mid + 1`

- 用 Python 内置函数

  ```python
  import bisect
  return bisect.bisect_left(nums, target)
  ```

**出错**：将 `right` 写成 `n - 1`

**解法 2**：闭区间 $[a,b]$ 写法

```python
def lower_bound(nums, target) -> int:
    left = 0
    right = len(nums) - 1
    while left <= right:  # 区间不为空
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1  # 范围缩小到 [mid+1, right]
        else:
            right = mid - 1  # 范围缩小到 [left, mid-1]
    return left
```

`right = mid - 1` ：虽然else中的mid可能包含答案，极端情况下（两数相同）left会+1，可以回到上次去掉的mid

---

### 240 搜索二维矩阵 II

编写一个高效的算法来搜索 `m × n` 矩阵 `matrix` 中的一个目标值 `target` 。该矩阵具有以下特性：

- 每行的元素从左到右升序排列
- 每列的元素从上到下升序排列

例：
$$
\begin{array}{|c|c|c|c|c|}
\hline
1 & 4 & 7 & 11 & 15 \\
\hline
2 & \mathbf{5} & 8 & 12 & 19 \\
\hline
3 & 6 & 9 & 16 & 22 \\
\hline
10 & 13 & 14 & 17 & 24 \\
\hline
18 & 21 & 23 & 26 & 30 \\
\hline
\end{array}
$$

```
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true
输入：同上，但 target = 20
输出：false
```

注：题35的应用

```python
class Solution(object):
    def searchMatrix(self, matrix, target):
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            idx_j = self._lower_bound(matrix[i], target) # _lower_bound要自己写
            if idx_j < n and matrix[i][idx_j] == target:
                return True
        return False
```

逐行应用左边界搜索二分查找就可以了

二分查找由于是独立的函数，`def _lower_bound(self, nums, target):` 要加 `self`

---

### 74 搜索二维矩阵

给你一个满足下述两条属性的 `m × n` 整数矩阵：

- 每行中的整数从左到右按非严格递增顺序排列
- 每行的第一个整数大于前一行的最后一个整数

给你一个整数 `target` ，如果 `target` 在矩阵中，返回 `true`；否则，返回 `false`

例：
$$
\begin{array}{|c|c|c|c|}
\hline
1 & \mathbf{3} & 5 & 7 \\
\hline
10 & 11 & 16 & 20 \\
\hline
23 & 30 & 34 & 60 \\
\hline
\end{array}
$$

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true
输入：同上，但 target = 13
输出：false
```

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        left = 0
        right = m * n
        
        while left < right:
            mid = (left + right) // 2
            val = matrix[mid // n][mid % n] # 列是关键
            
            if val < target:
                left = mid + 1
            else:
                right = mid
        if left < m * n and matrix[left // n][left % n] == target:
            return True
        return False
```

考虑区间 $[0,mn)$

只是每次的 val 要回到矩阵去提取，但是整体已经和“行向量”的效果是相同的了

`left < m * n` 同问题240中的 `idx < len(n)`

**出错**：`matrix[mid // n][mid % n]` 漏写 `matrix`

---

### 34 在排序数组中查找元素的第一个和最后一个位置

给你一个按照非递减顺序排列的整数数组 `nums`，和一个目标值 `target`。请你找出给定目标值在数组中的开始位置和结束位置

如果数组中不存在目标值 `target`，返回 `[-1, -1]`

你必须设计并实现时间复杂度为 $O(\log n)$ 的算法解决此问题

> 自注：（可以不严格）的单调递增

```
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
输入：nums = [], target = 0
输出：[-1,-1]
```

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        import bisect
        n = len(nums)
        i = bisect.bisect_left(nums, target)
        if i == n or nums[i] != target:
            return [-1, -1]
        else:
            j = bisect.bisect_left(nums, target + 1)
            return [i, j - 1]
```

---

### 33 搜索旋转排序数组

整数数组 `nums` 按**升序** （严格增） 排列，数组中的值 **互不相同**

在传递给函数之前，`nums` 在预先未知的某个下标 `k`（`0 <= k < nums.length`）上进行了 **向左旋转**，使数组变为 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`（下标 **从 0 开始**计数）。例如， `[0,1,2,4,5,6,7]` 下标 `3` 上向左旋转后可能变为 `[4,5,6,7,0,1,2]`

给你 **旋转后** 的数组 `nums` 和一个整数 `target` ，如果 `nums` 中存在这个目标值 `target` ，则返回它的下标，否则返回 `-1`

你必须设计一个时间复杂度为 $O(\log n)$ 的算法解决此问题

> 自注：即向左移动 $k$ 次

```
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
输入：nums = [1], target = 0
输出：-1
```

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left = 0
        right = n

        while left < right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[0] <= nums[mid]:
                if nums[0] <= target < nums[mid]:
                    right = mid
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[n - 1]: 
                    left = mid + 1
                else:
                    right = mid
        return -1
```

- 思路

  对 `nums[mid]` 的取值进行分类讨论，要判断完整的一边在哪里

- 左开右闭

  作为二分查找的问题，统一用左开右闭。因此 `right = n`

---

### 153 寻找旋转排序数组中的最小值

已知一个长度为 `n` 的数组，预先按照**升序**排列，经由 `1` 到 `n`次 **旋转** 后，得到输入数组。例如，原数组 `nums = [0,1,2,4,5,6,7]` 在变化后可能得到：

- 若旋转 `4` 次，则可以得到 `[4,5,6,7,0,1,2]`
- 若旋转 `7` 次，则可以得到 `[0,1,2,4,5,6,7]`

注意，数组 `[a[0], a[1], a[2], ..., a[n-1]]` **旋转一次** 的结果为数组 `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`

给你一个元素值 **互不相同** 的数组 `nums` ，它原来是一个升序排列的数组，并按上述情形进行了多次旋转。请你找出并返回数组中的 **最小元素**

你必须设计一个时间复杂度为 $O(\log n)$ 的算法解决此问题

> 自注：
>
> - 严格单调递增
> - 向右移动 $k$ 次（$k$ 未知）

```
输入：nums = [3,4,5,1,2]
输出：1
输入：nums = [4,5,6,7,0,1,2]
输出：0
输入：nums = [11,13,15,17]
输出：11
```

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        n = len(nums)
        left = 0
        right = n
        if nums[0] <= nums[-1]:
            return nums[0]

        while left < right:
            mid = (left+right) // 2
            if nums[mid] >= nums[0]:
                left = mid+1
            else:
                right = mid
        return nums[left]
```

- 算法思想

  本质：找第一个小于 `nums[0]` 的位置。因此如果没有旋转，是不存在这样的位置的

- 特判单调的原因

  如果一开始不特判单调，对于下述例子：

  ```python
  nums = [0, 1, 2, 4, 5, 6, 7]
  ```

  条件 `if nums[mid] >= nums[0]` 会一直满足，最后 `left = right = n`

  因此也可以不特判单调，但是最后 return 需要改为

  ```python
  return nums[left] if left < n else nums[0]
  ```

---

### 4 寻找两个正序数组的中位数

给定两个大小分别为 `m` 和 `n` 的正序（从小到大）数组 `nums1`和 `nums2`。请你找出并返回这两个正序数组的 **中位数**

算法的时间复杂度应该为 $O(\log (m+ n))$

```
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
```

```
nums1.length == m, nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-10^6 <= nums1[i], nums2[i] <= 10^6
```

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        n1 = len(nums1)
        n2 = len(nums2)
        k = (n1 + n2 + 1) // 2 # 左边需要的元素个数
        if n1 > n2:
            return self.findMedianSortedArrays(nums2, nums1)
        left = 0
        right = n1
        while left<right:
            m1 = (left + right) // 2
            m2 = k - m1
            if nums1[m1] < nums2[m2-1]:
                left = m1+1
            else:
                right = m1
        m1 = left
        m2 = k - left
        left_max = max(
            nums1[m1-1] if m1 > 0 else float('-inf'),
            nums2[m2-1] if m2 > 0 else float('-inf')
        )
        if (n1 + n2) % 2 == 1: # 奇数情况，左侧会多
            return left_max
        else:
            right_min = min(
                nums1[m1] if m1 < n1 else float('inf'),
                nums2[m2] if m2 < n2 else float('inf')
            )
            return (left_max + right_min)/2
```

- `nums2[m2 - 1]` 不会越界

  二分法可知 $0 \leq m_1 \leq n_1-1$，由于 $m_2 = k-m_1$，则
  $$
  k-n_1 \leq m_2-1 \leq k-1
  $$

  $$
  k=\left\lfloor \frac{n_1+n_2+1}{2}\right\rfloor
  \ge
  \left\lfloor \frac{n_1+n_1+1}{2}\right\rfloor
  =\left\lfloor n_1 + \frac12\right\rfloor=n_1
  $$

  $$
  k=\left\lfloor \frac{n_1+n_2+1}{2}\right\rfloor
  \le
  \left\lfloor \frac{n_2+n_2+1}{2}\right\rfloor
  =
  \left\lfloor n_2+\frac12 \right\rfloor
  =
  n_2
  $$

  故
  $$
  0 \leq m_2-1 \leq n_2 -1
  $$
  因此 `nums2[m2-1]` 数组的索引是安全的

最后输出的时候要注意边界情况

本题不算难，主要是记住

- `k = (n1 + n2 + 1) // 2`
- 控制 $n_1 \leq n_2$
- 二分法中用 $nums_1[m_1] < nums_2[m_2 - 1]$ 判断不对的情况

**出错**：最后可以直接输出 `left_max` 的是 $n_1 + n_2$ 为奇数的情况



## 栈

### 20 有效的括号

给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s` ，判断字符串是否有效

有效字符串需满足：

1. 左括号必须用**相同类型**的右括号闭合
2. 左括号必须以正确的顺序闭合
3. 每个右括号都有一个对应的相同类型的左括号

```
输入：s = "()"
输出：true
输入：s = "()[]{}"
输出：true
输入：s = "(]"
输出：false
输入：s = "([])"
输出：true
输入：s = "([)]"
输出：false
```

```python
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:
            return False

        mp = {
            ")" : "(",
            "]" : "[",
            "}": "{",
        }

        stack = []
        for ch in s:
            if ch in mp: 
                if not stack or stack[-1] != mp[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)
				
        return not stack
```

- 返回

  需要判断此时栈是否为空。在例子 `s = "["` 中，如果不判断输出 `True`，其实应为 `False`

  `return not stack` 也可以写成：

  ```python
  return True if stack == [] else False
  ```

- `if not stack or stack[-1] != mp[ch]:`

  碰到右括号时，我们需要和左括号消消乐

  前半部分的条件用于防御 `stack[-1]` 提取不出来的情况

---

### 155 最小栈

设计一个支持 `push` ，`pop` ，`top` 操作，并能在**常数时间**内**检索到最小元素**的栈

实现 `MinStack` 类:

- `MinStack()` 初始化堆栈对象
- `void push(int value)` 将元素 `value` 推入堆栈
- `void pop()` 删除堆栈顶部的元素
- `int top()` 获取堆栈顶部的元素
- `int getMin()` 获取堆栈中的最小元素

```
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
输出：
[null,null,null,null,-3,null,0,-2]
```

```
-2^31 <= val <= 2^31 - 1
pop、top 和 getMin 操作总是在 非空栈 上调用
push, pop, top, and getMin最多被调用 3 * 10^4 次
```

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(self.min_stack[-1], val))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

**出错**：栈顶用的是 [-1] 而不是 [0]

---

### 394 字符串解码

给定一个经过编码的字符串，返回它解码后的字符串

编码规则为: `k[encoded_string]`，表示其中方括号内部的 `encoded_string` 正好重复 `k` 次。注意 `k` 保证为正整数

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 `k` ，例如不会出现像 `3a` 或 `2[4]` 的输入

测试用例保证输出的长度不会超过 `10^5`

```
输入：s = "3[a]2[bc]"
输出："aaabcbc"
输入：s = "3[a2[c]]"
输出："accaccacc"
输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"
```

```
1 <= s.length <= 30
s 由小写英文字母、数字和方括号 '[]' 组成
s 保证是一个 有效 的输入。
s 中所有整数的取值范围为 [1, 300] 
```

```python
class Solution:
    def decodeString(self, s: str) -> str:
        cur_num = 0
        cur_str = ""
        stack = []

        for ch in s:
            if ch.isdigit(): # 注意写法
                cur_num = cur_num*10 + int(ch)
            elif ch == '[':
                stack.append((cur_str, cur_num))
                cur_num = 0
                cur_str = ""
            elif ch == ']':
                pre_str, times = stack.pop()
                cur_str = pre_str + times * cur_str
            else:
                cur_str = cur_str + ch
        return cur_str
```

`cur_str` 表示当前这一层正在构建的字符串

---

### 739 每日温度

给定一个整数数组 `temperatures` ，表示每天的温度，返回一个数组 `answer` ，其中 `answer[i]` 是指对于第 `i` 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 `0` 来代替

```
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]
输入: temperatures = [30,60,90]
输出: [1,1,0]
```

```
1 <= temperatures.length <= 10^5
30 <= temperatures[i] <= 100
```

- 单调栈

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        stack = [] # 压入还没有找到更热天气的日期下标
        ans = [0] * n
        
        for i in range(n):
            while stack and temperatures[stack[-1]] < temperatures[i]:
                j = stack.pop()
                ans[j] = i-j
            stack.append(i)
        return ans
```

**出错**：`stack` 写成了 `not stack`，原本是希望非空的，现在变成了如果空才执行

**法2**：暴力双循环

时间 $O(n^2)$

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        for i in range(n):
            for j in range(i+1,n):
                if temperatures[j] > temperatures[i]:
                    ans[i] = j-i
                    break
        return ans
```

---

### 84 柱状图中最大的矩形

给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 

求在该柱状图中，能够勾勒出来的矩形的最大面积

```
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
输入： heights = [2,4]
输出： 4
```

```
1 <= heights.length <=10^5
0 <= heights[i] <= 10^4
```

*算例、说明，见 notability*

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights = [0] + heights + [0]
        n = len(heights)
        ans = 0
        stack = []
        for i in range(n):
            while stack and heights[stack[-1]] > heights[i]:
                j = stack.pop()
                ans = max(ans, (i-stack[-1]-1)*heights[j])
            stack.append(i)
        return ans
```

- 栈里存的是**下标**，并且这些下标对应的高度满足单调增（但不用严格）

- 核心计算 `(i-stack[-1]-1)*heights[j]` 说明

  当下标 `j` 被弹出时，说明当前柱子 `i` 的高度小于 `heights[j]`，因此 `i` 是 `j` 右侧第一个比它矮的位置

  弹出 `j` 后，新的栈顶 `stack[-1]` 是 `j` 左侧最近的一个高度 $\leq$ `heights[j]` 的位置

  如果高度相等，**这次** 不会把它纳入 `j` 的宽度中，但 while 还会继续执行，轮到该相等高度的柱子弹出时，能计算出更大的宽度

  因此，以 `heights[j]` 为高度时，当前可确定的矩形横向范围是 `(stack[-1], i)`，不包含两端，其宽度为
  $$
  i - stack[-1] - 1
  $$

出错：`ans` 不能预设为 `float('-inf')`。在测试用例 `heights = [0]` 中，会输出 null，但实际应该是 0

---

### 32 最长有效括号

给你一个只包含 `'('` 和 `')'` 的字符串，找出最长有效（格式正确且连续）括号 子串 的长度

左右括号匹配，即每个左括号都有对应的右括号将其闭合的字符串是格式正确的，比如 `"(()())"`

```
输入：s = "(()"
输出：2
输入：s = ")()())"
输出：4
输入：s = ""
输出：0
```

```
0 <= s.length <= 3 * 10^4
s[i] 为 '(' 或 ')'
```

本来在 hot 100 中是动态规划，但这里我们用**栈**来解

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        stack = [-1] # 存的是s中的下标
        ans = 0
        for i in range(n):
            if s[i] == '(':
                stack.append(i) # 登记进去了一个要消除的下标
            else:
                stack.pop()
                if stack == []:
                    stack.append(i)
                else:
                    ans = max(ans, i - stack[-1])
        return ans
```

- `stack` 的定义

  当前还没有被匹配掉的括号的下标（栈底为边界）

  遇到 `'('` 时，把它的下标压栈，表示“这个左括号还在等待匹配”

  `stack = [-1]`：$-1$ 是最后一个无法参与匹配的位置，相当“边界”

  比如第一个是 `)`，和下标 -1 匹配掉后，这是一个无法匹配的边界，所以要马上把当前的 `i` 加入



## 堆

### 215 数组中的第K个最大元素

给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素

请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素

你必须设计并实现时间复杂度为 $O(n)$ 的算法解决此问题

```
输入: [3,2,1,5,6,4], k = 2
输出: 5
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
```

```
1 <= k <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
```

暴力解法，时间 $O(n \log n)$

**解法**：最小堆

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            heapq.heappush(heap, num)

            if len(heap) >= k+1:
                heapq.heappop(heap)
        return heap[0]
```

时刻维护 $k$ 个目前遇到的最大元素，堆顶是这 $k$ 个元素中最小的

如果要比较堆顶元素，可以写成

```python
for num in nums:
    if len(heap) < k:
        heapq.heappush(heap, num)
    elif num > heap[0]:
        heapq.heapreplace(heap, num)
```

首先堆要放够 $k$ 个元素，才可以开始维护 

---

### 347 前 K 个高频元素

给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案

```
输入：nums = [1,1,1,2,2,3], k = 2
输出：[1,2]
输入：nums = [1], k = 1
输出：[1]
输入：nums = [1,2,1,2,1,2,3,1,3,2], k = 2
输出：[1,2]
```

```
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
k 的取值范围是 [1, 数组中不相同的元素的个数]
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的
```

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        mp = {} # 元素频率
        for num in nums:
            mp[num] = mp.get(num,0) + 1
        
        heap = []
        for num, freq in mp.items():
            heapq.heappush(heap, (freq, num))

            if len(heap) > k:
                heapq.heappop(heap)
        return [num for _,num in heap]
```

**出错**：`for num, freq in mp.items():` 写成了 `for i in range(n):`，这样会重复入堆

解法2：（可以通过）

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        from collections import Counter
        count = Counter(nums)
        count_arr = []
        for num,freq in count.items():
            count_arr.append((freq, num))
        count_sort = sorted(count_arr, key = lambda p:p[0], reverse= True)
        # 先是freq，然后是数字
        count_sort_k = count_sort[:k]
        ans = []
        for _,num in count_sort_k:
            ans.append(num)
        return ans
```

---

### 295 数据流的中位数

**中位数**是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值

- 例如 `arr = [2,3,4]` 的中位数是 `3` 
- 例如 `arr = [2,3]` 的中位数是 `(2 + 3) / 2 = 2.5`

实现 MedianFinder 类:

- `MedianFinder()` 初始化 `MedianFinder` 对象
- `void addNum(int num)` 将数据流中的整数 `num` 添加到数据结构中
- `double findMedian()` 返回到目前为止所有元素的中位数。与实际答案相差 `10-5` 以内的答案将被接受

```
输入
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
输出
[null, null, null, 1.5, null, 2.0]
```

```python
class MedianFinder:

    def __init__(self):
        self.small = [] # 大根堆
        self.large = [] # 小根堆

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small): # small >= large
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        else:
            return (-self.small[0] + self.large[0]) / 2
```

- 看起来“每次都进 large”

  实际上每次都会竞争一次，每次有新的元素时，先暂时归类为 small，small 中较大的那个会被送到 large，一般（有时候可能不送回，保持 $len(small) \geq len(large)$）大的又会送回一个数到 small

  

## 贪心算法

### 121 买卖股票的最佳时机

给定一个数组 `prices` ，它的第 `i` 个元素 `prices[i]` 表示一支给定股票第 `i` 天的价格

你只能选择 **某一天** 买入这只股票，并选择在 **未来的某一个不同的日子** 卖出该股票。设计一个算法来计算你所能获取的最大利润

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 `0` 

```
输入：[7,1,5,3,6,4]
输出：5
输入：prices = [7,6,4,3,1]
输出：0
```

```
1 <= prices.length <= 10^5
0 <= prices[i] <= 10^4
```

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = prices[0]
        n = len(prices)
        ans = 0
        for i in range(n):
            ans = max(ans, prices[i] - min_price)
            if prices[i] < min_price:
                min_price = prices[i]
        return ans
```

要维护一个历史出现过的最低价

时间复杂度：$O(n)$

空间复杂度：$O(1)$

---

### 55 跳跃游戏

给你一个非负整数数组 `nums` ，你最初位于数组的 **第一个下标** 。数组中的每个元素代表你在该位置可以跳跃的最大长度

判断你是否能够到达最后一个下标，如果可以，返回 `true` ；否则，返回 `false`

```
输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。
```

```
1 <= nums.length <= 10^4
0 <= nums[i] <= 10^5
```

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_pos = 0
        n = len(nums)
        for i,jump in enumerate(nums): # 最后一个位置也是要验证的，因为如果 n-1 > max_pos的话，也还是False的，说明这个位置到不了
            if i > max_pos:
                return False
            max_pos = max (max_pos, i + jump)

            if max_pos >= n-1:
                return True
        return True
```

在算法迭代过程中始终维护一个能跳到的最远距离

---

### 45 跳跃游戏 II

给定一个长度为 `n` 的 **0 索引** 整数数组 `nums`。初始位置在下标 0

每个元素 `nums[i]` 表示从索引 `i` 向后跳转的最大长度。换句话说，如果你在索引 `i` 处，你可以跳转到任意 `(i + j)` 处：

- `0 <= j <= nums[i]` 且
- `i + j < n`

返回到达 `n - 1` 的最小跳跃次数。测试用例保证可以到达 `n - 1`

```
输入: nums = [2,3,1,1,4]
输出: 2
输入: nums = [2,3,0,1,4]
输出: 2
```

```
1 <= nums.length <= 10^4
0 <= nums[i] <= 1000
```

题目要求“测试用例保证可以到达 `n - 1`”，主要是为了专注于解决跳多少次的问题，本身即使无法到达，贪心算法也是正确的

```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        end = 0
        max_pos = 0
        jump = 0
        for i in range(n-1): # 最后一个不用看了，如果能跳到这里，就没必要再把jump+1
            max_pos = max(max_pos,i + nums[i])
            if i == end: # 要开始更新新一轮的边界了
                end = max_pos
                jump += 1
        return jump
```

当 `i = n-1` 时，应当开始统计 `jump` 的数量了，所以 return

先看 `max_pos` 再看 `jump` 是合理的，一开始 0 位置时，确实也没有跳

在下标 0 处肯定会被算1次，本次的范围就是 nums[0]

---

### 763 划分字母区间

给你一个字符串 `s`。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。例如，字符串 `"ababcc"` 能够被分为 `["abab", "cc"]`，但类似 `["aba", "bcc"]` 或 `["ab", "ab", "cc"]` 的划分是非法的

注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是 `s`

返回一个表示每个字符串片段的长度的列表

```
输入：s = "ababcbacadefegdehijhklij"
输出：[9,7,8]
输入：s = "eccbbbbdec"
输出：[10]
```

```
1 <= s.length <= 500
s 仅由小写英文字母组成
```

```python
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        # 每个字符最后出现的位置，一开始完全统计好
        ch_right = {ch:i for i,ch in enumerate(s)} # {字符 : 预先统计最后出现的位置}
        ans = []
        seg_len = 0
        max_right = 0
        
        for i,ch in enumerate(s):
            seg_len += 1
            max_right = max(max_right, ch_right[ch])
            if i == max_right:
                ans.append(seg_len)
                seg_len = 0
        return ans
```

贪心在于：每次出现一个字符，这一块的右端点就马上更新到这个字符处

---



## 动态规划

### 70 爬楼梯

假设你正在爬楼梯。需要 `n` 阶你才能到达楼顶

每次你可以爬 `1` 或 `2` 个台阶。你有多少种不同的方法可以爬到楼顶呢？

```
输入：n = 2
输出：2
输入：n = 3
输出：3
```

```
1 <= n <= 45
```

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0]*n
        dp[0] = 1
        dp[1] = 2
        for i in range(2,n):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n-1]
```

变体，增加限制不允许连续两次都上 2 级台阶（美的 24-11 经验贴）

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [0] * n
        end_with_two = [0] * n  # 到下标i时，本次使用2步的方法数量
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp[0] = 1
        dp[1] = 2
        end_with_two[0] = 0
        end_with_two[1] = 1
        for i in range(2,n):
            dp[i] = dp[i-1] + dp[i-2] - end_with_two[i-2]
            end_with_two[i] = dp[i-2] - end_with_two[i-2]
        return dp[n-1]
```

---

### 118 杨辉三角

给定一个非负整数 *`numRows`，*生成「杨辉三角」的前 *`numRows`* 行

在**「杨辉三角」**中，每个数是它左上方和右上方的数的和

```
输入: numRows = 5
输出: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
输入: numRows = 1
输出: [[1]]
```

```
1 <= numRows <= 30
```

```python
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        ans = [[1]]
        for i in range(1,numRows):
            tmp = []
            for j in range(i+1):
                if j==0:
                    tmp.append(1)
                elif j == i:
                    tmp.append(1)
                else:
                    tmp.append(ans[i-1][j-1] + ans[i-1][j])
            ans.append(tmp)
        return ans
```

---

### 53 最大子数组和

给你一个整数数组 `nums` ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和

**子数组** 是数组中的一个**连续部分**

**进阶：**如果你已经实现复杂度为 $O(n)$ 的解法，尝试使用更为精妙的 **分治法** 求解

```
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6
输入：nums = [1]
输出：1
输入：nums = [5,4,-1,7,8]
输出：23
```

**解法 1**：动态规划

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [float('-inf')]*n
        dp[0] = nums[0]
        ans = dp[0]
        for i in range(1, n):
            if dp[i-1] > 0:
                dp[i] = dp[i-1] + nums[i]
            else:
                dp[i] = nums[i]
            ans = max(ans, dp[i])
        return ans
```

时间：$O(n)$

空间：$O(n)$。使用了 `dp`

**解法 2**：空间优化的动态规划

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        dp = nums[0]
        ans = nums[0]
        for i in range(1, n):
            if dp > 0:
                dp = dp + nums[i]
            else:
                dp = nums[i]
            ans = max(ans, dp)
        return ans 
```

**解法 3**：分治法

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        def divide(left, right):
            if left == right:
                return nums[left]
            mid = (left + right) // 2
            left_max = divide(left, mid)
            right_max = divide(mid + 1, right)

            cur_sum = 0
            left_cross_max = float('-inf')
            right_cross_max = float('-inf')
            for i in range(mid,left-1,-1):
                cur_sum += nums[i]
                left_cross_max = max(left_cross_max, cur_sum)
            cur_sum = 0
            for i in range(mid+1, right+1):
                cur_sum += nums[i]
                right_cross_max = max(right_cross_max, cur_sum)
            cross_max = left_cross_max + right_cross_max
            return max(left_max, right_max, cross_max)

        return divide(0, len(nums) - 1)
```

- 复杂度

  - 时间：$O(n\log n)$

    设 $T(n)$ 表示输入规模为 $n$ 时，算法运行所需要的时间。则分治法有下述递推公式：
    $$
    T(n)=2T\left(\frac n2\right)+O(n)
    $$
    其中 $T\left(\frac n2\right)$  可以继续拆，大约会拆 $O(\log n)$ 次，每一次都会有一个 $O(n)$，因此时间复杂度大约为 $O(n \log n)$

  - 空间：$O(\log n)$

    二分的问题，递归调用栈的深度为 $O(\log n)$

- `right_max = divide(mid + 1, right)` 使用 `mid + 1` 而非 `mid` 的原因

  如果使用 `mid` 可能导致算法一直运行。例如外部运行 `divide(0, 1)`

  此时 $\text{left} = 0$，$\text{right} = 1$，计算得 `mid` 为 0，因此

  - `left_max = divide(0, 0)`
  - `right_max = divide(0, 1)` 这与原问题 `divide(0, 1)` 是相同的

  算法的 `left`、`right` 是闭区间写法，因此一定需要比原本的区间 **严格更小**

---

### 198 打家劫舍

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警**

给定一个代表每个房屋存放金额的非负整数数组，计算你 **不触动警报装置的情况下** ，一夜之内能够偷窃到的最高金额

```
输入：[1,2,3,1]
输出：4
输入：[2,7,9,3,1]
输出：12
```

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            dp[i] = max(dp[i-2] + nums[i], dp[i-1])

        return dp[n-1]
```

- 复杂度
  - 时间：$O(n)$，只需要进行一次遍历
  - 空间：$O(n)$，使用了状态数组，可以用滚动数组将数组压缩至 $O(1)$

- 状态转移方程

  设 $f(i)$ 表示偷窃到第 $i(i=0,\dots)$ 个房屋时，所能获得的最大金额，只有两个选择：

  ① 偷第 $i$ 间房：
  $$
  f(i) = f(i-2) + \text{nums}[i]f(i) = f(i-2) + \text{nums}[i]
  $$
  ② 不偷第 $i$ 间房：
  $$
  f(i) = f(i-1)
  $$
  故
  $$
  f(i) = \max(f(i-1), f(i-2) + \text{nums}[i])
  $$
  

如果不单独处理 $n =1,2$，程序的运行是依赖了 Python 的负索引特性（不规范写法）

---

### 279 完全平方数

给你一个整数 `n` ，返回 *和为 `n` 的完全平方数的最少**数量*** 

**完全平方数** 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，`1`、`4`、`9` 和 `16` 都是完全平方数，而 `3` 和 `11` 不是

```
输入：n = 12
输出：3 
输入：n = 13
输出：2
```

```
1 <= n <= 10^4
```

```python
class Solution:
    def numSquares(self, n: int) -> int:
        square = [i*i for i in range(1,101)]
        dp = [float('inf')] * (n+1) # dp[i]表示凑出整数 i 的平方数个数
        dp[0] = 0
        for i in range(1,n+1): # 考虑正整数1至n
            for j in square:
                if j>i:
                    break
                else:
                    dp[i] = min(dp[i], dp[i-j] + 1)
        return dp[n]
```

- 状态转移方程

  设 $f(i)$ 表示凑成正整数 $i$ 所需的**最少**完全平方数的**个数**

  对于每一个数字 $i$，我们可以尝试减去一个比它小的完全平方数 $j$， $j \in \{1, 4, 9, \dots, k^2 \le i\}$

  故
  $$
  f(i) = \min_{j \in \{k^2 \le i\}} \{ f(i - j) + 1 \}
  $$
  边界条件：$f(0) = 0$，凑成数字 0 需要 0 个平方数

**出错**：① `float('inf')` 写成 `float('int')`


---

### 322 零钱兑换

给你一个整数数组 `coins` ，表示不同面额的硬币；以及一个整数 `amount` ，表示总金额

计算并返回可以凑成总金额所需的 **最少的硬币个数** 。如果没有任何一种硬币组合能组成总金额，返回 `-1` 

你可以认为每种硬币的数量是无限的

```
输入：coins = [1, 2, 5], amount = 11
输出：3 
解释：11 = 5 + 5 + 1
输入：coins = [2], amount = 3
输出：-1
输入：coins = [1], amount = 0
输出：0
```

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins: 
                if i - coin >= 0:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return -1 if dp[amount] > amount else dp[amount]
```

- 状态转移方程

  设 $f(i)$ 表示凑成金额 $i$ 所需的最少硬币个数

  对于金额 $i$，可以尝试使用**硬币列表**中的**每一枚**硬币 $c$， $c \in \text{coins}$

  若选择面值为 $c$ 的硬币，则问题转化为：凑成金额 $i - c$ 所需的最少硬币个数 + 1，故
  $$
  f(i) = \min_{c \in \text{coins}, \ c \le i} \{ f(i - c) + 1 \}
  $$
  边界条件：$f(0)$

- 具体例子（最后为什么 $\infty$ 表示无法被凑出）

  设 `coins = [2]`、`amount = 3`，初始化 `dp = [0, inf, inf, inf]`

  - $f(1)$：唯一的硬币是 2。因 $2 > 1$，无法使用，$f(1)$ 保持 `inf`
  - $f(2)$：只有硬币 2 可以用。$f(2) = \min(\inf, f(2-2) + 1) = f(0) + 1 = 1$
  - $f(3)$：只有硬币 2 可以用。$f(3) = \min(\inf, f(3-2) + 1) = f(1) + 1 = \inf$

---

### 139 单词拆分

给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 `s` 则返回 `true`

**注意：**不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用

```
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
     注意，你可以重复使用字典中的单词。
输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false
```

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(n + 1):
            if dp[i]:
                for word in wordDict:
                    if s[i:i+len(word)] == word:
                        dp[i+len(word)] = True

        return dp[n]
```

- `dp` 的定义

  `dp[i]` 表示 $s[0:i)$ 是否是可以被凑出来的。因此 `dp[0]` 空串是肯定可以被凑出来的

---

### 300 最长递增子序列

给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。

**子序列** 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列。

问：你能将算法的时间复杂度降低到 $O(n \log (n))$ 吗?

```
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
输入：nums = [0,1,0,3,2,3]
输出：4
输入：nums = [7,7,7,7,7,7,7]
输出：1
```

```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [1] * n
        ans = 1

        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
            ans = max(ans, dp[i])

        return ans
```

初始状态需要设置为都是1，否则会出错，每一个元素都至少可以**自身**可以构成一个长度为 $1$ 的递增子序列

- 状态转移方程

  设 $f(i)$ 表示以 $\text{nums}[i]$ 结尾的最长严格递增子序列的**长度**
  $$
  f(i) = \max_{0 \le j < i, \text{nums}[j] < \text{nums}[i]} \{ f(j) \} + 1
  $$
  结果为
  $$
  \max_{0 \le i < n} \{ f(i) \}
  $$
  
- 时间复杂度：$O(n^2)$


**解法 2**：时间 $O(n \log(n))$

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        import bisect
        tail = []
        n = len(nums)
        for i in range(n):
            num = nums[i]
            idx = bisect.bisect_left(tail, num)
            if idx == len(tail):
                tail.append(num)
            else:
                if num < tail[idx]:
                    tail[idx] = num
        return len(tail)
```

- `tail` 的定义

  `tail[i]` 目前记录的长度为 $i + 1$ 的所有递增子序列中，**结尾元素**最小的

- **性质**：`tail` 数组是严格递增的

  证明：若不然，存在 $i(0\leq i \leq |\text{tail}|- 2)$，使得
  $$
  \text{tail}[i] \ge \text{tail}[i+1]
  $$
  存在一个长度为 $i+2$ 的严格递增子序列：
  $$
  a_1 < a_2 < \cdots < a_{i+1} < a_{i+2}
  $$
  使得 $a_{i+2} = \text{tail}[i+1]$，对于这个子序列，取第 1 至第 $i+1$ 项，则
  $$
  \text{tail}[i] \leq a_{i+1} < a_{i+2} = \text{tail}[i+1]
  $$
  即 $\text{tail}[i]  < \text{tail}[i+1]$，与假设矛盾 $\quad \square$

---

### 152 乘积最大子数组

给你一个整数数组 `nums` ，请你找出数组中乘积最大的非空连续 子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积

测试用例的答案是一个 **32-位** 整数

**请注意**，一个只包含一个元素的数组的乘积是这个元素的值 

```
输入: nums = [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
输入: nums = [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。
```

```
1 <= nums.length <= 2 * 10^4
-10 <= nums[i] <= 10
nums 的任何子数组的乘积都 保证 是一个 32-位 整数
```

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        ans = nums[0]
        cur_max = nums[0]
        cur_min = nums[0]
        n = len(nums)

        for i in range(1,n): #
            triple = (nums[i],cur_max * nums[i],cur_min * nums[i])
            cur_max = max(triple)
            cur_min = min(triple)
            ans = max(ans,cur_max)
        
        return ans
```

考虑最小值是因为两个负数相乘可能会变成一个更大的正数

双循环枚举，时间为 $O(n^2)$

---

### 416 分割等和子集

给你一个 **只包含正整数** 的 **非空** 数组 `nums` 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等

```
输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
输入：nums = [1,2,3,5]
输出：false
解释：数组不能分割成两个元素和相等的子集。
```

```
1 <= nums.length <= 200
1 <= nums[i] <= 100
```

**解法 1**：二维动态规划

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        nums_sum = sum(nums)
        if nums_sum % 2 == 1:
            return False
        
        target = nums_sum // 2
        m = len(nums)

        dp = [[False]*(target+1) for _ in range(m+1)]
        for i in range(m+1):
            dp[i][0] = True
        
        for i in range(1,m+1):
            for j in range(1,target+1):
                dp[i][j] = dp[i-1][j]
                if j >= nums[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j-nums[i-1]]
        return dp[m][target]
```

- `dp[i][j]` 的定义

  只看前 $i$ 个数时，是否能够凑出和 $j$

  返回的 `dp[n][target]` 表示允许使用 $n$ 个数，现在需要凑出 `target`

- b 站说是高频面试算法题

#### 带 memo 的回溯算法

**解法 2**：暴力回溯算法，无法通过

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        sum_nums = sum(nums)
        n = len(nums)
        if sum_nums % 2 == 1:
            return False
        else:
            target = sum_nums // 2

        def backtrack(i, total):  # i表示正在处理的下标
            if total == target:
                return True
            if total > target or i == n:  # 剪枝
                return False

            return backtrack(i + 1, total + nums[i]) or backtrack(i + 1, total)

        return backtrack(0, 0)
```

回溯算法本质上是“带剪枝的暴力搜索”

- `backtrack(i, total)` 的定义

  在只考虑下标 `i` 及之后的元素时，当前已经选出的元素和为 `total`，**是否存在一种选择**，使得最终可以达到 `target`

  所以他是有考虑了后面的

- 复杂度

  时间：$O(2^n)$。对于每个位置 `nums[i]`，都有两种选择：选、不选，因此递归树最多有大约 $2^n$ 个状态

  空间：$O(n)$。（按 **递归调用栈** 计）递归最深会到 $n$ 层

  但简单改一下上述算法，就能快很多，此时能够通过

**解法 3**：带 memo 的回溯算法

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        sum_nums = sum(nums)
        n = len(nums)

        memo = {}

        if sum_nums % 2 == 1:
            return False
        else:
            target = sum_nums // 2

        def backtrack(i, total):  # i表示正在处理的下标
            if (i, total) in memo:
                return memo[(i, total)]
            if total == target:
                return True
            if total > target or i == n:  # 剪枝
                return False

            res = backtrack(i + 1, total + nums[i]) or backtrack(i + 1, total)
            memo[(i,total)] = res

            return res

        return backtrack(0, 0)
```

记忆化搜索本质：把指数级的 “路径数”，压缩成多项式级的 “状态数”

---



## 多维动态规划

### 62 不同路径

一个机器人位于一个 `m x n` 网格的左上角 （起始点在下图中标记为 “Start” ）

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）

问总共有多少条不同的路径？

```
1 <= m, n <= 100
题目数据保证答案小于等于 2 * 10^9
```

**解法 1**

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0]*n for _ in range(m)]
        for i in range(m):
            dp[i][0] = 1
        for i in range(n):
            dp[0][i] = 1

        for i in range(1,m):
            for j in range(1,n):
                dp[i][j] = dp[i][j-1] + dp[i-1][j]
                
        return dp[m-1][n-1]
```

设 `dp[i][j]` 表示从左上角走到位置 `(i, j)` 的不同路径数

状态转移方程
$$
\text{dp}[i][j] = \text{dp}[i-1][j] + \text{dp}[i][j-1]
$$
**解法 2**：使用 **排列组合** 求解，路径数为
$$
N = C_{m+n-1}^{m-1}
$$
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        def combination(M, N): # C_M^N
            res = 1
            # 分子
            for i in range(M-N+1, M+1):
                res *= i
            # 分母
            for i in range(1,N+1):
                res = res // i
            return res
        return combination(m+n-2, m-1)
```

要用 `res = res // i`，不能用 `/`，真除法会有误差，答案最后可能会相差1

---

### 64 最小路径和

给定一个包含非负整数的 `m × n` 网格 `grid` ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小

**说明：**每次只能向下或者向右移动一步

```
1 <= m, n <= 200
0 <= grid[i][j] <= 200
```

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        dp = [[0]*n for _ in range(m)]

        dp[0][0] = grid[0][0] # 记得要写

        for j in range(1,n):
            dp[0][j] = dp[0][j-1] + grid[0][j]
        for i in range(1,m):
            dp[i][0] = dp[i-1][0] + grid[i][0]
        
        for i in range(1,m):
            for j in range(1,n):
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
        
        return dp[m-1][n-1]
```

本题初始化不用设为 inf，因为每个 `dp[i][j]` 都会被覆盖赋值。第一行、第一列：**单独初始化**，其余位置都会在循环中被计算出来

**出错**：`max` 写成了 `min`

---

### 5 最长回文子串

给你一个字符串 `s`，找到 `s` 中最长的 **回文** 子串

```
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
输入：s = "cbbd"
输出："bb"
```

```
1 <= s.length <= 1000
s 仅由数字和英文字母组成
```

**解法**：中心扩散法

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        ans = ""

        def expand(left,right):
            while left>=0 and right <= n-1 and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left+1:right]
        
        for i in range(n):
            s1 = expand(i,i)
            s2 = expand(i,i+1)

            if len(s1) > len(ans):
                ans = s1
            if len(s2) > len(ans):
                ans = s2
        return ans
```

要分两种中心，分别对应奇数、偶数的回文串

`s2 = expand(i,i+1)` 无需要检查 $i$ 与 $i+1$ 位置是否相同，此时 expand 中返回的 `s[left+1:right]` 是空的

当 $i = n-1$ 时，expand 传入 $(n-1,n)$，此时 `right` 不满足 expand 中的条件，返回 `s[n:n]`，这仍然是空的

因此不用增加额外的判断

而且如果 `for i in range(n):` 改成 $n-1$，会导致例子 `"a"` 不会进入循环，程序输出 `""`，而非 `"a"`

---

### 1143 最长公共子序列

给定两个字符串 `text1` 和 `text2`，返回这两个字符串的最长 **公共子序列** 的长度。如果不存在 **公共子序列** ，返回 `0` 

一个字符串的 **子序列** 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串

- 例如，`"ace"` 是 `"abcde"` 的子序列，但 `"aec"` 不是 `"abcde"` 的子序列

两个字符串的 **公共子序列** 是这两个字符串所共同拥有的子序列

```
输入：text1 = "abcde", text2 = "ace" 
输出：3  
输入：text1 = "abc", text2 = "abc"
输出：3
输入：text1 = "abc", text2 = "def"
输出：0
```

```
1 <= text1.length, text2.length <= 1000
text1 和 text2 仅由小写英文字符组成。
```

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m = len(text1)
        n = len(text2)
        dp = [[0]*(n+1) for _ in range(m+1)]

        for i in range(1,m+1):
            for j in range(1,n+1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]
```

算例，*见 notability*

`dp[i][j]` 表示 `text1` 的前 $i$ 个字符和 `text2` 的前 $j$ 个字符的最长公共子序列长度

---

### 72 编辑距离

给你两个单词 `word1` 和 `word2`， *请返回将 `word1` 转换成 `word2` 所使用的最少操作数*

你可以对一个单词进行如下三种操作：

- 插入一个字符
- 删除一个字符
- 替换一个字符

```
输入：word1 = "horse", word2 = "ros"
输出：3
输入：word1 = "intention", word2 = "execution"
输出：5
```

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1):
            dp[i][0] = i
        
        for j in range(n+1):
            dp[0][j] = j
        
        for i in range(1,m+1):
            for j in range(1,n+1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]) + 1
        return dp[m][n]
```


## 技巧

### 136 只出现一次的数字

给你一个 **非空** 整数数组 `nums` ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素

你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间

```
输入：nums = [2,2,1]
输出：1
输入：nums = [4,1,2,1,2]
输出：4
输入：nums = [1]
输出：1
```

```
1 <= nums.length <= 3 * 10^4
-3 * 10^4 <= nums[i] <= 3 * 10^4
除了某个元素只出现一次以外，其余每个元素均出现两次
```

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = nums[0]
        for i in range(1,len(nums)):
            ans ^= nums[i]
        return ans
```

`^` 按位异或（XOR，exclusive OR）

先转为二进制后，再按位异或，输出的结果再转为十进制数字

例：`3 ^ 5`，首先 3 = 110、5 = 101 异或结果为6，即 `3 ^ 5 = 6`

**性质**：这里 $a,b,c$ 在输入输出的时候，都是10进制数，$\oplus$ 表示二进制按位异或。本题需要用到以下性质

① $a \oplus a = 0$

② $a \oplus 0 = a$

③ 交换律：$a \oplus b = b \oplus a$

④ 结合律：$(a \oplus b) \oplus  c = a \oplus (b \oplus c)$

---

###  169 多数元素

给定一个大小为 `n` 的数组 `nums` ，返回其中的多数元素。多数元素是指在数组中出现次数 **大于** `⌊ n/2 ⌋` 的元素

你可以假设数组是非空的，并且给定的数组总是存在多数元素

**进阶：**尝试设计时间复杂度为 $O(n)$、空间复杂度为 $O(1)$ 的算法解决此问题

```
输入：nums = [3,2,3]
输出：3
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

```
n == nums.length
1 <= n <= 5 * 10^4
-10^9 <= nums[i] <= 10^9
输入保证数组中一定有一个多数元素
```

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        count = 0
        ans = nums[0]
        for i in range(n):
            if nums[i] == ans:
                count += 1
            else:
                if count == 0:
                    ans = nums[i]
                    count += 1
                else:
                    count -= 1
 
        return ans
```

思路：摩尔投票法（Boyer-Moore Voting Algorithm）

每次先看 `ans` 并分成两大类考虑，`ans` 先默认设为数组中的第一个元素

1. 若 `ans` 与本次相同，`count`  +1

2. 若 `ans` 与本次不同：

   ① 若 `count == 0`，修改 `ans` 并将 `count`  +1

   ② 若 `count > 0`，将 `count`  -1

**性质**：在总是存在多数元素的条件下，不会有大于1个的多数元素

**Proof**：① 若 $n$ 为偶数，$\text{count}(a) > \left \lfloor  \frac{n}{2}\right \rfloor =  \frac{n}{2}$，即 $\text{count}(a) \geq \frac{n}{2} + 1$，故
$$
\text{count}(a) + \text{count}(b) \geq n+2
$$
矛盾

② 若 $n$ 为奇数，$\text{count}(a) > \left \lfloor  \frac{n}{2}\right \rfloor =  \frac{n-1}{2}$，即 $\text{count}(a) \geq \frac{n+1}{2}$，故
$$
\text{count}(a) + \text{count}(b) \geq n+1
$$
矛盾 $\quad \square$

---

### 75 颜色分类

给定一个包含红色、白色和蓝色、共 `n` 个元素的数组 `nums` ，**原地** 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列

我们使用整数 `0`、 `1` 和 `2` 分别表示红色、白色和蓝色

必须在不使用库内置的 sort 函数的情况下解决这个问题

**进阶**：你能想出一个仅使用常数空间的一趟扫描算法吗？

```
输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
输入：nums = [2,0,1]
输出：[0,1,2]
```

```
n == nums.length
1 <= n <= 300
nums[i] 为 0、1 或 2
```

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        i = 0
        left = 0 
        right = n-1
        while i <= right:
            if nums[i] == 0:
                nums[i], nums[left] = nums[left], nums[i]
                i += 1
                left += 1
            elif nums[i] == 1:
                i += 1
            else:
                nums[i], nums[right] = nums[right], nums[i]
                right -= 1
```

`left` 下一个该放0的位置（还没有放）

`right` 下一个该放2的位置（也还没放）

`i` 当前扫描指针，是正在处理的未知区域

将数组划分为四个部分

```
[0 ... left-1]   → 0 区
[left ... i-1]   → 1 区
[i ... right]    → 未处理
[right+1 ... n-1] → 2 区
```

因此 `else:` 不用 `i += 1`，因为传过来的 `right` 位置还没有处理好，但是 `left` 是落在左边已处理好的区域 $[left, i-1]$ 中

**出错**：`while i <= right:` 没有加等号

---

### 31 下一个排列

整数数组的一个 **排列** 就是将其所有成员以序列或线性顺序排列

- 例如，`arr = [1,2,3]` ，以下这些都可以视作 `arr` 的排列：`[1,2,3]`、`[1,3,2]`、`[3,1,2]`、`[2,3,1]`

整数数组的 **下一个排列** 是指其整数的下一个字典序更大的排列。更正式地，如果数组的所有排列根据其字典顺序从小到大排列在一个容器中，那么数组的 **下一个排列** 就是在这个有序容器中排在它后面的那个排列。如果不存在下一个更大的排列，那么这个数组必须重排为字典序最小的排列（即，其元素按升序排列）

- 例如，`arr = [1,2,3]` 的下一个排列是 `[1,3,2]`
- 类似地，`arr = [2,3,1]` 的下一个排列是 `[3,1,2]`
- 而 `arr = [3,2,1]` 的下一个排列是 `[1,2,3]` ，因为 `[3,2,1]` 不存在一个字典序更大的排列

给你一个整数数组 `nums` ，找出 `nums` 的下一个排列

必须 **原地** 修改，只允许使用额外常数空间

```
输入：nums = [1,2,3]
输出：[1,3,2]
输入：nums = [3,2,1]
输出：[1,2,3]
输入：nums = [1,1,5]
输出：[1,5,1]
```

```
1 <= nums.length <= 100
0 <= nums[i] <= 100
```

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        if n == 1:
            return

        def reverse(left: int, right: int) -> None:
            while left < right:
                nums[left],nums[right] = nums[right],nums[left]
                left += 1
                right -= 1
        
        for i in range(n-2,-1,-1):
            if nums[i] < nums[i+1]: # 从右向左找到第一个下降位置
                for j in range(n-1,-1,-1):
                    if nums[j] > nums[i]: # 从右向左找到第一个更大的元素
                        nums[i],nums[j] = nums[j],nums[i]
                        reverse(i+1,n-1)
                        return
        reverse(0,n-1)
```

**出错**：① `reverse(i+1,n-1)` 写成了 `reverse(i+1, j-1)`

---

### 287 寻找重复数

给定一个包含 `n + 1` 个整数的数组 `nums` ，其数字都在 `[1, n]` 范围内（包括 `1` 和 `n`），可知至少存在一个重复的整数

假设 `nums` 只有 **一个重复的整数** ，返回 **这个重复的数**

你设计的解决方案必须 **不修改** 数组 `nums` 且只用常量级 $O(1)$ 的额外空间

**进阶**：如何证明 `nums` 中至少存在一个重复的数字？你可以设计一个线性级时间复杂度 $O(n)$ 的解决方案吗？

```
输入：nums = [1,3,4,2,2]
输出：2
输入：nums = [3,1,3,4,2]
输出：3
输入：nums = [3,3,3,3,3]
输出：3
```

```
1 <= n <= 10^5
nums.length == n + 1
1 <= nums[i] <= n
nums 中 只有一个整数 出现 两次或多次 ，其余整数均只出现 一次
```

用哈希表，时间 $O(n)$，空间 $O(n)$

- Floyd 快慢指针法（龟兔赛跑算法）

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = nums[0]
        fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                p1 = nums[0]
                p2 = fast
                while p1 != p2:
                    p1 = nums[p1]
                    p2 = nums[p2]
                return p1
```

本题与 *142 环形链表 II* 解法相同
