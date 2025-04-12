# Documentation Crawler & MCP Server

This project provides a toolset to crawl websites, generate Markdown documentation, and make that documentation searchable via a Model Context Protocol (MCP) server, designed for integration with tools like Cursor.

## Features

- **Web Crawler (`crawler_cli`)**:
  - Crawls websites starting from a given URL using `crawl4ai`.
  - Configurable crawl depth, URL patterns (include/exclude), content types, etc.
  - Optional cleaning of HTML before Markdown conversion (removes nav links, headers, footers).
  - Generates a single, consolidated Markdown file from crawled content.
  - Saves output to `./storage/` by default.
- **MCP Server (`mcp_server`)**:
  - Loads Markdown files from the `./storage/` directory.
  - Parses Markdown into semantic chunks based on headings.
  - Generates vector embeddings for each chunk using `sentence-transformers` (`multi-qa-mpnet-base-dot-v1`).
  - Utilizes caching (`pickle`) for faster subsequent loads.
  - Exposes MCP tools via `fastmcp` for clients like Cursor:
    - `list_documents`: Lists available crawled documents.
    - `get_document_headings`: Retrieves the heading structure for a document.
    - `search_documentation`: Performs semantic search over document chunks using vector similarity.
- **Cursor Integration**: Designed to run the MCP server via `stdio` transport for use within Cursor.

## Workflow

1. **Crawl:** Use the `crawler_cli` tool to crawl a website and generate a `.md` file in `./storage/`.
2. **Run Server:** Configure and run the `mcp_server` (typically managed by an MCP client like Cursor).
3. **Load & Embed:** The server automatically loads, chunks, and embeds the content from the `.md` files in `./storage/`.
4. **Query:** Use the MCP client (e.g., Cursor Agent) to interact with the server's tools (`list_documents`, `search_documentation`, etc.) to query the crawled content.

## Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and execution.

1. **Install `uv`**: Follow the instructions on the [uv website](https://github.com/astral-sh/uv).
2. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd doc-crawler
    ```

3. **Install dependencies:**

    ```bash
    uv sync
    ```

    This command creates a virtual environment (usually `.venv`) and installs all dependencies listed in `pyproject.toml`.

## Usage

### 1. Crawling Documentation

Run the crawler using the `crawl.py` script or directly via `uv run`.

**Basic Example:**

```bash
uv run python crawl.py https://docs.example.com
```

This will crawl `https://docs.example.com` with default settings and save the output to `./storage/docs.example.com.md`.

**Example with Options:**

```bash
uv run python crawl.py https://docs.another.site --output ./storage/custom_name.md --max-depth 2 --keyword "API" --keyword "Reference" --exclude-pattern "*blog*"
```

**View all options:**

```bash
uv run python crawl.py --help
```

Key options include:

- `--output`/`-o`: Specify output file path.
- `--max-depth`/`-d`: Set crawl depth (must be between 1 and 5).
- `--include-pattern`/`--exclude-pattern`: Filter URLs to crawl.
- `--keyword`/`-k`: Keywords for relevance scoring during crawl.
- `--remove-links`/`--keep-links`: Control HTML cleaning.
- `--cache-mode`: Control `crawl4ai` caching (`DEFAULT`, `BYPASS`, `FORCE_REFRESH`).

### 2. Running the MCP Server

The MCP server is designed to be run by an MCP client like Cursor via the `stdio` transport. The command to run the server is:

```bash
python -m mcp_server.main
```

However, it needs to be run from the project's root directory (`doc-crawler`) so that Python can find the `mcp_server` module.

### 3. Configuring Cursor

To use this server with Cursor, create a `.cursor/mcp.json` file in the root of this project (`doc-crawler/.cursor/mcp.json`) with the following content:

```json
{
  "mcpServers": {
    "doc-query-server": {
      "command": "uv",
      "args": [
        "--directory",
        // IMPORTANT: Replace with the ABSOLUTE path to this project directory on your machine
        "/path/to/your/doc-crawler",
        "run",
        "python",
        "-m",
        "mcp_server.main"
      ],
      "env": {}
    }
  }
}
```

**Explanation:**

- `"doc-query-server"`: A name for the server within Cursor.
- `"command": "uv"`: Specifies `uv` as the command runner.
- `"args"`:
  - `"--directory", "/path/to/your/doc-crawler"`: **Crucially**, tells `uv` to change its working directory to your project root before running the command. **Replace `/path/to/your/doc-crawler` with the actual absolute path on your system.**
  - `"run", "python", "-m", "mcp_server.main"`: The command `uv` will execute within the correct directory and virtual environment.

After saving this file and restarting Cursor, the "doc-query-server" should become available in Cursor's MCP settings and usable by the Agent (e.g., `@doc-query-server search documentation for "how to install"`).

## Dependencies

Key libraries used:

- `crawl4ai`: Core web crawling functionality.
- `fastmcp`: MCP server implementation.
- `sentence-transformers`: Generating text embeddings.
- `torch`: Required by `sentence-transformers`.
- `typer`: Building the crawler CLI.
- `uv`: Project and environment management.
- `beautifulsoup4` (via `crawl4ai`): HTML parsing.
- `rich`: Enhanced terminal output.
