import logging

from mcp.server import FastMCP
from protein_data_bank.constants import MCP_SERVER_PORT
from protein_data_bank.assembly import structural_assembly_description
from protein_data_bank.chemical_component import (
    chemical_component,
    drugbank_annotations,
)
from protein_data_bank.entity_instance import (
    polymer_entity_instance,
    branched_entity_instance,
    non_polymer_entity_instance,
)
from protein_data_bank.entity import (
    branched_entity,
    polymer_entity,
    non_polymer_entity,
    uniprot_annotations,
)
from protein_data_bank.entry import structure, pubmed_annotations
from protein_data_bank.groups import (
    aggregation_group_provenance,
    pdb_cluster_data_aggregation,
    pdb_cluster_data_aggregation_method,
)
from protein_data_bank.interface import pairwise_polymeric_interface_description

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp_server = FastMCP("protein-data-bank", port=MCP_SERVER_PORT)

tools = [
    structural_assembly_description,
    chemical_component,
    drugbank_annotations,
    polymer_entity_instance,
    branched_entity_instance,
    non_polymer_entity_instance,
    uniprot_annotations,
    branched_entity,
    polymer_entity,
    non_polymer_entity,
    structure,
    pubmed_annotations,
    aggregation_group_provenance,
    pdb_cluster_data_aggregation,
    pdb_cluster_data_aggregation_method,
    pairwise_polymeric_interface_description,
]

for tool in tools:
    mcp_server.tool()(tool)
