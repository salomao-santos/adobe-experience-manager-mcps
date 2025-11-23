"""Main entry point for running the MCP server as a module."""

from adobe_experience_manager_mcps.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
