## 查看剩余内存指令

```shell
free -m | grep 'Mem:' | awk '{print $4}'
```

## 查看文件 (日志) 具体大小

```shell
ll -h
```

## 查找 java 服务

```shell
ps -ef | grep java
ps -aux | grep java

jps # 查看java所有进程
ll /proc/进程id
kill -9 进程id
```

## 查看机器性能

```shell
lsblk
free -h
lscpu
```

## 查看端口对应的进程

```shell
netstat -tunlp | grep :<port>
```
