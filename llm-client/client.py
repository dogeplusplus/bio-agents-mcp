import asyncio
import logging
from contextlib import AsyncExitStack
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from hydra import compose, initialize
from mcp import ClientSession
from mcp.client.sse import sse_client
from ollama import chat

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv(find_dotenv())


class OllamaClient:
    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url

    def send_message(self, messages: List[str], tools: Optional[list] = None, stream: bool = False):
        stream = chat(
            model=self.model,
            tools=tools,
            messages=messages,
            stream=stream,
        )
        return stream


def ollama_tool_conversion(tool):
    return {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["input_schema"],
        },
    }


class MCPClient:
    def __init__(self, llm: OllamaClient):
        self.llm = llm
        self.exit_stack = AsyncExitStack()
        self.sessions = {}
        self.available_tools = []

    async def connect_to_servers(self, servers_config: dict):
        for server_name, config in servers_config.items():
            host = config["host"]
            port = config["port"]
            url = f"http://{host}:{port}/sse"

            sse_transport = await self.exit_stack.enter_async_context(sse_client(url))
            reader, writer = sse_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(reader, writer)
            )

            await session.initialize()
            self.sessions[server_name] = session

            response = await session.list_tools()
            server_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                }
                for tool in response.tools
            ]
            self.available_tools.extend(server_tools)

    async def process_query(self, query: str, history: List[str] = []) -> str:
        messages = [
            {
                "role": "system",
                "content": "The following is the history of the conversation:",
            },
        ]
        logger.info(f"History of the conversation: {history}")

        for message in history:
            messages.append(
                {"role": message["role"], "content": message["content"]})

        messages.extend(
            [
                {
                    "role": "system",
                    "content": """
                    You have access to tools for protein data bank and Chembl.
                    Use the API tools to extract the relevant information.
                    Fill in missing arguments with sensible values if the user
                    hasn't provided them such as the assembly_id.
                    """,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ]
        )

        tools = [ollama_tool_conversion(tool) for tool in self.available_tools]
        response = self.llm.send_message(messages, tools=tools)

        message = response.message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function = tool_call.function
                tool_name = function.name
                tool_args = function.arguments

                # Try each session until we find one that has the tool
                for session in self.sessions.values():
                    try:
                        result = await session.call_tool(tool_name, tool_args)
                        messages.append(
                            {"role": "system",
                                "content": result.content[0].text[:10000]}
                        )
                    except Exception as e:
                        logger.error(f"Error calling tool {tool_name}: {e}")

        response = self.llm.send_message(messages, stream=True)
        return response

    async def chat_loop(self):
        while True:
            try:
                query = input("Enter a query: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print(response)

            except Exception as e:
                print(f"\nAn error occurred: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    initialize(config_path="conf")
    cfg = compose(config_name="config")

    llm = OllamaClient(model=cfg.ollama.model, base_url=cfg.ollama.base_url)
    client = MCPClient(llm)

    await client.connect_to_servers(cfg.mcp.servers)

    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
