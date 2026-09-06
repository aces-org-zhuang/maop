# 技能触发率测试用例集

**输入**: skills_list.txt
**处理**: 根据description生成测试用例，注意，因为是中国人，触发词必须是中文
**输出**: test_cases.json
## Json格式: {skill_id,skill_name,test_type,trigger_phrase,expected_trigger}

**用例类型**:
- positive: 应该触发的场景
- negative: 不应触发的场景
- edge: 边缘情况

TODO: 请按以下示例补充相关测试用例
**示例**
```json
[
  {
    "skill_id": 1,
    "skill_name": "<skill_name>",
    "test_type": "positive|negative|edge",
    "trigger_phrase": "<测试的输入提示词>",
    "expected_trigger": "yes|no"
  },
  ...
]
```

**实际例子**
```json
[
  {
    "skill_id": 1,
    "skill_name": "algorithmic-art",
    "test_type": "positive",
    "trigger_phrase": "使用 p5.js创建 algorithmic art ",
    "expected_trigger": "yes"
  },
  {
    "skill_id": 2,
    "skill_name": "algorithmic-art",
    "test_type": "negative",
    "trigger_phrase": "写一个python脚本",
    "expected_trigger": "no"
  },
  {
    "skill_id": 3,
    "skill_name": "algorithmic-art",
    "test_type": "edge",
    "trigger_phrase": "创建code-based art",
    "expected_trigger": "yes"
  }
]
```
