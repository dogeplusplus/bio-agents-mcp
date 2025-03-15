# ChEMBL MCP Server

Micro-service for accessing the ChEMBL database through the MCP protocol. This service provides natural language access to chemical compounds, drug data, and bioactivity information.

## Features

- Access to ChEMBL REST API endpoints
- Chemical compound and drug information retrieval
- Bioactivity data access
- Built on FastMCP framework with async/await support

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure environment variables in `.env`:
```env
CHEMBL_MCP_HOST=localhost
CHEMBL_MCP_PORT=8081
```

## Docker Usage

Run with Docker Compose:
```bash
docker compose up chembl-server
```

The server will be available at `http://localhost:8081`.
