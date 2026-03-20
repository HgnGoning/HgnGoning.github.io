---
title: Java编程技巧
date: 2025-05-13 10:08:13
tags:
  - 编程
---

## 字符串String

字符串长度： s.length

字符串转数组： char[] s = S.toCharArray();

操作：

```java
string s = "/home/1"
s.split("/")
//stk为Sting
String.join("/", stk)
```

## 数组

数组长度： nums.length

数组排序：Arrays.sort()

## 排序比较器

可以直接使用Lambda

 `(p, q) -> p[0] - q[0]`

- **返回负值**：`p` 应排在 `q` 前（左端点更小）。
- **返回正值**：`q` 应排在 `p` 前（左端点更大）。
- **返回0**：两者视为相等。

## Collection 接口

### 1. 基础操作

| 方法 | 描述 |
| --- | --- |
| `boolean add(E e)` | 添加元素（`List`/`Set`/`Queue`通用） |
| `boolean remove(Object o)` | 删除指定元素 |
| `boolean contains(Object o)` | 判断是否包含元素 |
| `int size()` | 返回元素数量 |
| `boolean isEmpty()` | 判断是否为空 |
| `void clear()` | 清空容器 |

### 2. 批量操作

| 方法 | 描述 |
| --- | --- |
| `boolean addAll(Collection<? extends E> c)` | 添加另一个容器的所有元素 |
| `boolean removeAll(Collection<?> c)` | 删除与另一个容器共有的元素 |
| `boolean retainAll(Collection<?> c)` | 仅保留与另一个容器共有的元素 |
| `boolean containsAll(Collection<?> c)` | 判断是否包含另一个容器的所有元素 |

### 3. 遍历与转换

| 方法 | 描述 |
| --- | --- |
| `Iterator<E> iterator()` | 返回迭代器（`hasNext()`+ `next()`） |
| `Object[] toArray()` | 转换为数组 |
| `<T> T[] toArray(T[] a)` | 转换为指定类型的数组 |
| `default void forEach(Consumer<? super E> action)` | Java 8+ 遍历 |

## List

| 方法 | 描述 |
| --- | --- |
| `E get(int index)` | 获取指定位置的元素 |
| `E set(int index, E element)` | 修改指定位置的元素 |
| `void add(int index, E element)` | 在指定位置插入元素 |
| `E remove(int index)` | 删除指定位置的元素 |
| `int indexOf(Object o)` | 返回元素首次出现的索引 |
| `int lastIndexOf(Object o)` | 返回元素最后一次出现的索引 |

## ArrayList

动态数组，随机访问快（`O(1)`），插入删除慢（`O(n)`）

## Map

| 方法 | 描述 |
| --- | --- |
| `V put(K key, V value)` | 添加键值对（重复 key 会覆盖） |
| `V get(Object key)` | 获取指定 key 的值 |
| `V remove(Object key)` | 删除指定 key 的键值对 |
| `boolean containsKey(Object key)` | 判断是否包含 key |
| `boolean containsValue(Object value)` | 判断是否包含 value |
| `int size()` | 返回键值对数量 |
| `void clear()` | 清空 Map |

### 视图操作

| 方法 | 描述 |
| --- | --- |
| `Set<K> keySet()` | 返回所有 key 的 `Set`视图 |
| `Collection<V> values()` | 返回所有 value 的 `Collection`视图 |
| `Set<Map.Entry<K, V>> entrySet()` | 返回所有键值对的 `Set`视图 |

## Entry

entry 它表示 Map 中的一个键值对。这个循环是以 Map.Entry 的集合为变量进行遍历的，每次循环获得的是 m（这是一个 HashMap）中的一个键值对。

具体来说：
- entry.getKey() 会返回当前的键，也就是排序后的字符串。
- entry.getValue() 会返回对应的值，也就是具有相同异位词特征的字符串列表。

## Set

| 类 | 特点 |
| --- | --- |
| `HashSet` | 基于 `HashMap`，无序，`O(1)`查询 |
| `LinkedHashSet` | 保持插入顺序—-用在LRU |
| `TreeSet` | 基于 `TreeMap`，自然排序或自定义 `Comparator`，`O(log n)`查询 |

## Queue/Deque 接口（队列/双端队列）

### 1. Queue 方法

| 方法 | 描述 |
| --- | --- |
| `boolean offer(E e)` | 添加元素（队列满时返回 `false`） |
| `E poll()` | 移除并返回队首元素（队列空时返回 `null`） |
| `E peek()` | 查看队首元素（不移除） |
| `E remove()` | 移除队首元素（队列空时抛异常） |
| `E element()` | 查看队首元素（队列空时抛异常） |

### 2. Deque 方法（双端队列）

| 方法 | 描述 |
| --- | --- |
| `void addFirst(E e)` | 在队首添加元素 |
| `void addLast(E e)` | 在队尾添加元素 |
| `E pollFirst()` | 移除并返回队首元素 |
| `E pollLast()` | 移除并返回队尾元素 |

### 3. 实现类（LinkedList/PriorityQueue）

| 类 | 特点 |
| --- | --- |
| `LinkedList` | 可作 `List`或 `Deque`使用 |
| `ArrayDeque` | 高效双端队列（比 `LinkedList`更快） |
| `PriorityQueue` | 优先级队列（堆实现，按自然顺序或 `Comparator`排序） |

## BlockingQueue

| **插入** | `add(E e)` | 队列未满时插入，满时抛 `IllegalStateException` | ❌ |
| --- | --- | --- | --- |
|  | `offer(E e)` | 队列未满时插入并返回 `true`，满时返回 `false` | ❌ |
|  | `put(E e)` | 队列满时阻塞，直到有空位 | ✅ |
|  | `offer(E e, long timeout, TimeUnit unit)` | 队列满时阻塞，超时后返回 `false` | ✅ |
| **移除** | `remove()` | 队列非空时移除头部元素，空时抛 `NoSuchElementException` | ❌ |
|  | `poll()` | 队列非空时移除头部元素并返回，空时返回 `null` | ❌ |
|  | `take()` | 队列空时阻塞，直到有元素 | ✅ |
|  | `poll(long timeout, TimeUnit unit)` | 队列空时阻塞，超时后返回 `null` | ✅ |
| **检查** | `element()` | 返回头部元素（不移除），空时抛 `NoSuchElementException` | ❌ |
|  | `peek()` | 返回头部元素（不移除），空时返回 `null` | ❌ |

## 动态规划

### 备忘录解法

#### 斐波那契数列

1.暴力

大量重复运算导致复杂度上升，备忘录出现即避免这么多重复运算使用数组或者什么数据结构统计一下

#### 自顶向下和自底向上

取决于备忘录怎么记，从dp[5]往dp[1]构建还是反过来构建，两种方式都可以

[322. 零钱兑换 - 力扣（LeetCode）](https://leetcode.cn/problems/coin-change/?envType=study-plan-v2&envId=top-100-liked)

问：为什么不在二分的过程中，找到 target 就立刻返回？

问：为什么代码没有特判所有数都小于 target 的情况？

答：如果所有数都小于 target，那么循环中更新的只有 left，无论下面哪种二分写法，最后都一定会返回数组长度，所以无需特判这种情况。

问：如果所有数都大于 target 呢？

答：代码会返回 0。

问：是否需要特判 nums[mid]=target 的情况？

答：可以，但没必要
