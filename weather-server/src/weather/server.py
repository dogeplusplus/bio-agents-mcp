import logging
from typing import Any
import asyncio
import httpx
import signal
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions
import mcp.server.stdio

from mcp.server.fastmcp import FastMCP

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

server = FastMCP("weather")


async def make_nws_request(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }

    try:
        response = await client.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return (
        f"Event: {props.get('event', 'Unknown')}\n"
        f"Severity: {props.get('severity', 'Unknown')}\n"
        f"Area: {props.get('areaDesc', 'Unknown')}\n"
        f"Status: {props.get('status', 'Unknown')}\n"
        f"Headline: {props.get('headline', 'Unknown')}\n"
        "---"
    )

@server.tool()
async def get_alerts(state: str) -> str:
    state = state.upper()
    if len(state) != 2:
        raise ValueError("State must be a two-letter code")

    async with httpx.AsyncClient() as client:
        alerts_url = f"{NWS_API_BASE}/alerts/active?area={state}"
        alerts_data = await make_nws_request(client, alerts_url)

        if not alerts_data:
            return [types.TextContent(type="text", text="Failed to fetch alerts")]

        features = alerts_data.get("features", [])
        if not features:
            return [types.TextContent(type="text", text=f"No active alerts found for {state}")]

        formatted_alerts = [format_alert(feature) for feature in features[:20]]
        alert_texts = f"Active alerts for {state}:\n\n" + "\n".join(formatted_alerts)

    return [
        types.TextContent(type="text", text=alert_texts)
    ]


@server.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return [types.TextContent(
            type="text",
            text="Latitude must be between -90 and 90, and longitude must be between -180 and 180",
        )]

    async with httpx.AsyncClient() as client:
        lat_str = f"{latitude}"
        lon_str = f"{longitude}"

        points_url = f"{NWS_API_BASE}/points/{lat_str},{lon_str}"
        points_data = await make_nws_request(client, points_url)

        if not points_data:
            return [types.TextContent(type="text", text="Failed to fetch forecast")]

        properties = points_data.get("properties", {})
        forecast_url = properties.get("forecast")

        if not forecast_url:
            return [types.TextContent(type="text", text="Failed to get forecast URL from grid point data")]

        forecast_data = await make_nws_request(client, forecast_url)

        if not forecast_data:
            return [types.TextContent(type="text", text="Failed to fetch forecast")]

        periods = forecast_data.get("properties", {}).get("periods", [])
        if not periods:
            return [types.TextContent(type="text", text="No forecast periods found")]

        formatted_forecast = []
        for period in periods:
            forecast_text = (
                f"{period.get('name', 'Unknown')}:\n"
                f"Temperature: {period.get('temperature', 'Unknown')}°{period.get('temperatureUnit', 'F')}\n"
                f"Wind: {period.get('windSpeed', 'Unknown')} {period.get('windDirection', 'Unknown')}\n"
                f"{period.get('shortForecast', 'Unknown')}\n"
                "---"
            )
            formatted_forecast.append(forecast_text)

        forecast_text = f"Forecast for {latitude}, {longitude}:\n\n" + "\n".join(formatted_forecast)
        return [types.TextContent(
            type="text",
            text=forecast_text,
        )]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Running Main")
    print(asyncio.run(server.list_tools()))
    server.run(transport="sse")
    logging.debug("Finished Main")