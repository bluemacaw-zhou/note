### HBase读写框架

![[HBase读写框架.excalidraw]]

### HBase读写数据流程

![[HBase读写数据流程.excalidraw]]

### HBase数据结构

![[HBase数据结构.png]]]

### RowKey

用来检索记录的唯一主键 类似于Redis中的key 有三种查找方式

1. 通过get指令 访问单个rowkey的数据
2. 通过scan指令 扫描全表
3. 通过scan指令 指定rowkey范围 进行范围查找