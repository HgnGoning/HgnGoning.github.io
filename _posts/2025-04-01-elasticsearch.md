---
layout: post
title: Elasticsearch
date: 2025-04-01
categories: [java后端开发]
tags: [中间件]
---

## 初识

### 简介

elasticsearch:是一款非常强大的开源搜索引擎，可以帮助我们从海量数据中快速找到需要的内容。

elasticsearch结合kibana、Logstash、Beats,也就是elastic stack(ELK)。被广泛应用在日志数据分析、实时监控等领域。

**ELK:是以elasticsearch为核心的技术栈，包括beats、Logstash,kibana,elasticsearch**

![elasticsearch架构](/2025/04/01/elasticsearch/image-20250401095300312.png)

### 发展历程

Lucene是一个Java语言的搜索引擎类库（jar包），是Apache公司的顶级项目，由DougCutting于1999年研发
官网地址：https://lucene.apache.org/。

Lucene -> Compass  ->  Elasticsearch

### 技术排名

搜索引擎技术排名：
1.Elasticsearch:开源的分布式搜索引擎
2.Splunk:商业项目
3.Solr:Apache的开源搜索引擎

## 倒排索引

传统数据库（如MySQL)采用正向索引，例如：根据id一个个查

elasticsearch采用倒排索引：

- 文档（document)：每条数据就是一个文档
- 词条(term):文档按照语义分成的词语

![倒排索引](/2025/04/01/elasticsearch/image-20250401100043043.png)

## el与mysql差异

### 文档

elasticsearch是面向文档存储的，可以是数据库中的一条商品数据，一个订单信息。
文档数据会被序列化为**json格式**后存储在elasticsearch中。

### 索引(Index)

- 索引(index):相同类型的文档的集合
- 映射(mapping):索引中文档的字段约束信息，类似表的结构约束

![索引](/2025/04/01/elasticsearch/image-20250401100341559.png)

### 概览

![概览](/2025/04/01/elasticsearch/image-20250401100434357.png)

### 架构

MySql: 擅长事务类型操作，可以确保数据的安全和一致性
Elasticsearch: 擅长海量数据的搜索、分析、计算

![架构](/2025/04/01/elasticsearch/image-20250401100658782.png)
