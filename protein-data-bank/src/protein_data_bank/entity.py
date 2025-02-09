from typing import List

from mcp import types
from protein_data_bank.utils import fetch_data


async def branched_entity(entry_id: str, entity_id: str) -> List[types.TextContent]:
    api_suffix = f"/branched_entity/{entry_id}/{entity_id}"
    result = await fetch_data(api_suffix)
    return result


async def non_polymer_entity(entry_id: str, entity_id: str) -> List[types.TextContent]:
    api_suffix = f"/non_polymer_entity/{entry_id}/{entity_id}"
    result = await fetch_data(api_suffix)
    return result


async def polymer_entity(entry_id: str, entity_id: str) -> List[types.TextContent]:
    api_suffix = f"/polymer_entity/{entry_id}/{entity_id}"
    result = await fetch_data(api_suffix)
    return result


async def uniprot_annotations(entry_id: str, entity_id: str) -> List[types.TextContent]:
    api_suffix = f"/uniprot/{entry_id}/{entity_id}"
    result = await fetch_data(api_suffix)
    return result
