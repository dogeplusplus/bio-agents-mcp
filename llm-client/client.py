import asyncio
from contextlib import AsyncExitStack
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from hydra import compose, initialize
from mcp import ClientSession
from mcp.client.sse import sse_client
from ollama import chat


# Load environment variables from .env file
load_dotenv(find_dotenv())


class OllamaClient:
    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url

    def send_message(self, messages: List[str], tools: Optional[list] = None):
        stream = chat(
            model=self.model,
            tools=tools,
            messages=messages,
        )
        return stream


def ollama_tool_conversion(tool):
    return {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["input_schema"],
        }
    }

class MCPClient:
    def __init__(self, llm: OllamaClient):
        self.llm = llm
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, host: str, port: int):
        self.server_host = host
        self.server_port = port
        url = f"http://{host}:{port}/sse"

        sse_transport = await self.exit_stack.enter_async_context(sse_client(url))
        reader, writer = sse_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(reader, writer)
        )

        await self.session.initialize()

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        self.available_tools = available_tools

    async def process_query(self, query: str):
        messages = [
            {
                "role": "user",
                "content": query,
            },
        ]

        tools = [ollama_tool_conversion(tool) for tool in self.available_tools]
        response = self.llm.send_message(messages, tools=tools)

        tool_results = []
        final_text = []

        message = response.message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function = tool_call.function
                tool_name = function.name
                tool_args = function.arguments

                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                messages.append({"role": "system", "content": result.content[0].text[:10000]})

            messages.append({"role": "system", "content": "Use the API outputs to create the response."})
            response = self.llm.send_message(messages)
            final_text.append(response.message.content)
        else:
            final_text.append(message.content)
        return "\n".join(final_text)

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

    llm = OllamaClient(
        model=cfg.ollama.model,
        base_url=cfg.ollama.base_url
    )
    client = MCPClient(llm)

    try:
        await client.connect_to_server(cfg.mcp.server_host, cfg.mcp.server_port)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
