---
layout: post
title: "CodeTop 热题刷题记录"
date: 2026-03-21
categories: [算法]
tags: [LeetCode, Java, 算法, 刷题]
description: CodeTop 企业高频题刷题记录，包含思路解析和 Java 代码实现
---

# CodeTop 热题刷题记录

---

## 1. 两数之和
**LeetCode链接**: https://leetcode.cn/problems/two-sum/

### 思路
使用哈希表存储"期望值"。遍历数组，对于每个元素`nums[i]`：
- 检查哈希表中是否存在该值（即是否有之前的数期望它作为另一半）
- 如果存在，说明找到了两个数，直接返回它们的索引
- 如果不存在，将`target - nums[i]`作为期望值存入哈希表，表示期望找到另一个数为`nums[i]`

这种方法的核心思想是：当我们遍历到第i个数时，之前的所有数都已经处理过了，我们只需要检查当前数是否是某个之前数的"另一半"。

### 代码
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    int n = nums.length;
    for(int i = 0; i < n; i++){
        int t = nums[i];
        if(map.containsKey(t)){
            int j = map.get(t);
            return new int[]{i, j};
        }else{
            // 放个期望进去
            map.put(target - t, i);
        }
    }
    return null;
}
```

---

## 2. 两数相加
**LeetCode链接**: https://leetcode.cn/problems/add-two-numbers/

### 思路
使用虚拟头节点简化链表操作。同时遍历两个链表，逐位相加并处理进位：
1. 用两个指针`p1`和`p2`分别遍历两个链表
2. 用变量`carry`记录进位
3. 循环条件是：两个链表都没走完，或者还有进位
4. 每次计算当前位的值`val = carry + p1.val + p2.val`
5. 更新进位`carry = val / 10`，当前位值`val = val % 10`
6. 构建新节点，连接到结果链表

### 代码
```java
public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    // 在两条链表上的指针
    ListNode p1 = l1, p2 = l2;
    // 虚拟头结点（构建新链表时的常用技巧）
    ListNode dummy = new ListNode(-1);
    // 指针 p 负责构建新链表
    ListNode p = dummy;
    // 记录进位
    int carry = 0;
    // 开始执行加法，两条链表走完且没有进位时才能结束循环
    while (p1 != null || p2 != null || carry > 0) {
        // 先加上上次的进位
        int val = carry;
        if (p1 != null) {
            val += p1.val;
            p1 = p1.next;
        }
        if (p2 != null) {
            val += p2.val;
            p2 = p2.next;
        }
        // 处理进位情况
        carry = val / 10;
        val = val % 10;
        // 构建新节点
        p.next = new ListNode(val);
        p = p.next;
    }
    // 返回结果链表的头结点（去除虚拟头结点）
    return dummy.next;
}
```

---

## 3. 无重复字符的最长子串
**LeetCode链接**: https://leetcode.cn/problems/longest-substring-without-repeating-characters/

### 思路
滑动窗口经典题。使用哈希表记录窗口内各字符的出现次数：
1. 右指针不断扩展窗口，将字符加入窗口（计数+1）
2. 当某个字符出现次数大于1时，说明有重复，左指针收缩窗口
3. 每次收缩时，将左指针指向的字符计数-1，左指针右移
4. 直到该字符只出现一次为止
5. 每次更新最长长度

### 代码
```java
public int lengthOfLongestSubstring(String s) {
    int n = s.length(), ans = 0;
    Map<Character, Integer> map = new HashMap<>();
    int left = 0, right = 0;
    for (int i = 0; i < n; i++) {
        char c = s.charAt(i);
        right++;
        map.merge(c, 1, Integer::sum);
        while(map.get(c) > 1){
            char t = s.charAt(left);
            left++;
            map.merge(t, -1, Integer::sum);
        }
        ans = Math.max(ans, right - left + 1);
    }
    return ans;
}
```

---

## 4. 寻找两个正序数组的中位数
**LeetCode链接**: https://leetcode.cn/problems/median-of-two-sorted-arrays/

### 思路
中位数本质是找第k小的数。利用两个数组有序的特性，每次比较两个数组的第k/2个元素，排除较小那一侧的前k/2个元素（它们一定小于第k小），递归缩小范围。

核心优化：不必每次排除一个元素，可以每次排除k/2个元素。

边界处理：
- 数组为空时直接取另一个数组的第k个元素
- k=1时取两个数组首元素的最小值

时间复杂度O(log(m+n))。

### 代码
```java
public double findMedianSortedArrays(int[] nums1, int[] nums2) {
    int m = nums1.length;
    int n = nums2.length;
    int left = (m + n + 1) / 2; // 奇数情况
    int right = (m + n + 2) / 2;
    return (getKthNum(nums1, 0, m - 1, nums2, 0, n - 1, left) +
            getKthNum(nums1, 0, m - 1, nums2, 0, n - 1, right)) / 2.0;
}

private int getKthNum(int[] nums1, int start1, int end1, int[] nums2, int start2, int end2, int k) {
    int len1 = end1 - start1 + 1;
    int len2 = end2 - start2 + 1;
    // 保证len1 <= len2，简化边界处理
    if (len1 > len2) {
        return getKthNum(nums2, start2, end2, nums1, start1, end1, k);
    }
    if (len1 == 0) {
        return nums2[start2 + k - 1];
    }
    if (k == 1) {
        return Math.min(nums1[start1], nums2[start2]);
    }
    // k/2的速度减少
    int i = start1 + Math.min(len1, k / 2) - 1;
    int j = start2 + Math.min(len2, k / 2) - 1;
    if (nums1[i] > nums2[j]) {
        return getKthNum(nums1, start1, end1, nums2, j + 1, end2, k - (j - start2 + 1));
    } else {
        return getKthNum(nums1, i + 1, end1, nums2, start2, end2, k - (i - start1 + 1));
    }
}
```

---

## 5. 最长回文子串
**LeetCode链接**: https://leetcode.cn/problems/longest-palindromic-substring/

### 思路
中心扩展法。遍历每个字符，分别以：
1. 当前字符为中心（处理奇数长度回文串）
2. 当前字符与下一个字符之间为中心（处理偶数长度回文串）

从中心向两边扩展，当左右指针指向的字符相同时继续扩展，否则停止。记录最长的回文子串。

### 代码
```java
public String longestPalindrome(String s) {
    int n = s.length();
    String res = "";
    for(int i = 0; i < n; i++){
        String res1 = kuozhan(s, i, i);      // 奇数长度
        String res2 = kuozhan(s, i, i + 1);  // 偶数长度
        res = res.length() > res1.length() ? res : res1;
        res = res.length() > res2.length() ? res : res2;
    }
    return res;
}

private String kuozhan(String s, int left, int right) {
    // 当左右指针没有越界，并且指向的字符相同时，继续扩展
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return s.substring(left + 1, right);
}
```

---

## 7. 最大子数组和
**LeetCode链接**: https://leetcode.cn/problems/maximum-subarray/

### 思路
贪心/动态规划思想。遍历数组，累加当前元素到sum：
1. 每次累加后更新最大值
2. 如果sum小于等于0，说明对后面的和没有贡献，重置sum为0
3. 这样可以保证每一段连续的子数组和都是最大的可能值

### 代码
```java
public int maxSubArray(int[] nums){
    int n = nums.length;
    int max = nums[0];
    int sum = 0;
    for(int i = 0; i < n; i++){
        sum += nums[i];
        max = Math.max(max, sum);
        if(sum <= 0){
            sum = 0;
        }
    }
    return max;
}
```

---

## 8. 字符串转换整数 (atoi)
**LeetCode链接**: https://leetcode.cn/problems/string-to-integer-atoi/

### 思路
按步骤处理：
1. 跳过前导空格
2. 处理正负号
3. 逐个读取数字字符，拼接时判断是否越界

越界判断关键：如果`res > Integer.MAX_VALUE / 10`，或者`res == Integer.MAX_VALUE / 10`且当前数字大于7，则越界。

### 代码
```java
public int myAtoi(String s) {
    int res = 0;
    int i = 0;
    // 去除前导空格
    while (i < s.length() && s.charAt(i) == ' ') {
        i++;
    }
    // 处理正负号
    boolean isNegative = false;
    if (i < s.length() && (s.charAt(i) == '-' || s.charAt(i) == '+')) {
        isNegative = s.charAt(i) == '-';
        i++;
    }
    // 读取数字
    while (i < s.length() && Character.isDigit(s.charAt(i))) {
        int digit = s.charAt(i) - '0';
        // 判断是否越界
        if (res > Integer.MAX_VALUE / 10 || (res == Integer.MAX_VALUE / 10 && digit > 7)) {
            return isNegative ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        }
        res = res * 10 + digit;
        i++;
    }
    return isNegative ? -res : res;
}
```

---

## 11. 二叉树的层序遍历
**LeetCode链接**: https://leetcode.cn/problems/binary-tree-level-order-traversal/

### 思路
BFS广度优先搜索。使用队列实现：
1. 根节点入队
2. 每层遍历前，记录当前队列大小，这就是当前层的节点数
3. 遍历该层所有节点，将节点值加入临时列表，同时将子节点入队
4. 每层结束后将临时列表加入结果

### 代码
```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if(root == null) return res;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        List<Integer> tmp = new ArrayList<>();
        for(int i = queue.size(); i > 0; i--) {
            TreeNode node = queue.poll();
            tmp.add(node.val);
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
        }
        res.add(tmp);
    }
    return res;
}
```

---

## 12. 搜索旋转排序数组
**LeetCode链接**: https://leetcode.cn/problems/search-in-rotated-sorted-array/

### 思路
分两步走：
1. 先用二分找到旋转点（最小值位置）
   - 如果`nums[mid] > nums[right]`，最小值在mid右侧
   - 否则最小值在mid或左侧
2. 根据target与数组末尾元素的大小关系，确定target在哪个有序段中
3. 在该段中进行标准二分查找

### 代码
```java
public int search(int[] nums, int target) {
    int min = findMin(nums);
    int n = nums.length - 1;
    if(target > nums[n]){
        return findsearch(nums, 0, min - 1, target);
    }else{
        return findsearch(nums, min, n, target);
    }
}

public int findMin(int[] nums) {
    int left = 0;
    int n = nums.length;
    int right = n - 1;
    if (nums[left] < nums[right]) {
        return 0;  // 数组未旋转
    }
    while (left < right) {
        int mid = (left + right) >>> 1;
        if (nums[mid] > nums[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}

public int findsearch(int[] nums, int left, int right, int target){
    while(left <= right){
        int mid = (left + right) >>> 1;
        if(nums[mid] > target){
            right = mid - 1;
        }else if(nums[mid] < target){
            left = mid + 1;
        }else{
            return mid;
        }
    }
    return -1;
}
```

---

## 13. 岛屿数量
**LeetCode链接**: https://leetcode.cn/problems/number-of-islands/

### 思路
DFS flood fill算法。遍历网格：
1. 遇到'1'时，岛屿数量+1
2. 用DFS将与该位置相连的所有'1'变成'0'（淹没岛屿）
3. 这样可以保证每个岛屿只被计数一次

DFS函数递归地将当前位置及其上下左右的陆地变成海水。

### 代码
```java
public int numIslands(char[][] grid) {
    int n = grid.length;
    int m = grid[0].length;
    int cnt = 0;
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            if(grid[i][j] == '1'){
                dfs(grid, i, j);
                cnt++;
            }
        }
    }
    return cnt;
}

public void dfs(char[][] grid, int i, int j){
    int m = grid.length, n = grid[0].length;
    if (i < 0 || j < 0 || i >= m || j >= n) {
        return;  // 超出边界
    }
    if (grid[i][j] == '0') {
        return;  // 已经是海水
    }
    grid[i][j] = '0';  // 将陆地变成海水
    // 淹没上下左右的陆地
    dfs(grid, i + 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i - 1, j);
    dfs(grid, i, j - 1);
}
```

---

## 14. 两数之和
**LeetCode链接**: https://leetcode.cn/problems/two-sum/

### 思路
哈希表存期望值。遍历数组时，检查当前值是否在哈希表中（是否是某个之前数的期望值），如果是则找到答案，否则将期望值存入哈希表。

### 代码
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    int n = nums.length;
    for(int i = 0; i < n; i++){
        int t = nums[i];
        if(map.containsKey(t)){
            int j = map.get(t);
            return new int[]{i, j};
        }else{
            map.put(target - t, i);
        }
    }
    return null;
}
```

---

## 16. 合并两个有序数组
**LeetCode链接**: https://leetcode.cn/problems/merge-sorted-array/

### 思路
从后向前合并。因为nums1后面有多余空间，所以从两个数组的有效末尾开始比较：
1. 两个指针分别从nums1和nums2的有效末尾开始
2. 比较大小后放入nums1的末尾
3. 最后只需处理nums2剩余的元素（nums1剩余的元素本身就在正确位置）

### 代码
```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int i = m - 1, j = n - 1;
    int p = nums1.length - 1;
    while (i >= 0 && j >= 0) {
        if (nums1[i] > nums2[j]) {
            nums1[p] = nums1[i];
            i--;
        } else {
            nums1[p] = nums2[j];
            j--;
        }
        p--;
    }
    // 只需处理nums2剩余的元素
    while (j >= 0) {
        nums1[p] = nums2[j];
        j--;
        p--;
    }
}
```

---

## 17. 有效的括号
**LeetCode链接**: https://leetcode.cn/problems/valid-parentheses/

### 思路
栈的经典应用。遍历字符串：
1. 遇到左括号入栈
2. 遇到右括号时，弹出栈顶元素判断是否匹配
3. 最后检查栈是否为空（是否所有左括号都被匹配）

### 代码
```java
public boolean isValid(String s) {
    Deque<Character> st = new ArrayDeque<>();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.isEmpty()) {
                return false;
            }
            char top = st.pop();
            if (c == ')' && top != '(') return false;
            if (c == ']' && top != '[') return false;
            if (c == '}' && top != '{') return false;
        }
    }
    return st.isEmpty();
}
```

---

## 18. 买卖股票的最佳时机
**LeetCode链接**: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/

### 思路
动态规划。`dp[i][0]`表示第i天未持有股票的最大利润，`dp[i][1]`表示第i天持有股票的最大利润。

状态转移：
- `dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])` （继续不持有 或 卖出）
- `dp[i][1] = max(dp[i-1][1], -prices[i])` （继续持有 或 买入）

### 代码
```java
public int maxProfit(int[] prices) {
    int n = prices.length;
    int[][] dp = new int[n][2];
    for (int i = 0; i < n; i++) {
        if (i - 1 == -1) {
            dp[i][0] = 0;
            dp[i][1] = -prices[i];
            continue;
        }
        dp[i][0] = Math.max(dp[i - 1][0], dp[i - 1][1] + prices[i]);
        dp[i][1] = Math.max(dp[i - 1][1], -prices[i]);
    }
    return dp[n - 1][0];
}
```

---

## 19. 二叉树的最近公共祖先
**LeetCode链接**: https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/

### 思路
后序遍历。对于当前节点root：
1. 如果root是p或q，直接返回root
2. 在左右子树中查找p和q
3. 如果左右都找到了，说明root就是LCA
4. 如果只有一边找到了，返回找到的那一边

### 代码
```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || p == root || q == root) {
        return root;
    }
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left == null) return right;
    if (right == null) return left;
    return root;  // 左右都找到了，当前节点就是LCA
}
```

---

## 20. 反转链表 II
**LeetCode链接**: https://leetcode.cn/problems/reverse-linked-list-ii/

### 思路
使用虚拟头节点简化操作：
1. 找到反转区域的前一个节点p0
2. 在[left, right]范围内进行链表反转
3. 将反转后的子链表正确连接回原链表

关键点：反转后`p0.next`是反转后的尾节点，`pre`是反转后的头节点。

### 代码
```java
public ListNode reverseBetween(ListNode head, int left, int right) {
    ListNode dummy = new ListNode(-1, head);
    // 1. 找到反转区域的前一个节点 p0
    ListNode p0 = dummy;
    for (int i = 0; i < left - 1; i++) {
        p0 = p0.next;
    }
    ListNode pre = null;
    ListNode cur = p0.next;
    // 2. 反转从 left 到 right 的子链表
    for (int i = 0; i < right - left + 1; i++) {
        ListNode nxt = cur.next;
        cur.next = pre;
        pre = cur;
        cur = nxt;
    }
    // 3. 将反转后的子链表重新接回原链表
    p0.next.next = cur;
    p0.next = pre;
    return dummy.next;
}
```

---

## 21. 二叉树的锯齿形层序遍历
**LeetCode链接**: https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/

### 思路
BFS基础上增加方向标志flag：
1. 正常层序遍历
2. 每层遍历完后，根据flag决定是否翻转当前层的结果列表
3. 每层结束后反转flag

### 代码
```java
public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if(root == null) return res;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    boolean flag = true;
    while (!queue.isEmpty()) {
        List<Integer> tmp = new ArrayList<>();
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            tmp.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        if(!flag){
            Collections.reverse(tmp);
        }
        res.add(tmp);
        flag = !flag;
    }
    return res;
}
```

---

## 22. 环形链表
**LeetCode链接**: https://leetcode.cn/problems/linked-list-cycle/

### 思路
快慢指针。慢指针每次走一步，快指针每次走两步。如果快慢指针相遇，说明有环；如果快指针走到null，说明无环。

### 代码
```java
public boolean hasCycle(ListNode head) {
    if (head == null || head.next == null) {
        return false;
    }
    ListNode slow = head;
    ListNode fast = head.next;
    while (fast != null && fast.next != null) {
        if (slow == fast) {
            return true;
        }
        slow = slow.next;
        fast = fast.next.next;
    }
    return false;
}
```

---

## 23. 螺旋矩阵
**LeetCode链接**: https://leetcode.cn/problems/spiral-matrix/

### 思路
按层模拟。使用四个变量left、right、top、bottom表示当前边界：
1. 按上、右、下、左的顺序遍历
2. 每遍历完一条边就收缩对应边界
3. 直到边界交叉为止

### 代码
```java
public List<Integer> spiralOrder(int[][] matrix) {
    int n = matrix.length;
    int m = matrix[0].length;
    int left = 0, right = m - 1, top = 0, bottom = n - 1;
    List<Integer> res = new ArrayList<>();
    while(true){
        for(int i = left; i <= right; i++){
            res.add(matrix[top][i]);
        }
        top++;
        if(top > bottom) break;

        for(int i = top; i <= bottom; i++){
            res.add(matrix[i][right]);
        }
        right--;
        if(right < left) break;

        for(int i = right; i >= left; i--){
            res.add(matrix[bottom][i]);
        }
        bottom--;
        if(bottom < top) break;

        for(int i = bottom; i >= top; i--){
            res.add(matrix[i][left]);
        }
        left++;
        if(left > right) break;
    }
    return res;
}
```

---

## 24. 最长递增子序列
**LeetCode链接**: https://leetcode.cn/problems/longest-increasing-subsequence/

### 思路
动态规划。`dp[i]`表示以`nums[i]`结尾的最长递增子序列长度。

对于每个i，遍历i之前的所有元素j：
- 如果`nums[i] > nums[j]`，则`dp[i] = max(dp[i], dp[j] + 1)`

在计算dp的同时更新全局最大值。

### 代码
```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    if (n == 0) return 0;
    int[] dp = new int[n];
    int maxAns = 1;
    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxAns = Math.max(maxAns, dp[i]);
    }
    return maxAns;
}
```

---

## 25. 重排链表
**LeetCode链接**: https://leetcode.cn/problems/reorder-list/

### 思路
三步走：
1. 快慢指针找中点，将链表分成两半
2. 翻转后半部分链表
3. 合并两个链表，交替取节点

### 代码
```java
public void reorderList(ListNode head) {
    // 1. 找中间节点分成两半
    ListNode slow = head, fast = head.next;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    ListNode mid = slow.next;
    slow.next = null;
    // 2. 翻转后半部分
    ListNode pre = null;
    ListNode cur = mid;
    while (cur != null) {
        ListNode nxt = cur.next;
        cur.next = pre;
        pre = cur;
        cur = nxt;
    }
    // 3. 两个链表合并
    ListNode p0 = head;
    ListNode p1 = pre;
    while (p1 != null && p0 != null) {
        ListNode nxt0 = p0.next;
        ListNode nxt1 = p1.next;
        p0.next = p1;
        p1.next = nxt0;
        p0 = nxt0;
        p1 = nxt1;
    }
}
```

---

## 26. 合并K个升序链表
**LeetCode链接**: https://leetcode.cn/problems/merge-k-sorted-lists/

### 思路
归并排序思想。将K个链表分成两半，递归合并每半，然后将两个有序链表合并。

### 代码
```java
public ListNode mergeKLists(ListNode[] lists) {
    return merge(lists, 0, lists.length - 1);
}

private ListNode merge(ListNode[] lists, int l, int r) {
    if (l == r) return lists[l];
    if (l > r) return null;
    int mid = (l + r) / 2;
    return mergeTwoLists(merge(lists, l, mid), merge(lists, mid + 1, r));
}

private ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(-1);
    ListNode cur = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val < l2.val) {
            cur.next = l1;
            l1 = l1.next;
        } else {
            cur.next = l2;
            l2 = l2.next;
        }
        cur = cur.next;
    }
    cur.next = l1 == null ? l2 : l1;
    return dummy.next;
}
```

---

## 27. 字符串相加
**LeetCode链接**: https://leetcode.cn/problems/add-strings/

### 思路
模拟竖式加法。两个指针从后向前遍历两个字符串：
1. 计算当前位的和（包括进位）
2. 计算新的进位
3. 将当前位结果追加到StringBuilder
4. 最后反转结果

### 代码
```java
public String addStrings(String num1, String num2) {
    StringBuilder res = new StringBuilder();
    int i = num1.length() - 1;
    int j = num2.length() - 1;
    int carry = 0;
    while (i >= 0 || j >= 0 || carry != 0) {
        int digit1 = (i >= 0) ? num1.charAt(i) - '0' : 0;
        int digit2 = (j >= 0) ? num2.charAt(j) - '0' : 0;
        int sum = digit1 + digit2 + carry;
        carry = sum / 10;
        res.append(sum % 10);
        i--;
        j--;
    }
    return res.reverse().toString();
}
```

---

## 28. 相交链表
**LeetCode链接**: https://leetcode.cn/problems/intersection-of-two-linked-lists/

### 思路
双指针。p1从headA出发，p2从headB出发。当p1走到末尾时跳到headB，p2走到末尾时跳到headA。两个指针会在相交点相遇，或者同时到达null（无相交）。

原理：两个指针走过的总路程相同（a + b + c = b + a + c）。

### 代码
```java
public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    ListNode p1 = headA, p2 = headB;
    while (p1 != p2) {
        if (p1 == null) p1 = headB;
        else p1 = p1.next;
        if (p2 == null) p2 = headA;
        else p2 = p2.next;
    }
    return p1;
}
```

---

## 29. 合并区间
**LeetCode链接**: https://leetcode.cn/problems/merge-intervals/

### 思路
先按左边界排序。遍历区间，如果当前区间的左边界小于等于前一个区间的右边界，则合并（更新右边界为两者最大值）；否则将当前区间加入结果。

### 代码
```java
public int[][] merge(int[][] intervals) {
    int n = intervals.length;
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> res = new ArrayList<>();
    for(int i = 0; i < n; i++){
        int left = intervals[i][0];
        int right = intervals[i][1];
        while(i < n - 1 && right >= intervals[i + 1][0]){
            right = Math.max(right, intervals[i + 1][1]);
            i++;
        }
        res.add(new int[]{left, right});
    }
    return res.toArray(new int[res.size()][]);
}
```

---

## 30. 编辑距离
**LeetCode链接**: https://leetcode.cn/problems/edit-distance/

### 思路
动态规划。`dp[i][j]`表示word1前i个字符转换成word2前j个字符的最少操作数。

状态转移：
- 如果当前字符相等：`dp[i][j] = dp[i-1][j-1]`
- 否则：`dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1`（对应替换、删除、插入）

初始化：`dp[i][0] = i`, `dp[0][j] = j`

### 代码
```java
public int minDistance(String word1, String word2) {
    int m = word1.length();
    int n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    // 初始化
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int i = 0; i <= n; i++) dp[0][i] = i;
    // 状态转移
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1])) + 1;
            }
        }
    }
    return dp[m][n];
}
```

---

## 31. 接雨水
**LeetCode链接**: https://leetcode.cn/problems/trapping-rain-water/

### 思路
预处理左右最大值数组。对于每个位置i，它能接的雨水量等于`min(leftMax[i], rightMax[i]) - height[i]`。

其中`leftMax[i]`表示i左边（含i）的最大高度，`rightMax[i]`表示i右边（含i）的最大高度。

### 代码
```java
public int trap(int[] height) {
    int n = height.length;
    // 构造左右最大值
    int[] leftMax = new int[n];
    leftMax[0] = height[0];
    for(int i = 1; i < n; i++){
        leftMax[i] = Math.max(leftMax[i - 1], height[i]);
    }
    int[] rightMax = new int[n];
    rightMax[n - 1] = height[n - 1];
    for(int i = n - 2; i >= 0; i--){
        rightMax[i] = Math.max(rightMax[i + 1], height[i]);
    }
    // 计算每个位置的储水量
    int ans = 0;
    for(int i = 0; i < n; i++){
        ans += Math.min(leftMax[i], rightMax[i]) - height[i];
    }
    return ans;
}
```

---

## 32. 最长公共子序列
**LeetCode链接**: https://leetcode.cn/problems/longest-common-subsequence/

### 思路
动态规划。`dp[i][j]`表示text1前i个字符和text2前j个字符的最长公共子序列长度。

状态转移：
- 如果当前字符相等：`dp[i][j] = dp[i-1][j-1] + 1`
- 否则：`dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

### 代码
```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

---

## 36. 删除链表的倒数第N个节点
**LeetCode链接**: https://leetcode.cn/problems/remove-nth-node-from-end-of-list/

### 思路
快慢指针。快指针先走n步，然后快慢指针同时移动，当快指针到达末尾时，慢指针指向倒数第n+1个节点（即待删除节点的前一个节点）。

使用虚拟头节点简化删除操作。

### 代码
```java
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0, head);
    ListNode p1 = head;
    for (int i = 0; i < n; i++) {
        p1 = p1.next;
    }
    ListNode p2 = dummy;
    while (p1 != null) {
        p2 = p2.next;
        p1 = p1.next;
    }
    p2.next = p2.next.next;
    return dummy.next;
}
```

---

## 39. 二叉树的右视图
**LeetCode链接**: https://leetcode.cn/problems/binary-tree-right-side-view/

### 思路
层序遍历。每层遍历时，只将最后一个节点的值加入结果列表（当`i == size - 1`时）。

### 代码
```java
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if(root == null) return new ArrayList<>();
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while(!queue.isEmpty()){
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            if(node.left != null) queue.offer(node.left);
            if(node.right != null) queue.offer(node.right);
            if(i == size - 1){
                res.add(node.val);
            }
        }
    }
    return res;
}
```

---

## 40. 比较版本号
**LeetCode链接**: https://leetcode.cn/problems/compare-version-numbers/

### 思路
用`.`分割两个版本号得到两个数组。同时遍历两个数组，较短数组缺失的位置视为0。比较每个修订号的大小。

### 代码
```java
public int compareVersion(String version1, String version2) {
    String[] v1 = version1.split("\\.");
    String[] v2 = version2.split("\\.");
    int i = 0;
    while (i < v1.length || i < v2.length){
        int a = i < v1.length ? Integer.parseInt(v1[i]) : 0;
        int b = i < v2.length ? Integer.parseInt(v2[i]) : 0;
        if (a > b) return 1;
        if (a < b) return -1;
        i++;
    }
    return 0;
}
```

---

## 41. 缺失的第一个正数
**LeetCode链接**: https://leetcode.cn/problems/first-missing-positive/

### 思路
原地哈希。遍历数组，将每个正数x放到索引x-1的位置（通过交换实现）。处理完后再次遍历，第一个不在正确位置的索引i+1就是缺失的正数。

### 代码
```java
public int firstMissingPositive(int[] nums) {
    int n = nums.length;
    for(int i = 0; i < n; i++){
        while(nums[i] > 0 && nums[i] <= n && nums[i] != nums[nums[i] - 1]){
            int temp = nums[nums[i] - 1];
            nums[nums[i] - 1] = nums[i];
            nums[i] = temp;
        }
    }
    for(int i = 0; i < n; i++){
        if(nums[i] != i + 1){
            return i + 1;
        }
    }
    return n + 1;
}
```

---

## 42. 排序链表
**LeetCode链接**: https://leetcode.cn/problems/sort-list/

### 思路
归并排序。快慢指针找中点，将链表分成两半，递归排序两部分，然后合并两个有序链表。

### 代码
```java
public ListNode sortList(ListNode head) {
    if (head == null || head.next == null) {
        return head;
    }
    ListNode slow = head, fast = head, prev = null;
    while (fast != null && fast.next != null) {
        prev = slow;
        slow = slow.next;
        fast = fast.next.next;
    }
    prev.next = null;
    ListNode l1 = sortList(head);
    ListNode l2 = sortList(slow);
    return mergeTwoLists(l1, l2);
}

public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val < l2.val) {
            cur.next = l1;
            l1 = l1.next;
        } else {
            cur.next = l2;
            l2 = l2.next;
        }
        cur = cur.next;
    }
    cur.next = l1 != null ? l1 : l2;
    return dummy.next;
}
```

---

## 43. 字符串相乘
**LeetCode链接**: https://leetcode.cn/problems/multiply-strings/

### 思路
模拟竖式乘法。使用一个长度为m+n的数组存储结果。`nums1[i] * nums2[j]`的结果应该放在`res[i+j]`和`res[i+j+1]`两个位置。从后向前遍历两个字符串，计算乘积并处理进位。

### 代码
```java
public String multiply(String num1, String num2) {
    if (num1.equals("0") || num2.equals("0")) {
        return "0";
    }
    int[] res = new int[num1.length() + num2.length()];
    for (int i = num1.length() - 1; i >= 0; i--) {
        for (int j = num2.length() - 1; j >= 0; j--) {
            int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');
            int p1 = i + j, p2 = i + j + 1;
            int sum = mul + res[p2];
            res[p1] += sum / 10;
            res[p2] = sum % 10;
        }
    }
    int i = 0;
    if (res[i] == 0) i++;
    StringBuilder sb = new StringBuilder();
    for (; i < res.length; i++) {
        sb.append(res[i]);
    }
    return sb.toString();
}
```

---

## 44. 二分查找
**LeetCode链接**: https://leetcode.cn/problems/binary-search/

### 思路
标准二分。在`[left, right]`范围内查找，每次计算mid，根据`nums[mid]`与target的大小关系调整左右边界。

### 代码
```java
public int search(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while(left <= right){
        int mid = left + (right - left) / 2;
        if(nums[mid] == target){
            return mid;
        }else if(nums[mid] < target){
            left = mid + 1;
        }else{
            right = mid - 1;
        }
    }
    return -1;
}
```

---

## 45. 二叉树的中序遍历
**LeetCode链接**: https://leetcode.cn/problems/binary-tree-inorder-traversal/

### 思路
递归实现。按照左子树 -> 根节点 -> 右子树的顺序遍历。使用一个结果列表在递归过程中收集节点值。

### 代码
```java
public List<Integer> inorderTraversal(TreeNode root) {
    if(root == null) return new ArrayList<>();
    List<Integer> res = new ArrayList<>();
    dfs(root, res);
    return res;
}

private void dfs(TreeNode root, List<Integer> res) {
    if(root == null) return;
    dfs(root.left, res);
    res.add(root.val);
    dfs(root.right, res);
}
```

---

## 46. x 的平方根
**LeetCode链接**: https://leetcode.cn/problems/sqrtx/

### 思路
二分查找。在`[1, x/2]`范围内查找，如果mid的平方等于x则返回mid；如果mid的平方大于x则在左半部分找；否则在右半部分找。最后返回right（向下取整）。

### 代码
```java
public int mySqrt(int x) {
    if (x <= 1) return x;
    int left = 1;
    int right = x / 2;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (mid == x / mid) {
            return mid;
        } else if (mid > x / mid) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return right;
}
```

---

## 47. 滑动窗口最大值
**LeetCode链接**: https://leetcode.cn/problems/sliding-window-maximum/

### 思路
单调队列。维护一个双端队列，存储索引。队列保持递减（从队首到队尾）：
1. 每次添加新元素时，将队列中所有小于新元素的元素弹出
2. 当队首索引超出窗口范围时弹出
3. 窗口形成后，队首即为最大值

### 代码
```java
public int[] maxSlidingWindow(int[] nums, int k) {
    if (nums == null || nums.length == 0) {
        return new int[0];
    }
    int[] res = new int[nums.length - k + 1];
    int n = nums.length;
    Deque<Integer> q = new LinkedList<>();
    for (int i = 0; i < n; i++) {
        while(!q.isEmpty() && nums[i] > nums[q.getLast()]){
            q.removeLast();
        }
        q.addLast(i);
        if(!q.isEmpty() && q.getFirst() <= i - k){
            q.removeFirst();
        }
        int left = i - k + 1;
        if(left >= 0){
            res[left] = nums[q.getFirst()];
        }
    }
    return res;
}
```

---

## 48. 最长有效括号
**LeetCode链接**: https://leetcode.cn/problems/longest-valid-parentheses/

### 思路
使用栈。栈底始终保存一个基准位置（初始为-1）：
1. 遇到左括号将索引入栈
2. 遇到右括号先弹出栈顶
3. 如果栈非空，计算当前位置与栈顶的距离即为有效长度
4. 如果栈为空，将当前位置入栈作为新的基准位置

### 代码
```java
public int longestValidParentheses(String s) {
    int n = s.length();
    Stack<Integer> stack = new Stack<>();
    int res = 0;
    stack.push(-1);
    for(int i = 0; i < n; i++){
        if(s.charAt(i) == '(') {
            stack.push(i);
        } else {
            stack.pop();
            if(!stack.isEmpty()) {
                res = Math.max(res, i - stack.peek());
            } else {
                stack.push(i);
            }
        }
    }
    return res;
}
```

---

## 49. 下一个排列
**LeetCode链接**: https://leetcode.cn/problems/next-permutation/

### 思路
1. 从右向左找到第一个小于右侧相邻数字的数`nums[i]`
2. 如果存在，再从右向左找到第一个大于`nums[i]`的数`nums[j]`，交换两者
3. 将i后面的元素升序排列（直接sort即可）

### 代码
```java
public void nextPermutation(int[] nums) {
    int n = nums.length;
    int i = n - 2;
    for(; i >= 0; i--){
        if(nums[i] < nums[i + 1]){
            break;
        }
    }
    if(i >= 0){
        int j = n - 1;
        for(; j >= 0; j--){
            if(nums[j] > nums[i]){
                break;
            }
        }
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    Arrays.sort(nums, i + 1, n);
}
```

---

## 50. 括号生成
**LeetCode链接**: https://leetcode.cn/problems/generate-parentheses/

### 思路
回溯法。维护左右括号剩余数量：
- 每次选择放左括号或右括号
- 剪枝条件：左括号剩余数量大于右括号时返回（说明右括号放多了）
- 当左右括号都用完时，将当前字符串加入结果集

### 代码
```java
public List<String> generateParenthesis(int n) {
    List<String> res = new ArrayList<>();
    dfs(res, "", n, n);
    return res;
}

public void dfs(List<String> res, String s, int left, int right){
    if (left == 0 && right == 0){
        res.add(s);
        return;
    }
    if (left > right) return;
    if (left > 0) dfs(res, s + "(", left - 1, right);
    if (right > 0) dfs(res, s + ")", left, right - 1);
}
```

---

## 51. 删除排序链表中的重复元素 II
**LeetCode链接**: https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/

### 思路
使用虚拟头节点。pre指针指向已处理部分的最后一个节点，cur指针向后遍历找重复元素的末尾。如果cur移动了（说明有重复），则`pre.next`直接跳过所有重复节点。

### 代码
```java
public ListNode deleteDuplicates(ListNode head) {
    ListNode dummy = new ListNode(-1, head);
    ListNode pre = dummy;
    while (pre.next != null) {
        ListNode cur = pre.next;
        while (cur.next != null && cur.val == cur.next.val) {
            cur = cur.next;
        }
        if (cur != pre.next) {
            pre.next = cur.next;
        } else {
            pre = pre.next;
        }
    }
    return dummy.next;
}
```

---

## 53. 零钱兑换
**LeetCode链接**: https://leetcode.cn/problems/coin-change/

### 思路
完全背包问题。`dp[i]`表示凑成金额i所需的最少硬币数，初始化为`amount+1`表示不可达。

遍历所有金额，对每个金额尝试所有硬币，状态转移：`dp[i] = min(dp[i], dp[i-coins[j]] + 1)`

### 代码
```java
public int coinChange(int[] coins, int amount) {
    if(coins.length == 0) return -1;
    int[] memo = new int[amount+1];
    Arrays.fill(memo, amount+1);
    memo[0] = 0;
    for(int i = 1; i <= amount; i++){
        for(int j = 0; j < coins.length; j++){
            if(i - coins[j] >= 0){
                memo[i] = Math.min(memo[i], memo[i - coins[j]] + 1);
            }
        }
    }
    return memo[amount] == (amount+1) ? -1 : memo[amount];
}
```

---

## 55. 最小覆盖子串
**LeetCode链接**: https://leetcode.cn/problems/minimum-window-substring/

### 思路
滑动窗口。使用两个哈希表need和window记录需要的字符和窗口中的字符。右指针扩展窗口，当窗口满足条件时，左指针收缩窗口并更新最小覆盖子串的起始位置和长度。

### 代码
```java
public String minWindow(String s, String t) {
    Map<Character, Integer> need = new HashMap<>();
    Map<Character, Integer> window = new HashMap<>();
    for (char c : t.toCharArray()) {
        need.put(c, need.getOrDefault(c, 0) + 1);
    }
    int left = 0, right = 0;
    int valid = 0;
    int start = 0, len = Integer.MAX_VALUE;
    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        if (need.containsKey(c)) {
            window.put(c, window.getOrDefault(c, 0) + 1);
            if (window.get(c).equals(need.get(c)))
                valid++;
        }
        while (valid == need.size()) {
            if (right - left < len) {
                start = left;
                len = right - left;
            }
            char d = s.charAt(left);
            left++;
            if (need.containsKey(d)) {
                if (window.get(d).equals(need.get(d)))
                    valid--;
                window.put(d, window.get(d) - 1);
            }
        }
    }
    return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
}
```

---

## 56. 环形链表 II
**LeetCode链接**: https://leetcode.cn/problems/linked-list-cycle-ii/

### 思路
快慢指针找相遇点，然后从头出发一个新指针与慢指针同步移动，相遇点即为环的入口。

数学推导：相遇后，从头到入口的距离等于从相遇点到入口的距离。

### 代码
```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            break;
        }
    }
    if (fast == null || fast.next == null) {
        return null;
    }
    slow = head;
    while (slow != fast) {
        slow = slow.next;
        fast = fast.next;
    }
    return slow;
}
```

---

## 58. 子集
**LeetCode链接**: https://leetcode.cn/problems/subsets/

### 思路
回溯法。每次进入递归时先将当前路径加入结果。然后从start位置开始遍历，做出选择后递归处理下一层，然后撤销选择。

### 代码
```java
List<List<Integer>> result = new ArrayList<>();
public List<List<Integer>> subsets(int[] nums) {
    dfs(nums, 0, new ArrayList<>());
    return result;
}

private void dfs(int[] nums, int start, List<Integer> track) {
    result.add(new ArrayList<>(track));
    for (int i = start; i < nums.length; i++) {
        track.add(nums[i]);
        dfs(nums, i + 1, track);
        track.remove(track.size() - 1);
    }
}
```

---

## 59. 链表中倒数第k个节点
**LeetCode链接**: https://leetcode.cn/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/

### 思路
快慢指针。快指针先走k步，然后快慢指针同时移动，当快指针到达末尾时，慢指针就是倒数第k个节点。

### 代码
```java
public ListNode trainingPlan(ListNode head, int cnt) {
    ListNode slow = head;
    ListNode fast = head;
    for (int i = 0; i < cnt; i++) {
        fast = fast.next;
    }
    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }
    return slow;
}
```

---

## 60. 反转字符串中的单词
**LeetCode链接**: https://leetcode.cn/problems/reverse-words-in-a-string/

### 思路
先trim去除首尾空格，然后用正则`\\s+`分割字符串得到单词列表，反转列表，最后用空格连接。

### 代码
```java
public String reverseWords(String s) {
    s = s.trim();
    List<String> wordList = Arrays.asList(s.split("\\s+"));
    Collections.reverse(wordList);
    return String.join(" ", wordList);
}
```

---

## 70. 爬楼梯
**LeetCode链接**: https://leetcode.cn/problems/climbing-stairs/

### 思路
动态规划。`dp[i]`表示爬到第i阶的方法数。状态转移方程：`dp[i] = dp[i-1] + dp[i-2]`。初始化`dp[0]=dp[1]=1`。

### 代码
```java
public int climbStairs(int n) {
    int[] dp = new int[n + 1];
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}
```

---

## 82. 删除排序链表中的重复元素 II
**LeetCode链接**: https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/

### 思路
使用虚拟头节点。pre指针指向已处理部分的最后一个节点，cur指针向后遍历找重复元素的末尾。如果cur移动了（说明有重复），则`pre.next`直接跳过所有重复节点。

### 代码
```java
public ListNode deleteDuplicates(ListNode head) {
    ListNode dummy = new ListNode(-1, head);
    ListNode pre = dummy;
    while (pre.next != null) {
        ListNode cur = pre.next;
        while (cur.next != null && cur.val == cur.next.val) {
            cur = cur.next;
        }
        if (cur != pre.next) {
            pre.next = cur.next;
        } else {
            pre = pre.next;
        }
    }
    return dummy.next;
}
```

---

## 105. 从前序与中序遍历序列构造二叉树
**LeetCode链接**: https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

### 思路
递归。前序遍历的第一个元素是根节点，在中序遍历中找到该根节点的位置，左边是左子树，右边是右子树。用哈希表存储中序遍历中值到索引的映射，递归构建左右子树。

### 代码
```java
Map<Integer, Integer> inorderMap = new HashMap<>();
public TreeNode buildTree(int[] preorder, int[] inorder) {
    if (preorder == null || inorder == null || preorder.length != inorder.length) {
        return null;
    }
    for (int i = 0; i < inorder.length; i++) {
        inorderMap.put(inorder[i], i);
    }
    return buildTree(preorder, 0, preorder.length - 1, inorder, 0, inorder.length - 1);
}

private TreeNode buildTree(int[] preorder, int preStart, int preEnd, int[] inorder, int inStart, int inEnd) {
    if (preStart > preEnd || inStart > inEnd) {
        return null;
    }
    int rootIndex = inorderMap.get(preorder[preStart]);
    TreeNode root = new TreeNode(preorder[preStart]);
    root.left = buildTree(preorder, preStart + 1, preStart + (rootIndex - inStart), inorder, inStart, rootIndex - 1);
    root.right = buildTree(preorder, preStart + (rootIndex - inStart) + 1, preEnd, inorder, rootIndex + 1, inEnd);
    return root;
}
```

---

## 124. 二叉树中的最大路径和
**LeetCode链接**: https://leetcode.cn/problems/binary-tree-maximum-path-sum/

### 思路
后序遍历。对于每个节点，计算以该节点为根的最大路径和（左子树贡献 + 右子树贡献 + 当前节点值），更新全局最大值。返回当前节点能向上贡献的最大值（`max(左贡献, 右贡献) + 当前值`，负数则取0）。

### 代码
```java
int res = Integer.MIN_VALUE;
public int maxPathSum(TreeNode root) {
    dfs(root);
    return res;
}

public int dfs(TreeNode root){
    if(root == null) return 0;
    int left = Math.max(dfs(root.left), 0);
    int right = Math.max(dfs(root.right), 0);
    res = Math.max(res, left + right + root.val);
    return Math.max(left, right) + root.val;
}
```

---

## 206. 反转链表
**LeetCode链接**: https://leetcode.cn/problems/reverse-linked-list/

### 思路
迭代。使用pre、cur、nxt三个指针。每次将`cur.next`指向pre，然后三个指针依次后移。最后pre指向反转后的头节点。

### 代码
```java
public ListNode reverseList(ListNode head) {
    ListNode pre = null;
    ListNode cur = head;
    while(cur != null){
        ListNode nxt = cur.next;
        cur.next = pre;
        pre = cur;
        cur = nxt;
    }
    return pre;
}
```

---

## 215. 数组中的第K个最大元素
**LeetCode链接**: https://leetcode.cn/problems/kth-largest-element-in-an-array/

### 思路
小顶堆。维护一个大小为k的小顶堆，遍历数组将元素加入堆，当堆大小超过k时弹出堆顶。最终堆顶就是第k大的元素。

### 代码
```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> p = new PriorityQueue<>();
    for(int c : nums){
        p.offer(c);
        if(p.size() > k){
            p.poll();
        }
    }
    return p.peek();
}
```

---

## 232. 用栈实现队列
**LeetCode链接**: https://leetcode.cn/problems/implement-queue-using-stacks/

### 思路
使用两个栈模拟队列。stack1作为输入栈用于push操作，stack2作为输出栈用于pop和peek操作。pop/peek时需要将stack1的元素全部转移到stack2中，获取stack2顶部元素后再移回。

### 代码
```java
class MyQueue {
    Stack<Integer> stack1;  // 输入栈
    Stack<Integer> stack2;  // 输出栈

    public MyQueue() {
        stack1 = new Stack<>();
        stack2 = new Stack<>();
    }

    public void push(int x) {
        stack1.push(x);
    }

    public int pop() {
        while(!stack1.isEmpty()){
            stack2.push(stack1.pop());
        }
        int res = stack2.pop();
        while(!stack2.isEmpty()){
            stack1.push(stack2.pop());
        }
        return res;
    }

    public int peek() {
        while(!stack1.isEmpty()){
            stack2.push(stack1.pop());
        }
        int res = stack2.peek();
        while(!stack2.isEmpty()){
            stack1.push(stack2.pop());
        }
        return res;
    }

    public boolean empty() {
        return stack1.isEmpty();
    }
}
```

---

## 146. LRU缓存
**LeetCode链接**: https://leetcode.cn/problems/lru-cache/

### 思路
使用LinkedHashMap实现。LinkedHashMap内部维护了插入顺序，可以通过重新插入来更新访问顺序。

- get时：先检查是否存在，存在则重新插入（更新顺序）后返回
- put时：如果已存在则先删除，如果满了则删除最早插入的，然后插入新元素

### 代码
```java
class LRUCache{
    int capacity;
    Map<Integer, Integer> cache;
    LRUCache(int capacity){
        this.capacity = capacity;
        cache = new LinkedHashMap<>();
    }
    public int get(int key){
        if (!cache.containsKey(key)){
            return -1;
        }
        makeRecent(key);
        return cache.get(key);
    }
    private void makeRecent(int key){
        int value = cache.get(key);
        cache.remove(key);
        cache.put(key, value);
    }
    public void put(int key, int value){
        if (cache.containsKey(key)){
            cache.remove(key);
        } else if (cache.size() == capacity){
            cache.remove(cache.keySet().iterator().next());
        }
        cache.put(key, value);
    }
}
```

---

## 46. 全排列
**LeetCode链接**: https://leetcode.cn/problems/permutations/

### 思路
回溯法。使用used数组标记元素是否已使用。递归终止条件是path长度等于nums长度。每层遍历所有未使用的元素，做出选择后递归，然后撤销选择。

### 代码
```java
private List<List<Integer>> res = new ArrayList<>();
private boolean[] used;

public List<List<Integer>> permute(int[] nums) {
    if (nums == null || nums.length == 0) {
        return res;
    }
    used = new boolean[nums.length];
    dfs(nums, new ArrayList<>());
    return res;
}

private void dfs(int[] nums, List<Integer> path) {
    if (path.size() == nums.length) {
        res.add(new ArrayList<>(path));
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        path.add(nums[i]);
        used[i] = true;
        dfs(nums, path);
        path.remove(path.size() - 1);
        used[i] = false;
    }
}
```

---

## 25. K个一组翻转链表
**LeetCode链接**: https://leetcode.cn/problems/reverse-nodes-in-k-group/

### 思路
先统计链表长度n。使用虚拟头节点，每k个节点进行一次翻转。翻转时使用头插法，记录翻转后的头尾节点，将其正确连接到原链表中。更新p0指针到翻转后的尾节点位置，继续处理下一组。

### 代码
```java
public ListNode reverseKGroup(ListNode head, int k){
    ListNode dummy = new ListNode(0, head);
    ListNode p0 = dummy;
    ListNode pre = null;
    ListNode cur = head;
    int n = 0;
    for(; cur != null; cur = cur.next){
        n++;
    }
    cur = head;
    for(; n >= k; n -= k){
        pre = null;
        for(int i = 0; i < k; i++){
            ListNode next = cur.next;
            cur.next = pre;
            pre = cur;
            cur = next;
        }
        ListNode tmp = p0.next;
        p0.next = pre;
        tmp.next = cur;
        p0 = tmp;
    }
    return dummy.next;
}
```

---

## 912. 排序数组
**LeetCode链接**: https://leetcode.cn/problems/sort-an-array/

### 思路
快速排序。随机选择基准元素，进行partition操作，将小于基准的放左边，大于基准的放右边，递归处理左右两部分。

### 代码
```java
public int[] sortArray(int[] nums) {
    if (nums == null || nums.length == 0) {
        return nums;
    }
    quickSort(nums, 0, nums.length - 1);
    return nums;
}

public void quickSort(int[] nums, int left, int right) {
    if (left < right) {
        int randomIndex = left + new Random().nextInt(right - left + 1);
        swap(nums, left, randomIndex);
        int pivotIndex = partition(nums, left, right);
        quickSort(nums, left, pivotIndex - 1);
        quickSort(nums, pivotIndex + 1, right);
    }
}

public int partition(int[] arr, int low, int high) {
    int pivot = arr[low];
    int i = low + 1;
    int j = high;
    while (i <= j) {
        while (i <= high && arr[i] <= pivot) i++;
        while (j > low && arr[j] > pivot) j--;
        if (i < j) swap(arr, i, j);
    }
    swap(arr, low, j);
    return j;
}

private void swap(int[] arr, int i, int j) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}
```

---

## 21. 合并两个有序链表
**LeetCode链接**: https://leetcode.cn/problems/merge-two-sorted-lists/

### 思路
使用虚拟头节点。用两个指针分别遍历两个链表，比较当前节点值，将较小的节点接到结果链表上。最后将剩余未遍历完的链表直接接到结果链表末尾。

### 代码
```java
public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    ListNode l = new ListNode();
    ListNode c = l;
    while(list1 != null && list2 != null){
        if(list1.val < list2.val){
            l.next = list1;
            list1 = list1.next;
        }else{
            l.next = list2;
            list2 = list2.next;
        }
        l = l.next;
    }
    l.next = list1 == null ? list2 : list1;
    return c.next;
}
```

---

## 多线程题目

### PrintABC - 交替打印ABC
**思路**: 使用synchronized和wait/notifyAll机制。维护一个flag变量表示当前应该打印哪个字母（0:A, 1:B, 2:C）。每个线程打印自己的字母后，更新flag并唤醒其他线程，然后自己等待。

```java
public class PrintABC {
    private static final Object lock = new Object();
    private static int flag = 0; // 0:A, 1:B, 2:C

    public static void main(String[] args) {
        new Thread(() -> print("A", 0, 1), "Thread-A").start();
        new Thread(() -> print("B", 1, 2), "Thread-B").start();
        new Thread(() -> print("C", 2, 0), "Thread-C").start();
    }

    private static void print(String letter, int currentFlag, int nextFlag) {
        for (int i = 0; i < 5; i++) {
            synchronized (lock) {
                while (flag != currentFlag) { // 用while防止虚假唤醒
                    try {
                        lock.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                System.out.println(Thread.currentThread().getName() + " - " + letter);
                flag = nextFlag;
                lock.notifyAll();
            }
        }
    }
}
```

### PrintNumber - 交替打印数字
**思路**: 使用synchronized和wait/notifyAll机制。两个线程交替打印，打印后唤醒对方线程，然后自己等待，直到打印完100。

```java
public class PrintNumber {
    private static final Object lock = new Object();
    private static int i = 0;

    public static void main(String[] args) {
        new Thread(() -> printNumber(), "Even-Thread").start();
        new Thread(() -> printNumber(), "Odd-Thread").start();
    }

    private static void printNumber() {
        while (i <= 100) {
            synchronized (lock) {
                System.out.println(Thread.currentThread().getName() + " - " + i++);
                lock.notifyAll();
                if (i <= 100) {
                    try {
                        lock.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}
```

---

## 总结

本文档共收录 **60道 LeetCode 热题**，涵盖以下算法类型：
- **链表**: 反转、合并、环检测、双指针
- **二叉树**: 遍历、构造、LCA、路径和
- **动态规划**: 背包、股票、子序列、编辑距离
- **滑动窗口**: 最长子串、最小覆盖子串
- **回溯**: 全排列、子集、括号生成
- **二分查找**: 基础二分、旋转数组
- **图论**: 岛屿数量（DFS）
- **多线程**: wait/notifyAll 机制
