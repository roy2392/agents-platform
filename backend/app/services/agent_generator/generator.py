"""
Agent Generator — the core engine that turns natural language prompts
into production-ready multi-agent architectures.

Uses Azure OpenAI to decompose a user's task description into:
1. An agent graph (orchestrator + worker agents)
2. Tool bindings (MCP servers, APIs, built-in tools)
3. Memory configuration (Cosmos DB-backed)
4. Evaluation framework (groundedness, relevance, coherence + custom)
5. Guardrails (content safety, PII, jailbreak protection)
6. A2A agent cards for inter-agent communication
"""
import json
import uuid
from typing import Optional

from openai import AsyncAzureOpenAI

from app.core.config import settings
from app.core.logging import logger
from app.models.agent import (
    AgentGraph, AgentNode, AgentRole, ToolBinding, MemoryConfig, MemoryType,
    EvalConfig, EvalMetric, GuardrailConfig, MCPServerConfig, MCPTool,
    A2AAgentCard, A2ASkill, GenerateRequest, GenerateResponse,
    GeneratePreferences, CustomEvaluator,
)

SYSTEM_PROMPT = """You are an expert AI agent architect. Given a user's description of what they want
agents to do, you design a complete multi-agent system architecture.

You MUST output valid JSON matching this schema:
{
  "name": "system name",
  "description": "what the system does",
  "agents": [
    {
      "id": "unique-id",
      "name": "Agent Name",
      "role": "orchestrator|worker|evaluator|router|guardrail",
      "system_prompt": "detailed system prompt for this agent",
      "tools": [
        {"name": "tool_name", "type": "mcp|builtin|api", "description": "what it does"}
      ],
      "memory": {"type": "conversation|semantic|episodic", "semantic_search": true|false},
      "mcp_servers": [
        {"name": "server_name", "description": "what tools it provides",
         "tools": [{"name": "tool", "description": "desc", "input_schema": {}}]}
      ],
      "a2a_skills": [
        {"name": "skill_name", "description": "what this agent can do for other agents"}
      ],
      "downstream_agents": ["ids of agents this one delegates to"]
    }
  ],
  "entrypoint": "id of the orchestrator agent",
  "eval_metrics": ["groundedness", "relevance", "coherence"],
  "custom_evaluators": [
    {"name": "metric_name", "prompt_template": "evaluate {response} given {context}", "scoring": "1-5"}
  ]
}

Design principles:
1. SINGLE RESPONSIBILITY — each agent has one clear job
2. ORCHESTRATOR PATTERN — one agent coordinates, workers execute
3. TOOL-FIRST — prefer MCP tools over hard-coded logic
4. MEMORY BY DEFAULT — conversation memory minimum, semantic for knowledge-heavy agents
5. EVAL BUILT-IN — every system gets groundedness + relevance + coherence, add domain-specific evals
6. GUARDRAILS ALWAYS — content safety and PII detection on all agents
7. A2A READY — each agent exposes skills for inter-agent communication
8. MINIMAL AGENTS — use the fewest agents needed, don't over-decompose

Be specific with system prompts. Be practical with tool choices. Use real Azure service names."""


class AgentGenerator:
    """Generates multi-agent architectures from natural language prompts."""

    def __init__(self):
        self.client: Optional[AsyncAzureOpenAI] = None

    async def _get_client(self) -> AsyncAzureOpenAI:
        if self.client is None:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
            )
        return self.client

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate a complete agent architecture from a user prompt."""
        logger.info("generating_agent_architecture", prompt=request.prompt[:100])

        prefs = request.preferences or GeneratePreferences()
        client = await self._get_client()

        # Call Azure OpenAI to generate architecture
        response = await client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": self._build_user_prompt(request.prompt, prefs)},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=4000,
        )

        raw = json.loads(response.choices[0].message.content)
        graph = self._parse_architecture(raw, prefs)

        logger.info(
            "architecture_generated",
            agents=len(graph.agents),
            tools=sum(len(a.tools) for a in graph.agents),
            mcp_servers=sum(len(a.mcp_servers) for a in graph.agents),
        )

        return GenerateResponse(
            graph=graph,
            estimated_cost_per_1k_calls=self._estimate_cost(graph),
            deployment_ready=True,
        )

    def _build_user_prompt(self, prompt: str, prefs: GeneratePreferences) -> str:
        constraints = []
        if prefs.enable_mcp:
            constraints.append("- Use MCP (Model Context Protocol) servers for ALL tool integrations")
        if prefs.enable_a2a:
            constraints.append("- Define A2A (Agent-to-Agent) skills for each agent")
        constraints.append(f"- Use {prefs.model} as the base model")
        constraints.append(f"- Maximum {prefs.max_agents} agents")
        constraints.append(f"- Memory provider: {prefs.memory_provider}")

        return f"""Design an agent system for the following task:

{prompt}

Constraints:
{chr(10).join(constraints)}

Generate the complete architecture as JSON."""

    def _parse_architecture(self, raw: dict, prefs: GeneratePreferences) -> AgentGraph:
        """Parse LLM output into typed AgentGraph."""
        graph_id = f"ag-{uuid.uuid4().hex[:12]}"
        agents = []

        for agent_raw in raw.get("agents", []):
            agent_id = agent_raw.get("id", f"agent-{uuid.uuid4().hex[:8]}")

            # Parse tools
            tools = [
                ToolBinding(
                    name=t["name"],
                    type=t.get("type", "mcp"),
                    description=t.get("description", ""),
                )
                for t in agent_raw.get("tools", [])
            ]

            # Parse MCP servers
            mcp_servers = [
                MCPServerConfig(
                    name=s["name"],
                    description=s.get("description", ""),
                    tools=[
                        MCPTool(
                            name=t["name"],
                            description=t.get("description", ""),
                            input_schema=t.get("input_schema", {}),
                            handler=f"app.tools.{s['name']}.{t['name']}",
                        )
                        for t in s.get("tools", [])
                    ],
                )
                for s in agent_raw.get("mcp_servers", [])
            ]

            # Parse A2A card
            a2a_skills = agent_raw.get("a2a_skills", [])
            a2a_card = None
            if prefs.enable_a2a and a2a_skills:
                a2a_card = A2AAgentCard(
                    name=agent_raw.get("name", agent_id),
                    description=agent_raw.get("system_prompt", "")[:200],
                    url=f"/a2a/{agent_id}",
                    skills=[
                        A2ASkill(
                            id=f"{agent_id}-{s['name']}",
                            name=s["name"],
                            description=s.get("description", ""),
                        )
                        for s in a2a_skills
                    ],
                )

            # Memory config
            memory_raw = agent_raw.get("memory", {})
            memory = MemoryConfig(
                type=MemoryType(memory_raw.get("type", "conversation")),
                provider=prefs.memory_provider,
                semantic_search=memory_raw.get("semantic_search", False),
            )

            # Role
            role_str = agent_raw.get("role", "worker")
            try:
                role = AgentRole(role_str)
            except ValueError:
                role = AgentRole.WORKER

            agents.append(AgentNode(
                id=agent_id,
                name=agent_raw.get("name", f"Agent {agent_id}"),
                role=role,
                model=prefs.model,
                system_prompt=agent_raw.get("system_prompt", ""),
                tools=tools,
                memory=memory,
                guardrails=GuardrailConfig(),
                mcp_servers=mcp_servers,
                a2a_card=a2a_card,
                downstream_agents=agent_raw.get("downstream_agents", []),
            ))

        # Build eval config
        eval_metrics = [
            EvalMetric(m) for m in raw.get("eval_metrics", ["groundedness", "relevance", "coherence"])
            if m in [e.value for e in EvalMetric]
        ]
        custom_evaluators = [
            CustomEvaluator(
                name=e["name"],
                prompt_template=e.get("prompt_template", ""),
                scoring=e.get("scoring", "1-5"),
            )
            for e in raw.get("custom_evaluators", [])
        ]

        return AgentGraph(
            id=graph_id,
            name=raw.get("name", "Agent System"),
            description=raw.get("description", ""),
            agents=agents,
            entrypoint=raw.get("entrypoint", agents[0].id if agents else ""),
            eval=EvalConfig(metrics=eval_metrics, custom_evaluators=custom_evaluators),
            global_guardrails=GuardrailConfig(),
            global_memory=MemoryConfig(provider=prefs.memory_provider),
        )

    def _estimate_cost(self, graph: AgentGraph) -> float:
        """Rough cost estimate per 1K calls based on agent count and model."""
        base_cost = {
            "gpt-4o": 0.015,
            "gpt-4o-mini": 0.003,
            "gpt-4": 0.04,
        }
        per_agent = base_cost.get(graph.agents[0].model if graph.agents else "gpt-4o", 0.015)
        # Assume avg 3 turns per call, each agent processes ~500 tokens
        return round(per_agent * len(graph.agents) * 3 * 1000 * 0.5, 2)


# Singleton
agent_generator = AgentGenerator()
