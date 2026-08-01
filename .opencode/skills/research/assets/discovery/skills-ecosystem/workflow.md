# Skills Ecosystem Discovery

用于从开放 agent skills 生态中发现并安装合适的技能。

## When To Use

- 用户询问“如何做 X”，且 X 可能已有通用 skill。
- 用户说“找 skill”“有没有某个 skill”“能不能扩展某个能力”。
- 用户想搜索工具、模板、工作流或 agent 能力。

## Discovery Steps

1. 明确领域、具体任务和是否常见。
2. 先查看 https://skills.sh/ leaderboard 或已知高信誉来源。
3. 必要时运行 `npx skills find <query>`。
4. 推荐前检查安装量、来源声誉、GitHub stars、维护状态和权限风险。
5. 展示候选 skill、用途、安装命令和来源链接。
6. 只有用户明确同意后才安装。

## Commands

```bash
npx skills find <query>
npx skills add <owner/repo@skill>
npx skills check
npx skills update
```

使用 `-g` 全局安装或 `-y` 跳过确认前，必须确认用户意图和风险。

## If No Skill Exists

- 说明没有找到高可信候选。
- 可直接用当前 agent 能力帮助完成任务。
- 如果该能力会重复使用，可建议转入 `skill-creator` 创建新 skill。
