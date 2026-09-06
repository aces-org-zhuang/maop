# Skill Trigger Tester Workflow

## 基本信息

**工作流名称**: skill-trigger-tester-workflow
**工作流类型**: skill
**项目目录**: ./
**工作流文件路径**: skills/skill-trigger-tester/references/workflow.md
**本工作流是否有效**: true
**创建时间**: 2026-04-05
**负责人**: Developer

## 核心原则

### 核心原则说明
- 精简高效原则
- 测试驱动验证
- 工作流命名标准

## 目录结构

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

## 执行步骤

### Stage 1: 列出可用技能
[ ] Task: 列出所有可用技能
    - 操作(必选)：
        Step1: 运行 `skill-trigger-test --list-skills`
        Step2: 记录技能名称列表

### Stage 2: 定义测试用例
[ ] Task: 创建包含触发短语的测试用例
    - 操作(必选)：
        Step1: 遵循 test_cases_example.json 格式
        Step2: 创建正向用例：应该触发的短语
        Step3: 创建负向用例：不应该触发的短语
        Step4: 创建边界用例：边界条件

### Stage 3: 运行测试
[ ] Task: 执行测试套件
    - 操作(必选)：
        Step1: 运行 `skill-trigger-test --file test_cases.json`
        Step2: 收集测试结果和触发率

### Stage 4: 分析结果
[ ] Task: 审查触发准确率报告
    - 操作(必选)：
        Step1: 计算触发成功率
        Step2: 计算误触发率
        Step3: 计算漏触发率

### Stage 5: 优化描述
[ ] Task: 基于结果更新SKILL.md描述
    - 操作(必选)：
        Step1: 使用 trigger_rate.md 的优化建议
        Step2: 应用 optimization_map.md 的建议
        Step3: 优化后重新测试

## 异常场景和处理方式

| 错误代码 | 异常描述 | 处理动作 | 负责人 |
|----------|----------|----------|--------|
| ERROR:001 | 测试用例文件未找到 | 使用模板创建 test_cases.json | 开发人员 |
| ERROR:002 | JSON格式无效 | 验证JSON语法 | 开发人员 |
| ERROR:003 | 测试期间未找到技能 | 检查技能名称拼写 | 开发人员 |
| ERROR:004 | 测试超时 | 增加超时时间或简化测试 | 开发人员 |

## 决策场景

| 触发条件 | 决策动作 | 预期结果 | 回退方案 |
|----------|----------|----------|----------|
| WHEN: 检测到低触发率 | THEN: 优化技能描述 | 更高的触发率 | 保持原描述 |
| WHEN: 检测到误触发 | THEN: 添加负向测试用例 | 更好的准确率 | 添加DO NOT TRIGGER子句 |
| WHEN: 边界用例不清晰 | THEN: 测试边界条件 | 清晰的触发规则 | 使用保守方法 |

## 观测模块

| 检查点 | 观测方法 | 预期状态 | 异常处理 |
|--------|----------|----------|----------|
| OBS: CLI安装 | 运行 `pip install -e scripts` | 成功无错误 | 检查Python路径 |
| OBS: 命令可用 | 运行 `skill-trigger-test --help` | 显示帮助 | 重新安装包 |
| OBS: 测试结果 | 审查生成的报告 | 有效的指标 | 检查测试用例格式 |

## 交付物

- 测试用例文件 (test_cases.json)
- 触发率报告 (trigger_rate.md)
- 优化后的描述 (optimized_descriptions.json)
- 验证日志

## 占位符号变量清单

| 变量 | 来源 |
|------|------|
| {{WORKFLOW_NAME}} | 工作流创建时指定 |
| {{WORKFLOW_TYPE}} | 工作流类型，如skill |
| {{CREATE_TIME}} | 工作流创建时间戳 |
| {{OWNER}} | 工作流负责人 |
| {{STEP_1_DESCRIPTION}} | 第一步骤的描述 |

### 工作流命名标准
- 使用小写字母、数字和连字符
- 最大长度64字符
- 优先使用动词短语描述动作

## AI能力增强

| 类型 | 名称 | 预期使用 |
|------|------|----------|
| skill | skill-creator | 创建或改进技能时使用 |
| skill | unicode-script-fixer | 修复脚本编码问题时使用 |
| mcp | filesystem | 读写文件时使用 |
| mcp | git | 版本控制时使用 |
