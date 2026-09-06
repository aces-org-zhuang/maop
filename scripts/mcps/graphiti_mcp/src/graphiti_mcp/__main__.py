from __future__ import annotations

from .config import Settings
from .server import create_server


def main() -> None:
    settings = Settings.from_env()
    settings.validate()
    create_server(settings).run(transport="stdio")


if __name__ == "__main__":
    main()
