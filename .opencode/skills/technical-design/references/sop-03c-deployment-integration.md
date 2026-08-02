# SOP 03c: Deployment Integration Design

用于第三方能力、软件、工具链、容器镜像、CLI、二进制、SDK、服务或系统包的部署引入设计。它是 `technical-design` 的子阶段，不是独立入口；真实安装、构建和验证转入 `implementation-delivery`。

## Goal

把依赖接入统一为 tech 流水线设计：先决定引入形态、目录归属、配置来源、构建/运行边界、验证信号和回滚路径，再交付实施。不要从源码下载、脚本安装或自建镜像开始反推设计。

## Deployment-First Adoption Order

优先级从高到低：

```text
managed service / hosted API
  -> package manager dependency
  -> SDK / framework dependency
  -> CLI / release binary
  -> container image by tag/digest
  -> system package
  -> pinned submodule
  -> build from source
  -> fork / patch
  -> self-build / self-reimplementation
```

选择低优先级引入方式时，必须说明为什么更高优先级方式不满足需求，并把维护成本、配置成本、license/security、构建验证和回滚风险标为可追踪证据。

## Directory Planning

目录规划必须统一到项目 tech 流水线，而不是复制固定 `.aces/deploy` 或历史脚本目录：

| Asset | Preferred location rule |
| --- | --- |
| Build/install scripts | 项目已有 scripts、tools、infra、ops、build 或 docs 指定目录；没有规范时先提出候选并经用户确认。 |
| Dependency config | 项目既有 package manifest、lockfile、env/config 目录或部署配置目录；不要新增孤立 config 目录。 |
| Source build cache | `{temp_root}` 或项目允许的临时目录，不进入长期源码树。 |
| Generated artifacts | 项目既有 build/dist/output/artifacts 目录；没有规范时在 integration-plan 中声明并确认。 |
| Installed binaries/tools | 系统包、包管理器缓存、project-local tools/bin、vendor/runtime 或用户确认的位置。 |
| Container image definition | 仅当必须自建镜像时放入项目既有 docker/containers/infra 目录；优先引用官方镜像 tag/digest。 |
| Submodule | 仅当设计收敛到 pinned submodule 时转入 `submodule-manager` 规划路径。 |

## Image Adoption Rule

- 优先使用官方或可信镜像的 tag/digest，记录镜像名、来源、license/security、runtime contract、env/volume/network 边界、healthcheck 和回滚 tag。
- 只有官方镜像缺失、工具链必须固化、构建环境需要可复现或安全策略要求时，才设计自建镜像。
- 自建镜像设计必须说明 Dockerfile 所在目录、base image、版本 tag 策略、cache 策略、tool verification、build log、rollback 和最小验证命令。
- 不把镜像构建脚本作为默认入口；真实构建转入 `implementation-delivery`，并先通过 Configuration Readiness Gate。

## Software Integration Rule

- 先查官方包、SDK、release binary、CLI、container image、系统包或服务 API；都不满足时才设计 source-build。
- 如果需要 build/install 脚本，只设计统一入口和接口契约，不在 technical-design 中执行脚本。
- 统一入口应说明 `install/build/verify` 命令、输入配置、输出产物、日志位置和失败处理。
- Skills 不应内联安装逻辑；设计阶段输出 `integration-plan.md`，执行阶段由 `implementation-delivery` 按已确认命令落地。

## Required Outputs

- `integration-plan.md`：引入形态、目录归属、配置获取方式、版本锁定、license/security、验证命令、回滚/替换路径。
- `software-build-map.md`：first-party 组件、third-party 能力、引入形态、构建/运行/验证链路。
- `selection-matrix.md`：Adoption form、why not higher-priority mode、source-build/fork/self-build RED 风险。

## Review Checks

- 依赖是否优先通过部署引入，而不是源码引入。
- 目录是否遵循项目 tech 流水线，而不是硬编码 `.aces/deploy` 或复制历史模板。
- source-build/fork/patch/self-build 是否有不可替代证据。
- 是否已通过 Configuration Readiness Gate。
- 是否有版本锁、验证信号和回滚路径。
