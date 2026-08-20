# SOP-04 Description Optimization

## Goal and scope

用真实 trigger 集优化 frontmatter description，并按需打包技能。描述是主要触发机制；优化不应过拟合单个 query，也不自动宣称 trigger 率已验证。

## Trigger eval set

生成约 20 条真实 query：8-10 条 should-trigger、8-10 条 near-miss should-not-trigger；可混合正式、口语、缩写、大小写、错字、竞争技能和未点名文件类型的场景。避免抽象一词任务和明显无关负例。先读取 `assets/eval_review.html`，替换 `__EVAL_DATA_PLACEHOLDER__`、`__SKILL_NAME_PLACEHOLDER__`、`__SKILL_DESCRIPTION_PLACEHOLDER__`，写到用户授权临时路径供人工编辑；导出 JSON 后再保存到 workspace。

## Optimization loop

准备好 eval set、skill path、当前模型和配置后运行：

```text
python -m scripts.run_loop --eval-set <trigger-eval.json> --skill-path <path-to-skill> --model <model-id> --max-iterations 5 --verbose
```

`run_loop.py` 将 60% train / 40% held-out test 分层拆分，每个 query 默认运行 3 次，调用 `run_eval.py`，失败时调用 `improve_description.py`，最多 5 轮，并按 test score 选择 best description。可用 `--results-dir` 保存结果和日志，`--report` 控制报告；需要报告时使用 `scripts/generate_report.py` 的输出。

`improve_description.py` 通过 `claude -p` 读取当前 description、失败 trigger、历史和技能内容，要求短于 1024 字符；超限会再次请求缩短。它可记录 `log_dir` 的 iteration JSON。运行前确认 CLI、模型、认证和外部副作用配置，否则标记 blocked，不臆造结果。

## Human review and feedback

循环完成后，若存在 runs、grading 和 benchmark，使用 `eval-viewer/generate_review.py`；第 2 轮起传 `--previous-workspace`。用户提交的 `feedback.json` 才是人工反馈证据；读取后只针对具体意见泛化修复。结束 viewer 服务并记录退出状态。无浏览器/显示时使用 `--static`，不声称已打开浏览器。

## Apply and package

将 `best_description` 与原 description 对比后，经主 LLM 验证长度、trigger 边界和内容保真，再更新目标 `SKILL.md` frontmatter。保持原 skill name。打包前运行：

```text
python -m scripts.package_skill <path-to-skill-folder> [output-directory]
```

该脚本调用 `scripts.quick_validate.validate_skill`，排除 `__pycache__`、`node_modules`、`*.pyc` 和 root `evals`，生成 `<skill-name>.skill`。若验证失败不得打包；许可信息来自目标目录的 `LICENSE.txt`。

## Iteration and stop

改进已有技能时每轮重跑所有 cases 并保留 baseline/旧版本；停止条件为用户满意、反馈为空、无有意义进展、达到 max iterations 或出现未解决 critical RED。每轮必须更新 todo/status。

## Return contract

```text
Finding: <description 变化及触发结果>
Evidence: <eval、run_loop、feedback、报告或包路径>
Confidence: <0..1；未运行就写 unknown/block>
Fidelity: <保留原触发意图程度>
RED: <过拟合、held-out 失败、配置缺失>
Excluded scope: <未执行的 opencode/browser/外部模型动作>
Next step: <应用、继续 round 或 sop-05>
```
