"""
Agents Platform Backend — FastAPI application.

The main entry point that wires together:
- Agent generation (prompt -> architecture)
- Deployment to Azure AI Foundry
- MCP tool servers
- A2A agent directory
- Evaluation pipelines
- Content safety guardrails
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.api.routes import agents, a2a, mcp, health
from app.services.mcp.server import mcp_manager
from app.services.deployment.foundry import foundry_deployer
from app.services.memory.cosmos import cosmos_memory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle — startup and shutdown."""
    logger.info("starting", env=settings.app_env)
    yield
    # Graceful shutdown
    logger.info("shutting_down")
    await mcp_manager.shutdown()
    await foundry_deployer.shutdown()
    await cosmos_memory.close()
    logger.info("shutdown_complete")


app = FastAPI(
    title="Agents Platform",
    description=(
        "Generate and deploy production-ready multi-agent systems to Azure AI Foundry. "
        "Describe what your agents should do — we handle orchestration, memory, "
        "evaluation, guardrails, MCP tool integration, and A2A communication."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router)
app.include_router(agents.router)
app.include_router(a2a.router)
app.include_router(mcp.router)


@app.get("/")
async def root():
    return {
        "name": "Agents Platform API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "generate": "POST /api/agents/generate",
            "deploy": "POST /api/agents/deploy",
            "deployments": "GET /api/agents/deployments",
            "a2a_directory": "GET /a2a/directory",
            "mcp_servers": "GET /mcp/servers",
            "health": "GET /health",
        },
    }
