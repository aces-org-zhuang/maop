from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000
    storage: str = "memory"
    provider: str = "memory"
    log_level: str = "INFO"
    server_name: str = "graphiti-mcp"

    @classmethod
    def from_env(cls) -> "Settings":
        prefix = "GRAPHITI_MCP_"
        return cls(
            transport=os.getenv(prefix + "TRANSPORT", cls.transport).lower(),
            host=os.getenv(prefix + "HOST", cls.host),
            port=int(os.getenv(prefix + "PORT", str(cls.port))),
            storage=os.getenv(prefix + "STORAGE", cls.storage).lower(),
            provider=os.getenv(prefix + "PROVIDER", cls.provider).lower(),
            log_level=os.getenv(prefix + "LOG_LEVEL", cls.log_level).upper(),
            server_name=os.getenv(prefix + "SERVER_NAME", cls.server_name),
        )

    def validate(self) -> None:
        if self.transport not in {"stdio", "http"}:
            raise ValueError("GRAPHITI_MCP_TRANSPORT must be 'stdio' or 'http'")
        if self.transport == "http":
            raise NotImplementedError("HTTP transport is reserved but not implemented")
        if self.storage != "memory":
            raise ValueError("only GRAPHITI_MCP_STORAGE=memory is implemented")
        if self.provider != "memory":
            raise ValueError("only GRAPHITI_MCP_PROVIDER=memory is implemented")
        if not 1 <= self.port <= 65535:
            raise ValueError("GRAPHITI_MCP_PORT must be between 1 and 65535")
