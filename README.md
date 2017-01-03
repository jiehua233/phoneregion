# 手机号码归属地查询

## 使用方法

使用默认的数据导入MySQL：

    python main.py --loaddb

抓取更新数据:

    python main.py --scrapy

## 数据来源

<http://www.ip138.com>

## 原理

遍历各个手机号码段(前7位)
