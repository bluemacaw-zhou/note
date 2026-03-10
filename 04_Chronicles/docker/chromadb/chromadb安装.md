---
type: chronicle
source: 历史笔记迁移
distilled: 2026-03-10
tags: ["docker", "chromadb"]
---

# ChromaDB 安装

```yaml
version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:latest
    container_name: chromadb
    # 关键：明确绑定到所有网络接口
    ports:
      - "0.0.0.0:18000:8000"
    volumes:
      - /home/michael/workspace/docker/chromadb/data:/chroma/chroma
      - /home/michael/workspace/docker/chromadb/config:/chroma/config
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
      - CHROMA_SERVER_AUTH_CREDENTIALS_FILE=/chroma/config/server.htpasswd
      - CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER=chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider
      - CHROMA_SERVER_AUTH_PROVIDER=chromadb.auth.basic.BasicAuthServerProvider
      - CHROMA_LOG_LEVEL=INFO
      # 关键：允许外部访问
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    restart: unless-stopped
    networks:
      - chromadb_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  chromadb_network:
    driver: bridge
```
