# Apache Airflow MCP Server

The **Apache Airflow MCP Server** enables users to orchestrate and manage Airflow workflows using natural language, powered by [Claude Desktop](https://claude.ai/). All source code is containerized for easy deployment and integration. This solution lets users interact with Airflow DAGs, assets, and management tools through conversational prompts, streamlining workflow automation and monitoring.

---

## 🚀 Features

- **Natural Language Workflow Orchestration:** Control and query Airflow using plain English.
- **Containerized Architecture:** All components run in Docker for portability and reproducibility.
- **Claude Desktop Integration:** Seamless communication between MCP server and Claude Desktop.
- **Auto-Discovery of Tools:** Registered Airflow tools are automatically available in Claude Desktop.
- **Easy Setup:** Minimal prerequisites and simple configuration.

---

## 🛠 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Claude Desktop](https://claude.ai/)
- (Optional) Python 3.10+ for local development
- A running Apache Airflow instance (local or remote)

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/airflow-mcp-server.git
cd airflow-mcp-server
```

### 2. Build the Docker Image

```bash
docker build -t airflow-mcp-server .
```

### 3. Start Airflow Instance Locally

```bash
docker-compose up -d
```

### 4. Access Airflow UI

Open [http://localhost:8080](http://localhost:8080) in your browser.

### 5. Configure Claude Desktop

To connect Claude Desktop to your MCP server, follow these steps:

1. **Open Claude Desktop**
- Launch the Claude Desktop application.

2. **Navigate to Settings**
- Click on the **Settings** icon (usually a gear ⚙️) in the sidebar.

3. **Go to Developer Section**
- In the Settings menu, scroll down and select **Developer**.

4. **Edit Configuration**
- Click on **Edit Config** to open the configuration file in the built-in editor.

5. **Add MCP Server Entry**
- In the configuration file, locate the `"claude_desktop_config.json"` file.
- Insert the following block (update the image name if needed):

```json
"mcpServers": {
    "airflow-mcp-server": {
        "command": "docker",
        "args": [
            "run",
            "-i",
            "--rm",
            "airflow-mcp-server"
        ]
    }
}
```

6. **Save Changes**
- Click **Save** to apply your changes.

7. **Restart Claude Desktop**
- Restart Claude Desktop to ensure the new MCP server configuration is loaded.

**Tip:**
If you need to pass environment variables or use a custom Docker image, adjust the `"args"` array accordingly.

For more details, refer to the [Claude Desktop documentation](https://claude.ai/docs).

---

## 💬 Using MCP with Claude Desktop

Once connected, you can list all available Airflow tools directly in Claude Desktop by entering a prompt such as `List available MCP tools`. Claude Desktop will display the registered tools and their descriptions.

Claude Desktop will send your requests to the MCP server, which translates them into Airflow API calls and returns the results conversationally. This enables intuitive workflow management and monitoring without needing to write code or use the Airflow UI.

**Example Prompts:**
- `List all Airflow DAGs`
- `Get details for dag_id=my_etl_pipeline`
- `Show all workflow assets`
- `Trigger the daily_report DAG`
- `What is the status of the data_ingestion DAG?`

**How it works:**
- Claude Desktop sends your prompt to the MCP server.
- The MCP server translates your request to Airflow's REST API.
- Results are returned conversationally in Claude Desktop.

---

## 🧩 Advanced Usage

- **Register Custom Tools:** Add Python modules to the `/tools` directory to extend MCP capabilities.
- **Environment Variables:** Configure Airflow API URL, credentials, and MCP server settings in `.env`.
- **Security:** Use dedicated Airflow credentials and restrict network access as needed.

---

## 📝 Troubleshooting

- **Claude Desktop can't find MCP tools:** Ensure the MCP server is running and correctly configured.
- **Authentication errors:** Check your Airflow credentials in the `.env` file.
- **Docker issues:** Use `docker logs airflow-mcp-server` to view error messages.

---
## 📚 Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Claude Desktop Documentation](https://claude.ai/docs)
- [Docker Documentation](https://docs.docker.com/)