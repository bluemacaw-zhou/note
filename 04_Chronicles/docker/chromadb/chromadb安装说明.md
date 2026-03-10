# ChromaDB 安装说明

## 前置准备
创建挂载目录：
```bash
mkdir -p /home/michael/workspace/docker/chromadb/data
mkdir -p /home/michael/workspace/docker/chromadb/config
```

## 启动
```bash
docker-compose up -d
```

## 服务端口
| 服务 | 端口 | 说明 |
|------|------|------|
| ChromaDB | 18000 | HTTP 接口（映射自容器 8000） |
