# mcp_weather

An MCP server that provides weather alerts and forecasts using the [National Weather Service API](https://www.weather.gov/documentation/services-web-api).

Based on the article [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server).

## Tools

- **`get_alerts(state)`** — returns active weather alerts for a US state (two-letter code, e.g. `CA`, `NY`)
- **`get_forecast(latitude, longitude)`** — returns a multi-period forecast for a given location

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Running the server

```bash
uv run weather.py
```

The server communicates over `stdio`, which is the standard transport for MCP integrations with Claude Desktop.

## Claude Desktop integration

Add the following to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp_weather", "weather.py"]
    }
  }
}
```

Replace `/path/to/mcp_weather` with the absolute path to this repository.
