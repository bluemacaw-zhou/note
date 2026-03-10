---
type: chronicle
source: 历史笔记迁移
distilled: 2026-03-10
tags: ["docker", "mongodb"]
---

# MongoDB 安装

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
      MONGO_INITDB_DATABASE: mydb
    command: mongod --logpath /var/log/mongodb/mongod.log --logappend
    volumes:
      - E:/workspace/docker/mongodb/data:/data/db
      - E:/workspace/docker/mongodb/config:/data/configdb
      - E:/workspace/docker/mongodb/logs:/var/log/mongodb
    networks:
      - mongodb_network

  mongo-express:
    image: mongo-express:latest
    container_name: mongo-express
    restart: always
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin@mongodb:27017/
      ME_CONFIG_BASICAUTH: false
    depends_on:
      - mongodb
    networks:
      - mongodb_network

networks:
  mongodb_network:
    driver: bridge
```
