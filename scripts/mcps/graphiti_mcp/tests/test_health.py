from graphiti_mcp.health import health


def test_health_reports_runtime_boundary():
    result = health()
    assert result["status"] == "ok"
    assert result["transport"] == "stdio"
    assert result["storage"] == "memory"
