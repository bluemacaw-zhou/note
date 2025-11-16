查询条件对照表

| SQL    | MQL            |
| ------ | -------------- |
| a = 1  | {a: 1}         |
| a != 1 | {a: {$ne: 1}}  |
| a > 1  | {a: {$gt: 1}}  |
| a >= 1 | {a: {$gte: 1}} |
| a < 1  | {a: {$lt: 1}}  |
| a <= 1 | {a: {$lte: 1}} |

逻辑对照表

| SQL             | MQL                      |
| --------------- | ------------------------ |
| a = 1 AND b = 1 | {$and: [{a: 1}, {b: 1}]} |
| a = 1 OR b = 1  | {$or: [{a: 1}, {b: 1}]}  |
| a IS NULL       | {a: {$exists: false}}    |
| a IN (1, 2, 3)  | {a: {$in: [1, 2, 3]}}    |

### 查找数据

```shell
# 查找type是travel favCount大于60的文档
db.books.find({type:"travel",favCount:{$gt:60}})
```

### 分页查找数据

```shell
# 每页大小为8 查询第三页的数据
db.books.find().skip(16).limit(8)
```