# SOP-02 Evals and Runs

## Goal and scope

建立测试 prompt、并行运行 with-skill 与 baseline/old-skill，并保存可供评分和 viewer 使用的产物。不要把“命令可执行”误报成外部模型已验证。

## Test case setup

保存目标 skill 的 `evals/evals.json`；schema 见 `references/schemas.md`。每项包含 `id`、`prompt`、`expected_output`、可选 `files`、`expectations`。每个运行目录写 `eval_metadata.json`：`eval_id`、描述性 `eval_name`、prompt、assertions。

工作区布局：

```text
<skill-name>-workspace/iteration-N/eval-name/
  eval_metadata.json
  with_skill/outputs/
  old_skill/outputs/       # 改进已有技能时
  without_skill/outputs/   # 创建新技能时
```

不要预先创建全部目录；按运行进度创建。每个执行代理返回 `Finding/Evidence/Confidence/Fidelity/RED/Excluded scope/Next step`，并在启动/完成时更新 todo/status。

## Delegate all runs together

对每个 eval 同一批次并行委派 with-skill 与 baseline；改进已有 skill 时先 snapshot，再将旧版本作为 `old_skill`。提示至少包括：skill path、task、input files、outputs path、用户关心的输出。保持 prompt、输入和输出要求一致，只改变 skill configuration。

代理完成通知含 `total_tokens`、`duration_ms` 时立即写同一 run 的 `timing.json`：

```json
{"total_tokens": 84852, "duration_ms": 23332, "total_duration_seconds": 23.3}
```

若没有真实通知，不补猜 timing。运行异常写 `transcript.md` 或日志并标记 failed/blocker。

## Assertions while running

不要等待空闲：根据用户成功标准起草客观 assertions；主观视觉/写作品质留给人工 review。assertions 应检查真实任务结果，不应只检查文件名或表面字符串。运行中更新 metadata 和目标 eval JSON，并在 status 中记录批次。

## Supported execution paths

- 有 child agents：同一 turn 并行 with-skill/baseline；使用 bounded prompt。
- 无 child agents：串行运行每个 prompt，跳过无意义 baseline，保留定性检查。
- 有独立 eval/file 检查：并行；有共享状态或顺序依赖：串行。
- 评测未达门槛且有可操作新证据：进入下一 round；无新证据或达到上限：退出并报告 RED。

## Viewer handoff

完成运行后将 `outputs/`、metadata、transcript、metrics、timing交给 `eval-viewer/generate_review.py`。它读取真实工作区，加载同目录 `viewer.html`，服务或生成 static HTML，并写 `feedback.json`。只在用户确实需要人工评审时启动 viewer；无 display 用 `--static`。不要手写替代 viewer。

## Validation

检查每个 run 有正确 configuration、输出目录、metadata；检查计时字段来自真实通知；检查 assertions 可证据化；检查 viewer 所需字段为 `text`、`passed`、`evidence`。本 SOP 不执行外部 `opencode run`，除非当前环境、配置和用户授权都明确提供。
