from typing import Any

from .config import Settings
from .health import health
from .provider import InMemoryMemoryStore, MemoryProvider


def create_server(settings: Settings | None = None, provider: MemoryProvider | None = None) -> Any:
    """Build the SDK server; importing this function does not require SDK startup."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("MCP SDK is required for the stdio server; install the package with pip") from exc

    settings = settings or Settings.from_env()
    settings.validate()
    store = provider or InMemoryMemoryStore()
    mcp = FastMCP(settings.server_name)

    @mcp.tool()
    def health_tool() -> dict[str, Any]:
        """Return service and configured backend health."""
        return health(settings)

    @mcp.tool()
    def memory_add(content: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        return store.add(content, metadata).as_dict()

    @mcp.tool()
    def memory_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
        return [item.as_dict() for item in store.search(query, limit)]

    @mcp.tool()
    def memory_get(memory_id: str) -> dict[str, Any] | None:
        item = store.get(memory_id)
        return item.as_dict() if item else None

    @mcp.tool()
    def memory_delete(memory_id: str) -> dict[str, Any]:
        return {"deleted": store.delete(memory_id), "id": memory_id}

    @mcp.tool()
    def memory_list(limit: int = 100) -> list[dict[str, Any]]:
        return [item.as_dict() for item in store.list(limit)]

    return mcp
