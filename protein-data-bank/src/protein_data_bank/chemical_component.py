from typing import List

from mcp import types
from protein_data_bank.utils import fetch_data


async def chemical_component(comp_id: str) -> List[types.TextContent]:
    api_suffix = f"/chemcomp/{comp_id}"
    result = await fetch_data(api_suffix)
    return result


async def drugbank_annotations(comp_id: str) -> List[types.TextContent]:
    api_suffix = f"/drugbank/{comp_id}"
    result = await fetch_data(api_suffix)
    return result
