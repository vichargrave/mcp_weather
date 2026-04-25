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

## Claude Desktop integration (macOS)

### 1. Find the config file

Claude Desktop stores its MCP server configuration at:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Open it in any editor, e.g.:

```bash
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If the file doesn't exist yet, create it.

### 2. Add the weather server

Paste the following into `claude_desktop_config.json`, replacing `/path/to/mcp_weather` with the absolute path to this repository (e.g. `/Users/yourname/src/mcp_weather`):

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

If the file already has other servers under `"mcpServers"`, add the `"weather"` block alongside them — do not create a second `"mcpServers"` key.

### 3. Restart Claude Desktop

Quit Claude Desktop fully (Cmd+Q or **Claude → Quit Claude**) and reopen it. New MCP servers are only loaded on startup.

### 4. Verify the connection

Click the **plug icon** (MCP) in the Claude Desktop chat bar. You should see `weather` listed with the tools `get_alerts` and `get_forecast`. If it's missing, check Console.app for errors from the `Claude` process and confirm `uv` is on your PATH (run `which uv` in Terminal to verify).
