---
layout: post
title: MyBatis-Plus
date: 2025-04-07
categories: [java后端开发]
tags: [中间件, MyBatis-Plus]
---

## 简介

mybaitsplus非常强大这里只做可能使用到的，更多的详情请查看官网

[简介 | MyBatis-Plus](https://baomidou.com/pages/24112f/)

## 持久层接口

本文详细介绍了 MyBatis-Plus 进行持久化操作的各种方法，包括插入、更新、删除、查询和分页等。通过本文，您可以了解到 MyBatis-Plus 提供的各种方法是如何进行数据操作的，以及它们对应的 SQL 语句。

## Service Interface

IService 是 MyBatis-Plus 提供的一个通用 Service 接口，它封装了常用的 CRUD 操作。

IService 接口中的方法命名遵循了一定的规范，如 get 用于查询单行，remove 用于删除，list 用于查询集合，page 用于分页查询，这样可以避免与 Mapper 层的方法混淆

提示

- 泛型 T 为任意实体对象
- 建议如果存在自定义通用 Service 方法，请创建自己的 IBaseService 继承 IService
- ServiceImpl 是 IService 的实现类

## 基本使用

### Insert

```java
// 插入一条记录
boolean save(T entity);

// 插入（批量）
boolean saveBatch(Collection<T> entityList);

// 插入（批量）
boolean saveBatch(Collection<T> entityList, int batchSize);
```

### Delete

```java
// 根据 entity 条件，删除记录
boolean remove(Wrapper<T> queryWrapper);

// 根据 ID 删除
boolean removeById(Serializable id);

// 根据 columnMap 条件，删除记录
boolean removeByMap(Map<String, Object> columnMap);

// 删除（根据ID 批量删除）
boolean removeByIds(Collection<? extends Serializable> idList);
```

### Update

```java
// 根据 UpdateWrapper 条件，更新记录 需要设置sqlset
boolean update(Wrapper<T> updateWrapper);

// 根据 whereWrapper 条件，更新记录
boolean update(T entity, Wrapper<T> whereWrapper);

// 根据 ID 选择修改
boolean updateById(T entity);

// 根据ID 批量更新
boolean updateBatchById(Collection<T> entityList);

// 根据ID 批量更新
boolean updateBatchById(Collection<T> entityList, int batchSize);
```

### Select

```java
// 根据 ID 查询
T getById(Serializable id);

// 根据 Wrapper，查询一条记录。结果集，如果是多个会抛出异常，随机取一条加上限制条件 wrapper.last("LIMIT 1")
T getOne(Wrapper<T> queryWrapper);

// 根据 Wrapper，查询一条记录
T getOne(Wrapper<T> queryWrapper, boolean throwEx);

// 根据 Wrapper，查询一条记录
T getOne(Wrapper<T> queryWrapper);

// 查询所有
List<T> list();

// 查询列表
List<T> list(Wrapper<T> queryWrapper);

// 查询（根据ID 批量查询）
Collection<T> listByIds(Collection<? extends Serializable> idList);

// 查询（根据 columnMap 条件）
Collection<T> listByMap(Map<String, Object> columnMap);

// 查询所有列表
List<Map<String, Object>> listMaps();

// 查询列表
List<Map<String, Object>> listMaps(Wrapper<T> queryWrapper);

// 查询全部记录
List<Object> listObjs();

// 查询全部记录
<V> List<V> listObjs(Function<? super Object, V> mapper);

// 根据 Wrapper 条件，查询全部记录
<V> List<V> listObjs(Wrapper<T> queryWrapper, Function<? super Object, V> mapper);
```

### Page

```java
// 无条件分页查询
IPage<T> page(IPage<T> page);

// 条件分页查询
IPage<T> page(IPage<T> page, Wrapper<T> queryWrapper);

// 无条件分页查询
IPage<Map<String, Object>> pageMaps(IPage<T> page);

// 条件分页查询
IPage<Map<String, Object>> pageMaps(IPage<T> page, Wrapper<T> queryWrapper);
```

## 条件构造器

### Wrapper

AbstractWrapper 是 MyBatis-Plus 条件构造器的抽象基类，它提供了丰富的查询条件构建方法。

```java
// 等于
eq(R column, Object val);

// 不等于
ne(R column, Object val);

// 大于
gt(R column, Object val);

// 大于等于
ge(R column, Object val);

// 小于
lt(R column, Object val);

// 小于等于
le(R column, Object val);

// BETWEEN 值1 AND 值2
between(R column, Object val1, Object val2);

// NOT BETWEEN 值1 AND 值2
notBetween(R column, Object val1, Object val2);

// LIKE '%值%'
like(R column, Object val);

// NOT LIKE '%值%'
notLike(R column, Object val);

// LIKE '%值'
likeLeft(R column, Object val);

// LIKE '值%'
likeRight(R column, Object val);

// 字段 IS NULL
isNull(R column);

// 字段 IS NOT NULL
isNotNull(R column);

// 字段 IN (value.get(0), value.get(1), ...)
in(R column, Collection<?> value);

// 字段 NOT IN (value.get(0), value.get(1), ...)
notIn(R column, Collection<?> value);

// 字段 IN (v0, v1, ...)
in(R column, Object... values);

// 字段 NOT IN (v0, v1, ...)
notIn(R column, Object... values);

// 分组：GROUP BY 字段, ...
groupBy(R... columns);

// 排序：ORDER BY 字段, ... ASC
orderByAsc(R... columns);

// 排序：ORDER BY 字段, ... DESC
orderByDesc(R... columns);

// OR 嵌套
or();

// AND 嵌套
and(Consumer<Param> consumer);

// 嵌套
nested(Consumer<Param> consumer);

// 自定义 sql 片段
apply(String applySql, Object... values);

// 拼接 sql
last(String lastSql);
```

### QueryWrapper

QueryWrapper 继承自 AbstractWrapper，主要用于查询条件封装。

```java
QueryWrapper<User> queryWrapper = new QueryWrapper<>();
queryWrapper.eq("name", "张三")
            .gt("age", 18)
            .orderByDesc("create_time");
List<User> users = userMapper.selectList(queryWrapper);
```

### LambdaQueryWrapper

LambdaQueryWrapper 是 QueryWrapper 的 Lambda 表达式版本，可以避免字段名硬编码。

```java
LambdaQueryWrapper<User> lambdaQueryWrapper = new LambdaQueryWrapper<>();
lambdaQueryWrapper.eq(User::getName, "张三")
                  .gt(User::getAge, 18)
                  .orderByDesc(User::getCreateTime);
List<User> users = userMapper.selectList(lambdaQueryWrapper);
```

### UpdateWrapper

UpdateWrapper 继承自 AbstractWrapper，主要用于更新条件封装和设置更新字段。

```java
UpdateWrapper<User> updateWrapper = new UpdateWrapper<>();
updateWrapper.eq("name", "张三")
             .set("age", 20);
userMapper.update(null, updateWrapper);
```

### LambdaUpdateWrapper

LambdaUpdateWrapper 是 UpdateWrapper 的 Lambda 表达式版本。

```java
LambdaUpdateWrapper<User> lambdaUpdateWrapper = new LambdaUpdateWrapper<>();
lambdaUpdateWrapper.eq(User::getName, "张三")
                   .set(User::getAge, 20);
userMapper.update(null, lambdaUpdateWrapper);
```

## 注解

### @TableName

表名注解，标识实体类对应的表。

```java
@TableName("sys_user")
public class User {
    // ...
}
```

### @TableId

主键注解，标识实体类中的主键字段。

```java
@TableName("sys_user")
public class User {
    @TableId(value = "user_id", type = IdType.AUTO)
    private Long userId;
    // ...
}
```

### @TableField

字段注解（非主键）。

```java
@TableName("sys_user")
public class User {
    @TableId(value = "user_id", type = IdType.AUTO)
    private Long userId;

    @TableField("nickname")
    private String name;

    @TableField(exist = false)  // 表示该属性不为数据库表字段
    private String address;
    // ...
}
```

### @Version

乐观锁注解。

```java
@Version
private Integer version;
```

### @EnumValue

枚举字段注解，标记数据库存的值。

### @TableLogic

表字段逻辑处理注解（逻辑删除）。

```java
@TableLogic
private Integer deleted;
```

## 分页插件

### 配置

```java
@Configuration
@MapperScan("com.baomidou.mybatisplus.samples.quickstart.mapper")
public class MybatisPlusConfig {

    /**
     * 添加分页插件
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```

### 使用

```java
// 分页查询
Page<User> page = new Page<>(1, 10);
IPage<User> userPage = userMapper.selectPage(page, null);

// 获取分页数据
List<User> users = userPage.getRecords();
long total = userPage.getTotal();
long pages = userPage.getPages();
```

## 代码生成器

MyBatis-Plus 提供了代码生成器，可以快速生成 Entity、Mapper、Service、Controller 等代码。

```java
AutoGenerator generator = new AutoGenerator();

// 全局配置
GlobalConfig globalConfig = new GlobalConfig();
globalConfig.setOutputDir("D://");
globalConfig.setAuthor("author");
globalConfig.setOpen(false);
generator.setGlobalConfig(globalConfig);

// 数据源配置
DataSourceConfig dataSourceConfig = new DataSourceConfig();
dataSourceConfig.setUrl("jdbc:mysql://localhost:3306/test?useUnicode=true&useSSL=false&characterEncoding=utf8");
dataSourceConfig.setDriverName("com.mysql.cj.jdbc.Driver");
dataSourceConfig.setUsername("root");
dataSourceConfig.setPassword("password");
generator.setDataSource(dataSourceConfig);

// 包配置
PackageConfig packageConfig = new PackageConfig();
packageConfig.setParent("com.baomidou.mybatisplus.samples");
generator.setPackageInfo(packageConfig);

// 策略配置
StrategyConfig strategyConfig = new StrategyConfig();
strategyConfig.setNaming(NamingStrategy.underline_to_camel);
strategyConfig.setColumnNaming(NamingStrategy.underline_to_camel);
strategyConfig.setEntityLombokModel(true);
strategyConfig.setRestControllerStyle(true);
generator.setStrategy(strategyConfig);

generator.execute();
```

## 类型处理器

MyBatis-Plus 支持自定义类型处理器，用于处理 Java 类型与 JDBC 类型之间的转换。

```java
@MappedTypes({String.class})
@MappedJdbcTypes({JdbcType.VARCHAR})
public class JsonTypeHandler extends BaseTypeHandler<String> {
    // 实现方法...
}
```

## 多租户

MyBatis-Plus 支持多租户模式，可以通过配置实现。

```java
@Bean
public MybatisPlusInterceptor mybatisPlusInterceptor() {
    MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
    TenantLineInnerInterceptor tenantInterceptor = new TenantLineInnerInterceptor();
    tenantInterceptor.setTenantLineHandler(new TenantLineHandler() {
        @Override
        public Expression getTenantId() {
            // 返回租户ID
            return new LongValue(1L);
        }

        @Override
        public String getTenantIdColumn() {
            // 返回租户ID字段名
            return "tenant_id";
        }

        @Override
        public boolean ignoreTable(String tableName) {
            // 忽略某些表
            return false;
        }
    });
    interceptor.addInnerInterceptor(tenantInterceptor);
    return interceptor;
}
```

## 性能分析

MyBatis-Plus 提供了性能分析插件，用于输出每条 SQL 语句及其执行时间。

```java
@Bean
public PerformanceInterceptor performanceInterceptor() {
    PerformanceInterceptor performanceInterceptor = new PerformanceInterceptor();
    // 设置SQL执行最大时长，超过自动停止运行
    performanceInterceptor.setMaxTime(1000);
    // 是否格式化SQL
    performanceInterceptor.setFormat(true);
    return performanceInterceptor;
}
```

## 总结

MyBatis-Plus 是一个强大的 MyBatis 增强工具，简化了开发工作：

- 无侵入：只做增强不做改变，引入不会对现有工程产生影响
- 强大的 CRUD 操作：内置通用 Mapper、Service，少量配置即可实现单表大部分 CRUD 操作
- 支持 Lambda 表达式：通过 Lambda 表达式方便编写各类查询条件
- 支持主键自动生成：支持多达 4 种主键策略
- 内置分页插件：基于 MyBatis 物理分页，配置好插件后即可使用
- 内置代码生成器：采用代码或者 Maven 插件可快速生成 Mapper、Model、Service、Controller 层代码
- 内置性能分析插件：可输出 SQL 语句以及执行时间
- 内置全局拦截插件：提供全表 delete、update 操作智能分析阻断
