---
name: skill-trigger-tester
description: 罗列所有可用技能，并Test skill trigger accuracy and opencode skill recognition performance. Validate skill trigger phrases effectiveness, analyze trigger rates, and generate optimization suggestions. Help improve skill descriptions and boost trigger accuracy. Use when 1- Testing skill trigger phrases, (2) Validating skill recognition, (3) Optimizing skill descriptions, (4) Auditing skill coverage. Triggers on phrases like "test skill triggers", "validate skill accuracy", "check trigger rate", "improve skill descriptions", "audit skill coverage".
---

# Skill Trigger Tester

Test and validate opencode skill trigger accuracy.

## Output

- Trigger accuracy reports (CSV/Markdown)
- Optimized skill description suggestions
- Test case templates
- Detailed execution logs

## Checklist

- [ ] Install CLI: `pip install -e scripts`
- [ ] List skills: `skill-trigger-test --list-skills`
- [ ] Define trigger phrases (positive/negative/edge cases)
- [ ] Run tests: `skill-trigger-test --file test_cases.json`
- [ ] Analyze reports and optimization suggestions
- [ ] Update SKILL.md descriptions based on results
- [ ] Re-test to validate improvements

## Usage

```bash
# List all available skills
skill-trigger-test --list-skills

# Test single skill trigger
skill-trigger-test --skill xlsx --trigger "create Excel spreadsheet"

# Test from JSON file
skill-trigger-test --file test_cases.json

# Update SKILL.md descriptions
skill-trigger-test --fix --fix-file optimized_descriptions.json
```

## References

- [trigger_rate.md](references\trigger_rate.md) - Trigger rate calculation and metrics
- [optimization_map.md](references\optimization_map.md) - Description optimization guide
- [skill_triggering_mechanism.md](references\skill_triggering_mechanism.md) - How opencode triggers work
- [test_cases_example.json](references\test_cases_example.json) - Test case format
- [workflow.md](references\workflow.md) - Workflow for skill trigger testing

## Results

| Metric | Description |
|--------|-------------|
| Trigger Success Rate | % of positive phrases that triggered |
| False Positive Rate | % of negative phrases that accidentally triggered |
| False Negative Rate | % of positive phrases that failed to trigger |

## 交付文件目录结构

```
.aces/projects/skill-trigger-tester/
├── outputs/                # 交付目录
│   ├── test_cases.json        # 测试用例(参照test_cases_example.json)
│   ├── optimized_descriptions.json     # 优化后的description 提供给skill-trigger-test --fix --fix-file使用
│   ├── test_results.csv    # 测试结果CSV
│   ├── trigger_rate.md     # 触发率报告
│   └── optimization_map.md # 优化映射
├── tests/                  # 测试目录
├── temp/                   # 临时文件，包括临时脚本和过程文件
└── logs/                   # 日志目录
```