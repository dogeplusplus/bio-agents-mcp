import json
import aiohttp
from typing import List
from mcp import types

from protein_data_bank_mcp.constants import PDB_API_URL


async def fetch_data(api_suffix: str) -> List[types.TextContent]:
    url = f"{PDB_API_URL}{api_suffix}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
    result = types.TextContent(
        type="text", text=json.dumps(response_json, indent=2))
    return result
