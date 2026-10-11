# SOP-01 RCA Trace Init

## Goal

初始化并持续维护 `fix-rca-trace.md`，作为唯一事实载体。

## Steps

1. 确认报告位置：默认写在当前工作目录的 `docs/debugs/fix-rca-trace.md`；若宿主项目已有约定的故障记录目录，优先用该目录。
2. 读取 `templates/fix-rca-trace.md`，按其小节顺序创建报告文件；已存在则跳过创建，直接进入更新。
3. 按 `templates/rca-steps-plan.json` 的阶段顺序推进，每个阶段只做两件事：写入该阶段对应小节、把仍是空的必填小节补齐。
   - `problem-definition` -> `Symptom` / `Environment` / `Reproduction`
   - `evidence` -> `Evidence` / `Timeline`
   - `reasoning-slice` -> `Direct Cause`（先记候选根因与排除项，不预先定论）
   - `root-cause` -> `Root Cause`
   - `fix` -> `Fix`
   - `non-regression` -> `Verification: Problem Still Reproduces?`
   - `handoff` -> `Residual Risk` / `Follow-up Actions`
4. 每阶段结束后读取一次报告，确认本阶段小节已落盘，且没有把结论写进尚未验证的小节。
5. 阶段推进的判断依据是报告内容本身，不依赖外部进度文件：读报告就知道当前停在哪一步。

## Output

可持续更新的 RCA 追踪报告；报告文件即当前进度状态。
