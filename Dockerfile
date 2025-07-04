FROM python:3.10

# Install uv
RUN pip install uv

# Install uvicorn
RUN pip install uvicorn

# Set the working directory
WORKDIR /app

# Copy the repository content
COPY . /app

# Install dependencies using uv
RUN uv sync

# Command to run the MCP server
CMD ["uv", "run", "python", "-m", "mcp_server.main"]
