---
title: "常用数据结构"
date: 2025-04-21
categories: ["java"]
tags: ["java","数据结构"]
---

## 零、常用枚举技巧

### 枚举右，维护左

对于 双变量问题，例如两数之和 a + b = c ，可以枚举右边的 a,转化单变量问题


### 枚举中间

对于三个或者四个变量的问题，枚举中间的变量往往更好算


[2909. 元素和最小的山形三元组 II](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-ii/)


给定(i，j，k)找出一个山形元素



```java
class Solution {
    public int minimumSum(int[] nums) {
        int n = nums.length;
        int[] suf = new int[n]; // 后缀最小值
        suf[n - 1] = nums[n - 1];
        for (int i = n - 2; i > 1; i--) {
            suf[i] = Math.min(suf[i + 1], nums[i]);
        }

        int ans = Integer.MAX_VALUE;
        int pre = nums[0]; // 前缀最小值
        for (int j = 1; j if (pre  suf[j + 1]) { // 山形
                ans = Math.min(ans, pre + nums[j] + suf[j + 1]); // 更新答案
            }
            pre = Math.min(pre, nums[j]);
        }
        return ans == Integer.MAX_VALUE ? -1 : ans;
    }
}

```



## 前缀和

### 前缀和基础

模板题：


![image-20250405171637483](/2025/04/21/%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/image-20250405171637483.png)


定义s[0] = 0,就不需要特判left=0的情况了，右减去左会将左的位置减去



```java
class NumArray {
    private final int[] s;

    public NumArray(int[] nums) {//前缀和数组计算
        s = new int[nums.length + 1];
        for (int i = 0; i 1] = s[i] + nums[i];
        }
    }

    public int sumRange(int left, int right) {//求特定[left, right]
        return s[right + 1] - s[left];
    }
}

```





### 前缀和与哈希表

#### [560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)

计算子数组(连续非空序列)的和为k,很简单自然而然想到两次遍历以j为终点，用i遍历0-j为k则+1


但可以用前缀和，前缀和中s[j]-s[i]=k,计算就是连续序列的和，但可以发现了这里子数组并不能直接计算啊，那怎么办呢，使用哈希表，使用哈希表来统计这个s[i]从0，j有多少个就行了，这样我们就能计算出以j为终点的连续子数组了，这就是妙用



```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        int count = 0, pre = 0;
        Map cnt = new HashMap<>(nums.length + 1); // 设置容量可以快 2ms
        mp.put(0, 1);// s[0]=0 单独统计，mp数组的意思是前缀和为0的数组有一个即s[0]
        for(int i = 0; i if(mp.containsKey(pre - k)){
                count += mp.get(pre - k);
            }
            mp.put(pre, mp.getOrDefault(pre, 0) + 1);
            //cnt.merge(s, 1, Integer::sum); // cnt[s]++
        }
        return count;
    }
}

```



### 前缀异或和

#### [从集合论到位运算，常见位运算技巧分类总结！](https://leetcode.cn/discuss/post/3571304/cong-ji-he-lun-dao-wei-yun-suan-chang-ji-enve/)

#### [1177. 构建回文串检测](https://leetcode.cn/problems/can-make-palindrome-from-substring/)

对于子数组检测待检字串是否替换k个考研成为回文串


- 回文意味着从左往右第 *i* 个字母和从右往左第 *i* 个字母是相同的。（回文串关于回文中心是对称的。）
- 如果有偶数个 a，那么可以均分成两部分，分别放置在字符串的中心对称位置上。例如有 4 个 a，可以在字符串的最左边放置 2 个 a，最右边放置 2 个 a，这样字符串中的 a 是回文的。其它字母如果出现偶数次，也同理。
  
  
  如果有奇数个 a，多出的一个 a 要单独拿出来讨论：
  
  
  —假如只有 a 出现奇数次，其它字母都出现偶数次。此时字符串的长度一定是奇数，那么可以把多出的这个 a 放在字符串的中心，我们仍然可以得到一个回文串，无需替换任何字母。
—如果有两种字母出现奇数次（假设是字母 a,b），由于多出的一个 a 和一个 b 无法组成回文串，可以把一个 b 改成 a（或者把一个 a 改成 b），这样 a 和 b 就都出现偶数次了。
—如果有三种字母出现奇数次（假设是字母 a,b,c），把一个 b 改成 c，就转换成只有 a 出现奇数次的情况了。


方案一，使用数组


1. 预处理 s 的长为 i 的前缀中，每种字母各出现多少次。为方便后续优化，这里用 n×26 的二维数组 sum 存储前缀和，其中 sum[i+1][j] 表示从 s[0] 到 s[i] 中，字母表的第 j 个小写字母的出现次数。
2. 对于 queries[i]，利用前缀和计算出每种字母出现次数，统计有多少种字母出现奇数次，设为 m。如果 ⌊ m/2⌋≤k，那么 answer[i] 为真，反之为假。



```java
class Solution {
    public List canMakePaliQueries(String s, int[][] queries) {
        int n = s.length();//字符串长度length()
        var sum = new int[n+1][26];
        for(int i = 0; i 1] = sum[i].clone;
            sum[i][s.charAt(i) - 'a']++;
        }

        var ans = new ArrayList(queries.length); // 预分配空间
        for (var q : queries) {
            int left = q[0], right = q[1], k = q[2], m = 0;
            for (int j = 0; j 1][j] - sum[left][j]) % 2; // 奇数+1，偶数+0
            ans.add(m / 2 return ans;
    }
}

```



方案二：


- 由于只关心每种字母出现次数的奇偶性，所以不需要在前缀和中存储每种字母的出现次数，只需要保存每种字母出现次数的奇偶性。
- 为方便计算，用 0 表示出现偶数次，用 1 表示出现奇数次。
- 注意只有奇数减偶数，或者偶数减奇数，才能得到奇数。所以如果相减的结果不为 0（或者说相减的两个数不相等），就表示出现了奇数次。



```java
class Solution {
    public List canMakePaliQueries(String s, int[][] queries) {
        int n = s.length();
        var sum = new int[n + 1][26];
        for (int i = 0; i 1] = sum[i].clone();
            sum[i + 1][s.charAt(i) - 'a']++;
            sum[i + 1][s.charAt(i) - 'a'] %= 2; // 偶数是 0---在这优化
        }

        var ans = new ArrayList(queries.length); // 预分配空间
        for (var q : queries) {
            int left = q[0], right = q[1], k = q[2], m = 0;
            for (int j = 0; j 1][j] != sum[left][j] ? 1 : 0);
            ans.add(m / 2 return ans;
    }
}

```



方案三：


- 由于异或运算满足 1 和 0 的结果是 1，而 0 和 0，以及 1 和 1 的结果都是 0，所以可以用异或替换上面的减法。
- 由于长为 26 的数组中只存储 0 和 1，可以压缩到一个二进制数中，二进制数从低到高第 i 个比特存储着 0 和 1 的信息。
- 例如二进制 10010 表示 b 和 e 出现奇数次，其余字母出现偶数次。
- 在计算前缀和时（准确地说是异或前缀和）：
  
  
  
  修改 a 出现次数的奇偶性，可以异或二进制 1；
- 修改 b 出现次数的奇偶性，可以异或二进制 10；
- 修改 c 出现次数的奇偶性，可以异或二进制 100；



依此类推。
此外，由于异或可以「并行计算」，对前缀和中的两个二进制数直接异或，便得到了子串中每种字母出现次数的奇偶性。再计算这个二进制数中的 1 的个数，便得到了 m。



例如 10010⊕01110=11100，说明有 3 种字母出现奇数次。





```java
class Solution {
    public List canMakePaliQueries(String s, int[][] queries) {
        int n = s.length();
        var sum = new int[n + 1];
        for (int i = 0; i //左移操作int bit = 1 1] = sum[i] ^ bit; 
            // 该比特对应字母的奇偶性：奇数变偶数，偶数变奇数
            /*
            异或运算的性质：
					0 ^ 1 = 1（偶数变奇数）
					1 ^ 1 = 0（奇数变偶数）
            */
        }

        var ans = new ArrayList(queries.length); // 预分配空间
        for (var q : queries) {
            int left = q[0], right = q[1], k = q[2];
            int m = Integer.bitCount(sum[right + 1] ^ sum[left]);
            ans.add(m / 2 return ans;
    }
}

```



### 二维前缀和

![image-20250408154523509](/2025/04/21/%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/image-20250408154523509.png)


![image-20250408155046277](/2025/04/21/%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/image-20250408155046277.png)


[304. 二维区域和检索 - 矩阵不可变 - 力扣（LeetCode）](https://leetcode.cn/problems/range-sum-query-2d-immutable/)


## 差分

### 基础概念

**差分数组的主要适用场景是频繁对原始数组的某个区间的元素进行增减**。


![image-20250408095450220](https://raw.githubusercontent.com/HgnGoning/images/main/img/image-20250408095450220.png)


### 代码

差分数组：



```java
int[] diff = new int[nums.length];
// 构造差分数组
diff[0] = nums[0];
for (int i = 1; i 1];
}

```



还原：



```java
int[] res = new int[diff.length];
// 根据差分数组构造结果数组
res[0] = diff[0];
for (int i = 1; i 1] + diff[i];
}

```



差分数组工具类：



```java
// 差分数组工具类
class Difference {
    // 差分数组
    private int[] diff;
    
    // 输入一个初始数组，区间操作将在这个数组上进行
    public Difference(int[] nums) {
        assert nums.length > 0;
        diff = new int[nums.length];
        // 根据初始数组构造差分数组
        diff[0] = nums[0];
        for (int i = 1; i 1];
        }
    }

    // 给闭区间 [i, j] 增加 val（可以是负数）
    public void increment(int i, int j, int val) {
        diff[i] += val;
        if (j + 1 1] -= val;
        }
    }

    // 返回结果数组
    public int[] result() {
        int[] res = new int[diff.length];
        // 根据差分数组构造结果数组
        res[0] = diff[0];
        for (int i = 1; i 1] + diff[i];
        }
        return res;
    }
}

```



### 二维差分

![image-20250408101825082](https://raw.githubusercontent.com/HgnGoning/images/main/img/image-20250408101825082.png)


## 栈

#### [3170. 删除星号以后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/)

核心思路：由于要去掉最小的字母，为了让字典序尽量小，相比去掉前面的字母，去掉后面的字母更好。


- 从左到右遍历 s，用 26 个栈模拟。
- 第 i 个栈维护第 i 个小写字母的下标。
- 遇到 * 时，弹出第一个非空栈的栈顶下标。
- 最后把所有栈顶下标对应的字母组合起来，即为答案。


写法一：



```java
class Solution {
    public String clearStars(String S) {
        char[] s = S.toCharArray();//将String转为可操作的char
        List[] st = new ArrayList[26];
        Arrays.setAll(st, i -> new ArrayList<>());////----每一个位置再加一个数组
        for (int i = 0; i if (s[i] != '*') {
                st[s[i] - 'a'].add(i);
                continue;
            }
            for (List p : st) {
                if (!p.isEmpty()) {
                    p.remove(p.size() - 1);
                    break;
                }
            }
        }
		
        //创建一个新的 ArrayList 对象 idx，用于存储所有非星号字符的位置索引。
        List idx = new ArrayList<>();
        for (List p : st) {
            idx.addAll(p);//将每个列表中的所有元素添加到 idx 中。
        }
        Collections.sort(idx);//对 idx 进行排序，确保索引是按顺序排列的。

        StringBuilder t = new StringBuilder(idx.size());
        for (int i : idx) {
            t.append(s[i]);
        }
        return t.toString();
        /*char[] result = new char[idx.size()];
        for (int i = 0; i             result[i] = s[idx.get(i)];
        }
        return new String(result);*/
    }
}

```



## 堆

[8.1  堆 - Hello 算法](https://www.hello-algo.com/chapter_heap/heap/)


就是一个优先级队列，以完全二叉树的形式展现，可以很轻松的找出k个最大元素


例如：


有一堆石头，每块石头的重量都是正整数。


每一回合，从中选出两块 **最重的** 石头，然后将它们一起粉碎。假设石头的重量分别为 `x` 和 `y`，且 `x <= y`。那么粉碎的可能结果如下：


- 如果 `x == y`，那么两块石头都会被完全粉碎；
- 如果 `x != y`，那么重量为 `x` 的石头将会完全粉碎，而重量为 `y` 的石头新重量为 `y-x`。


最后，最多只会剩下一块石头。返回此石头的重量。如果没有石头剩下，就返回 `0`。



```java
class Solution {
    public int lastStoneWeight(int[] stones) {
        PriorityQueue pq = new PriorityQueue((a, b) -> b - a);
        for (int stone : stones) {
            pq.offer(stone);
        }

        while (pq.size() > 1) {
            int a = pq.poll();
            int b = pq.poll();
            if (a > b) {
                pq.offer(a - b);
            }
        }
        return pq.isEmpty() ? 0 : pq.poll();
    }
}

```



## Trie树

## 并查集

## 树状数组和线段树

# hot100

## 1

## 2

## 3

## 4

## 8 [无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

滑动窗口做，一个hashmap统计一下进入窗口的有哪些，hashmap存字符，有重复就一直出，直到当前字符为一个，ans存最大


## 9

用滑动窗口做统计，字串长度大于二，滑动到二作比较，然后收缩