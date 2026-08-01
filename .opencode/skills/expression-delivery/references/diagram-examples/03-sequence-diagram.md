# 时序图经典案例：OpenCode Gateway 消息处理流程

```mermaid
sequenceDiagram
    participant WeChat as 微信客户端
    participant WPlugin as WeChat Plugin
    participant Core as OpenClaw Core
    participant Gateway as Gateway Server
    participant RiskCtrl as 风控模块
    participant OpenCode as OpenCode Server
    participant Callback as OpenClaw回调
    
    WeChat->>WPlugin: 发送消息
    WPlugin->>Core: 转发消息
    Core->>Gateway: POST /openclaw/inbound
    Gateway->>RiskCtrl: 检查敏感词
    alt 消息安全
        RiskCtrl-->>Gateway: 允许处理
        Gateway->>OpenCode: 调用AI生成回复
        OpenCode-->>Gateway: 返回生成结果
        Gateway->>Callback: 分片推送回复
        Callback-->>Core: 接收分片回复
        Core-->>WPlugin: 转发回复到微信
        WPlugin-->>WeChat: 显示回复
    else 消息不安全
        RiskCtrl-->>Gateway: 拦截消息
        Gateway-->>WeChat: 发送拦截提示
    end
```

**说明**：
- **正常流程**：消息经风控检查后，由OpenCode生成回复，通过分片方式回推给用户
- **风控流程**：检测到敏感内容时直接拦截并返回提示
- **分片机制**：将长回复按字符切分，模拟流式效果

**关键组件**：
- 微信插件负责与客户端通信
- 网关服务器处理核心业务逻辑
- OpenCode服务器提供AI能力
- 风控模块确保消息安全性
