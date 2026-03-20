---
layout: post
title: JUC并发编程
date: 2025-04-17
categories: [java基础]
tags: [JUC, 并发编程]
---

## 导学

## 进程与线程

### 进程与线程

#### 进程

- 程序由指令和数据组成，但这些指令要运行，数据要读写，就必须将指令加载至 CPU，数据加载至内存。在 指令运行过程中还需要用到磁盘、网络等设备。
- 进程就是用来加载指令、管理内存、管理 IO 的 当一个程序被运行，从磁盘加载这个程序的代码至内存，这时就开启了一个进程。
- 进程就可以视为程序的一个实例。大部分程序可以同时运行多个实例进程（例如记事本、画图、浏览器 等），也有的程序只能启动一个实例进程（例如网易云音乐、360 安全卫士等）

#### 线程

- 一个进程之内可以分为一到多个线程。
- 一个线程就是一个指令流，将指令流中的一条条指令以一定的顺序交给 CPU 执行
- Java 中，线程作为最小调度单位，进程作为资源分配的最小单位。 在 windows 中进程是不活动的，只是作为线程的容器

#### 二者对比

- 进程基本上相互独立的，而线程存在于进程内，是进程的一个子集
- 进程拥有共享的资源，如内存空间等，供其内部的线程共享
- 进程间通信较为复杂
  - 同一台计算机的进程通信称为 IPC（Inter-process communication）
  - 不同计算机之间的进程通信，需要通过网络，并遵守共同的协议，例如 HTTP
- 线程通信相对简单，因为它们共享进程内的内存，一个例子是多个线程可以访问同一个共享变量
- 线程更轻量，线程上下文切换成本一般上要比进程上下文切换低

### 并行与并发

单核 cpu 下，线程实际还是 串行执行 的。操作系统中有一个组件叫做任务调度器，将 cpu 的时间片（windows 下时间片最小约为 15 毫秒）分给不同的程序使用，只是由于 cpu 在线程间（时间片很短）的切换非常快，人类感 觉是 同时运行的 。总结为一句话就是：微观串行，宏观并行

一般会将这种 **线程轮流使用 CPU** 的做法称为并发， concurrent

多核 cpu下，每个  核（core） 都可以调度运行线程，这时候线程可以是并行的。

引用 Rob Pike 的一段描述：

- 并发（concurrent）是同一时间应对（dealing with）多件事情的能力
- 并行（parallel）是同一时间动手做（doing）多件事情的能力
- 家庭主妇做饭、打扫卫生、给孩子喂奶，她一个人轮流交替做这多件事，这时就是并发
- 家庭主妇雇了个保姆，她们一起这些事，这时既有并发，也有并行（这时会产生竞争，例如锅只有一口，一 个人用锅时，另一个人就得等待）
- 雇了3个保姆，一个专做饭、一个专打扫卫生、一个专喂奶，互不干扰，这时是并行

### 应用

#### 应用之异步调用

以调用方角度来讲，如果

- 需要等待结果返回，才能继续运行就是同步
- 不需要等待结果返回，就能继续运行就是异步

1. 设计
   多线程可以让方法执行变为异步的（即不要巴巴干等着）比如说读取磁盘文件时，假设读取操作花费了 5 秒钟，如 果没有线程调度机制，这 5 秒 cpu 什么都做不了，其它代码都得暂停...

2. 结论

- 比如在项目中，视频文件需要转换格式等操作比较费时，这时开一个新线程处理视频转换，避免阻塞主线程
- tomcat 的异步 servlet 也是类似的目的，让用户线程处理耗时较长的操作，避免阻塞 tomcat 的工作线程
- ui 程序中，开线程进行其他操作，避免阻塞 ui 线程

## java线程

### 创建和运行线程

#### 方法一，直接使用 Thread

```java
// 创建线程对象
Thread t = new Thread() {
 public void run() {
 // 要执行的任务
    }
 };
 // 启动线程
t.start();
```

例如：

```java
// 构造方法的参数是给线程指定名字，推荐
Thread t1 = new Thread("t1") {
 @Override
 // run 方法内实现了要执行的任务
public void run() {
 log.debug("hello");
    }
 };
 t1.start();
```

#### 方法二，使用 Runnable 配合 Thread

把【线程】和【任务】（要执行的代码）分开

- Thread 代表线程
- Runnable 可运行的任务（线程要执行的代码）

```java
Runnable runnable = new Runnable() {
 public void run(){
 // 要执行的任务
    }
 };
 // 创建线程对象
Thread t = new Thread( runnable );
 // 启动线程
t.start();
```

例如：

```java
// 创建任务对象
Runnable task2 = new Runnable() {
 @Override
 public void run() {
 log.debug("hello");
    }
 };
 // 参数1 是任务对象; 参数2 是线程名字，推荐
Thread t2 = new Thread(task2, "t2");
 t2.start();
```

java8之后可以使用lambda:

可以直接在匿名内部类使用alt+enter直接帮助你

```java
// 创建任务对象
Runnable task2 = () -> log.debug("hello");
 // 参数1 是任务对象; 参数2 是线程名字，推荐
Thread t2 = new Thread(task2, "t2");
 t2.start()
```

##### 原理之 Thread 与 Runnable 的关系

分析 Thread 的源码，理清它与 Runnable 的关系

最终走的是thread的run方法，只是run方法的实现不同,一个是自己的匿名内部类来实现的,一个是通过Runnable里面的run方法来执行的

小结

- 方法1 是把线程和任务合并在了一起，
- 方法2 是把线程和任务分开了 用 Runnable 更容易与线程池等高级 API 配合
- 用 Runnable 让任务类脱离了 Thread 继承体系，更灵活

#### 方法三，FutureTask 配合 Thread，有返回

FutureTask 能够接收 Callable 类型的参数，用来处理有返回结果的情况

```java
// 创建任务对象
FutureTask<Integer> task3 = new FutureTask<>(() -> {
 log.debug("hello");
 return 100;
 });
 // 参数1 是任务对象; 参数2 是线程名字，推荐
new Thread(task3, "t3").start();
 // ---主线程阻塞，同步等待 task 执行完毕的结果---阻塞等待
Integer result = task3.get();
 log.debug("结果是:{}", result);
```

### 线程运行

交替执行 谁先谁后，不由我们控制

**windows**

- 任务管理器可以查看进程和线程数，也可以用来杀死进程
- tasklist 查看进程
- taskkill 杀死进程

**linux**

- ps -fe 查看所有进程
- ps -fT -p  查看某个进程（PID）的所有线程
- kill  杀死进程
- top 按大写 H 切换是否显示线程
- top -H -p  查看某个进程（PID）的所有线程

**Java**

- jps 命令查看所有 Java 进程
- jstack  查看某个 Java 进程（PID）的所有线程状态
- jconsole 来查看某个 Java 进程中线程的运行情况（图形界面）

#### jconsole 远程监控配置—JDK自带的

需要以如下方式运行你的 java 类

```
java -Djava.rmi.server.hostname=`ip地址` -Dcom.sun.management.jmxremote  Dcom.sun.management.jmxremote.port=`连接端口` -Dcom.sun.management.jmxremote.ssl=是否安全连接  Dcom.sun.management.jmxremote.authenticate=是否认证 java类
```

修改 /etc/hosts 文件将 127.0.0.1 映射至主机名

如果要认证访问，还需要做如下步骤：

- 复制 jmxremote.password 文件
- 修改 jmxremote.password 和 jmxremote.access 文件的权限为 600 即文件所有者可
- 读写 连接时填入 controlRole（用户名），R&D（密码）

### 线程运行原理

#### 栈与栈帧

Java Virtual Machine Stacks （Java 虚拟机栈）

一个栈帧包括：局部变量表,操作数,栈动态链接,返回值等信息;

我们都知道 JVM 中由堆、栈、方法区所组成，其中栈内存是给谁用的呢？其实就是线程，每个线程启动后，虚拟机就会为其分配一块栈内存。

- 每个栈由多个栈帧（Frame）组成，对应着每次方法调用时所占用的内存
- 每个线程只能有一个活动栈帧，对应着当前正在执行的那个方法

**一个方法一个栈帧，最底层main方法，调用方法记录返回地址，由程序计数器逐步执行**

#### 线程上下文切换（Thread Context Switch）

因为以下一些原因导致 cpu 不再执行当前的线程，转而执行另一个线程的代码

- 线程的 cpu 时间片用完
- 垃圾回收
- 有更高优先级的线程需要运行
- 线程自己调用了 sleep、yield、wait、join、park、synchronized、lock 等方法

当 Context Switch 发生时，需要由操作系统保存当前线程的状态，并恢复另一个线程的状态，Java 中对应的概念 就是程序计数器（Program Counter Register），它的作用是记住下一条 jvm 指令的执行地址，是线程私有的

- 状态包括程序计数器、虚拟机栈中每个栈帧的信息，如局部变量、操作数栈、返回地址等
- Context Switch 频繁发生会影响性能

### API

### start和run方法

```java
public static void main(String[] args) {
     Thread t1 = new Thread("t1") {
     @Override
     public void run() {
         log.debug("running...");
     }
 };
 // 直接调用run方法
 t1.run();
 // 调用start方法
 t1.start();
}
```

- 直接调用 run 是在主线程中执行了 run，没有启动新线程
- 使用 start 是启动了新线程，通过新线程间接执行 run 中的代码

### sleep 与 yield

#### sleep

1. 调用 sleep 会让当前线程从 Running 进入 Timed Waiting 状态（阻塞）
2. 其它线程可以使用 interrupt 方法打断正在睡眠的线程，这时 sleep 方法会抛出 InterruptedException
3. 睡眠结束后的线程未必会立刻得到执行
4. 建议用 TimeUnit 的 sleep 代替 Thread 的 sleep 来获得更好的可读性

#### yield

1. 调用 yield 会让当前线程从 Running 进入 Runnable 就绪状态，然后调度执行其它线程
2. 具体的实现依赖于操作系统的任务调度器

#### 线程优先级

- 线程优先级会提示（hint）调度器优先调度该线程，但它仅仅是一个提示，调度器可以忽略它
- 如果 cpu 比较忙，那么优先级高的线程会获得更多的时间片，但 cpu 闲时，优先级几乎没作用

### join 方法

用于等待某个线程结束。

```java
// 等待线程结束
t.join();
// 等待线程结束，最多等多少毫秒
t.join(long millis);
```

### interrupt 方法

#### 打断 sleep，wait，join 的线程

这几个方法都会让线程进入阻塞状态。打断 sleep，wait，join 的线程，会清空打断状态。

#### 打断正常运行的线程

打断正常运行的线程，不会清空打断状态。

### 不推荐的方法

- stop() 停止线程运行（已过时）
- suspend() 挂起（暂停）线程运行（已过时）
- resume() 恢复线程运行（已过时）

## 线程状态

### 五种状态

这是从 **操作系统** 层面来描述的

- **初始状态**：仅是在语言层面创建了线程对象，还未与操作系统线程关联
- **可运行状态**：（就绪状态）指该线程已经被创建（与操作系统线程关联），可以由 CPU 调度执行
- **运行状态**：指获取了 CPU 时间片运行中的状态
  - 当 CPU 时间片用完，会从【运行状态】转换至【可运行状态】，会导致线程的上下文切换
- **阻塞状态**
  - 如果调用了阻塞 API，如 BIO 操作，此时线程不会使用 CPU，会导致线程上下文切换
  - 当 BIO 操作完毕，会由操作系统唤醒阻塞的线程，转换至【可运行状态】
- **终止状态**：表示线程已经执行完毕，生命周期已经结束，不会再转换为其它状态

### 六种状态

这是从 **Java API** 层面来描述的

根据 Thread.State 枚举，分为六种状态：

- NEW：线程刚被创建，但是还没有调用 start() 方法
- RUNNABLE：当调用了 start() 方法之后的状态。注意，Java API 层面的 RUNNABLE 状态涵盖了操作系统层面的【可运行状态】、【运行状态】和【阻塞状态】
- BLOCKED、WAITING、TIMED_WAITING：都是 Java API 层面对【阻塞状态】的细分
- TERMINATED：当线程代码运行结束

## 共享模型

### 共享带来的问题

#### 临界区 Critical Section

- 一个程序运行多个线程本身是没有问题的
- 问题出现在多个线程访问**共享资源**
  - 多个线程读共享资源其实也没有问题
  - 在多个线程对共享资源读写操作时发生指令交错，就会出现问题
- 一段代码块内如果存在对共享资源的多线程读写操作，称这段代码块为**临界区**

#### 竞态条件 Race Condition

多个线程在临界区内执行，由于代码的**执行序列不同**而导致结果无法预测，称之为发生了**竞态条件**

### synchronized

#### 互斥

为了避免临界区的竞态条件发生，有多种手段可以达到目的。

- 阻塞式的解决方案：synchronized，Lock
- 非阻塞式的解决方案：原子变量

synchronized，俗称"对象锁"，它采用互斥的方式让同一时刻至多只有一个线程能持有对象锁，其它线程再想获取这个对象锁时就会阻塞住。

#### 使用方式

```java
// 同步代码块
synchronized(对象) {
    // 临界区
}

// 同步方法
public synchronized void method() {
    // 临界区
}

// 静态同步方法
public static synchronized void method() {
    // 临界区
}
```

### 线程安全分析

#### 成员变量和静态变量

- 如果它们没有共享，则线程安全
- 如果它们被共享了，根据它们的状态是否能够改变，又分两种情况
  - 如果只有读操作，则线程安全
  - 如果有读写操作，则这段代码是临界区，需要考虑线程安全

#### 局部变量

- 局部变量是线程安全的
- 但局部变量引用的对象则未必
  - 如果该对象没有逃离方法的作用范围，它是线程安全的
  - 如果该对象逃离方法的作用范围，需要考虑线程安全

### 常见线程安全类

- String
- Integer 等包装类
- StringBuffer
- Random
- Vector
- Hashtable
- java.util.concurrent 包下的类

## 锁

### Monitor

Monitor 被翻译为监视器或管程

每个 Java 对象都可以关联一个 Monitor 对象，如果使用 synchronized 给对象上锁（重量级）之后，该对象头的 Mark Word 中就被设置指向 Monitor 对象的指针。

### synchronized 进阶

#### 轻量级锁

轻量级锁的使用场景：如果一个对象虽然有多线程要加锁，但加锁的时间是错开的（也就是没有人可以竞争），那么可以使用轻量级锁来优化。

#### 锁膨胀

如果在尝试加轻量级锁的过程中，CAS 操作无法成功，这时一种情况就是有其它线程为此对象加上了轻量级锁（有竞争），这时需要进行锁膨胀，将轻量级锁变为重量级锁。

#### 自旋优化

重量级锁竞争的时候，还可以使用自旋来进行优化，如果当前线程自旋成功（即这时候持锁线程已经退出了同步块，释放了锁），这时当前线程就可以避免阻塞。

#### 偏向锁

轻量级锁在没有竞争时（就自己这个线程），每次重入仍然需要执行 CAS 操作。Java 6 中引入了偏向锁来做进一步优化：只有第一次使用 CAS 将线程 ID 设置到对象的 Mark Word 头，之后发现这个线程 ID 是自己的就表示没有竞争，不用重新 CAS。

## Wait/Notify

### 原理

- Owner 线程发现条件不满足，调用 wait 方法，即可进入 WaitSet 变为 WAITING 状态
- BLOCKED 和 WAITING 的线程都处于阻塞状态，不占用 CPU 时间片
- BLOCKED 线程会在 Owner 线程释放锁时唤醒
- WAITING 线程会在 Owner 线程调用 notify 或 notifyAll 时唤醒，但唤醒后并不意味者立刻获得锁，仍需进入 EntryList 重新竞争

### API

- obj.wait() 让进入 object 监视器的线程到 waitSet 等待
- obj.notify() 在 object 上正在 waitSet 等待的线程中挑一个唤醒
- obj.notifyAll() 让 object 上正在 waitSet 等待的线程全部唤醒

它们都是线程之间进行协作的手段，都属于 Object 对象的方法。必须获得此对象的锁，才能调用这几个方法。

### sleep(long n) 和 wait(long n) 的区别

1. sleep 是 Thread 方法，而 wait 是 Object 的方法
2. sleep 不需要强制和 synchronized 配合使用，但 wait 需要和 synchronized 一起用
3. sleep 在睡眠的同时，不会释放对象锁的，但 wait 在等待的时候会释放对象锁
4. 它们状态都是 TIMED_WAITING

## Park/Unpark

它们是 LockSupport 类中的方法

```java
// 暂停当前线程
LockSupport.park();
// 恢复某个线程的运行
LockSupport.unpark(线程对象);
```

### 特点

与 Object 的 wait & notify 相比

- wait，notify 和 notifyAll 必须配合 Object Monitor 一起使用，而 park，unpark 不必
- park & unpark 是以线程为单位来【阻塞】和【唤醒】线程，而 notify 只能随机唤醒一个等待线程，notifyAll 是唤醒所有等待线程，就不那么【精确】
- park & unpark 可以先 unpark，而 wait & notify 不能先 notify

## 活跃性

### 死锁

有这样的情况：一个线程需要同时获取多把锁，这时就容易发生死锁。

死锁产生的四个必要条件：
1. 互斥条件
2. 不可剥夺条件
3. 请求与保持条件
4. 循环等待条件

### 哲学家就餐问题

五位哲学家围坐在圆桌旁，每个人面前有一碗米饭，两只筷子。哲学家要么思考，要么吃饭。吃饭时需要同时拿到左右两边的筷子。

### 活锁

活锁出现在两个线程互相改变对方的结束条件，最后谁也无法结束。

### 饥饿

很多教程中把饥饿定义为，一个线程由于优先级太低，始终得不到 CPU 调度执行，也不能够结束。

## ReentrantLock

相对于 synchronized 它具备如下特点

- 可中断
- 可以设置超时时间
- 可以设置为公平锁
- 支持多个条件变量

与 synchronized 一样，都支持可重入。

### 基本语法

```java
// 获取锁
reentrantLock.lock();
try {
    // 临界区
} finally {
    // 释放锁
    reentrantLock.unlock();
}
```

### 可重入

可重入是指同一个线程如果首次获得了这把锁，那么因为它是这把锁的拥有者，因此有权利再次获取这把锁。

### 可打断

```java
ReentrantLock lock = new ReentrantLock();
Thread t1 = new Thread(() -> {
    try {
        // 如果没有竞争，那么此方法就会获取 lock 对象锁
        // 如果有竞争，就进入阻塞队列，可以被其它线程用 interrupt 方法打断
        lock.lockInterruptibly();
    } catch (InterruptedException e) {
        e.printStackTrace();
        return;
    }
    try {
        log.debug("获得了锁");
    } finally {
        lock.unlock();
    }
}, "t1");
lock.lock();
t1.start();
```

### 锁超时

```java
ReentrantLock lock = new ReentrantLock();
Thread t1 = new Thread(() -> {
    // 尝试获取锁，最多等待 1 秒
    if (!lock.tryLock(1, TimeUnit.SECONDS)) {
        log.debug("获取不到锁");
        return;
    }
    try {
        log.debug("获得了锁");
    } finally {
        lock.unlock();
    }
}, "t1");
```

### 公平锁

synchronized 锁是非公平锁，ReentrantLock 默认也是非公平锁，但可以通过构造方法设置为公平锁。

### 条件变量

synchronized 中也有条件变量，就是我们讲单个条件变量时，ReentrantLock 支持多个条件变量。

```java
static ReentrantLock lock = new ReentrantLock();
// 创建条件变量
static Condition condition1 = lock.newCondition();
static Condition condition2 = lock.newCondition();

// 等待
condition1.await();
// 唤醒
condition1.signal();
condition1.signalAll();
```
