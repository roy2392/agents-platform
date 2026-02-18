"""
Cosmos DB Memory Service.

Provides persistent memory for deployed agents:
- Conversation history (per session)
- Semantic memory (searchable knowledge base)
- Episodic memory (long-term event storage)

Each agent graph gets its own container with partitioning by agent_id.
"""
from typing import Optional
from datetime import datetime, timezone

from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey

from app.core.config import settings
from app.core.logging import logger


class CosmosMemoryService:
    """Cosmos DB-backed memory for agent systems."""

    def __init__(self):
        self._client: Optional[CosmosClient] = None
        self._database = None

    async def _get_client(self):
        if self._client is None:
            if not settings.cosmos_db_endpoint:
                logger.warning("cosmos_db_not_configured")
                return None
            self._client = CosmosClient(
                url=settings.cosmos_db_endpoint,
                credential=settings.cosmos_db_key,
            )
            self._database = self._client.get_database_client(settings.cosmos_db_database)
        return self._client

    async def ensure_container(self, graph_id: str):
        """Create or get a Cosmos DB container for an agent graph."""
        client = await self._get_client()
        if not client:
            logger.info("cosmos_skipped_no_config", graph_id=graph_id)
            return

        try:
            await self._database.create_container_if_not_exists(
                id=f"memory-{graph_id}",
                partition_key=PartitionKey(path="/agent_id"),
                default_ttl=-1,  # No expiration by default
            )
            logger.info("cosmos_container_ready", graph_id=graph_id)
        except Exception as e:
            logger.error("cosmos_container_failed", graph_id=graph_id, error=str(e))

    async def store(self, graph_id: str, agent_id: str, memory_type: str, content: dict):
        """Store a memory entry."""
        client = await self._get_client()
        if not client:
            return

        container = self._database.get_container_client(f"memory-{graph_id}")
        doc = {
            "id": f"{agent_id}-{datetime.now(timezone.utc).timestamp()}",
            "agent_id": agent_id,
            "type": memory_type,
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await container.create_item(body=doc)

    async def query(
        self, graph_id: str, agent_id: str,
        memory_type: Optional[str] = None, limit: int = 50,
    ) -> list[dict]:
        """Query memory entries for an agent."""
        client = await self._get_client()
        if not client:
            return []

        container = self._database.get_container_client(f"memory-{graph_id}")
        query = "SELECT * FROM c WHERE c.agent_id = @agent_id"
        params = [{"name": "@agent_id", "value": agent_id}]

        if memory_type:
            query += " AND c.type = @type"
            params.append({"name": "@type", "value": memory_type})

        query += " ORDER BY c.created_at DESC OFFSET 0 LIMIT @limit"
        params.append({"name": "@limit", "value": limit})

        items = []
        async for item in container.query_items(query=query, parameters=params):
            items.append(item)
        return items

    async def close(self):
        if self._client:
            await self._client.close()


# Singleton
cosmos_memory = CosmosMemoryService()
