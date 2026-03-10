---
type: chronicle
source: 历史笔记迁移
distilled: 2026-03-10
tags: ["docker", "rabbitmq-mongdb-clickhouse", "RabbitMQ", "MongoDB", "ClickHouse"]
---

# RabbitMQ + MongoDB + ClickHouse 安装

```yaml
version: '3.8'

services:
  # MongoDB 8.0.15 副本集 - CDC 需要副本集模式
  mongodb:
    image: mongo:8.0.15
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
      MONGO_INITDB_DATABASE: im_db
    entrypoint: ["/bin/bash", "-c"]
    command: >
      "cp /tmp/mongodb-keyfile /data/mongodb-keyfile &&
       chown mongodb:mongodb /data/mongodb-keyfile &&
       chmod 400 /data/mongodb-keyfile &&
       exec docker-entrypoint.sh mongod --replSet rs0 --bind_ip_all --keyFile /data/mongodb-keyfile"
    volumes:
      - E:/workspace/docker/rabbitmq-mongo-clickhouse/mongodb/data:/data/db
      - ./init-scripts/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
      - ./init-scripts/mongodb-keyfile:/tmp/mongodb-keyfile:ro
    networks:
      - data-pipeline
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  # ClickHouse 24.3 - LTS 版本，与 MongoDB 8.x 兼容
  clickhouse:
    image: clickhouse/clickhouse-server:24.3
    container_name: clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    environment:
      CLICKHOUSE_DB: im_analytics
      CLICKHOUSE_USER: admin
      CLICKHOUSE_PASSWORD: admin
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
    volumes:
      - E:/workspace/docker/rabbitmq-mongo-clickhouse/clickhouse/data:/var/lib/clickhouse
      - ./init-scripts/clickhouse-init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - data-pipeline
    ulimits:
      nofile:
        soft: 262144
        hard: 262144
    healthcheck:
      test: ["CMD", "clickhouse-client", "--user", "admin", "--password", "admin", "--query", "SELECT 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  clickhouse-tabix:
    image: spoonest/clickhouse-tabix-web-client:latest
    container_name: clickhouse-tabix
    ports:
      - "8124:80"
    networks:
      - data-pipeline
    depends_on:
      - clickhouse

  # RabbitMQ - 消息队列
  rabbitmq:
    image: rabbitmq:3.12-management
    container_name: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
    volumes:
      - E:/workspace/docker/rabbitmq-mongo-clickhouse/rabbitmq/data:/var/lib/rabbitmq
    networks:
      - data-pipeline
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  data-pipeline:
    driver: bridge
```
