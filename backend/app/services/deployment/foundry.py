"""
Azure AI Foundry Deployment Service.

Handles the actual deployment of agent graphs to Azure AI Foundry:
1. Creates AI Project if not exists
2. Provisions agent instances via Azure AI Agent Service
3. Configures tool connections
4. Sets up Cosmos DB memory containers
5. Registers Content Safety filters
6. Creates eval pipeline via Azure AI Evaluation
7. Registers A2A agent cards
8. Returns deployment endpoints

Uses the azure-ai-projects SDK for Agent Service integration.
"""
import uuid
from typing import Optional

from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    AgentThread,
    MessageRole,
)

from app.core.config import settings
from app.core.logging import logger
from app.models.agent import (
    AgentGraph, AgentNode, DeployRequest, DeployResponse,
    DeployedAgent, DeploymentStatus,
)
from app.services.mcp.server import mcp_manager
from app.services.a2a.protocol import a2a_directory
from app.services.memory.cosmos import cosmos_memory
from app.services.evaluation.evaluator import eval_service
from app.services.guardrails.safety import safety_service


class FoundryDeploymentService:
    """Deploys agent systems to Azure AI Foundry."""

    def __init__(self):
        self._client: Optional[AIProjectClient] = None
        self._deployments: dict[str, DeployResponse] = {}

    async def _get_client(self) -> AIProjectClient:
        """Get or create the Azure AI Project client."""
        if self._client is None:
            conn_str = settings.azure_ai_foundry_project_connection_string
            if not conn_str:
                raise ValueError(
                    "AZURE_AI_FOUNDRY_PROJECT_CONNECTION_STRING is required. "
                    "Get it from Azure AI Foundry > Project > Overview > Connection String"
                )
            self._client = AIProjectClient.from_connection_string(
                credential=DefaultAzureCredential(),
                conn_str=conn_str,
            )
        return self._client

    async def deploy(self, request: DeployRequest) -> DeployResponse:
        """
        Deploy an agent graph to Azure AI Foundry.

        Steps:
        1. Validate graph configuration
        2. Create memory containers in Cosmos DB
        3. Configure content safety filters
        4. Create each agent via AI Agent Service
        5. Set up MCP servers for tool access
        6. Register A2A agent cards
        7. Configure eval pipeline
        8. Return deployment endpoints
        """
        deployment_id = f"deploy-{uuid.uuid4().hex[:12]}"
        graph = request.graph

        logger.info(
            "deployment_started",
            deployment_id=deployment_id,
            graph_id=graph.id,
            agent_count=len(graph.agents),
        )

        deployed_agents: list[DeployedAgent] = []

        try:
            client = await self._get_client()

            # Step 1: Set up memory
            await cosmos_memory.ensure_container(graph.id)
            logger.info("memory_provisioned", graph_id=graph.id)

            # Step 2: Configure guardrails
            await safety_service.configure(graph.global_guardrails)
            logger.info("guardrails_configured", graph_id=graph.id)

            # Step 3: Deploy each agent
            for agent_node in graph.agents:
                deployed = await self._deploy_agent(client, graph, agent_node, deployment_id)
                deployed_agents.append(deployed)

            # Step 4: Configure eval pipeline
            eval_run_id = await eval_service.create_pipeline(
                graph_id=graph.id,
                eval_config=graph.eval,
            )
            logger.info("eval_pipeline_created", graph_id=graph.id, run_id=eval_run_id)

            # Build response
            project_name = request.project_name or graph.name.lower().replace(" ", "-")
            base_url = f"https://{project_name}.inference.ai.azure.com"

            response = DeployResponse(
                deployment_id=deployment_id,
                status=DeploymentStatus.RUNNING,
                endpoint_url=f"{base_url}/agents/{graph.entrypoint}/chat",
                eval_dashboard_url=f"https://ai.azure.com/evals/{eval_run_id}",
                a2a_directory_url=f"{base_url}/a2a/directory",
                agents_deployed=deployed_agents,
            )

            self._deployments[deployment_id] = response
            logger.info("deployment_completed", deployment_id=deployment_id)
            return response

        except Exception as e:
            logger.error("deployment_failed", deployment_id=deployment_id, error=str(e))
            return DeployResponse(
                deployment_id=deployment_id,
                status=DeploymentStatus.FAILED,
                agents_deployed=deployed_agents,
            )

    async def _deploy_agent(
        self,
        client: AIProjectClient,
        graph: AgentGraph,
        agent: AgentNode,
        deployment_id: str,
    ) -> DeployedAgent:
        """Deploy a single agent to Azure AI Foundry Agent Service."""
        try:
            # Create agent via AI Agent Service
            ai_agent = await client.agents.create_agent(
                model=agent.model,
                name=agent.name,
                instructions=agent.system_prompt,
            )

            # Set up MCP servers for this agent's tools
            mcp_url = None
            for mcp_config in agent.mcp_servers:
                server = await mcp_manager.create_server(mcp_config)
                mcp_url = f"/mcp/{agent.id}/{mcp_config.name}"

            # Register A2A card
            a2a_url = None
            if agent.a2a_card:
                await a2a_directory.register_agent(agent.id, agent.a2a_card)
                a2a_url = f"/a2a/{agent.id}/agent.json"

            logger.info(
                "agent_deployed",
                agent_id=agent.id,
                name=agent.name,
                role=agent.role,
                tools=len(agent.tools),
                mcp_servers=len(agent.mcp_servers),
            )

            return DeployedAgent(
                agent_id=agent.id,
                name=agent.name,
                status=DeploymentStatus.RUNNING,
                endpoint=f"/agents/{agent.id}/chat",
                mcp_server_url=mcp_url,
                a2a_card_url=a2a_url,
            )

        except Exception as e:
            logger.error("agent_deploy_failed", agent_id=agent.id, error=str(e))
            return DeployedAgent(
                agent_id=agent.id,
                name=agent.name,
                status=DeploymentStatus.FAILED,
            )

    async def get_deployment(self, deployment_id: str) -> Optional[DeployResponse]:
        return self._deployments.get(deployment_id)

    async def list_deployments(self) -> list[DeployResponse]:
        return list(self._deployments.values())

    async def shutdown(self):
        if self._client:
            await self._client.close()


# Singleton
foundry_deployer = FoundryDeploymentService()
