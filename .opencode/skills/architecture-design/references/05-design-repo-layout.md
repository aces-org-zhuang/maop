# SOP 05 - 设计仓分层与归属

## Goal

决定架构资产应该放在哪一层、哪个仓，避免多个项目共用一个被 submodule 引用的设计仓导致 gitlink 指针抖动，同时保留跨项目架构视图能力。

## When Required

新建设计仓、决定某个架构内容归属、或用户提出「把所有项目的设计放到一个仓」时。

## 核心机制：为什么不能单一大设计仓

Git submodule 在主仓记录的是**子仓 HEAD commit**，与实际使用哪个子目录无关。因此：

- 单一大设计仓被 A/B/C 三个项目各自 `submodule add`；
- 设计仓任意一次提交都会改变 gitlink；
- 三个项目仓都需要开 PR 更新指针，即使这次改动与两个项目毫无关系。

这是**指针抖动**，代价是 N 个仓各提一个 PR，而非磁盘占用。

### sparse-checkout 不能解决问题

sparse-checkout 只影响工作区检出内容，**不影响 gitlink 指向的 commit**。它省的是磁盘与 clone 时间，不省 PR 负担。

更严重的是：LikeC4 CLI 需要完整工作区才能 `validate` 与 `build`。只检出一个项目的目录会导致跨项目视图直接失败——模型文件里的 `include acme.*` 找不到符号。

## 分层结构

```text
aces-architecture  全局层（聚合发布层）
  跨项目上下文图、服务全景、依赖矩阵、部署拓扑
  不被任何项目 submodule 引用
  CI 聚合各项目设计仓并发布总览站点
        ▲ 引用（方向相反，无循环依赖）
        │
design-<project>  项目层（每项目独立仓）
  本项目的 model / views / dynamic views / deployment / ADR
  被本项目主仓以 submodule 引用
  独立 CI 构建发布
```

### 项目层

```bash
git submodule add https://github.com/<org>/design-<project>.git vendor/design/aces-design
```

- 内容：本项目的模型、视图、时序图、部署视图、ADR、接口契约。
- 引用方：只有本项目主仓。
- 变更只影响自己的指针。
- 在主仓 `docs/02-development/submodules-index.md` 登记，`build_entry` 写 `none`（主仓不构建它）。

### 全局层

- 内容：跨项目上下文图、服务全景、依赖矩阵。
- **不做任何项目的 submodule**，方向与项目层相反：全局层依赖项目层。
- CI 定时或 watch 拉取各项目设计仓，合成总览站点并发布 gh-pages。
- 额外收益：能编译校验**跨项目一致性**。两个项目之间存在调用关系但无人建模时，全局层 `validate` 能发现。单一大仓做不到——那里项目边界只是约定。

## 决策口诀

| 条件 | 归属 |
| --- | --- |
| 只服务一个项目 | 项目层设计仓 + submodule |
| 描述项目之间的关系 | 全局聚合层，不作 submodule |
| 变更要能单独发版给别人看 | 全局层 |
| 变更必须与代码同一个 PR | 主仓 `docs/`，**不放设计仓** |

最后一条是设计仓的定位原则：**设计仓是跨 PR 生命周期的资产，不是代码的附属**。凡是需要与代码同 PR 的内容（模块划分、接口草案、实现级契约），放设计仓就是错的——它会造成设计滞后于代码，架构图随即腐烂。

## 目录建议

```text
design-<project>/
  likec4.config.ts
  src/
    specification.c4
    model/
    views/
      context.c4
      use-cases.c4
    deployment/
  adr/
  package.json
```

```text
aces-architecture/
  likec4.config.ts
  src/
    systems/<project>.c4     # 各项目系统定义
    views/cross-system.c4
    views/dependency-matrix.c4
  package.json
```

全局层聚合各项目模型时，跨文件引用必须用 **FQN**（见 `references/02-multifile-and-fqn.md`）。这是 AI 生成全局层文件时最常见的失败原因。

## 常见失败模式

- 把所有项目设计放进单一仓，再被多个项目 submodule 引用 → 指针抖动。
- 用 sparse-checkout 试图解决抖动 → 不解决，且破坏 LikeC4 构建。
- 设计必须与代码同 PR 的内容放进设计仓 → 设计滞后于代码。
- 全局层被项目仓 submodule 引用 → 形成循环依赖，违反 submodule 规则。
- 全局层只做展示不做 `validate` → 跨项目一致性无人守。
- 主仓 CI 构建设计仓 → 职责越界。

## 与 submodule-manager 的关系

执行本 SOP 涉及 submodule 写操作时，必须转入 `submodule-manager`，由其完成路径推导、`.gitmodules` 同步、授权确认和 `submodules-index.md` 登记。

本 SOP 只决定**归属层级**，不替代 submodule 机制治理。
