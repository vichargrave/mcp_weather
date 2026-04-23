# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Run the MCP server:
```
uv run weather.py
```

Install/sync dependencies:
```
uv sync
```

Run the simple CLI client (fetches CA alerts + San Jose forecast):
```
uv run weather_cli.py
```

Run the interactive Claude-powered client:
```
uv run weather_cli_inter.py weather.py
```

## Architecture

This is a single-file MCP server (`weather.py`) built with `FastMCP`. It exposes two tools to MCP clients (e.g. Claude Desktop):

- `get_alerts(state)` — fetches active weather alerts for a US state from the NWS API
- `get_forecast(latitude, longitude)` — fetches a multi-period forecast by first resolving coordinates to a grid endpoint, then fetching that grid's forecast

All NWS requests go through `make_nws_request()`, which uses `httpx` with a 30-second timeout and returns `None` on any error. The server runs over `stdio` transport, which is the standard transport for MCP integrations with Claude Desktop.

The entry point registered in `pyproject.toml` is `mcp-weather = "weather:main"`. The `[tool.hatch.build.targets.wheel] include = ["weather.py"]` config is required because hatchling does not auto-discover top-level single-file modules.

### CLI clients

**`weather_cli.py`** — minimal MCP client that connects to the server over stdio, lists available tools, then calls `get_alerts("CA")` and `get_forecast(37.3387, -121.8853)` (San Jose) and prints results.

**`weather_cli_inter.py`** — interactive MCP client that connects to any `.py` or `.js` MCP server (pass path as argv[1]), then runs a chat loop backed by the Claude API. Each user query is sent to Claude with the server's tools available; Claude decides which tools to call. Requires `ANTHROPIC_API_KEY` in the environment.

## Claude Code automation hooks

Configured in `.claude/settings.local.json`:

- **PostToolUse / Write** — auto-stages each file written by Claude (`git add <file>`)
- **PostToolUse / Bash** — runs `git push` after any Bash command containing `git commit`
- **Stop** — on Claude exit, commits all uncommitted changes with a timestamped message and pushes to GitHub
