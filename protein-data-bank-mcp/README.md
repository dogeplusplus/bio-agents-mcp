# Protein Data Bank

## Description

The `protein_data_bank_mcp` module provides a server that interacts with the Protein Data Bank (PDB) API to fetch structural assembly descriptions. It is built using the FastMCP framework and supports asynchronous operations with `aiohttp`.

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
python src/protein_data_bank_mcp/server.py
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

### Get Chemical Component

- **Endpoint:** `/chemcomp/{comp_id}`
- **Method:** GET
- **Description:** Fetches the chemical component for the given component ID from the PDB API.

### Get DrugBank Annotations

- **Endpoint:** `/drugbank/{comp_id}`
- **Method:** GET
- **Description:** Fetches the DrugBank annotations for the given component ID from the PDB API.

### Get Branched Entity

- **Endpoint:** `/branched_entity/{entry_id}/{entity_id}`
- **Method:** GET
- **Description:** Fetches the branched entity for the given entry ID and entity ID from the PDB API.

### Get Non-Polymer Entity

- **Endpoint:** `/non_polymer_entity/{entry_id}/{entity_id}`
- **Method:** GET
- **Description:** Fetches the non-polymer entity for the given entry ID and entity ID from the PDB API.

### Get Polymer Entity

- **Endpoint:** `/polymer_entity/{entry_id}/{entity_id}`
- **Method:** GET
- **Description:** Fetches the polymer entity for the given entry ID and entity ID from the PDB API.

### Get UniProt Annotations

- **Endpoint:** `/uniprot/{entry_id}/{entity_id}`
- **Method:** GET
- **Description:** Fetches the UniProt annotations for the given entry ID and entity ID from the PDB API.

### Get Structure

- **Endpoint:** `/entry/{entry_id}`
- **Method:** GET
- **Description:** Fetches the structure for the given entry ID from the PDB API.

### Get PubMed Annotations

- **Endpoint:** `/pubmed/{entry_id}`
- **Method:** GET
- **Description:** Fetches the PubMed annotations for the given entry ID from the PDB API.

### Get PDB Cluster Data Aggregation

- **Endpoint:** `/entry_groups/{group_id}`
- **Method:** GET
- **Description:** Fetches the PDB cluster data aggregation for the given group ID from the PDB API.

### Get Aggregation Group Provenance

- **Endpoint:** `/group_provenance/{group_provenance_id}`
- **Method:** GET
- **Description:** Fetches the aggregation group provenance for the given group provenance ID from the PDB API.

### Get PDB Cluster Data Aggregation Method

- **Endpoint:** `/polymer_entity_groups/{group_id}`
- **Method:** GET
- **Description:** Fetches the PDB cluster data aggregation method for the given group ID from the PDB API.

### Get Pairwise Polymeric Interface Description

- **Endpoint:** `/interface/{entry_id}/{assembly_id}/{interface_id}`
- **Method:** GET
- **Description:** Fetches the pairwise polymeric interface description for the given entry ID, assembly ID, and interface ID from the PDB API.
