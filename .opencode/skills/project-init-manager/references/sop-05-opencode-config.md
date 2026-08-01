# SOP 05: OpenCode Config

## 目标

初始化项目本地 `.opencode/`，承载项目专属 skills、agents、commands、插件说明和可选 `opencode.json`。配置必须渐进生成，避免写错 schema 导致 OpenCode 启动失败。

## 标准目录

```text
.opencode/
  README.md
  skills/
  agents/
  commands/
  plugins/
```

`plugins/` 可按需创建；如果项目不使用插件，可只在 README 中说明。

## 项目仓与 maop 的 .opencode 边界

- 项目仓 `.opencode/` 保存项目级 skills、agents、commands、配置说明和项目本地路由规则。
- `vendor/ai/maop/.opencode/` 属于 maop AI 引擎 submodule，由 maop 仓库独立演进。
- 不把 maop 的 `.opencode` 复制到项目仓，也不把项目仓 `.opencode` 写入 maop submodule。
- 如果项目需要调用 maop 能力，只在主仓 docs 或 `.opencode/README.md` 中记录路径、版本、消费关系和验证方式。

## opencode.json 策略

只有满足以下任一条件才生成 `.opencode/opencode.json`：

- 用户提供项目配置模板。
- 当前环境可读取并确认 `https://opencode.ai/config.json` schema。
- 项目已有有效 `opencode.json`，本次只是增量合并。
- 用户明确要求生成，并接受需要后续重启 OpenCode 验证。

如果不满足条件，不生成 `opencode.json`；改为创建 `.opencode/README.md`，记录后续生成条件和推荐 schema 地址。

## 执行步骤

1. 创建 `.opencode/skills/`、`.opencode/agents/`、`.opencode/commands/`。
2. 创建 `.opencode/README.md`，说明本地组件目录用途、配置策略和重启要求。
3. 如果需要迁入项目 skill，将 skill 放到 `.opencode/skills/<skill-name>/SKILL.md`。
4. 如果需要 project agent，使用 `.opencode/agents/<name>.md` 文件形式，不把复杂 prompt 塞进 `opencode.json`。
5. 如需 `opencode.json`，必须带 `$schema`，并保留用户已有字段。
6. 配置变更后提醒用户重启 OpenCode。

## 模板

- `templates/opencode-README.md.template`

## 常见 RED 点

- 猜测 `opencode.json` 字段导致配置无效。
- 把复杂 agent prompt inline 到 config。
- 修改配置后没有提醒重启 OpenCode。
- 把项目本地 skill 放错目录名或缺少 `SKILL.md` frontmatter。
- 混合项目仓 `.opencode` 与 maop `.opencode`，导致两个仓库的 agent 能力无法独立升级。
