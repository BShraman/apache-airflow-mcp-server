# Apache Airflow MCP Server

This project is an **Apache Airflow MCP (Model Context Protocol) Server** that allows you to interact with Airflow DAGs, assets, and management tools via [Claude Desktop](https://claude.ai/) or other MCP-compatible clients.

The MCP server runs inside a **local Docker container** and exposes registered tools for interacting with Airflow’s REST API.

---
## 🛠 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running locally  
- [Claude Desktop](https://claude.ai/) installed for integrating with the MCP server  
- (Optional) Python 3.10+ for local development and testing  
- A running Apache Airflow instance accessible by the server

---

## Setup and Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/airflow-mcp-server.git
cd airflow-mcp-server
```

### 2. Build the Docker Image
```bash
docker build -t airflow-mcp-server .
```

### 3. Run Airflow Local using Docker-compose
```bash
docker-compose up -d
```

### 4. Access Airflow UI
http://localhost:8080


### 5 . Configuration for Claude Desktop
Edit the MCP Config with
```json
#claude_desktop_config.json
{
  "mcpServers": {
    "airflow-custom-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "airflow-custom-mcp"
      ]
    }
  }
}
```

## Using in Claude Desktop

- **Tools**: Auto-listed in Claude Desktop and ready to invoke.
- **Example Prompts**:
- `list all airflow dags`
- `get dag details for {dag_id}`
- `list all assets`