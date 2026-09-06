from __future__ import annotations

from typing import Any

from .config import Settings


def health(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or Settings.from_env()
    return {
        "status": "ok",
        "service": settings.server_name,
        "transport": settings.transport,
        "storage": settings.storage,
        "provider": settings.provider,
    }
