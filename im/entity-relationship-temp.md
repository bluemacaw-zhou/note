@startuml 完整实体关系图-IM系统
!theme plain
skinparam linetype ortho

title IM系统完整实体关系图

' ============ 组织架构实体 ============
package "组织架构" {
  entity "Company\n(公司)" as Company {
    * id: String <<PK>>
    --
    * name: String // 公司名称
    * code: String // 公司编码
    * type: String // 公司类型
    * status: Integer // 状态
    create_time: Date
    update_time: Date
  }

  entity "User\n(用户)" as User {
    * id: Long <<PK>>
    --
    * company_id: String <<FK>>
    * username: String
    * nickname: String
    * email: String
    * phone: String
    * avatar: String
    * status: Integer // 在线状态
    create_time: Date
    update_time: Date
  }

  entity "Group\n(群组)" as Group {
    * id: String <<PK>>
    --
    * company_id: String <<FK>>
    * name: String // 群名称
    * avatar: String // 群头像
    * creator_id: Long <<FK>> // 创建者
    * owner_id: Long <<FK>> // 群主
    * group_type: String // 群类型
    * max_members: Integer // 最大成员数
    * status: Integer // 群状态
    create_time: Date
    update_time: Date
  }
}

' ============ 通信核心实体 ============
package "通信核心" {
  entity "Session\n(会话)" as Session {
    * id: String <<PK>>
    --
    * session_type: String // private/group
    * group_id: String <<FK>> // 关联的群组ID（私聊为null）
    create_time: Date
    update_time: Date
  }

  entity "UserSession\n(用户会话)" as UserSession {
    * id: String <<PK>>
    --
    * user_id: Long <<FK>>
    * session_id: String <<FK>>
    * session_type: String // private/group（冗余字段，避免JOIN）
    --
    join_time: Date // 加入时间
    leave_time: Date // 退出时间(null=在会话中)
    --
    unread_count: Long // 未读消息数(跨设备共享)
    last_ack_seq: Long // 最后确认序号(跨设备共享)
    last_ack_time: Date
    --
    create_time: Date
    update_time: Date
    --
    索引:
    - (user_id, session_id) 唯一
    - (session_id, leave_time) // 查询会话当前成员
    - (user_id, session_type) // 按类型查询用户的会话
  }

  entity "SessionView\n(会话视图-设备级)" as SessionView {
    * id: String <<PK>>
    --
    * user_id: Long <<FK>>
    * session_id: String <<FK>>
    * device_id: String // 设备唯一标识
    --
    unsync_count: Long // 该设备未同步消息数
    last_sync_seq: Long // 该设备最后同步消息id
    last_sync_time: Date // 该设备最后同步时间点
    --
    create_time: Date
    update_time: Date
    --
    索引:
    - (user_id, session_id, device_id) 唯一
    - (device_id) // 查询设备的所有会话
  }

  entity "Message\n(消息)" as Message {
    * id: String <<PK>>
    --
    * session_id: String <<FK>>
    * seq: Long // 会话内消息序号
    --
    * from_id: Long // 发送者ID
    * to_id: Long // 接收者ID
    * from_company: String // 发送者公司
    * to_company: String // 接收者公司
    --
    * msg_type: Integer
    * content: String
    * msg_time: Date // 消息时间（毫秒级）
    --
    client_msg_id: String // 客户端消息ID（去重）
    client_info: String // 客户端信息
    --
    deleted: Integer // 删除标记
    status: Integer // 消息状态
    --
    索引:
    - (session_id, seq) 唯一
    - (session_id, msg_time) // 基于时间查询
    - (id) 唯一
  }

  entity "MessageInvisibleRange\n(消息不可见范围)" as MessageInvisibleRange {
    * id: String <<PK>>
    --
    * session_id: String <<FK>>
    * user_id: Long <<FK>>
    --
    * invisible_start_time: Date // 不可见起始时间（包含）
    * invisible_end_time: Date // 不可见结束时间（包含），null表示持续到现在
    --
    * range_type: String // 范围类型(unfriend/blocked/kicked/left_group)
    * event_time: Date // 事件发生时间
    --
    create_time: Date // 记录创建时间
    --
    说明:
    - 该用户不能看 invisible_start_time <= msg_time <= invisible_end_time 的消息
    - 多条记录表示多个不可见区间（如多次解除好友又添加）
    - 查询时只需排除落在这些区间内的消息
    --
    示例:
    用户A和B的关系变化:
    1. 10:00:00 解除好友 -> (start=10:00:00, end=20:00:00)
    2. 20:00:00 重新添加 -> 更新上一条记录的 end_time
    3. 30:00:00 再次解除 -> (start=30:00:00, end=null)
    --
    索引:
    - (user_id, session_id) // 查询用户在某会话的所有不可见区间
    - (session_id, user_id, invisible_start_time, invisible_end_time) // 范围查询
  }
}

' ============ 关系定义 ============

' 组织架构关系
Company ||--o{ User : "雇用"
Company ||--o{ Group : "拥有"
User ||--|| Group : "创建"
User ||--|| Group : "拥有(群主)"

' 通信关系
Group ||--|| Session : "关联会话(1:1)"
User ||--o{ UserSession : "参与会话(1:N)"
Session ||--o{ UserSession : "成员(1:N)"
UserSession ||--o{ SessionView : "设备视图(1:N)"
User ||--o{ Message : "发送"
Session ||--o{ Message : "包含(1:N)"
User ||--o{ MessageInvisibleRange : "不可见区间"
Session ||--o{ MessageInvisibleRange : "范围限制"
Message ||--o{ Message : "回复/转发"

@enduml
