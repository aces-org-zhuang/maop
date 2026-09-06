from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graphiti_mcp.config import Settings
from graphiti_mcp.health import health


if __name__ == "__main__":
    settings = Settings.from_env()
    settings.validate()
    print(health(settings))
