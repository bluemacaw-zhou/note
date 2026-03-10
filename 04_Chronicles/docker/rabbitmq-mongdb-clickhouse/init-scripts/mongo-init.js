// MongoDB 副本集初始化脚本
// 这个脚本会在容器启动时执行

// 等待 MongoDB 完全启动
sleep(5000);

print('开始初始化 MongoDB 副本集...');

try {
    // 初始化副本集
    rs.initiate({
        _id: "rs0",
        members: [
            { _id: 0, host: "mongodb:27017" }
        ]
    });

    print('副本集初始化成功！');

    // 等待副本集稳定
    sleep(5000);

    // 切换到 im_db 数据库
    db = db.getSiblingDB('im_db');

    // 创建示例集合和索引
    db.createCollection('messages');
    db.messages.createIndex({ "conversation_id": 1, "send_time": -1 });
    db.messages.createIndex({ "sender_id": 1 });
    db.messages.createIndex({ "receiver_id": 1 });

    // 插入示例数据
    db.messages.insertMany([
        {
            conversation_id: "conv_001",
            sender_id: "user_001",
            receiver_id: "user_002",
            message_type: 1,
            content: "Hello, this is a test message",
            send_time: new Date(),
            status: 1
        },
        {
            conversation_id: "conv_001",
            sender_id: "user_002",
            receiver_id: "user_001",
            message_type: 1,
            content: "Hi, received your message",
            send_time: new Date(),
            status: 1
        }
    ]);

    print('示例数据插入成功！');
    print('MongoDB 初始化完成！');

} catch (e) {
    print('初始化过程中出现错误: ' + e);
}
