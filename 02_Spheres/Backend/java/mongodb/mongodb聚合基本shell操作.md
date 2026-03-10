## 检索books集合中所有文档计数

```shell
db.books.countDocuments()
```

## 计算与查询匹配的所有文档

```shell
db.books.countDocuments({favCount:{$gt:50}})
```

## 返回不同type的数组

```shell
db.books.distinct("type")
```

## 返回收藏数大于90的文档不同type的数组

```shell
db.books.distinct("type",{favCount:{$gt:90}})
```

| 阶段       | 描述   | SQL等价运算符        |
| -------- | ---- | --------------- |
| $match   | 筛选条件 | WHERE           |
| $project | 投影   | AS              |
| $lookup  | 左外连接 | LEFT OUTER JOIN |
| $sort    | 排序   | ORDER BY        |
| $group   | 分组   | GROUP BY        |
| $skip    | 分页   |                 |
| $limit   | 分页   |                 |

## $project

```shell
# 将文档的title字段起个别名name后输出
db.books.aggregate([{$project:{name:"$title"}}])

# 在上面这个语句的基础上 控制输出的字段 id不要输出 type和author输出
db.books.aggregate([{$project:{name:"$title",_id:0,type:1,author:1}}])
```

## $match

在实际应用中尽可能将$match放在管道的前面位置。
这样有两个好处：
1. 快速将不需要的文档过滤掉，以减少管道的工作量
2. 如果再投射和分组之前执行$match，查询可以使用索引

```shell
# 查询类型是technology的书籍
db.books.aggregate([{$match:{type:"technology"}}])

# 配合投影 将输出的结果按照自定需求输出
db.books.aggregate([
{$match:{type:"technology"}},
{$project:{name:"$title",_id:0,type:1,author:{name:1}}}
])
```

## $count

```shell
db.books.aggregate([
{$match:{type:"technology"}},
{$count: "type_count"}
])
```

## $group

group阶段的内存限制为100M。默认情况下，如果stage超过此限制，group将产生错
误


| 名称   | 描述           | 类比sql |
| ---- | ------------ | ----- |
| $max | 获取分组的最大值     | max   |
| $min | 获取分组的最小值     | min   |
| $pop | 将表达式的值添加到数组中 |       |
| $sum | 计算总和         | sum   |

```shell
db.books.aggregate([
    {
        $group: {
            _id: null,
            count: {$sum: 1},
            favAll: {$sum: "$favCount"},
            favAvg: {$avg: "$favCount"}
        }
    }
])
```