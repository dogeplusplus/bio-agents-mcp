# Protein Data Bank

## Description

The `protein_data_bank` module provides a server that interacts with the Protein Data Bank (PDB) API to fetch structural assembly descriptions. It is built using the FastMCP framework and supports asynchronous operations with `aiohttp`.

## Features

- Fetch structural assembly descriptions from the PDB API.
- Asynchronous operations for efficient data retrieval.
- Configurable server settings using Hydra and environment variables.

## Requirements

- Python 3.12 or higher
- `aiohttp` >= 3.11.12
- `httpx` >= 0.28.1
- `mcp` >= 1.1.2
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
    MCP_SERVER_PORT=8080
    ```

## Configuration

The server configuration is managed using Hydra. The configuration file is located at `conf/config.yaml`.

Example configuration (`conf/config.yaml`):
```yaml
server:
  port: ${oc.env:MCP_SERVER_PORT,8080}
pdb_api_url: "https://data.rcsb.org/rest/v1/core"
```

## Usage

To start the server, run the following command:
```sh
python src/protein_data_bank/server.py
```

The server will start and listen on the configured port (default: 8080).

## Docker

A Dockerfile is provided to build a Docker image for the server.

1. Build the Docker image:
    ```sh
    docker build -t protein-data-bank .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8080:8080 --env-file .env protein-data-bank
    ```

## API Endpoints

### Get Structural Assembly Description

- **Endpoint:** `/assembly/{entry_id}/{assembly_id}`
- **Method:** GET
- **Description:** Fetches the structural assembly description for the given entry ID and assembly ID from the PDB API.
