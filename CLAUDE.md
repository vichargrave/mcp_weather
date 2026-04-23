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

Syntax-check a Python file without running it:
```
python -m py_compile <file>.py
```

## Environment

`weather_cli_inter.py` requires `ANTHROPIC_API_KEY`. Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your-key-here
```

The key is loaded via `python-dotenv` (`load_dotenv()` at module top). The other two scripts do not use the Anthropic API and do not need this key.

## Architecture

This is a single-file MCP server (`weather.py`) built with `FastMCP`. It exposes two tools to MCP clients (e.g. Claude Desktop):

- `get_alerts(state)` — fetches active weather alerts for a US state from the NWS API
- `get_forecast(latitude, longitude)` — fetches a multi-period forecast by first resolving coordinates to a grid endpoint, then fetching that grid's forecast

All NWS requests go through `make_nws_request()`, which uses `httpx` with a 30-second timeout and returns `None` on any error. The server runs over `stdio` transport, which is the standard transport for MCP integrations with Claude Desktop.

The entry point registered in `pyproject.toml` is `mcp-weather = "weather:main"`. The `[tool.hatch.build.targets.wheel] include = ["weather.py"]` config is required because hatchling does not auto-discover top-level single-file modules.

### Inline script dependencies

`weather.py` and `weather_cli.py` embed PEP 723 inline dependency metadata (`# /// script` headers), so `uv run` can execute them as standalone scripts without the project venv. `weather_cli_inter.py` has no such header and relies on the project venv managed by `pyproject.toml`.

### CLI clients

**`weather_cli.py`** — minimal MCP client that connects to the server over stdio, lists available tools, then calls `get_alerts("CA")` and `get_forecast(37.3387, -121.8853)` (San Jose) and prints results.

**`weather_cli_inter.py`** — interactive MCP client that connects to any `.py` or `.js` MCP server (pass path as argv[1]), then runs a chat loop backed by the Claude API. Each user query is sent to Claude with the server's tools available; Claude decides which tools to call. The Claude model is set by `ANTHROPIC_MODEL` at the top of the file. `process_query` handles one round of tool calls per query — Claude can call one tool and incorporate its result, but does not loop for multi-step agentic tool chains.

## Git workflow

After completing any meaningful unit of work — a new feature, bug fix, refactor, or documentation update — commit the changes and push to GitHub immediately. Do not batch unrelated changes into a single commit.

Commit message format:
- Use the imperative mood: "Add X", "Fix Y", "Update Z"
- First line: short summary (50 chars or less)
- Keep messages specific enough that the history tells the story of what was built and why

```
git add <changed files>
git commit -m "Short description of what changed and why"
git push
```

Never let work accumulate uncommitted. If a task spans multiple steps, commit at each logical checkpoint so progress is never lost.

## Claude Code automation hooks

Configured in `.claude/settings.local.json`:

- **PostToolUse / Write** — auto-stages each file written by Claude (`git add <file>`)
- **PostToolUse / Bash** — runs `git push` after any Bash command containing `git commit`
- **Stop** — on Claude exit, commits all uncommitted changes with a timestamped message and pushes to GitHub
