FROM python:3.13-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy only dependency files first (improves Docker layer caching)
COPY pyproject.toml uv.lock .env ./

# Create virtual environment and install dependencies
RUN uv venv && uv sync

# Copy rest of the source code
COPY server/ ./server/

# Expose FastAPI port if needed (not required for stdio)
EXPOSE 8000

# Run MCP server using stdio transport (for Claude)
CMD ["uv", "run", "server/main.py", "--transport", "stdio"]