FROM python:3.10

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set the working directory
WORKDIR /app

# Copy the repository content
COPY . /app

# Install dependencies
RUN uv sync

# Command to run the MCP server
CMD ["uv", "run", "python", "-m", "mcp_server.main"]
