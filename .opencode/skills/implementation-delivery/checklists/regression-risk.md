# Regression Risk Checklist

- [ ] 共享 API 或契约消费者已考虑。
- [ ] 持久化数据、配置和迁移影响已考虑。
- [ ] 平台差异和环境依赖已考虑。
- [ ] 异步、缓存、重试和状态顺序已考虑。
- [ ] 用户可见流程和错误反馈已考虑。
- [ ] Test Surface 已覆盖受影响入口、失败路径、手工 smoke 或说明无法覆盖原因。
- [ ] Delegation fallback 没有被当作验证通过或完成证据。
