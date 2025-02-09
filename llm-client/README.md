# LLM Client

## Description

The `llm-client` module provides a client that interacts with a Language Model (LLM) server to process queries and utilize available tools. It is built using the FastMCP framework and supports asynchronous operations with `aiohttp`.

## Features

- Connect to an LLM server and process queries.
- Utilize available tools provided by the LLM server.
- Asynchronous operations for efficient data processing.
- Configurable client settings using Hydra and environment variables.

## Requirements

- Python 3.12 or higher
- `httpx` >= 0.27.2
- `mcp` >= 1.1.2
- `ollama` >= 0.4.4
- `requests` >= 2.32.3
- `hydra-core` >= 1.2.0
- `python-dotenv` >= 1.0.1

## Installation

1. Install the dependencies using the uv package manager:
    ```sh
    uv sync --frozen --no-install-project --no-dev
    ```

2. Set up the environment variables:
    Create a `.env` file in the root directory with the following content:
    ```env
    OLLAMA_HOST=localhost
    OLLAMA_PORT=11434
    MCP_SERVER_HOST=localhost
    MCP_SERVER_PORT=8080
    ```

3. Install Ollama:
    Follow the instructions on the [Ollama GitHub page](https://github.com/ollama/ollama) to install Ollama.

## Configuration

The client configuration is managed using Hydra. The configuration file is located at `conf/config.yaml`.

Example configuration (`conf/config.yaml`):
```yaml
ollama:
  model: "qwen2.5:14b"
  base_url: "http://${oc.env:OLLAMA_HOST}:${oc.env:OLLAMA_PORT}"
mcp:
  server_host: ${oc.env:MCP_SERVER_HOST}
  server_port: ${oc.env:MCP_SERVER_PORT}
```

## Usage

To start the client, run the following command:
```sh
python client.py
```

The client will connect to the configured LLM server and start processing queries.

## Docker

A Dockerfile is provided to build a Docker image for the client.

1. Build the Docker image:
    ```sh
    docker build -t llm-client .
    ```

2. Run the Docker container:
    ```sh
    docker run --env-file .env llm-client
    ```
