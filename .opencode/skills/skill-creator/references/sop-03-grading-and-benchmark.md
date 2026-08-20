# SOP-03 Grading and Benchmark

## Goal and scope

评分运行结果、聚合 benchmark、分析隐藏模式，并在需要时进行盲比。所有结论以真实 transcript、outputs、JSON 和命令结果为证据。

## Grader delegation

读取 `agents/grader.md`，对每个 run 委派独立 grader。输入为 expectations、transcript path、outputs dir；输出写 `outputs_dir/../grading.json`。grader 必须实际检查文件，不仅相信 transcript；通过条件是证据真实、具体且反映任务完成；不确定按 fail。

`grading.json` 的 expectations 每项必须有精确字段 `text`、`passed`、`evidence`。同时填写 summary、可得 execution_metrics、timing、claims、user_notes_summary，并在有明显缺口时写 eval_feedback。代理返回统一七字段，缺失即 blocked。

## Aggregate

运行：

```text
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

脚本支持 eval 目录直接位于 benchmark root 或 `runs/` 下；发现 `with_skill`/`without_skill`、`old_skill` 等配置，输出 `benchmark.json` 与 `benchmark.md`。它计算 pass rate、time、tokens 的 mean/stddev/min/max 和前两配置 delta。必须使用 schema 中的 `configuration`、嵌套 `result` 和 viewer 需要的字段。

运行 benchmark 前后更新 todo/status。脚本返回非零、缺 grading、JSON 损坏或配置不足时标记 blocked/failed，不把空统计当成功。

## Analyzer delegation

需要基准模式分析时读取 `agents/analyzer.md` 的 benchmark 分支。分析：两种配置都通过/都失败的非区分 assertion；with-skill 改善或伤害；高方差 eval；跨 eval 难度；time/token/tool_calls/error outlier。只报告数据观察，不在 benchmark analyzer 阶段臆测因果或提出改进。

## Blind comparison

用户要严格 A/B 或“新版本是否更好”时读取 `agents/comparator.md`：给代理 output A/B、eval prompt 和 expectations，禁止透露来源。代理按内容（correctness/completeness/accuracy）和结构（organization/formatting/usability）1-5 评分，输出 overall、strengths、weaknesses、winner A/B/TIE 和 expectation_results。随后读取 `agents/analyzer.md` 的 post-hoc 分支，解除盲态并比较技能、transcript、工具和错误恢复，输出 `analysis.json`。

## Round and convergence

把每轮结果放入新的 `iteration-N`；保留旧轮用于比较。收敛依据用户成功标准、assertion evidence、benchmark、agent findings 和 human feedback，不依据单一平均分。无进展、结果冲突或 RED 未被新证据覆盖时进入 `blocked` 或 `exited`。

## Validation and return

检查每个 grading JSON schema、benchmark 文件存在且非空、配置顺序和统计来源；检查 analyzer 不越权改 skill；记录：

```text
Finding: <评分/基准/比较观察>
Evidence: <grading.json、benchmark.json、analysis.json 路径>
Confidence: <0..1>
Fidelity: <与原运行结果一致程度>
RED: <弱断言、方差、缺输出>
Excluded scope: <未运行的配置或未检查的外部系统>
Next step: <反馈、修复或 sop-05>
```
