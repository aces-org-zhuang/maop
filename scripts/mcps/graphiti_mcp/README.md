# Graphiti MCP

`maop` 维护的独立 MCP 部署包，位于 `scripts/mcps/graphiti_mcp/`。它不属于 Aces Desktop，不读取宿主项目配置，也不复用 Aces Desktop runtime。

当前状态必须明确：本包当前仅实现进程内 `memory fallback`，不是实际的 Graphiti provider；本包没有接入真实 Graphiti SDK，也不应被描述为已实现 Graphiti SDK；本包不提供任何历史 Graphiti 数据、配置、协议或行为兼容性。

## Directory Responsibilities

- `src/graphiti_mcp/`: 包实现、配置边界、provider protocol、health 响应和 stdio MCP server。
- `tests/`: 配置拒绝规则、fallback 生命周期、health 和 MCP server 边界测试。
- `scripts/healthcheck.py`: 容器 healthcheck；只检查本地配置和 health 响应，不启动 MCP client。
- `scripts/smoke_mcp.py`: 不依赖 MCP SDK 的最小 memory fallback smoke test。
- `Dockerfile`、`docker-compose.yml`: 独立容器运行定义；容器入口仍是 stdio MCP server。
- `.env.example`: `GRAPHITI_MCP_*` 配置示例，不包含凭据。

## 状态

- 支持 `stdio` transport，通过 MCP Python SDK 暴露 `health`、`memory_add`、`memory_search`、`memory_get`、`memory_delete`、`memory_list`。
- 默认且当前唯一实现的是进程内 `InMemoryMemoryStore` memory fallback，只适合 smoke/test 和本地开发。
- `GRAPHITI_MCP_STORAGE=memory` 是当前唯一实现的存储后端；持久化 provider 是明确的扩展边界。
- 当前没有真实 Graphiti provider，也没有真实 Graphiti SDK 集成。
- 当前不承诺历史兼容：不兼容或读取历史 Graphiti 数据、配置、协议和行为不是本包的已实现能力。
- HTTP transport 当前未实现。`GRAPHITI_MCP_TRANSPORT=http` 会在启动时明确报错，而不是伪装支持。

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m graphiti_mcp
```

MCP client 应以 stdio 方式启动该命令。容器默认运行 healthcheck 脚本；stdio MCP server 本身不会提供 HTTP health endpoint。

容器方式：

```powershell
docker compose up --build
```

`GRAPHITI_MCP_TRANSPORT=http` 当前会在启动时失败。不要通过端口映射或 compose 配置把 stdio 入口描述成 HTTP 服务。

## Configuration

所有配置使用 `GRAPHITI_MCP_*` 命名空间，详见 `.env.example` 和 `src/graphiti_mcp/config.py`。provider/storage 只通过这些配置和包内接口连接，不读取 Aces Desktop 配置。

## Development

```powershell
python -m pytest
# 如果全局 pytest 插件与项目 pytest 版本不兼容：
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
python -m pytest
python -m py_compile (Get-ChildItem -Recurse -Filter *.py src tests scripts | ForEach-Object FullName)
python scripts\smoke_mcp.py
python scripts\healthcheck.py
```

`mcp` SDK 是运行 stdio 入口的正式依赖。单元测试不需要启动外部服务。完整测试默认使用项目 dev 依赖；若机器上的 pytest 自动加载了不兼容的全局插件，可设置 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 后重试。若环境没有安装 `mcp`，MCP server 边界测试会按其测试契约检查清晰的缺失依赖错误，不能把这种环境状态当成真实 MCP server 已启动。

## Sparse-Checkout Note

maop 的宿主 checkout 默认只包含 `/.opencode/` 和 `/README.md`。需要维护本包时，在 maop 仓库内临时把 `/scripts/mcps/graphiti_mcp/` 加入 sparse-checkout；完成后可恢复默认 patterns。sparse-checkout 是 checkout-local 状态，不要把 `.git/info/sparse-checkout` 当作包资产提交，也不要把包复制到 Aces Desktop。

## Extension boundary

实现真实 Graphiti provider 时，应实现 `MemoryProvider`，并在 `server.py` 的 provider factory 中显式注册。不要把 Graphiti SDK、数据库连接或凭据读取逻辑放入 `InMemoryMemoryStore`，也不要复用 Aces Desktop runtime。
