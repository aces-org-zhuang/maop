# SOP 06: Research Workspace

## 目标

研究区是新项目初始化的必建部分，并锁定为 `vendor/research/aces-research` -> `https://github.com/aces-org-zhuang/aces-research.git` submodule。它保存研究过程、论文、开源仓库对比、证据包和课题内参考仓，且不进入主仓默认项目知识库。

## 标准结构

```text
vendor/research/aces-research/
  index.md
  topics/
    <research_slug>/
      README.md
      sources/
      selection/
      repos/
      insights/
      matrix/
      evidence/
      paper/
```

研究工作区必须按锁定 URL 规划为 Git submodule：

```text
path: vendor/research/aces-research
url:  https://github.com/aces-org-zhuang/aces-research.git
```

如果当前环境不能执行 submodule 写操作，先创建计划和索引规则；写操作前按 `sop-07-submodule-governance.md` 请求确认。

## 执行步骤

1. 检查或规划 `vendor/research/aces-research` submodule，作为研究续点入口。
2. 创建 `topics/` 目录。
3. 如果用户已有第一个课题，创建 `topics/<research_slug>/README.md` 和标准子目录。
4. 在主仓 `docs/README.md` 和根 `AGENTS.md` 中只放研究区入口和边界规则，不默认读取课题材料。
5. 在研究区 `index.md` 记录课题清单、状态、最近续点和重要产物路径。
6. 更新 `.gitmodules` 和 submodule 索引；如果尚未执行写操作，输出明确的 `git submodule add https://github.com/aces-org-zhuang/aces-research.git vendor/research/aces-research` 计划。

## 研究区规则

- 研究过程、候选材料、论文草稿和证据包不得写入主仓 `docs/`。
- 开源参考仓必须放到具体课题 `topics/<research_slug>/repos/<repo_name>`，优先 submodule。
- 不得把参考仓普通 clone 到主仓目录。
- 不得把参考仓放在研究工作区根目录。
- 只有沉淀为长期项目事实、开发规则、架构判断、失效模式或实现证据时，才从研究区反哺到 `docs/`。

## 模板

- `templates/research-index.md.template`

## 常见 RED 点

- 把研究区设计成可选。
- 使用非锁定 URL 或非标准路径创建研究区。
- 主仓默认读取全部研究材料，造成上下文膨胀。
- 跨课题共享未隔离参考仓。
- 研究过程没有 `index.md` 续点，后续无法恢复上下文。
