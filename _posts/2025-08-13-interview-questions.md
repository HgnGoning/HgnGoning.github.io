---
title: 牛客面试题
date: 2025-08-13 19:41:32
tags:
  - 面试
  - TTDB
---

## pdd

### 一、Java基础与JVM（6题）

- HashMap扩容时链表转红黑树的阈值为什么是8？退化为6的原因？

​	Java 的 `HashMap`在决定链表长度阈值时，参考了 **泊松分布**,退化为6主要是避免为了重复转化留有缓冲的余地

- synchronized锁升级过程？

​	JDK1.6之后引入，对象刚创建时处于无锁状态，当有一个线程来访问同步代码块的时候此时无竞争，标记为偏向锁，当第二个线程过来竞争，得不到会自旋避免线程阻塞，此时为轻量级锁，当有多个线程过来，此时会升级重量级锁，会被挂起等待，等待唤醒

- G1垃圾回收器如何预测停顿时间？Region大小如何设置？

​	G1通过 **分Region回收 + 停顿预测模型** 来实现近似实时的垃圾回收。

​	G1的Region大小直接影响 **内存分配粒度** 和 **回收效率**。

- volatile能否保证数组元素的可见性？如何解决？

​	不能直接保证数组元素的可见性。原因如下：volatile修饰的是 数组引用本身，而不是数组的 内部元素。如果多个线程修改数组的不同元素，volatile只能保证 数组引用的可见性，但无法保证 元素修改的可见性。

​	使用 `AtomicIntegerArray`，内部使用 `volatile`+ `Unsafe`保证 每个元素的原子性和可见性。

使用 `synchronized`或 `ReentrantLock`对整个数组操作加锁，保证 原子性 + 可见性。

- ThreadLocal内存泄漏的根本原因？JDK改进方案？

​	ThreadLocal的内存泄漏问题主要源于 ThreadLocalMap 的弱引用设计 + 线程长期存活，导致 ThreadLocal对象和 value无法被回收。ThreadLocal被回收但是其中的entry，key是弱引用会被回收，但value是强引用不会被回收，线程池场景下会导致大量无用Entry,会导致OOM。

1. Entry`使用弱引用（`WeakReference`）
   - 确保 `ThreadLocal`对象在无强引用时能被 GC 回收。
2. set()/ get()/ remove()时清理无效 Entry
   - 调用这些方法时，会检查 `key == null`的 `Entry`，并清理其 `value`（`expungeStaleEntry`）。

- java 8中Stream的并行处理原理？ForkJoinPool工作窃取机制？

​	Java 8 的 `Stream`并行处理基于 ForkJoinPool 实现，核心思想是 分治（Divide-and-Conquer）。会有Spliterator可分割迭代器拆分数据，然后每个分片提交ForkJoinPool线程池中工作，最后合并。

​	每个线程会维护一个双端队列，线程从队头取任务，空闲线程会从队尾去窃取任务

### 二、并发编程（5题）

- AQS中为什么用CLH队列而不用普通链表？

​	CLH队列每个节点会维护节点状态，前驱和后继节点，可以通过前驱节点的状态判断是不是该轮到自己来获得锁，是一种公平锁，能够更好的适应高并发。普通链表，若想实现公平锁需要额外的同步机制并且不知道是不是该轮到自己

- 线程池核心参数设置规则？美团动态调整方案？

​	核心，最大线程数，存活时间，任务队列，拒绝策略

​	美团将参数外部化，`corePoolSize`、`maxPoolSize`、`queueCapacity`等参数存入配置中心，监听配置变更，然后使用setCorePoolsize会触发线程变更无需重启应用。

- ConcurrentHashMap的size()方法为何不精确？替代方案？

​	高并发下统计代价过大，必须全局加锁，会严重影响性能，同时ConcurrentHashMap设计目标是高并发和弱一致性，size的值可能瞬间过期，其他线程可能正在修改。

​	 **`mappingCount()`**比size好点，阻塞所有操作统计一次，搞一个自定义的插入增加删除递减

- 如何用CAS实现一个无锁栈？ABA问题如何规避？

无锁栈的核心是通过 **CAS（Compare-And-Swap）** 原子操作实现线程安全的 `push`和 `pop`，避免传统锁的性能开销。

```java
import java.util.concurrent.atomic.AtomicReference;

public class LockFreeStack<T> {
    private AtomicReference<Node<T>> top = new AtomicReference<>();

    // 入栈
    public void push(T value) {
        Node<T> newNode = new Node<>(value);
        Node<T> oldTop;
        do {
            oldTop = top.get();      // 读取当前栈顶
            newNode.next = oldTop;   // 新节点指向旧栈顶
        } while (!top.compareAndSet(oldTop, newNode)); // CAS 更新栈顶
    }

    // 出栈
    public T pop() {
        Node<T> oldTop;
        Node<T> newTop;
        do {
            oldTop = top.get();      // 读取当前栈顶
            if (oldTop == null) {
                return null;         // 栈为空
            }
            newTop = oldTop.next;    // 新栈顶为旧栈顶的下一个节点
        } while (!top.compareAndSet(oldTop, newTop)); // CAS 更新栈顶
        return oldTop.value;
    }

  	//节点
    class Node<T> {
    T value;
    Node<T> next;

    public Node(T value) {
        this.value = value;
    }
	}
}
```

- **`push`**：
  1. 创建新节点，其 `next`指向当前栈顶。
  2. 通过 CAS 将 `top`从旧栈顶更新为新节点。
  3. 如果 CAS 失败（其他线程修改了栈顶），重试。

- **`pop`**：
  1. 读取当前栈顶，若为空则返回 `null`。
  2. 通过 CAS 将 `top`更新为栈顶的下一个节点。
  3. 如果 CAS 失败（其他线程修改了栈顶），重试。

ABA：

- **场景**：
  - 线程 1 读取栈顶为 `A`。
  - 线程 2 弹出 `A`，然后压入 `B`、`A`，栈顶又变回 `A`。
  - 线程 1 执行 CAS，发现栈顶仍是 `A`，操作成功，但实际栈已被修改。

版本号引入:判断是否为栈顶是不使用版本号会出现ABA问题

```java
import java.util.concurrent.atomic.AtomicStampedReference;

public class LockFreeStackABAFree<T> {
    private static class Node<T> {
        T value;
        Node<T> next;
        public Node(T value) {
            this.value = value;
        }
    }

    private AtomicStampedReference<Node<T>> top =
        new AtomicStampedReference<>(null, 0);

    public void push(T value) {
        Node<T> newNode = new Node<>(value);
        int[] stampHolder = new int[1];
        Node<T> oldTop;
        do {
            oldTop = top.get(stampHolder);
            newNode.next = oldTop;
        } while (!top.compareAndSet(oldTop, newNode, stampHolder[0], stampHolder[0] + 1));
    }

    public T pop() {
        int[] stampHolder = new int[1];
        Node<T> oldTop;
        Node<T> newTop;
        do {
            oldTop = top.get(stampHolder);
            if (oldTop == null) {
                return null;
            }
            newTop = oldTop.next;
        } while (!top.compareAndSet(oldTop, newTop, stampHolder[0], stampHolder[0] + 1));
        return oldTop.value;
    }
}
```

- CompletableFuture如何实现多个异步任务依赖执行？

​	这个确实不知道干嘛的

### 三、数据库与Redis

- MySQL索引失效的10种场景？最左前缀原则的底层原理？

​	（这不是妥妥的纯八股吗）

1. ​	**违反最左前缀原则**
2. ​	**在索引列上使用函数或计算**
3. ​	**隐式类型转换**
4. ​	**使用 `!=`或 `NOT IN`**
5. ​	**`LIKE`以通配符开头**
6. ​	**使用 `OR`连接非索引列**
7. ​	**联合索引中范围查询后的列失效**
8. ​	**数据分布不均导致优化器放弃索引**
9. ​	**使用 `IS NULL`或 `IS NOT NULL`**
10. ​	**索引列参与数学运算**

​	最左前缀原则的底层原理：

​		**规则**：查询必须从联合索引的最左列开始，且不能跳过中间列。

​		**原因**：

​			B+树的排序方式决定了必须按索引定义的顺序匹配。

​			跳过 `a`直接查 `b`时，`b`是无序的，无法利用索引。

- 十亿级订单表如何优化分页查询？
- Redis大Key删除导致集群崩溃，如何避免？

​	避免直接删除大key,redis单线程模型下del大key会长时间占用主席那成，导致气压请求超时，若大Key分布在多个节点，同时删除可能导致多个实例阻塞。

​	首先避免产生大key, 设计是可以拆分大key.如果非要删除大key,那么可以将Key备份到磁盘在异步删除？？(不太确定)

- Redis事务与MySQL事务的ACID区别？

​	Redis追求高性能，MySQL强调数据安全

​	A：原子性，redis的每个命令都是原子的，事务内失败不会回滚，但Mysql会

​	C：一致性，redis弱一致性，主从同步或集群可以出现短暂不一致，Mysql强一致性，通过redo log恢复一致。

​	I：隔离性，redis天然单线程，串行化执行，无锁机制，mysql有四种隔离级别

​	D：持久性，redisAOF+RDB，mysql严格持久，通过日志来redolog,双写缓冲

- 缓存与数据库一致性方案对比？拼多多秒杀采用哪种？

| **方案** | **实现方式** | **优点** | **缺点** | **适用场景** |
| --- | --- | --- | --- | --- |
| **Cache Aside** | 读：先读缓存，未命中读DB再回写缓存 写：先更新DB，再删除缓存 | 简单易实现，高并发读友好 | 存在短暂不一致（删除缓存失败时） | 读多写少（如商品详情） |
| **Read Through** | 缓存代理层自动处理：读请求直接由缓存处理，未命中时缓存从DB加载并返回 | 业务代码简洁 | 需缓存组件支持（如Redis Module） | 缓存层可控的系统 |
| **Write Through** | 写请求先更新缓存，缓存同步更新DB（缓存层控制） | 强一致性 | 写性能下降，缓存组件需支持 | 写一致性要求高的场景 |
| **Write Behind** | 写请求只更新缓存，缓存异步批量更新DB | 极高写入性能 | 数据可能丢失（缓存宕机） | 写密集型（如日志、计数） |
| **双删策略** | 写DB → 删缓存 → 延迟几百毫秒 → 再次删缓存 | 降低不一致时间 | 延迟删除时间难确定 | 高并发写场景（如秒杀） |
| **分布式锁** | 写DB和缓存时加锁（如Redisson） | 强一致性 | 性能下降，复杂度高 | 金融交易等严格一致性场景 |

​	**组合方案：Cache Aside + 双删 + 本地缓存**

- **读流程**：
  1. 先读本地缓存（如Guava Cache）→ 命中则返回。
  2. 未命中则读Redis → 仍未命中则读DB并回写Redis（设置较短过期时间，如5秒）。

- **写流程**：
  1. 更新DB（扣减库存）。
  2. 删除Redis缓存。
  3. 延迟500ms再次删除缓存（防脏读）。

- **优化点**：
  - **库存预热**：秒杀前将商品库存加载到Redis（用 `DECR`原子扣减）。
  - **本地缓存**：减少Redis压力（但需短过期时间，如500ms）。
  - **限流**：前端队列 + Redis Lua脚本限流（防超卖）。

- Redis Cluster的slot迁移过程会阻塞请求吗？

- MySQL死锁排查步骤？如何用gap锁解决幻读？

### 四、分布式与微服务（6题）

TCC事务的Confirm阶段失败怎么办？
如何设计一个支撑百万QPS的分布式ID生成器？
Nacos如何实现配置动态推送？长轮询原理？
RocketMQ如何保证消息不丢失？
Dubbo的泛化调用使用场景？如何实现服务降级？
CAP理论在拼多多购物车中的取舍？

### 五、系统设计（4题）

设计拼多多砍价系统，如何防止刷单？
订单超时未支付自动关闭，如何实现？
如何设计一个实时热卖排行榜？
分布式锁在库存扣减中的应用，Redisson实现原理

## 小厂

#### 请解释Java中的synchronized和ReentrantLock的区别

synchronized是JVM内置锁会自动释放不可中断且是非公平锁而ReentrantLock需要手动释放锁可以中断可以设置为公平锁还提供Condition条件变量在需要更精细控制时使用ReentrantLock更合适但要注意避免忘记释放锁

#### Spring Boot自动装配原理是什么

Spring Boot自动装配通过SpringBootApplication注解触发会加载META-INF目录下的自动配置类这些配置类使用Conditional系列注解进行条件判断当满足条件时才会生效开发者也可以通过自定义starter实现自己的自动配置逻辑

#### Redis在物联网场景中的典型应用

Redis在物联网中常用于设备状态缓存设备指令队列管理设备地理围栏实现以及设备事件订阅发布特别适合需要高性能读写和实时通信的场景

#### 如何设计一个高并发的设备消息处理系统

设计高并发消息系统需要考虑接入层使用Netty处理连接消息队列如Kafka进行流量削峰业务处理层采用异步方式存储层根据数据类型选择合适的数据库同时要做好监控和熔断机制

#### MySQL索引优化在IoT场景的应用

在物联网场景中设备数据表通常需要建立设备ID加时间戳的复合索引写多读少的表要控制索引数量查询尽量使用覆盖索引避免回表操作

#### 解释TCP粘包拆包问题及解决方案

TCP粘包拆包是因为TCP是字节流协议解决方案包括固定消息长度使用特殊分隔符或者在消息头添加长度字段其中长度字段加内容的方式最为灵活可靠

#### 什么是分布式ID生成方案

常见的分布式ID方案有UUID数据库自增序列Redis原子操作和雪花算法其中雪花算法能生成趋势递增的ID性能好且适合分布式环境是最推荐的方案

#### Spring Cloud在物联网平台的适用性

Spring Cloud适合物联网平台的后端服务治理如服务发现配置管理熔断限流等但对于设备直接通信建议使用专门的物联网协议如MQTT

#### 如何保证设备数据的一致性

保证数据一致性可以通过本地事务加消息表TCC补偿事务或者最终一致性方案具体选择要根据业务场景和对一致性的要求来决定

#### JVM调优在嵌入式设备上的特殊考虑

嵌入式设备上JVM调优需要减小堆内存使用Serial垃圾收集器关闭非必要功能同时要特别注意native内存的使用情况

#### Netty的Reactor模型是什么

Netty采用主从Reactor模型主Reactor负责接收连接从Reactor处理IO操作业务处理可以交给专门的业务线程池这种架构能很好支持高并发场景

#### 什么是边缘计算

边缘计算是将计算能力下沉到靠近数据源的位置减少数据传输延迟提高响应速度特别适合需要实时处理的场景

#### 如何处理海量设备日志

处理海量日志需要建立完整的采集传输存储分析链路常用方案包括Filebeat采集Kafka传输Elasticsearch存储和Spark分析同时要考虑日志压缩和生命周期管理

> 作者：程序员小白条
> 链接：https://www.nowcoder.com/discuss/784501998488911872?sourceSSR=search
> 来源：牛客网
