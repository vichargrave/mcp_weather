#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp[cli]",
# ]
# ///

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent


SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=["run", "weather.py"],
)


def _extract_text(result) -> str:
    return "\n".join(c.text for c in result.content if isinstance(c, TextContent))


async def call_get_alerts(session: ClientSession, state: str) -> str:
    return _extract_text(await session.call_tool("get_alerts", {"state": state}))


async def call_get_forecast(session: ClientSession, latitude: float, longitude: float) -> str:
    return _extract_text(await session.call_tool("get_forecast", {"latitude": latitude, "longitude": longitude}))


async def main() -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")
            print()

            # --- get_alerts ---
            state = "CA"
            print(f"=== Weather alerts for {state} ===")
            alerts = await call_get_alerts(session, state)
            print(alerts)
            print()

            # --- get_forecast ---
            # Default coords: San Jose, CA
            lat, lon = 37.3387, -121.8853
            print(f"=== Forecast for ({lat}, {lon}) ===")
            forecast = await call_get_forecast(session, lat, lon)
            print(forecast)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
