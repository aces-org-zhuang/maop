from graphiti_mcp.provider import InMemoryMemoryStore


def test_memory_lifecycle():
    store = InMemoryMemoryStore()
    item = store.add("Graphiti memory boundary", {"source": "test"})
    assert store.get(item.id).metadata["source"] == "test"
    assert store.search("memory")[0].id == item.id
    assert store.list()[0].id == item.id
    assert store.delete(item.id) is True
    assert store.get(item.id) is None


def test_empty_content_rejected():
    store = InMemoryMemoryStore()
    try:
        store.add("  ")
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError("empty content must be rejected")
