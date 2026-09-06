# Skill Description 优化映射

基于测试结果，提供description优化建议。
记住 description 必须是中文 因为是中国人

## 触发率低于80%的Skill优化建议
TODO: 按以下格式补充skill description优化建议。
**示例**
```markdown
| Skill | 当前问题 | 优化建议 | 优先级 |
|-------|---------|---------|-------|
...
```

## 关键词优化矩阵

TODO: 按以下格式补充关键词优化
### 高频触发关键词（触发率>90%）

以下关键词组合具有很高的触发率：

**示例**
```markdown
| 关键词组合 | 适用Skill | 效果 |
|-----------|----------|-----|
| .docx, Word document | docx | 高 |
...
```

### 低频触发关键词（需优化）

以下关键词组合触发率较低：
**示例**
```markdown
| 关键词组合 | 当前Skill | 问题 | 建议 |
|-----------|----------|------|-----|
| artistic, visual art | canvas-design | 太抽象 | 添加"poster", "design"等具体词 |
| documentation | doc-coauthoring | 通用性太强 | 添加"proposal", "spec"等具体词 |
| testing | webapp-testing | 需指定框架 | 添加"Playwright", "browser" |
...
...
```

## 优化操作清单

**示例**
```markdown
1. **增加技术栈关键词**: 如Python/JavaScript/React等具体技术名称
2. **使用文件扩展名**: .docx, .pdf, .xlsx等明确文件类型
3. **增加使用场景**: 明确在什么情况下应触发
4. **添加DO NOT TRIGGER说明**: 明确什么时候不应触发
5. **使用动词开头**: "Build", "Create", "Use"等行动词
```

