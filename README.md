## 手机号码归属地查询

### 使用方法

```sql
CREATE DATABASE IF NOT EXISTS `phonenum` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `phonenum`;
```

### 数据来源

<http://www.ip138.com>

### 原理

遍历各个手机号码段(前7位)
