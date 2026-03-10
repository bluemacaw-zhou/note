# MongoDB 安装说明

## 前置准备
创建挂载目录：
```bash
mkdir -p E:/workspace/docker/mongodb/data
mkdir -p E:/workspace/docker/mongodb/config
mkdir -p E:/workspace/docker/mongodb/logs
```

## 启动
```bash
docker-compose up -d
```

## 服务端口
| 服务 | 端口 | 说明 |
|------|------|------|
| MongoDB | 27017 | 主连接端口 |
| Mongo Express | 8081 | Web 管理界面 |
