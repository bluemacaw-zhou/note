# IM 系统设计文档

本文档整理了 IM 系统各个流程的核心设计思想和关键要点。

## 目录

- [核心实体关系](#核心实体关系)
- [核心实体生命周期](#核心实体生命周期)
- [发送消息流程](#发送消息流程)
- [查询消息流程](#查询消息流程)
- [未读数同步流程](#未读数同步流程)
- [未同步数同步流程](#未同步数同步流程)
- [数据生命周期](#数据生命周期)

---

## 核心实体关系

> 流程图文件：`entity-relationship.md`

本章节描述 IM 系统的核心实体关系模型，包括组织架构、通信核心实体及其关联关系。

### 组织架构实体

**Company（公司）**：

公司是组织架构的顶层实体，包含名称、编码、类型、状态等基本信息。公司与用户是一对多关系，一个公司雇用多个用户。

**User（用户）**：

用户隶属于公司，包含用户名、昵称、邮箱、电话、头像、在线状态等信息。用户可以参与多个会话，可以发送消息。

**Group（群组）**：

群组存储群名称和群头像等展示信息，详细信息由外部系统维护。群组与 Session 是一对一关系，session_id 等于 group_id。

### 通信核心实体

**Session（会话）**：

会话是消息的容器，包含 session_type（private/group）和 version（会话版本号）。version 是逻辑时钟，单调递增，每条新消息使 version 加1。群聊场景中 session_id 等于 group_id，私聊场景中 session_id 由两个用户 ID 推导生成。

**UserSessionState（用户会话状态）**：

用户会话状态记录用户在特定会话中的参与情况，包含：
- last_read_version：最后已读版本号
- join_version：加入时的会话版本号（可见性起点）
- leave_version：离开时的会话版本号（可见性终点）
- join_time 和 leave_time：加入和离开的时间

未读数计算公式根据状态不同：
- 正常：Session.version - last_read_version
- 已离开：leave_version - last_read_version

可见性范围：join_version <= visible_version <= leave_version

**DeviceSyncState（设备同步状态）**：

设备同步状态为每个设备独立维护同步进度，包含：
- last_sync_version：该设备最后同步的版本号
- leave_version：用户离开时的会话版本号（冻结未同步数）
- device_id：设备唯一标识

未同步数计算公式：
- 正常：Session.version - last_sync_version
- 已离开：leave_version - last_sync_version

**Message（消息）**：

消息包含 session_id、version（对应会话版本号）、发送者和接收者信息、消息类型和内容。version 字段用于增量拉取和可见性控制。消息同时记录发送者和接收者的公司快照，便于按公司维度查询。

### 核心设计原则

**生命周期同步**：

Session 和 UserSessionState 在同一事务中创建，保证数据一致性。Session 永不销毁，UserSessionState 永不销毁，DeviceSyncState 定期清理。

**版本号机制**：

version 作为逻辑时钟单调递增，是计算未读数和未同步数的基础。所有计算都基于版本差值，避免存储冗余字段。

**可见性边界控制**：

join_version 标记可见性起点，后加入成员只能看到加入后的消息。leave_version 标记可见性终点，离开后的消息完全不可见。

---

## 核心实体生命周期

> 流程图文件：`flow-entity-lifecycle.md`

本章节描述 Session、UserSessionState、DeviceSyncState 三个核心实体的完整生命周期管理策略。

### Session 生命周期

**创建时机 - 主动创建**：

Session 采用主动创建策略，而非懒创建。在加好友或建群时立即创建 Session 记录，version 初始化为 0。这样设计的好处是保证会话的稳定性，避免消息发送时才创建会话导致的竞态条件。

**更新时机 - 每条消息**：

每条消息发送时，Session.version 自增1，Session.update_time 更新为当前时间。版本号是整个系统计算未读数和未同步数的基础，必须严格单调递增。

**销毁时机 - 永不销毁**：

Session 永不删除，即使好友解除或群解散。保留历史 Session 记录有助于审计、合规和数据分析。通过 UserSessionState 的 leave_time 字段来标识用户是否还在会话中。

### UserSessionState 生命周期

**创建时机 - 跟随 Session**：

UserSessionState 跟随 Session 创建，但针对不同场景有细微差异：
- 加好友时：为双方用户各创建一条记录，join_version = 0
- 建群时：为所有初始成员创建记录，join_version = 0
- 后续加群时：为新成员创建记录，join_version = 当前 Session.version

关键设计：后加入的成员的 join_version 记录加入时刻的版本号，配合 leave_version 形成精确的可见性范围（join_version <= visible_version <= leave_version），确保新成员只能看到加入后的消息。

**更新时机 - 已读版本**：

根据用户在线状态和会话状态分为三种情况：
- 在线且在会话中：客户端周期性上报已读版本（滚动到最新消息、5秒定时器、切换会话时触发）
- 在线但不在会话中：用户点击会话时一次性上报已读版本，清零未读数
- 离线：不更新，未读数在服务端自动累积

**更新时机 - 离开会话**：

当发生踢出、解散、退群、解除好友等事件时，立即更新 leave_time 和 leave_version。leave_version 记录离开时刻的 Session.version，冻结可见性上限和未读数计算。即使会话继续活跃，已离开用户的未读数保持不变。

**销毁时机 - 永不销毁**：

UserSessionState 永不删除，保留用户在会话中的完整历史。通过 leave_time 字段区分用户是活跃成员还是已离开成员，支持审计和合规需求。

### DeviceSyncState 生命周期

**创建时机 - 懒创建**：

DeviceSyncState 采用懒创建策略，设备首次登录某个会话时才创建记录。last_sync_version 初始化为 0，表示需要从头同步所有历史消息。这种设计避免为所有可能的设备预先创建记录，节省存储空间。

**更新时机 - ACK 确认**：

客户端发送 ACK 时更新 last_sync_version。触发场景包括：收到推送消息后立即 ACK、拉取历史消息后批量 ACK。采用缓冲策略（100毫秒时间窗口或10条消息数量阈值）减少数据库更新频率。

**更新时机 - 用户离开**：

当用户离开会话时，批量更新该用户所有设备的 DeviceSyncState，设置 leave_time 和 leave_version。所有设备只能同步到 version <= leave_version 的消息，冻结未同步数计算上限。

**销毁时机 - 7天未活跃**：

定时任务每天凌晨执行，删除 update_time 超过7天的 DeviceSyncState 记录。清理原因包括：避免数据无限增长、7天未登录的设备大概率不再使用、用户可能换设备或卸载应用。设备下次登录时重新创建记录，从头同步即可。

### 关键设计原则

**数据分层管理**：
- Session：永久存在，会话主体不可删除
- UserSessionState：永久存在，记录用户参与历史
- DeviceSyncState：定期清理，设备状态数据可重建

**版本号边界控制**：
- join_version：标记可见性起点，后加入成员只能看到加入后的消息
- leave_version：标记可见性终点，离开后的消息完全不可见

**状态标记而非删除**：
- 通过 leave_time 标记用户是否离开，而非删除记录
- 保留完整历史，支持审计和数据分析
- 查询时通过 leave_time IS NULL 过滤活跃成员

---

## 发送消息流程

> 流程图文件：`flow-send-message.md`

### 并行架构设计

采用推送与存储并行的架构，实现实时性与可靠性的平衡。消息到达后立即推送给在线用户（延迟10-50ms），用户可以马上看到消息，同时通过MQ异步解耦存储操作，避免阻塞推送流程。

### 存储层设计

**MongoDB 按月分 collection 策略**：

采用 messages_YYYYMM 的命名规范，每月一个独立 collection。这种设计带来三大优势：
- 支持秒级清理历史数据（直接 DROP collection）
- 方便按月归档数据到对象存储
- 实现冷热分离（旧数据迁移到 HDD 或归档存储）

**原子性保证**：

通过 MongoDB 事务保证消息插入和会话版本更新的原子性。每条新消息都会触发 Session.version 自增，这个版本号是整个系统计算未读数和未同步数的基础。

### 分析层同步

**Change Stream 自动同步**：

数据通过 MongoDB Change Stream 自动同步到 ClickHouse 分析库，无需引入第三方同步组件。采用批量缓冲策略（累积1000条消息或等待1秒），在延迟和性能之间取得平衡，实现1-3秒的准实时同步。支持断点续传机制，即使同步进程重启也能从上次位置继续。

**ClickHouse 分析能力**：

ClickHouse 列式存储提供约10:1的压缩比，大幅降低存储成本。支持任意维度的组合查询（如按公司、消息类型、时间范围等），满足合规审计和数据分析需求。

---

## 查询消息流程

> 流程图文件：`flow-query-messages.md`

本章节描述基于可见性控制的消息查询流程，所有查询场景都必须先检查 UserSessionState 获取可见性范围。

### 三种核心查询场景

**场景1：查询最近消息（Redis缓存）**

针对群聊的最近消息使用 Redis SortedSet 缓存，以 version 作为 score 实现有序存储。查询流程分为三步：

步骤1：查询 UserSessionState 获取 join_version 和 leave_version，确定用户的可见性范围。

步骤2：判断数据源。群聊且在7天内从 Redis 查询（ZREVRANGE），私聊或超过7天查询 MongoDB，查询条件包含 version >= join_version 过滤加入前的消息。

步骤3：应用可见性过滤。过滤 version < join_version 的消息（加入前不可见），过滤 version > leave_version 的消息（离开后不可见）。

性能：5-15ms。适用场景：群聊最近7天消息的高频访问。

**场景2：查询历史消息（MongoDB跨月查询）**

针对历史消息使用 MongoDB 跨月循环查询策略，查询流程分为两步：

步骤1：查询 UserSessionState 获取 join_version 和 leave_version，确定可见性范围（如 50 <= version <= current）。

步骤2：初始化跨月查询。从 cursor_version 对应的月份开始，查询条件包含 version < cursor_version（分页）、version >= join_version（可见性起点）、version <= leave_version（如果已离开）。如果当前月份消息数量不够，往前推一个月继续查询，循环至多3个月直到凑够目标数量或到达 join_version 或达到月份限制。

循环查询示例：需要20条，cursor_version=130，join_version=50。第一次查询 messages_202503，范围 50 <= version < 130，返回15条。第二次查询 messages_202502，范围 50 <= version < 115，返回5条。凑够20条结束。所有返回消息都满足 version >= join_version 的可见性保障。

性能：10-20ms。适用场景：私聊和群聊的历史消息查询。

**场景3：组合条件搜索会话（ClickHouse）**

针对复杂组合条件（如按公司、消息类型、时间范围等）采用两阶段查询策略：

阶段1：聚合查询符合条件的会话。ClickHouse 按条件（from_company、msg_type、date_range）聚合查询，返回符合条件的 session_id 列表（不含具体消息）。GROUP BY session_id，ORDER BY last_msg_time，返回会话列表供用户选择。性能：200-600ms。

阶段2：用户点击会话查看消息。步骤1：查询 UserSessionState 获取该会话的 join_version 和 leave_version。步骤2：在可见性范围内查询消息，查询条件为 join_version <= version <= leave_version，在数据库层面应用可见性过滤，只返回可见范围内的消息。性能：10-20ms。

适用场景：按公司、类型、时间等组合条件搜索会话。

### 核心设计原则

**所有查询必须先检查可见性**：

每个查询场景的第一步都是查询 UserSessionState 获取 join_version 和 leave_version，确定用户在该会话的可见性范围。

**join_version 控制可见性起点**：

后加入成员只能看到加入后的消息，查询条件包含 version >= join_version。新成员加入时 join_version 设置为当前 Session.version，历史消息对其不可见。

**leave_version 控制可见性终点**：

离开后的消息不可见，查询条件包含 version <= leave_version（如果已离开）。用户被踢出或退出时 leave_version 设置为当前 Session.version，之后的消息对其不可见。

**数据库层面过滤**：

可见性控制通过索引过滤在数据库层面实现，性能优于应用层后置过滤。利用 version 字段的索引快速定位可见范围。

---

## 未读数同步流程

> 流程图文件：`flow-unread-count-sync.md`

本章节描述基于版本号动态计算未读数的流程，系统不存储冗余字段，完全通过版本差值实时计算。

### 两种核心场景

**场景1：接收者在线**

消息发送后 Session.version 自增，推送服务推送给在线用户。接收者分为两种情况：

在线且在会话中：用户正在查看该会话，收到推送后周期性上报已读版本。触发时机包括滚动到最新消息、5秒定时器、切换会话。服务端异步更新 UserSessionState.last_read_version，未读数保持为0。

在线但不在会话中：用户在其他页面，收到推送后客户端在本地维护未读数并显示角标。服务端的 last_read_version 保持不变，未读数自动累积。用户点击会话后一次性上报当前最新版本，清零未读数。

**场景2：接收者离线 - 上线查询未读数**

推送服务检测到接收者不在线，不推送消息。服务端的 last_read_version 保持不变，未读数累积在服务端。

用户上线时连表查询 Session 和 UserSessionState，自动处理 leave_version：
- 有 leave_version：使用冻结版本计算 unread = leave_version - last_read_version
- 无 leave_version：使用当前版本计算 unread = Session.version - last_read_version

只返回 unread_count > 0 的会话。客户端根据未读数显示角标。

### 核心设计原则

**版本号动态计算**：

未读数公式为 Session.version - last_read_version（正常）或 leave_version - last_read_version（已离开）。系统不存储冗余字段，避免数据不一致风险。

**在线时客户端自维护**：

在线用户的未读数由客户端维护并周期性上报已读版本，减少服务端压力。服务端只存储 last_read_version，由客户端负责计算和显示未读角标。

**离线时服务端连表查询**：

用户上线时一次性连表查询所有会话的未读数。Session 和 UserSessionState 生命周期同步，连表查询无缺失。leave_version 自动处理，无需特殊逻辑。

**多端同步**：

用户在一个设备上阅读消息后，通过 WebSocket 推送已读事件到其他在线设备。其他设备收到后更新本地已读版本，清除未读角标，实现多端已读同步。

---

## 未同步数同步流程

> 流程图文件：`flow-unsync-count-sync.md`

本章节描述设备维度的消息同步流程，每个设备独立维护 last_sync_version，支持不同的同步进度。

### 三种核心场景

**场景1：设备在线**

消息发送后 Session.version 自增，推送服务推送给所有在线设备。在线设备收到推送后保存到本地数据库，发送批量 ACK 确认。服务端异步更新 DeviceSyncState.last_sync_version，未同步数保持为0。

批量 ACK 策略：客户端缓冲100毫秒或10条消息，先到先发送，减少请求频率。服务端也采用批量更新，缓冲100毫秒后使用 bulkWrite 批量更新多个设备，减少数据库压力。

**场景2：设备离线 - 上线查询未同步数**

推送服务检测到设备不在线，不推送消息。设备的 last_sync_version 保持不变，未同步数累积在服务端。

设备上线时连表查询 Session、UserSessionState 和 DeviceSyncState，自动处理 leave_version：
- 有 leave_version：从 UserSessionState fork leave_version 到 DeviceSyncState，使用冻结版本计算 unsync = leave_version - last_sync_version
- 无 leave_version：使用当前版本计算 unsync = Session.version - last_sync_version

只返回 unsync_count > 0 的会话。设备拉取未同步消息，支持分批拉取（每批100条），发送 ACK 后更新 last_sync_version。

**场景3：DeviceSyncState 过期 - 从 UserSessionState fork leave_version**

设备7天未登录，DeviceSyncState 被清理以节省存储空间。期间用户可能被踢出群（UserSessionState.leave_version 已设置）。

设备重新登录时查询 DeviceSyncState 返回空。系统查询 UserSessionState 获取用户状态。懒创建 DeviceSyncState，从 UserSessionState fork leave_version 到设备维度。这样保证设备维度的可见性一致性，未同步数和可见性范围正确。

fork 机制的关键作用：防止错误计算未同步数，使用 leave_version 而不是 Session.version。支持过期重建，DeviceSyncState 过期清理后重新登录时从 UserSessionState 恢复状态。双层 leave_version 控制：UserSessionState.leave_version（用户维度）和 DeviceSyncState.leave_version（设备维度，fork 自用户）。

### 核心设计原则

**设备在线时批量 ACK**：

在线设备收到推送后批量 ACK（100ms 或10条），减少服务端压力。服务端也批量更新，在千人大群场景下减少99%的数据库操作。

**设备离线时连表查询**：

设备上线时一次性连表查询所有未同步会话。leave_version 自动处理，无需特殊逻辑。从 UserSessionState fork leave_version 到设备维度。

**DeviceSyncState 过期后重建**：

7天未登录的设备 DeviceSyncState 被清理。重新登录时从 UserSessionState 恢复状态。fork 机制保证设备维度可见性一致性。

**多设备独立同步**：

每个设备独立维护 last_sync_version，支持不同的同步进度。设备级别的 leave_version 精确控制未同步数和可见性范围。

---

## 数据生命周期

> 流程图文件：`data-lifecycle.md`

本章节描述数据如何从 MongoDB 主库自动同步到 Redis 缓存和 ClickHouse 分析库。

### MongoDB Change Stream 同步机制

系统使用 MongoDB Change Stream 监听消息插入事件，实时触发数据同步和计算。Change Stream 是 MongoDB 原生功能，支持断点续传（Resume Token），无需引入第三方同步组件。

消息创建后毫秒级触发 Change Stream，消息存储服务监听到变更事件并执行计算逻辑（聚合、统计等）。

### Redis 缓存维护（仅群聊）

针对群聊消息更新 Redis 缓存。使用 ZADD 操作，Key 为 session:{session_id}:messages，Score 为 version，Value 为消息 JSON 字符串。

缓存限制策略：只缓存群聊消息，私聊消息不缓存。保留最近7天、最多1000条消息。使用 ZREMRANGEBYRANK 限制缓存大小，只保留最新1000条。TTL 设置为7天自动过期。

私聊消息不缓存，直接查询 MongoDB 即可，避免缓存膨胀。

### ClickHouse 分析库同步

消息存储服务执行计算后投递到 RabbitMQ，ClickHouse 消费服务自动消费消息（延迟1-3秒）。写入 message_analytics 表用于分析查询。

ClickHouse 采用列式存储和 ZSTD 压缩，压缩比约10:1。按月自动分区（202501、202502等），支持 TTL 自动删除10年前数据。

查询性能：合规查询200-500ms，复杂组合查询800ms-2s，支持任意维度的组合查询。

### 数据流转全流程

原始消息到达 → RabbitMQ 队列 → 消息存储服务 → MongoDB 主库（T0时刻）→ Change Stream 触发（T0+毫秒级）→ 消息存储服务监听变更并执行计算 → 群聊消息更新 Redis 缓存 → 投递到 RabbitMQ → ClickHouse 消费服务 → ClickHouse 分析库（T0+秒级）。

整个流程实现准实时同步，MongoDB 作为主库保证事务和一致性，Redis 缓存提供极速查询，ClickHouse 支持复杂分析。

---

## 总结

本 IM 系统采用基于版本号的设计，实现了以下核心特性：

### 版本号机制

- Session.version 作为会话进度的唯一标识
- 通过版本差值动态计算未读数和未同步数
- 避免存储冗余字段，降低数据不一致风险
- 支持精确的增量查询和同步

### 零写扩散

- 发送消息只更新 Session.version 一条记录
- UserSessionState 和 DeviceSyncState 按需懒更新
- 在线设备 ACK 时才更新同步状态
- 大群场景下性能优势明显

### leave_version 边界控制

- 用户离开会话时立即冻结版本号
- 精确控制离开后的消息边界和计数
- UserSessionState.leave_version 控制未读数（用户维度）
- DeviceSyncState.leave_version 控制未同步数（设备维度）
- 防止越权访问离开后的消息

### 多设备支持

- 每个设备独立维护 last_sync_version
- 支持不同设备的不同同步进度
- 批量 ACK 优化降低数据库压力
- 设备级别的 leave_version 精确控制

### 分层存储与查询

- Redis 缓存满足高频访问（5-10ms）
- MongoDB 按月分 collection 支持历史查询（10-15ms）
- ClickHouse 支持复杂组合查询（500ms-1.5s）
- 五种场景的智能路由策略
- 循环查询和批量过滤优化性能

这些设计共同构成了一个高性能、可扩展、精确控制的 IM 消息系统。
