# Research Skill Layout

`research` 是基于 `research_root` 的发现、研究、创新、证据和报告统一流水线。

## Directory Semantics

- `SKILL.md`: 唯一主入口和高层路由规则。
- `evals/`: 技能触发和路由验证样例。
- `router/`: path 和深度研究子模块索引。
- `paths/`: path-based pipeline SOP，只描述执行路径和门禁。
- `modules/`: 深度研究子技能，用于仓库研究、论文建模和证据验证等较重阶段。
- `assets/`: 从旧发现/创新技能迁移来的参考资料和工作流资产。
- `templates/`: 输出模板。
- `checklists/`: 质量检查清单。
- `tools/`: 辅助脚本和 CLI 原型。

## Rules

- skill 内部资产目录不要模拟 `research_root` 输出目录。
- `research_root` 输出目录只在运行时创建到 `vendor/research/aces-research/topics/<research_slug>`。
- 新增 path SOP 放入 `paths/`。
- 新增深度子模块放入 `modules/`。
- 新增参考资料放入 `assets/`。
