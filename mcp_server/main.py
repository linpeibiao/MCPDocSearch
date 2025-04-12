import traceback
from pathlib import Path

# Import the shared FastMCP instance
from mcp_server.app import mcp_server as mcp_app_instance

# Import the data loading function
from mcp_server.data_loader import load_and_chunk_documents
# Import the tools module to ensure decorators run and register tools
import mcp_server.mcp_tools

# --- Main Execution (for direct run `python -m mcp_server.main`) ---
if __name__ == "__main__":
    # Load documents synchronously before starting the server
    # print("Loading documents...") # Removed print
    load_and_chunk_documents()
    # print("Document loading complete.") # Removed print

    # print("Starting MCP server on STDIO...") # Removed print
    try:
        # Call run directly on the imported instance
        mcp_app_instance.run(transport="stdio")
        # print("MCP server on STDIO finished.") # Removed print
    except KeyboardInterrupt:
        # Use stderr for user stop message if desired
        import sys
        print("\nServer stopped by user.", file=sys.stderr)
    except Exception as e:
        # Use stderr for errors
        import sys
        print(f"An error occurred: {e}", file=sys.stderr)
        # Print the full traceback to see the sub-exception details
        traceback.print_exc() # This already prints to stderr by default
