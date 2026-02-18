"""
A2A (Agent-to-Agent) Protocol implementation.

Implements the Google A2A protocol for inter-agent communication:
- Agent Cards: public identity and capability discovery
- Task lifecycle: send/receive tasks between agents
- Streaming: real-time updates via SSE
- Push notifications: webhook-based event delivery

Each deployed agent gets an A2A endpoint that other agents can discover
and communicate with.
"""
import uuid
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.core.logging import logger
from app.models.agent import A2AAgentCard, AgentNode


class A2ATask(BaseModel):
    """A task sent from one agent to another via A2A."""
    id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:12]}")
    from_agent: str
    to_agent: str
    skill_id: str
    input_text: str
    status: str = "pending"  # pending | in_progress | completed | failed
    output_text: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    metadata: dict = Field(default_factory=dict)


class A2AMessage(BaseModel):
    """A message within an A2A task conversation."""
    role: str  # "user" | "agent"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class A2ADirectory:
    """
    Agent directory for A2A discovery.

    Maintains a registry of all deployed agents and their capabilities.
    Agents can query the directory to find other agents with specific skills.
    """

    def __init__(self):
        self._agents: dict[str, A2AAgentCard] = {}
        self._tasks: dict[str, A2ATask] = {}

    async def register_agent(self, agent_id: str, card: A2AAgentCard):
        """Register an agent in the A2A directory."""
        self._agents[agent_id] = card
        logger.info("a2a_agent_registered", agent_id=agent_id, skills=len(card.skills))

    async def unregister_agent(self, agent_id: str):
        self._agents.pop(agent_id, None)

    async def get_agent_card(self, agent_id: str) -> Optional[A2AAgentCard]:
        """Get an agent's A2A card (the /.well-known/agent.json equivalent)."""
        return self._agents.get(agent_id)

    async def discover_agents(self, skill_name: Optional[str] = None) -> list[A2AAgentCard]:
        """Discover agents, optionally filtered by skill name."""
        if not skill_name:
            return list(self._agents.values())
        return [
            card for card in self._agents.values()
            if any(s.name == skill_name for s in card.skills)
        ]

    async def send_task(self, task: A2ATask) -> A2ATask:
        """Send a task from one agent to another."""
        self._tasks[task.id] = task
        logger.info(
            "a2a_task_sent",
            task_id=task.id,
            from_agent=task.from_agent,
            to_agent=task.to_agent,
            skill=task.skill_id,
        )
        return task

    async def get_task(self, task_id: str) -> Optional[A2ATask]:
        return self._tasks.get(task_id)

    async def complete_task(self, task_id: str, output: str) -> Optional[A2ATask]:
        """Mark an A2A task as completed with output."""
        task = self._tasks.get(task_id)
        if task:
            task.status = "completed"
            task.output_text = output
            task.completed_at = datetime.now(timezone.utc).isoformat()
            logger.info("a2a_task_completed", task_id=task_id)
        return task

    async def list_tasks(self, agent_id: Optional[str] = None) -> list[A2ATask]:
        """List all tasks, optionally filtered by agent."""
        if not agent_id:
            return list(self._tasks.values())
        return [
            t for t in self._tasks.values()
            if t.from_agent == agent_id or t.to_agent == agent_id
        ]


# Singleton
a2a_directory = A2ADirectory()
