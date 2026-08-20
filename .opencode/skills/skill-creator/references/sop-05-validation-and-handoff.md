# SOP-05 Validation and Handoff

## Goal and scope

在任何成功、阻塞或失败退出前验证文件、引用、语法、执行完整性和置信度，并交付可重启的证据包。它不能替代未实际运行的外部服务验证。

## Local validation gate

至少执行并记录：

1. `SKILL.md` 行数小于等于 300。
2. frontmatter 可解析且含 `name`、`description`；入口只包含约定四类内容。
3. 连续编号的 `references/sop-NN-*.md` 存在；资源索引中的每个 bundled path 存在。
4. Markdown 相对引用逐一解析；示例中的目标 skill/workspace 路径要明确标注运行时，不当作 bundled 引用。
5. Python 编译：`python -m compileall -q scripts eval-viewer`。
6. 适用时运行 `python scripts/quick_validate.py <skill-path>`、`python scripts/package_skill.py <skill-path>`；没有用户授权或依赖时只报告未执行。
7. 目标 skill 的执行模型必须显式包含主 LLM 派发代理执行 SOP 的说明。
8. 目标 skill 的执行模型必须显式包含执行前后更新 `todo/status` 的说明。
9. 目标 skill 的执行模型必须显式包含任务依赖树、round、loop，以及需要时的 dialectical/对抗合并策略。
10. `references/target-skill-execution-model.md` 必须存在，且目标 skill 生成流程必须引用它而不是把模板正文硬塞回入口。
11. 生成的目标 skill 必须默认采用 SOP-routed 目录结构，且 `references/` 至少包含 intake/routing、execution、validation、handoff 这四类覆盖；不接受单文件草稿作为最终交付。

本技能的仓库改动验证可使用 PowerShell/可用 shell；只检查和修改用户授权目录。不要为了让检查通过而删除用户已有改动。

## Confidence gate

用户要求自测、trigger 率或 90% 时完整读取 `references/self-test-confidence.md`。至少 10 prompt；复杂技能 15-20、60/40 train/held-out。计算：

```text
confidence = 0.30*trigger + 0.30*completeness + 0.25*quality + 0.15*safety
```

只有 confidence >= 0.90、held-out >= 0.90、无 critical RED 且有验证路径才可写 `Gate: PASS`。没有真实 `opencode run`、benchmark、人工 review 或 timing 时，写 `not run`/`unknown`，不能填充数字。

## Second reasoning-map review

完成修改后复查：

```text
[Trigger] should / should-not
   -> [Execution] SOP route / delegation / validation
      -> [Quality] output / format / success criteria
         -> [Risk] write boundary / secrets / over-trigger
            -> [Evidence] logs / benchmark / human review
```

每个原始 RED 必须已修复、有测试、有证据或被明确 bounded；检查 downstream consumer、eval、template、feedback route、restart/package guidance 是否同步。

## Unified exit report

```text
Skill: <name>
Status: SUCCEEDED | BLOCKED | FAILED | EXITED
Finding: <完成的关键事实>
Evidence: <命令、文件、日志和产物路径>
Confidence: <实际计算值或 unknown>
Fidelity: <迁移/重构保留程度>
RED: <none 或逐项说明>
Excluded scope: <未执行的外部验证、未授权目录或未提供输入>
Next step: <用户可重启的命令或下一 SOP>
```

退出前逐项将 todo/status 更新为 `succeeded`、`blocked` 或 `failed`，最后设置 workflow 为 `exited`。Success 不得隐藏 blocked 子项；Blocked 不得伪造产物；Failed 必须保留可诊断证据。
