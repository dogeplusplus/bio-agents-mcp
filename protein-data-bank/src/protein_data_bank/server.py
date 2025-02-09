import json
import logging
from typing import List

import aiohttp
from dotenv import find_dotenv, load_dotenv
from hydra import compose, initialize
from mcp import types
from mcp.server import FastMCP

# Load environment variables from .env file
load_dotenv(find_dotenv())


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

initialize(config_path="../../conf")
cfg = compose(config_name="config")

mcp = FastMCP("protein-data-bank", port=cfg.server.port)


@mcp.tool()
async def get_structural_assembly_description(
    entry_id: str, assembly_id: str
) -> List[types.TextContent]:

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.pdb_api_url}/assembly/{entry_id}/{assembly_id}") as response:
            response_json = await response.json()

    result = types.TextContent(type="text", text=json.dumps(response_json, indent=2))
    return result


if __name__ == "__main__":
    mcp.run(transport="sse")
