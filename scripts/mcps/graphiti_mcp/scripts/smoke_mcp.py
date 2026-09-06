from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graphiti_mcp.provider import InMemoryMemoryStore


if __name__ == "__main__":
    store = InMemoryMemoryStore()
    item = store.add("smoke memory")
    assert store.search("smoke")[0].id == item.id
    assert store.delete(item.id)
    print("graphiti_mcp smoke ok")
