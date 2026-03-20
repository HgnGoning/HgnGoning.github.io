---
title: "Java反射"
date: 2025-04-21
categories: ["java后端开发"]
tags: ["spring","反射"]
---

参考：[大白话说Java反射：入门、使用、原理 - 陈树义 - 博客园](https://www.cnblogs.com/chanshuyi/p/head_first_of_reflection.html)


[Java反射机制-十分钟搞懂 - 知乎](https://zhuanlan.zhihu.com/p/405325823)


# 正与反

反射之中包含了一个「反」字，所以想要解释反射就必须先从「正」开始解释。


一般情况下，我们使用某个类时必定知道它是什么类，是用来做什么的。于是我们直接对这个类进行实例化，之后使用这个类对象进行操作。



```java
Apple apple = new Apple(); //直接初始化，「正射」
apple.setPrice(4);

```



上面这样子进行类对象的初始化，我们可以理解为「正」。


而反射则是一开始并不知道我要初始化的类对象是什么，自然也无法使用 new 关键字来创建对象了。


这时候，我们使用 JDK 提供的反射 API 进行反射调用：



```javascript
Class clz = Class.forName("com.chenshuyi.reflect.Apple");
Method method = clz.getMethod("setPrice", int.class);
Constructor constructor = clz.getConstructor();
Object object = constructor.newInstance();
method.invoke(object, 4);

```



上面两段代码的执行结果，其实是完全一样的。但是其思路完全不一样，第一段代码在未运行时就已经确定了要运行的类（Apple），而第二段代码则是在运行时通过字符串值才得知要运行的类（com.chenshuyi.reflect.Apple）。


所以说什么是反射？


**反射就是在运行时才知道要操作的类是什么，并且可以在运行时获取类的完整构造，并调用对应的方法。**


# 反射的原理

下图是类的正常加载过程、反射原理与class对象：


[Class对象](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=Class%E5%AF%B9%E8%B1%A1&zhida_source=entity)的由来是将.class文件读入内存，并为之创建一个Class对象。


![image-20250419111322345](/2025/04/21/%E5%8F%8D%E5%B0%84/image-20250419111322345.png)


源码理解有点繁琐，可以查看[大白话说Java反射：入门、使用、原理 - 陈树义 - 博客园](https://www.cnblogs.com/chanshuyi/p/head_first_of_reflection.html)


# 反射常用

## 类文件

- Java.lang.Class;
- Java.lang.reflect.[Constructor](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=Constructor&zhida_source=entity);
- Java.lang.reflect.[Field](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=Field&zhida_source=entity);
- Java.lang.reflect.[Method](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=Method&zhida_source=entity);
- Java.lang.reflect.Modifier;
- 在JDK中，主要由以下类来实现Java反射机制，**这些类都位于java.lang.reflect包中**
  
  
  
  
  Class类：代表一个类
- Constructor 类：代表类的构造方法
- Field 类：代表类的成员变量(属性)
- Method类：代表类的成员方法






## 反射的入口—Class类

**-Class类是Java 反射机制的起源和入口**


- 用于获取与类相关的各种信息
- 提供了获取类信息的相关方法
- Class类继承自Object类


**-Class类是所有类的共同的图纸**


- 每个类有自己的对象，好比图纸和实物的关系
- 每个类也可看做是一个对象，有共同的图纸Class，存放类的结构信息，比如类的名字、属性、方法、构造方法、父类和接口，能够通过相应方法取出相应信息


**-Class类的对象称为类对象**


![img](https://pic1.zhimg.com/v2-6ee665ccfc20b55900cc4726195be0e6_1440w.jpg)


## 代码演示：认知Class类

```java
public class TestClass1 {
    public static void main(String[] args) throws Exception {
        //1.获取一个类的结构信息（类对象 Class对象）
        //Class.forName 静态方法
        Class clazz = Class.forName("com.bjsxt.why.Dog");
        //使用 .class 方法---编译前就知道操作的 Class
        Class clazz = String.class
        //使用类对象的 getClass() 方法
        String str = new String("Hello");
		Class clz = str.getClass();  
        
        //2.从类对象中获取类的各种结构信息
        //2.1 获取基本结构信息
        System.out.println(clazz.getName());
        System.out.println(clazz.getSimpleName());
        System.out.println(clazz.getSuperclass());
        System.out.println(Arrays.toString(clazz.getInterfaces()));
        
        //2.2 获取构造方法
        //只能得到public修饰的构造方法
        //Constructor[] constructors = clazz.getConstructors();
        //可以得到所有的构造方法
        Constructor[] constructors = clazz.getDeclaredConstructors(); 
        System.out.println(constructors.length);
        for(Constructor con :constructors){
            //System.out.println(con.toString());
            System.out.println(con.getName() + "||" + 
                    Modifier.toString(con.getModifiers())+"  ||"
                    + Arrays.toString(con.getParameterTypes()));
        }
        //Constructor con = clazz.getConstructor();//获取无参数构造方法
      //Constructor con = clazz.getConstructor(String.class,String.class);
        Constructor con = 
clazz.getDeclaredConstructor(String.class,String.class);
        System.out.println(con);
        //2.3 获取属性
       //Field[] fields = clazz.getFields();
        Field [] fields = clazz.getDeclaredFields();
        System.out.println(fields.length);
        for(Field f :fields){
            System.out.println(f);
        }
        //Field f = clazz.getField("color");
        //private 默认 protecte public都可以获取，但不包括父类的
        Field f = clazz.getDeclaredField("age");
        System.out.println(f);
        //2.3 获取方法
       //Method[] methods = clazz.getMethods();
        Method [] methods = clazz.getDeclaredMethods();
        for(Method m : methods){
            System.out.println(m);
        }
        //Method m = clazz.getMethod("shout",String.class);
        //Method m = clazz.getMethod("run");//public
        Method m = clazz.getDeclaredMethod("run");
        System.out.println(m);
    }
}

```



## **Class类的常用方法：**

**getFields()——** 获得类的public类型的属性。


**getDeclaredFields()——** 获得类的所有属性


**getField(String name)——** 获得类的指定属性


**getMethods()——** 获得类的public类型的方法


**getMethod (String name,Class [] args)——** 获得类的指定方法


**getConstrutors()——** 获得类的public类型的构造方法


**getConstrutor(Class[] args)——** 获得类的特定构造方法


**newInstance()——** 通过类的无参构造方法创建对象


**getName()——** 获得类的完整名字


**getPackage()——** 获取此类所属的包


**getSuperclass()——** 获得此类的父类对应的Class对象


## 获取一个类的类对象的三种方式：

```java
public class TestClass2 {
    public static void main(String[] args) throws  Exception {
        //1.获取一个类的结构信息（类对象 Class对象）
        // 1.1Class.forName(类的完整路径字符串);
        //Class clazz = Class.forName("java.lang.String");
        //1.2 类名.class
       // Class clazz = String.class;
        //1.3 对象名.getClass()
        String str = "bjsxt";
        Class clazz = str.getClass();
        //Integer in = new Integer(20);
        //2.从类对象中获取类的各种结构信息
        System.out.println(clazz.getName());
        System.out.println(clazz.getSimpleName());
        System.out.println(clazz.getSuperclass());
        System.out.println(Arrays.toString(clazz.getInterfaces()));
    }
}

```



**其中类名.class、对象名.getClass()方式在编码时已经知道了要操作的类**，而Class.forName()方式在操作的时候，可以知道，也可以不知道要操作的类。所以当编码时还不知道要操作的具体类，就只能使用Class.forName()方式了。


## 使用反射创建对象

**调用无参数构造方法创建对象**


**方法1：通过Class的newInstance()方法**


- 该方法要求该Class对象的对应类有无参构造方法
- 执行newInstance()实际上就是执行无参构造方法来创建该类的实例


**代码示例：通过Class的newInstance()方法**



```java
public class TestConstructor1 {
    public static void main(String[] args) throws Exception{
        //不使用反射创建对象
        //Dog dog = new Dog();
        //使用反射创建对象
        //1.获取类的完整路径字符串
        String className = "com.bjsxt.why.Dog";
        //2.根据完整路径字符串获取Class对象信息
        Class clazz = Class.forName(className);
        //3.直接使用Class的方法创建对象
        Object obj = clazz.newInstance();
        System.out.println(obj.toString());
    }
}

```



**方法2：通过Constructor的newInstance()方法**


- 先使用Class对象获取指定的Constructor对象
- 再调用Constructor对象的newInstance()创建Class对象对应类的对象
- 通过该方法可选择使用指定构造方法来创建对象


**代码示例：通过Constructor的newInstance()方法创建对象**



```java
public class TestConstructor2  {
    public static void main(String[] args) throws Exception{
        //不使用反射创建对象
        //Dog dog = new Dog();
        //使用反射创建对象
        //1.获取类的完整路径字符串
        String className = "com.bjsxt.why.Dog";
        //2.根据完整路径字符串获取Class对象信息
        Class clazz = Class.forName(className);
        //3.获取无参数构造方法
        Constructor con = clazz.getConstructor();
        //4.使用无参数构造方法来创建对象
        Object obj = con.newInstance();
        System.out.println(obj);
    }
}

```



## 使用反射操作属性

通过Class对象的getFields()或者getField()方法可以获得该类所包括的全部Field属性或指定Field属性。Field类提供了以下方法来访问属性


- getXxx(Object obj)：获取obj对象该Field的属性值。此处的Xxx对应8个基本数据类型，如果该属性类型是引用类型则直接使用get(Object obj)
- setXxx(Object obj,Xxx val)：将obj对象的该Field赋值val。此处的Xxx对应8个基本数据类型，如果该属性类型是引用类型则直接使用set(Object obj, Object val)
- setAccessible(Boolean flag)：若flag为true，则取消属性的访问权限控制，即使private属性也可以进行访问


**代码示例：使用反射操作属性**



```java
public class TestField {
    public static void main(String[] args) throws Exception{
        //不使用反射操作属
//        Dog dog = new Dog();
//        dog.nickName = "旺财";
//        dog.age ="黑色";
//        System.out.println(dog.nickName);
//        System.out.println(dog.color);
        //使用反射操作属性  实际操作中使用反射直接操作属性也不多
        //1.获取类的完整路径字符串
        String className = "com.bjsxt.why.Dog";
        //2.得到类对象
        Class clazz = Class.forName(className);
        //3.使用反射创建对象
        //Object dog = clazz.newInstance();
        Object dog = clazz.getConstructor().newInstance();
        //4.获取属性
        Field f1 =  clazz.getField("color");
       //Field f2 = clazz.getField("age");
        Field f2 = clazz.getDeclaredField("age");
        //5.给属性赋值
        f1.set(dog,"黑色1"); //  dog.color ="黑色";
        f2.setAccessible(true);//突破权限的控制
        f2.set(dog,10);
        //6.输出给属性
        System.out.println(f1.get(dog)); //dog.color
        System.out.println(f2.get(dog)); //dog.age
        System.out.println(dog);
    }
}

```



## 使用反射执行方法

- 通过Class对象的getMethods() 方法可以获得该类所包括的全部方法, 返回值是Method[]
- 通过Class对象的getMethod()方法可以获得该类所包括的指定方法, 返回值是Method
- 每个Method对象对应一个方法，获得Method对象后，可以调用其invoke() 来调用对应方法
- Object invoke(Object obj,Object [] args):obj代表当前方法所属的对象的名字，args代表当前方法的参数列表，返回值Object是当前方法的返回值，即执行当前方法的结果。


**代码示例：使用反射执行方法**



```java
public class TestMethod {
    public static void main(String[] args) throws Exception{
        //不使用反射执行方法
//        Dog dog = new Dog();
//        dog.shout();
//        int result = dog.add(10,20);
//        System.out.println(result);
        //使用反射执行方法
        //1.获取类的完整路径字符串
        String className = "com.bjsxt.why.Dog";
        //2.得到类对象
        Class clazz = Class.forName(className);
        //3.使用反射创建对象
        //Object dog = clazz.newInstance();
        Object dog = clazz.getConstructor().newInstance();
        //4.获取方法
        Method m1 = clazz.getMethod("shout");
        Method m2 = clazz.getMethod("add",int.class,int.class);
        //5.使用反射执行方法
        m1.invoke(dog);//dog.shout();
        Object result = m2.invoke(dog,10,20);   
        System.out.println(result);
    }
}

```



# 反射的应用场合

- 在编译时根本无法知道该对象或类可能属于哪些类，程序只依靠运行时信息来发现该对象和类的真实信息
- 比如：**[log4j](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=log4j&zhida_source=entity)，[Servlet](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=Servlet&zhida_source=entity)、[SSM框架](https://zhida.zhihu.com/search?content_id=178202404&content_type=Article&match_order=1&q=SSM%E6%A1%86%E6%9E%B6&zhida_source=entity)技术**都用到了**反射机制**