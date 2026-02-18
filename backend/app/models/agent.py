"""Agent system data models."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# --- Enums ---

class AgentRole(str, Enum):
    """Roles an agent can play in a multi-agent system."""
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    EVALUATOR = "evaluator"
    ROUTER = "router"
    GUARDRAIL = "guardrail"


class MemoryType(str, Enum):
    CONVERSATION = "conversation"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"


class EvalMetric(str, Enum):
    GROUNDEDNESS = "groundedness"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    SIMILARITY = "similarity"
    F1_SCORE = "f1_score"
    CUSTOM = "custom"


class DeploymentStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    DEPLOYING = "deploying"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"


# --- Tool & Protocol Models ---

class MCPServerConfig(BaseModel):
    """MCP (Model Context Protocol) server configuration for tool exposure."""
    name: str = Field(description="MCP server name")
    description: str = Field(description="What tools this server provides")
    transport: str = Field(default="stdio", description="Transport: stdio | sse | streamable-http")
    tools: list[MCPTool] = Field(default_factory=list)
    resources: list[MCPResource] = Field(default_factory=list)


class MCPTool(BaseModel):
    """A tool exposed via MCP."""
    name: str
    description: str
    input_schema: dict = Field(default_factory=dict)
    handler: str = Field(description="Python function path for tool implementation")


class MCPResource(BaseModel):
    """A resource exposed via MCP."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


class A2ASkill(BaseModel):
    """Agent-to-Agent (A2A) protocol skill definition."""
    id: str = Field(description="Unique skill identifier")
    name: str
    description: str
    input_modes: list[str] = Field(default=["text"])
    output_modes: list[str] = Field(default=["text"])


class A2AAgentCard(BaseModel):
    """A2A Agent Card — the public identity of an agent in the A2A network."""
    name: str
    description: str
    url: str = Field(description="Agent's A2A endpoint URL")
    skills: list[A2ASkill] = Field(default_factory=list)
    version: str = "1.0.0"
    protocol_version: str = "0.2"


# --- Agent Architecture Models ---

class ToolBinding(BaseModel):
    """A tool available to an agent — either MCP-based or built-in."""
    name: str
    type: str = Field(description="mcp | azure_function | builtin | api")
    description: str
    mcp_server: Optional[str] = Field(default=None, description="MCP server name if type is mcp")
    endpoint: Optional[str] = Field(default=None, description="API endpoint if type is api or azure_function")
    config: dict = Field(default_factory=dict)


class MemoryConfig(BaseModel):
    """Memory layer configuration for an agent."""
    type: MemoryType = MemoryType.CONVERSATION
    provider: str = Field(default="cosmos_db", description="cosmos_db | redis | in_memory")
    ttl_hours: Optional[int] = Field(default=None, description="Memory TTL in hours, None = permanent")
    max_entries: int = Field(default=1000)
    semantic_search: bool = Field(default=False, description="Enable semantic search over memory")
    embedding_model: str = Field(default="text-embedding-3-large")


class EvalConfig(BaseModel):
    """Evaluation framework configuration."""
    metrics: list[EvalMetric] = Field(
        default=[EvalMetric.GROUNDEDNESS, EvalMetric.RELEVANCE, EvalMetric.COHERENCE]
    )
    custom_evaluators: list[CustomEvaluator] = Field(default_factory=list)
    eval_frequency: str = Field(default="per_session", description="per_turn | per_session | on_demand")
    threshold: float = Field(default=0.7, description="Minimum passing score")


class CustomEvaluator(BaseModel):
    """Custom evaluation metric definition."""
    name: str
    prompt_template: str = Field(description="Evaluation prompt template with {response} and {context} placeholders")
    scoring: str = Field(default="1-5", description="Scoring scale")


class GuardrailConfig(BaseModel):
    """Content safety and guardrail configuration."""
    content_safety: bool = Field(default=True, description="Enable Azure Content Safety")
    pii_detection: bool = Field(default=True)
    jailbreak_protection: bool = Field(default=True)
    custom_blocklist: list[str] = Field(default_factory=list)
    max_output_tokens: int = Field(default=4096)
    allowed_topics: list[str] = Field(default_factory=list, description="Empty = all topics allowed")
    blocked_topics: list[str] = Field(default_factory=list)


class AgentNode(BaseModel):
    """A single agent node in the multi-agent graph."""
    id: str
    name: str
    role: AgentRole
    model: str = Field(default="gpt-4o")
    system_prompt: str
    tools: list[ToolBinding] = Field(default_factory=list)
    memory: Optional[MemoryConfig] = None
    guardrails: Optional[GuardrailConfig] = None
    mcp_servers: list[MCPServerConfig] = Field(default_factory=list)
    a2a_card: Optional[A2AAgentCard] = None
    downstream_agents: list[str] = Field(
        default_factory=list, description="IDs of agents this node can delegate to"
    )


class AgentGraph(BaseModel):
    """The complete multi-agent system architecture."""
    id: str
    name: str
    description: str
    agents: list[AgentNode]
    entrypoint: str = Field(description="ID of the orchestrator/entry agent")
    eval: EvalConfig = Field(default_factory=EvalConfig)
    global_guardrails: GuardrailConfig = Field(default_factory=GuardrailConfig)
    global_memory: MemoryConfig = Field(default_factory=MemoryConfig)


# --- API Request/Response Models ---

class GenerateRequest(BaseModel):
    """User's request to generate an agent system."""
    prompt: str = Field(
        description="Natural language description of the agent system to build",
        min_length=10,
        max_length=5000,
    )
    preferences: Optional[GeneratePreferences] = None


class GeneratePreferences(BaseModel):
    """Optional preferences for agent generation."""
    model: str = Field(default="gpt-4o")
    memory_provider: str = Field(default="cosmos_db")
    eval_metrics: list[EvalMetric] = Field(
        default=[EvalMetric.GROUNDEDNESS, EvalMetric.RELEVANCE, EvalMetric.COHERENCE]
    )
    enable_a2a: bool = Field(default=True, description="Enable A2A protocol for inter-agent communication")
    enable_mcp: bool = Field(default=True, description="Enable MCP for tool integration")
    max_agents: int = Field(default=10, ge=1, le=50)


class GenerateResponse(BaseModel):
    """Response from agent generation — the proposed architecture."""
    graph: AgentGraph
    estimated_cost_per_1k_calls: float
    deployment_ready: bool = True
    warnings: list[str] = Field(default_factory=list)


class DeployRequest(BaseModel):
    """Request to deploy a generated agent graph to Azure AI Foundry."""
    graph: AgentGraph
    project_name: Optional[str] = None
    auto_scale: bool = True


class DeployResponse(BaseModel):
    """Response from deployment."""
    deployment_id: str
    status: DeploymentStatus
    endpoint_url: Optional[str] = None
    eval_dashboard_url: Optional[str] = None
    a2a_directory_url: Optional[str] = None
    agents_deployed: list[DeployedAgent] = Field(default_factory=list)


class DeployedAgent(BaseModel):
    """Status of a single deployed agent."""
    agent_id: str
    name: str
    status: DeploymentStatus
    endpoint: Optional[str] = None
    mcp_server_url: Optional[str] = None
    a2a_card_url: Optional[str] = None


# Forward references
MCPServerConfig.model_rebuild()
EvalConfig.model_rebuild()
