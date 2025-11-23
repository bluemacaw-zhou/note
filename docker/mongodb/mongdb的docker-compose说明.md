## 查看 MongoDB 日志
docker-compose logs -f mongodb

## 查看 Mongo Express 日志
docker-compose logs mongo-express

## MongoDB连接信息

Host: localhost
Port: 27017
Username: admin
Password: admin
连接字符串: mongodb://admin:admin@localhost:27017/

## Mongo Express Web界面

打开浏览器访问: http://localhost:8081

## 终端启动
docker exec -it mongodb mongosh -u admin -p admin --authenticationDatabase admin

## url链接启动
mongodb://admin:admin@192.168.254.129:27017/?authSource=admin