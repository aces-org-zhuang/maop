# Failure Mode: maop 源仓被当作宿主项目自嵌套

## Trigger

运行 `project-init-manager` 初始化或审计目标仓库时，目标仓库本身就是 `maop` 源仓，但初始化规则仍套用普通宿主项目规则，要求添加 `vendor/ai/maop`。

## Symptoms

- 输出要求当前仓库添加 `vendor/ai/maop -> https://github.com/aces-org-zhuang/maop.git`。
- `.opencode/opencode.json` 被错误要求引用 `../vendor/ai/maop/.opencode/skills`。
- `.opencode/skills/` 被误判为项目本地覆盖目录，而不是 maop 的核心能力源码目录。
- 初始化结果把 LLM 能力开发项目误描述为传统技术栈项目。

## Root Cause

`project-init-manager` 只有“宿主项目消费 maop”的默认路径，没有 intake 阶段的 `maop_source_mode` 判定。目标仓库远端、目录名和 `.opencode/README.md` 已能证明当前仓库就是 maop，但 SOP 没有把这些信号转成排除规则。

## Fix

- 在 `sop-00-intake.md` 增加 `maop_source_mode`，由 Git remote、项目名和 `.opencode/skills/` 等信号自动判定。
- 在 `sop-05-opencode-config.md` 增加 maop 源仓模式：本仓 `.opencode/skills/` 是一等源码，`.opencode/opencode.json` 可指向 `./skills`。
- 在 `sop-07-submodule-governance.md` 明确 maop 源仓模式不得执行 `git submodule add https://github.com/aces-org-zhuang/maop.git vendor/ai/maop`。
- 在 `sop-08-validation.md` 增加自嵌套排除检查。

## Prevention

- 初始化前必须先用 `reasoning-map` 覆盖 `.opencode`、submodule 和目录职责域。
- 对仓库 URL 为 `https://github.com/aces-org-zhuang/maop.git` 或目录名为 `maop` 且存在 `.opencode/skills/` 的目标，默认进入 maop 源仓模式。
- 只有宿主项目才创建 `vendor/ai/maop` 并桥接 `../vendor/ai/maop/.opencode/skills`。
