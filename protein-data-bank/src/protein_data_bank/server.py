import os
import json
import aiohttp
import logging
from typing import List
from mcp.server import FastMCP
from mcp import types
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())

mcp = FastMCP("protein-data-bank", port=os.environ.get("MCP_SERVER_PORT", 8080))

PDB_API_URL = "https://data.rcsb.org/rest/v1/core"

@mcp.tool()
async def get_structural_assembly_description(entry_id: str, assembly_id: str) -> List[types.TextContent]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{PDB_API_URL}/assembly/{entry_id}/{assembly_id}") as response:
            response_json = await response.json()

    result = types.TextContent(type="text", text=json.dumps(response_json, indent=2))
    return result


if __name__ == "__main__":
    mcp.run(transport="sse")
