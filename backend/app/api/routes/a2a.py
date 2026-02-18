"""
A2A (Agent-to-Agent) Protocol API routes.

Implements the A2A protocol endpoints:
GET  /a2a/directory          — Discover all registered agents
GET  /a2a/{agent_id}/agent.json — Get an agent's A2A card
POST /a2a/{agent_id}/tasks   — Send a task to an agent
GET  /a2a/{agent_id}/tasks   — List tasks for an agent
GET  /a2a/tasks/{task_id}    — Get task status
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.services.a2a.protocol import a2a_directory, A2ATask

router = APIRouter(prefix="/a2a", tags=["a2a"])


@router.get("/directory")
async def list_agents(skill: Optional[str] = None):
    """
    Discover agents in the A2A directory.
    Optionally filter by skill name.
    """
    agents = await a2a_directory.discover_agents(skill_name=skill)
    return {"agents": [a.model_dump() for a in agents]}


@router.get("/{agent_id}/agent.json")
async def get_agent_card(agent_id: str):
    """
    Get an agent's A2A card — the public identity and capabilities.
    This is the /.well-known/agent.json equivalent.
    """
    card = await a2a_directory.get_agent_card(agent_id)
    if not card:
        raise HTTPException(status_code=404, detail="Agent not found in A2A directory")
    return card.model_dump()


@router.post("/{agent_id}/tasks")
async def send_task(agent_id: str, task: A2ATask):
    """Send a task to an agent via A2A protocol."""
    card = await a2a_directory.get_agent_card(agent_id)
    if not card:
        raise HTTPException(status_code=404, detail="Target agent not found")

    task.to_agent = agent_id
    result = await a2a_directory.send_task(task)
    return result.model_dump()


@router.get("/{agent_id}/tasks")
async def list_agent_tasks(agent_id: str):
    """List all tasks for an agent."""
    tasks = await a2a_directory.list_tasks(agent_id=agent_id)
    return {"tasks": [t.model_dump() for t in tasks]}


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get status of a specific A2A task."""
    task = await a2a_directory.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.model_dump()
