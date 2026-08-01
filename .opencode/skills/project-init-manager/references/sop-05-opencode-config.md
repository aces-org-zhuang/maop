# SOP 05: OpenCode Config

## 目标

初始化项目本地 `.opencode/` 桥接配置，使项目开发时可以稳定使用 maop AI 引擎提供的 OpenCode 能力面。配置必须最小、可验证，避免写错 schema 导致 OpenCode 启动失败。

## 标准目录

```text
.opencode/
  opencode.json
  README.md              可选，仅用于项目本地说明
  skills/                可选，仅用于项目本地覆盖或项目专属 skill
  agents/                可选，仅用于项目本地覆盖或项目专属 agent
  commands/              可选，仅用于项目本地覆盖或项目专属 command
  plugins/               可选
```

`plugins/` 可按需创建；如果项目不使用插件，可只在 README 中说明。

## maop sparse-checkout 桥接规则

- 普通宿主项目默认必须创建 `vendor/ai/maop` submodule，来源锁定为 `https://github.com/aces-org-zhuang/maop.git`。
- maop submodule 使用 sparse-checkout，只检出 `.opencode` 和 `README.md`，让 AI 引擎能力面由 maop 维护。
- 项目仓 `.opencode/opencode.json` 是桥接配置，必须把 `../vendor/ai/maop/.opencode/skills` 加入 `skills.paths`。
- 项目仓 `.opencode/opencode.json` 必须把 `../vendor/ai/maop/.opencode` 登记为 `maop-opencode` reference。
- 项目本地 `.opencode/skills`、`.opencode/agents`、`.opencode/commands` 只在确有项目专属覆盖时创建；不要复制 maop 的 `.opencode` 内容。
- 后续新增或修改 engine-side OpenCode 组件应优先进入 maop 子仓。

## maop 源仓模式

当 intake 判定目标仓库本身就是 `maop` 源仓时，不执行普通项目桥接规则：

- 不创建 `vendor/ai/maop` submodule。
- `.opencode/skills/` 是本仓一等源码目录，不是项目本地覆盖目录。
- `.opencode/opencode.json` 可以把 `skills.paths` 指向 `./skills`，并把 `references.maop-opencode.path` 指向当前 `.opencode` 目录。
- 文档必须说明：宿主项目才通过 `../vendor/ai/maop/.opencode/skills` 消费 maop，本仓不自嵌套。

## opencode.json 策略

新项目初始化默认生成最小 `.opencode/opencode.json`，用于桥接 maop：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": [
      "../vendor/ai/maop/.opencode/skills"
    ]
  },
  "references": {
    "maop-opencode": {
      "path": "../vendor/ai/maop/.opencode",
      "description": "maop-owned OpenCode skills, agents, commands, and engine-side configuration reference."
    }
  }
}
```

既有项目如已有 `.opencode/opencode.json`，只增量合并 `skills.paths` 和 `references.maop-opencode`，保留用户既有字段。maop 源仓模式下按本仓路径合并，不写入 `../vendor/ai/maop/.opencode/skills`。

## 执行步骤

1. 非 maop 源仓模式下，确认 `vendor/ai/maop/.opencode/skills` 存在；不存在时先执行 `sop-07-submodule-governance.md` 引入或修复 maop submodule。
2. 创建或合并 `.opencode/opencode.json`，必须带 `$schema`。
3. 非 maop 源仓模式下，将 `../vendor/ai/maop/.opencode/skills` 加入 `skills.paths`，避免与项目本地 skill 重复扫描。
4. 非 maop 源仓模式下，将 `../vendor/ai/maop/.opencode` 登记为 `references.maop-opencode`。
5. maop 源仓模式下，将 `./skills` 加入 `skills.paths`，并将当前 `.opencode` 登记为 `references.maop-opencode`。
6. 项目确有本地覆盖时，再创建 `.opencode/skills/`、`.opencode/agents/`、`.opencode/commands/`；maop 源仓模式下这些目录属于 maop 能力源码，可按能力开发需要存在。
7. 配置变更后提醒用户重启 OpenCode。

## 模板

- `templates/opencode-README.md.template`

## 常见 RED 点

- 猜测 `opencode.json` 字段导致配置无效。
- 把复杂 agent prompt inline 到 config。
- 修改配置后没有提醒重启 OpenCode。
- 没有启用 maop sparse-checkout，导致主仓拉取整个 AI 引擎仓库。
- 把 maop `.opencode` 复制回项目仓 `.opencode`，形成双源维护。
- 漏掉 `skills.paths` 或 `maop-opencode` reference，导致项目开发时无法使用 AI 引擎能力。
- maop 源仓模式下仍写入宿主项目桥接路径，导致本仓误指向不存在的 `vendor/ai/maop`。
