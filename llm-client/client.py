import os
import asyncio
from typing import List
from ollama import chat
from typing import Optional
from contextlib import AsyncExitStack


from mcp import ClientSession


class OllamaClient:
    def __init__(self, model: str = "llama3.2:1b", base_url: str = "http://ollama:11434"):
        self.model = model
        self.base_url = base_url

    def send_message(self, messages: List[str], tools: Optional[list] = None):
        stream = chat(
            model=self.model,
            tools=tools,
            messages=messages,
            base_url=self.base_url
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
    def __init__(self, llm: OllamaClient, session: Optional[ClientSession] = None):
        self.session = session
        self.llm = llm
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, host: str = "localhost", port: int = 8080):
        reader, writer = await asyncio.open_connection(host, port)
        self.stdio = reader
        self.write = writer

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
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
        print(f"Available tools: {available_tools}")


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

                print(f"Calling tool {tool_name} with args {tool_args}")
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                messages.append({"role": "assistant", "content": result.content[0].text[:10000]})

            messages.append({"role": "system", "content": "Use only the assistant outputs to create the response."})
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
    ollama_host = os.environ["OLLAMA_HOST"]
    ollama_port = os.environ["OLLAMA_PORT"]

    llm = OllamaClient(
        model="llama3.2:1b",
        base_url=f"http://{ollama_host}:{ollama_port}"
    )
    client = MCPClient(llm)

    weather_host = os.environ["WEATHER_SERVER_HOST"]
    weather_port = os.environ["WEATHER_SERVER_PORT"]

    try:
        await client.connect_to_server(weather_host, weather_port)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
