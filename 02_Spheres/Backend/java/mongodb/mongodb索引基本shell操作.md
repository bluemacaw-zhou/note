假设集合是books

## 创建单键索引
```shell
db.books.createIndex({title:1})
```

## 创建复合索引

```shell
db.books.createIndex({type:1,favCount:1})
```

## 创建hash索引

```shell
db.users.createIndex({author : 'hashed'})
```

## 查看索引信息

```shell
db.books.getIndexes()
```

## 查看索引键

```shell
db.books.getIndexKeys()
```

## explain
在查询语句后加上explain就可以看到查询语句是不是命中索引

```shell
# 更快的定位索引相关的信息
db.books.find({title:"book‐1"}).explain().queryPlanner.winningPlan
```

单键索引输出

```json
winningPlan: {
      isCached: false,
      stage: 'FETCH',
      inputStage: {
        stage: 'IXSCAN', // 索引扫描
        keyPattern: {
          title: 1
        },
        indexName: 'title_1', // 使用了名为"title_1"的索引
        isMultiKey: false,
        multiKeyPaths: {
          title: []
        },
        isUnique: false,
        isSparse: false,
        isPartial: false,
        indexVersion: 2,
        direction: 'forward',
        indexBounds: {
          title: [
            '["book-0", "book-0"]'
          ]
        }
      }
    }
```

hash索引输出

```json
winningPlan: {
      isCached: false,
      stage: 'FETCH',
      filter: {
        author: {
          '$eq': 'xxx0'
        }
      },
      inputStage: {
        stage: 'IXSCAN', // 索引扫描
        keyPattern: {
          author: 'hashed' // hash索引
        },
        indexName: 'author_hashed',
        isMultiKey: false,
        isUnique: false,
        isSparse: false,
        isPartial: false,
        indexVersion: 2,
        direction: 'forward',
        indexBounds: {
          author: [
            '[-6031660221272173267, -6031660221272173267]'
          ]
        }
      }
    }
```

stage状态

| 状态       | 描述         |
| -------- | ---------- |
| COLLSCAN | 全表扫描       |
| FETCH    | 根据索引检索指定文档 |
| IXSCAN   | 索引扫描       |
