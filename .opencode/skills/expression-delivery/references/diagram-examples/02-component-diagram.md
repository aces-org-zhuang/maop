# 组件图经典案例：OpenCode WeChat/QQ Gateway 系统架构

```mermaid
graph TB
    subgraph 客户端层
        WeChat[微信客户端]
        QQ[QQ客户端]
    end
    
    subgraph OpenClaw平台
        WPlugin[WeChat Plugin]
        QPlugin[QQ Plugin]
        Core[OpenClaw Core]
        MessageEngine[消息处理引擎]
        SessionManager[会话管理器]
    end
    
    subgraph 网关服务层
        Gateway[Gateway Server]
        Receiver[消息接收模块]
        RiskControl[风控拦截模块]
        HistoryMgr[会话历史管理]
        OpenCodeCaller[OpenCode调用模块]
        StreamChunker[流式分片模块]
        CallbackPusher[OpenClaw回推模块]
    end
    
    subgraph OpenCode服务层
        OpencodeServer[opencode serve]
        SessionMgr[会话管理]
        MessageGen[消息生成]
        EventStream[事件流]
    end
    
    subgraph 数据存储
        SessionStore[(会话历史)]
        ConfigStore[(配置信息)]
    end
    
    %% 关系定义
    WeChat -.include.-> WPlugin
    QQ -.include.-> QPlugin
    WPlugin -.include.-> Core
    QPlugin -.include.-> Core
    Core -.include.-> Gateway
    Receiver -.include.-> RiskControl
    HistoryMgr -.include.-> SessionStore
    OpenCodeCaller -.include.-> OpencodeServer
    StreamChunker -.include.-> CallbackPusher
    CallbackPusher -.include.-> MessageEngine
    OpencodeServer -.include.-> SessionMgr
    OpencodeServer -.include.-> MessageGen
    OpencodeServer -.include.-> EventStream
    OpenCodeCaller --> SessionStore
    OpenCodeCaller --> ConfigStore
```

**说明**：
- **客户端层**：微信和QQ客户端通过各自的OpenClaw插件接入
- **OpenClaw平台**：核心的消息处理和会话管理功能
- **网关服务层**：主要包含消息接收、风控、会话管理、OpenCode调用和流式分片等核心模块
- **OpenCode服务层**：提供会话管理和AI生成能力
- **数据存储**：存储会话历史和配置信息

**关系类型**：
- `-.include.- >`：包含关系，表示组件间的调用依赖
- `-->`：关联关系，表示数据流向或调用方向
