## 官方文档

https://www.mongodb.com/zh-cn/docs/manual/

## 如何保证不丢数据

### writeConcern
写数据时指定
writeConcern: {w: "majority", j: true, timeout: 5000}
majority指的是写入集群大部分节点 比如说3个节点至少写入2个节点

### journal日志
类似mysql的redo日志 只要redo日志落盘 数据库宕机 数据仍然能够恢复
writeConcern中的j指的是是不是要写完journal日志后返回

## 安全

### 服务启动
服务启动时 需要开启安全认证 可以通过admin数据库添加角色 从而达到库级别的安全认证

## 调优

### wiredTigerCacheSizeGB
mongodb启动后会把一定的数据加载到内存 内存的大小由这个参数决定
默认是机器(内存 - 1G) / 2