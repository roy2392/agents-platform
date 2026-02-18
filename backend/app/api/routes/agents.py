"""
Agent API routes — the main product endpoints.

POST /api/agents/generate  — Turn a prompt into an agent architecture
POST /api/agents/deploy    — Deploy a generated architecture to Azure AI Foundry
GET  /api/agents/deployments — List all deployments
GET  /api/agents/deployments/{id} — Get deployment status
"""
from fastapi import APIRouter, HTTPException

from app.models.agent import (
    GenerateRequest, GenerateResponse,
    DeployRequest, DeployResponse,
)
from app.services.agent_generator.generator import agent_generator
from app.services.deployment.foundry import foundry_deployer

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/generate", response_model=GenerateResponse)
async def generate_agents(request: GenerateRequest):
    """
    Generate a multi-agent architecture from a natural language prompt.

    The prompt describes what the agent system should do. The platform:
    1. Decomposes the task into an agent graph
    2. Assigns tools via MCP servers
    3. Configures memory (Cosmos DB)
    4. Sets up evaluation metrics
    5. Defines guardrails

    Returns the complete architecture ready for deployment.
    """
    try:
        return await agent_generator.generate(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.post("/deploy", response_model=DeployResponse)
async def deploy_agents(request: DeployRequest):
    """
    Deploy a generated agent graph to Azure AI Foundry.

    Provisions:
    - Agent instances via AI Agent Service
    - Cosmos DB memory containers
    - Content Safety filters
    - MCP tool servers
    - A2A agent cards
    - Evaluation pipeline

    Returns deployment endpoints and status.
    """
    try:
        return await foundry_deployer.deploy(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")


@router.get("/deployments")
async def list_deployments():
    """List all agent deployments."""
    return await foundry_deployer.list_deployments()


@router.get("/deployments/{deployment_id}")
async def get_deployment(deployment_id: str):
    """Get status of a specific deployment."""
    deployment = await foundry_deployer.get_deployment(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment
