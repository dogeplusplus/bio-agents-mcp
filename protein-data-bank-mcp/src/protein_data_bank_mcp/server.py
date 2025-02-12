import logging

from mcp.server import FastMCP
from protein_data_bank_mcp.constants import MCP_SERVER_PORT
from protein_data_bank_mcp.assembly import structural_assembly_description
from protein_data_bank_mcp.chemical_component import (
    chemical_component,
    drugbank_annotations,
)
from protein_data_bank_mcp.entity_instance import (
    polymer_entity_instance,
    branched_entity_instance,
    non_polymer_entity_instance,
)
from protein_data_bank_mcp.entity import (
    branched_entity,
    polymer_entity,
    non_polymer_entity,
    uniprot_annotations,
)
from protein_data_bank_mcp.entry import structure, pubmed_annotations
from protein_data_bank_mcp.groups import (
    aggregation_group_provenance,
    pdb_cluster_data_aggregation,
    pdb_cluster_data_aggregation_method,
)
from protein_data_bank_mcp.interface import pairwise_polymeric_interface_description
from protein_data_bank_mcp.schema import (
    assembly_schema,
    branched_entity_instance_schema,
    branched_entity_schema,
    chem_comp_schema,
    drugbank_schema,
    entry_schema,
    nonpolymer_entity_instance_schema,
    nonpolymer_entity_schema,
    polymer_entity_instance_schema,
    polymer_entity_schema,
    pubmed_schema,
    uniprot_schema,
)
from protein_data_bank_mcp.repository_holdings import (
    current_entry_ids,
    structure_status,
    structure_list_status,
    removed_structure_description,
    removed_entry_ids,
    unreleased_structures,
    unreleased_structure_processing,
    unreleased_entry_ids,
)

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
    # Schema endpoints
    assembly_schema,
    branched_entity_instance_schema,
    branched_entity_schema,
    chem_comp_schema,
    drugbank_schema,
    entry_schema,
    nonpolymer_entity_instance_schema,
    nonpolymer_entity_schema,
    polymer_entity_instance_schema,
    polymer_entity_schema,
    pubmed_schema,
    uniprot_schema,
    # Repository holdings endpoints
    current_entry_ids,
    structure_status,
    structure_list_status,
    removed_structure_description,
    removed_entry_ids,
    unreleased_structures,
    unreleased_structure_processing,
    unreleased_entry_ids,
]

for tool in tools:
    mcp_server.tool()(tool)
