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

## Architecture

This is a single-file MCP server (`weather.py`) built with `FastMCP`. It exposes two tools to MCP clients (e.g. Claude Desktop):

- `get_alerts(state)` — fetches active weather alerts for a US state from the NWS API
- `get_forecast(latitude, longitude)` — fetches a multi-period forecast by first resolving coordinates to a grid endpoint, then fetching that grid's forecast

All NWS requests go through `make_nws_request()`, which uses `httpx` with a 30-second timeout and returns `None` on any error. The server runs over `stdio` transport, which is the standard transport for MCP integrations with Claude Desktop.

The entry point registered in `pyproject.toml` is `mcp-weather = "weather:main"`. The `[tool.hatch.build.targets.wheel] include = ["weather.py"]` config is required because hatchling does not auto-discover top-level single-file modules.
