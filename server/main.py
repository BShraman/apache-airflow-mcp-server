# from fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP 

from tools.register_tools import RegisterTools

# ---------------- Initialize MCP Server ---------------------- #
mcp = FastMCP(
    name="Airflow MCP Server",
    instructions="Interact with Apache Airflow via REST API."
    )

# ---------------- Register Tools ------------------------------ #
RegisterTools(mcp)._dags()
RegisterTools(mcp)._backfills()
RegisterTools(mcp)._assets()
RegisterTools(mcp)._connections()
RegisterTools(mcp)._tasks_instance()

# ----------------- Run the server ----------------------------- #
if __name__ == "__main__":
    import sys
    print("🚀 Starting MCP server", file=sys.stderr)

    mcp.run(transport="stdio")
