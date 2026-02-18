"""
MCP (Model Context Protocol) Server Manager.

Creates and manages MCP servers for agent tool integration.
Each agent can have one or more MCP servers exposing tools that
other agents (or external MCP clients) can discover and invoke.

Supports transports: stdio, SSE, and Streamable HTTP.
"""
import importlib
from typing import Any, Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from app.core.logging import logger
from app.models.agent import MCPServerConfig, MCPTool


class MCPServerManager:
    """Manages MCP server instances for deployed agents."""

    def __init__(self):
        self._servers: dict[str, Server] = {}
        self._tool_handlers: dict[str, Callable] = {}

    async def create_server(self, config: MCPServerConfig) -> Server:
        """Create an MCP server from config, registering all tools."""
        server = Server(config.name)

        # Register tool list handler
        @server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.input_schema or {"type": "object", "properties": {}},
                )
                for tool in config.tools
            ]

        # Register tool call handler
        @server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            handler = self._tool_handlers.get(f"{config.name}.{name}")
            if not handler:
                # Try dynamic import
                tool_config = next((t for t in config.tools if t.name == name), None)
                if tool_config:
                    handler = self._load_handler(tool_config.handler)
                    self._tool_handlers[f"{config.name}.{name}"] = handler

            if handler:
                result = await handler(arguments)
                return [TextContent(type="text", text=str(result))]
            else:
                return [TextContent(type="text", text=f"Error: tool '{name}' handler not found")]

        self._servers[config.name] = server
        logger.info("mcp_server_created", name=config.name, tools=len(config.tools))
        return server

    def _load_handler(self, handler_path: str) -> Callable:
        """Dynamically load a tool handler from a dotted path."""
        module_path, func_name = handler_path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_path)
            return getattr(module, func_name)
        except (ImportError, AttributeError) as e:
            logger.warning("handler_load_failed", path=handler_path, error=str(e))
            # Return a stub handler
            async def stub(args: dict) -> str:
                return f"Stub handler for {handler_path}: received {args}"
            return stub

    async def get_server(self, name: str) -> Server | None:
        return self._servers.get(name)

    async def list_servers(self) -> list[str]:
        return list(self._servers.keys())

    async def shutdown(self):
        """Gracefully shut down all MCP servers."""
        for name, server in self._servers.items():
            logger.info("mcp_server_shutdown", name=name)
        self._servers.clear()


# Singleton
mcp_manager = MCPServerManager()
