#sourcecode
#druid
### 核心概念
![[Druid链接.excalidraw]]

#### 逻辑链接
DruidPooledConnection

#### 物理连接
Connection

#### 逻辑连接和物理连接区别
针对关闭连接的动作 
物理链接直接使得连接不可用
逻辑连接则是把连接归还到连接池当中

参考文献
https://www.cnblogs.com/liconglong/p/17924322.html