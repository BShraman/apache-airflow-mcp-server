# Apache Airflow MCP Server

This project is an **Apache Airflow MCP (Multi-Connection Platform) Server** running locally inside a Docker container, designed to be used with **Claude Desktop** for seamless interaction with Apache Airflow's REST API.

---
## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running locally  
- [Claude Desktop](https://claude.ai/) installed for integrating with the MCP server  
- (Optional) Python 3.10+ for local development and testing  

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

