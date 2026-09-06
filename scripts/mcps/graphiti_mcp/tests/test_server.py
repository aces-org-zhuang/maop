import pytest

from graphiti_mcp.config import Settings
from graphiti_mcp.server import create_server


def test_server_requires_sdk_or_builds_boundary():
    try:
        server = create_server(Settings())
    except RuntimeError as exc:
        assert "MCP SDK" in str(exc)
    else:
        assert server is not None


def test_http_cannot_be_started():
    with pytest.raises(NotImplementedError):
        create_server(Settings(transport="http"))
