# 流程图经典案例：OpenCode Gateway 消息处理逻辑

```mermaid
flowchart TD
    Start([开始]) --> ReceiveMsg[接收OpenClaw消息]
    ReceiveMsg --> VerifySig[验证HMAC签名]
    VerifySig -->|有效| ParseMsg[解析消息内容]
    ParseMsg --> RiskCheck[风控检查]
    
    RiskCheck -->|安全| BuildPrompt[构建提示词]
    RiskCheck -->|敏感| SendBlocked[发送拦截消息]
    SendBlocked --> LogEvent[记录日志]
    LogEvent --> End([结束])
    
    BuildPrompt --> CallOpenCode[调用opencode]
    CallOpenCode --> GenerateResp[生成回复]
    GenerateResp --> ChunkStream[分片处理]
    
    ChunkStream --> PushToCallback[推送到OpenClaw回调]
    PushToCallback --> LogEvent
    
    %% 异常处理分支
    CallOpenCode -->|超时| HandleTimeout[处理超时]
    HandleTimeout --> SendError[发送错误消息]
    SendError --> LogEvent
    
    CallOpenCode -->|失败| HandleError[处理错误]
    HandleError --> SendError
    HandleError --> LogEvent
```

**说明**：
- **正常流程**：消息接收→签名验证→风控检查→AI生成→分片推送
- **风控拦截**：检测到敏感内容时直接返回拦截提示
- **异常处理**：包含超时和调用失败的错误处理机制
- **日志记录**：所有关键操作都记录日志便于追踪

**流程特点**：
- 采用模块化设计，每个步骤职责清晰
- 完善的异常处理和日志机制
- 支持实时流式回复效果
