FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md .env.example ./
COPY src ./src
COPY scripts ./scripts

RUN pip install --no-cache-dir .

ENV GRAPHITI_MCP_TRANSPORT=stdio \
    GRAPHITI_MCP_STORAGE=memory \
    GRAPHITI_MCP_PROVIDER=memory

ENTRYPOINT ["graphiti-mcp"]
