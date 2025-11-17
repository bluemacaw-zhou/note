-- ClickHouse 初始化脚本
-- 创建数据库
CREATE DATABASE IF NOT EXISTS im_analytics;

-- 使用数据库
USE im_analytics;

-- 创建消息表 (使用 MergeTree 引擎)
CREATE TABLE IF NOT EXISTS messages
(
    _id String,
    conversation_id String,
    sender_id String,
    receiver_id String,
    message_type Int32,
    content String,
    send_time DateTime64(3),
    status Int32,
    create_time DateTime64(3) DEFAULT now64(),
    update_time DateTime64(3) DEFAULT now64()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(send_time)
ORDER BY (conversation_id, send_time)
SETTINGS index_granularity = 8192;

-- 创建消息统计表 (用于实时聚合)
CREATE TABLE IF NOT EXISTS message_stats
(
    date Date,
    hour UInt8,
    conversation_id String,
    sender_id String,
    message_count UInt64,
    total_length UInt64
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, hour, conversation_id, sender_id)
SETTINGS index_granularity = 8192;

-- 创建物化视图 (自动聚合消息数据)
CREATE MATERIALIZED VIEW IF NOT EXISTS message_stats_mv
TO message_stats
AS
SELECT
    toDate(send_time) AS date,
    toHour(send_time) AS hour,
    conversation_id,
    sender_id,
    count() AS message_count,
    sum(length(content)) AS total_length
FROM messages
GROUP BY date, hour, conversation_id, sender_id;

-- 创建用户活跃度表
CREATE TABLE IF NOT EXISTS user_activity
(
    user_id String,
    activity_date Date,
    message_sent UInt32,
    message_received UInt32,
    active_hours Array(UInt8),
    last_active_time DateTime64(3)
)
ENGINE = ReplacingMergeTree(last_active_time)
PARTITION BY toYYYYMM(activity_date)
ORDER BY (user_id, activity_date)
SETTINGS index_granularity = 8192;

-- 输出初始化完成信息
SELECT 'ClickHouse 数据库初始化完成！' AS status;
