import chainlit as cl
import logging

from dotenv import find_dotenv, load_dotenv
from hydra import compose, initialize
from client import OllamaClient, MCPClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv(find_dotenv())
initialize(config_path="conf")
cfg = compose(config_name="config")

llm = OllamaClient(model=cfg.ollama.model, base_url=cfg.ollama.base_url)
client = MCPClient(llm)


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    await client.connect_to_servers(cfg.mcp.servers)

    response = await client.process_query(message.content, history=[])

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()
