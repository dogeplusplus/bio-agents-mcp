# Model Context Protocol Example

## Description

This project contains multiple modules that interact with various services and APIs using the FastMCP framework. Each module is designed to perform specific tasks and can be run independently or together using Docker Compose.

## Modules

### LLM Client

The `llm-client` module provides a client that interacts with a Language Model (LLM) server to process queries and utilize available tools. It is built using the FastMCP framework and supports asynchronous operations with `aiohttp`.

For more details, refer to the [LLM Client README](llm-client/README.md).

### Protein Data Bank

The `protein_data_bank` module provides a server that interacts with the Protein Data Bank (PDB) API to fetch structural assembly descriptions. It is built using the FastMCP framework and supports asynchronous operations with `aiohttp`.

For more details, refer to the [Protein Data Bank README](protein-data-bank/README.md).

## Docker

Dockerfiles are provided for each module to build Docker images.

- **Build the Docker image:**
  ```sh
  docker build -t <module-name> .
  ```

- **Run the Docker container:**
  ```sh
  docker run --env-file .env <module-name>
  ```

## Docker Compose

A `docker-compose.yml` file is provided to run all services together.

- **Start all services:**
  ```sh
  docker-compose up -d
  ```

- **Stop all services:**
  ```sh
  docker-compose down
  ```

## Makefile

A `Makefile` is provided to simplify common tasks.

- **Available targets:**
  - `setup-env`: Set up the initial environment.
  - `build`: Build all Docker images.
  - `up`: Start all services using docker-compose.
  - `down`: Stop all services using docker-compose.
  - `restart`: Restart all services using docker-compose.
