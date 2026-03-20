---
layout: post
title: Java设计模式
date: 2025-08-28
categories: [java基础]
tags: [设计模式]
---

## 一、装饰器模式

装饰器模式（Decorator Pattern）是一种结构型设计模式，允许在不改变对象结构的情况下，动态地给对象添加额外的职责。

### 1、核心概念

装饰器模式通过创建一个包装对象（装饰器）来包裹真实对象，并在保持真实对象接口不变的前提下，为其添加额外的功能。

### 2、主要角色

- **Component（抽象组件）**：定义对象的接口，可以给这些对象动态添加职责
- **ConcreteComponent（具体组件）**：定义具体的对象，也可以给这个对象添加一些职责
- **Decorator（抽象装饰器）**：持有一个 Component 对象的引用，并实现 Component 接口
- **ConcreteDecorator（具体装饰器）**：具体装饰器类，负责给组件添加新的职责

### 3、代码示例

```java
// 抽象组件
interface Coffee {
    double cost();
    String description();
}

// 具体组件
class SimpleCoffee implements Coffee {
    @Override
    public double cost() {
        return 10;
    }

    @Override
    public String description() {
        return "Simple Coffee";
    }
}

// 抽象装饰器
abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;

    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }

    @Override
    public double cost() {
        return coffee.cost();
    }

    @Override
    public String description() {
        return coffee.description();
    }
}

// 具体装饰器 - 加牛奶
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public double cost() {
        return super.cost() + 2;
    }

    @Override
    public String description() {
        return super.description() + ", Milk";
    }
}

// 具体装饰器 - 加糖
class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public double cost() {
        return super.cost() + 1;
    }

    @Override
    public String description() {
        return super.description() + ", Sugar";
    }
}

// 使用示例
public class Main {
    public static void main(String[] args) {
        Coffee coffee = new SimpleCoffee();
        System.out.println(coffee.description() + " Cost: " + coffee.cost());

        // 加牛奶
        coffee = new MilkDecorator(coffee);
        System.out.println(coffee.description() + " Cost: " + coffee.cost());

        // 加糖
        coffee = new SugarDecorator(coffee);
        System.out.println(coffee.description() + " Cost: " + coffee.cost());
    }
}
```

### 4、应用场景

- 需要动态地给对象添加职责
- 需要组合多个装饰器来创建复杂的对象
- 不希望使用继承来扩展功能

### 5、优缺点

**优点：**
- 比继承更灵活，可以动态地添加或删除职责
- 可以组合多个装饰器
- 遵循单一职责原则

**缺点：**
- 会产生很多小对象
- 装饰器模式比继承更容易出错

---

> 注：本文内容待继续补充其他设计模式。
