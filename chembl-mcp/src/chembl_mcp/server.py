import logging

from mcp.server import FastMCP
from chembl_mcp.constants import MCP_SERVER_PORT

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp_server = FastMCP("protein-data-bank-mcp", port=MCP_SERVER_PORT)

tools = [
]

for tool in tools:
    mcp_server.tool()(tool)
