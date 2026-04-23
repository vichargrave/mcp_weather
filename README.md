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

**Via `uv run` (no install required):**
```bash
uv run weather.py
```

**Via the installed entry point (after `uv sync`):**
```bash
uv run mcp-weather
```

**Directly as an executable (uses the `uv run` shebang):**
```bash
chmod +x weather.py
./weather.py
```

The server communicates over `stdio`, which is the standard transport for MCP integrations with Claude Desktop.

## CLI clients

Two standalone MCP clients are included for testing and interacting with the server directly.

### `weather_cli.py` — simple client

Connects to the server, lists tools, then calls `get_alerts("CA")` and `get_forecast` for San Jose and prints the results.

```bash
uv run weather_cli.py
```

### `weather_cli_inter.py` — interactive Claude-powered client

Connects to any `.py` or `.js` MCP server and starts a chat loop backed by the Claude API. Natural language queries are sent to Claude, which decides which MCP tools to call and returns a response.

```bash
export ANTHROPIC_API_KEY=your-key-here
uv run weather_cli_inter.py weather.py
```

Requires an `ANTHROPIC_API_KEY` environment variable (or a `.env` file in the project root).

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
