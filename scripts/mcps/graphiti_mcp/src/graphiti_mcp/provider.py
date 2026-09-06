from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol
from uuid import uuid4


@dataclass
class Memory:
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class MemoryProvider(Protocol):
    def add(self, content: str, metadata: dict[str, Any] | None = None) -> Memory: ...
    def search(self, query: str, limit: int = 10) -> list[Memory]: ...
    def get(self, memory_id: str) -> Memory | None: ...
    def delete(self, memory_id: str) -> bool: ...
    def list(self, limit: int = 100) -> list[Memory]: ...


class InMemoryMemoryStore:
    """Deterministic fallback for local smoke tests; it is not persistence."""

    def __init__(self) -> None:
        self._items: dict[str, Memory] = {}

    def add(self, content: str, metadata: dict[str, Any] | None = None) -> Memory:
        if not content.strip():
            raise ValueError("content must not be empty")
        item = Memory(content=content, metadata=metadata or {})
        self._items[item.id] = item
        return item

    def search(self, query: str, limit: int = 10) -> list[Memory]:
        terms = {term.lower() for term in query.split() if term}
        matches = [item for item in self._items.values() if terms.intersection(item.content.lower().split())]
        return matches[:limit]

    def get(self, memory_id: str) -> Memory | None:
        return self._items.get(memory_id)

    def delete(self, memory_id: str) -> bool:
        return self._items.pop(memory_id, None) is not None

    def list(self, limit: int = 100) -> list[Memory]:
        return list(self._items.values())[:limit]
