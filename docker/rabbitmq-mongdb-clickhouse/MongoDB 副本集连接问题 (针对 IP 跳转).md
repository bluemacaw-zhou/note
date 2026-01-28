**场景**：Compass 或 Spring Boot 连接时报错提示 `ETIMEDOUT 192.168.x.x`，而你填写的 IP 是 `10.106.x.x`。

- **根本原因**：MongoDB 副本集内部配置了私有 IP，客户端连接后会触发“自发现”机制，尝试重定向到那个无法访问的内网地址。
    
- **生产方案（修正服务器配置）**：
    
    1. 登录 Linux 容器：`docker exec -it mongodb mongosh -u admin -p`
        
    2. 获取配置：`cfg = rs.conf();`
        
    3. 修改成员地址：`cfg.members[0].host = "10.106.51.218:27017";`
        
    4. 应用配置：`rs.reconfig(cfg);`
        
- **快速绕过方案**：
    
    - **Spring Boot**：在 URI 后面加上 `?directConnection=true`。
        
    - **Compass**：在 Advanced Options 中勾选 **Direct Connection**。
