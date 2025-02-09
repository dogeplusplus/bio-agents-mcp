from typing import List, Callable

from mcp import types
from protein_data_bank.utils import fetch_data


async def fetch_schema(api_suffix: str) -> List[types.TextContent]:
    result = await fetch_data(api_suffix)
    return result


schemas = [
    "assembly",
    "branched_entity_instance",
    "branched_entity",
    "chem_comp",
    "drugbank",
    "entry",
    "nonpolymer_entity_instance",
    "nonpolymer_entity",
    "polymer_entity_instance",
    "polymer_entity",
    "pubmed",
    "uniprot",
]


def create_schema_function(schema_name: str) -> Callable[[], List[types.TextContent]]:
    async def schema_function() -> List[types.TextContent]:
        api_suffix = f"/schema/{schema_name}"
        return await fetch_schema(api_suffix)

    return schema_function


for schema in schemas:
    globals()[f"{schema}_schema"] = create_schema_function(schema)
