"""
MCP (Model Context Protocol) API routes.

Exposes MCP server information for tool discovery:
GET  /mcp/servers              — List all MCP servers
GET  /mcp/{agent_id}/servers   — List MCP servers for a specific agent
"""
from fastapi import APIRouter

from app.services.mcp.server import mcp_manager

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.get("/servers")
async def list_mcp_servers():
    """List all registered MCP servers."""
    servers = await mcp_manager.list_servers()
    return {"servers": servers}
