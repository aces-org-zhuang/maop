import pytest

from graphiti_mcp.config import Settings


def test_defaults_are_namespaced(monkeypatch):
    monkeypatch.delenv("GRAPHITI_MCP_TRANSPORT", raising=False)
    assert Settings.from_env().transport == "stdio"


def test_http_is_explicitly_reserved():
    with pytest.raises(NotImplementedError, match="not implemented"):
        Settings(transport="http").validate()


def test_unknown_storage_is_rejected():
    with pytest.raises(ValueError, match="STORAGE"):
        Settings(storage="sqlite").validate()
