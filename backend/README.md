# Agents Platform — Backend

Generate and deploy production-ready multi-agent systems to Azure AI Foundry from a single prompt.

## Architecture

```
User Prompt
    │
    ▼
┌─────────────────────────────────┐
│      Agent Generator            │  ← Azure OpenAI decomposes prompt
│  (prompt → agent architecture)  │     into multi-agent graph
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│    Deployment Pipeline          │
│                                 │
│  ┌───────────┐ ┌─────────────┐ │
│  │ MCP Server│ │ A2A Protocol│ │  ← Tools via MCP, inter-agent via A2A
│  │  Manager  │ │  Directory  │ │
│  └───────────┘ └─────────────┘ │
│                                 │
│  ┌───────────┐ ┌─────────────┐ │
│  │ Cosmos DB │ │ Content     │ │  ← Memory + Safety guardrails
│  │  Memory   │ │ Safety      │ │
│  └───────────┘ └─────────────┘ │
│                                 │
│  ┌───────────┐                  │
│  │ Eval      │                  │  ← Groundedness, relevance, coherence
│  │ Framework │                  │
│  └───────────┘                  │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│    Azure AI Foundry             │
│    (Agent Service)              │  ← Production deployment
│                                 │
│  Agent endpoints + Eval dash    │
└─────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Runtime** | Python 3.12 + FastAPI |
| **Agent Service** | Azure AI Foundry Agent Service (`azure-ai-projects`) |
| **LLM** | Azure OpenAI GPT-4o |
| **Memory** | Azure Cosmos DB |
| **Evaluation** | Azure AI Evaluation SDK |
| **Safety** | Azure AI Content Safety |
| **Tool Protocol** | MCP (Model Context Protocol) |
| **Agent Protocol** | A2A (Agent-to-Agent) |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/agents/generate` | Generate agent architecture from prompt |
| `POST` | `/api/agents/deploy` | Deploy to Azure AI Foundry |
| `GET` | `/api/agents/deployments` | List deployments |
| `GET` | `/api/agents/deployments/{id}` | Get deployment status |
| `GET` | `/a2a/directory` | A2A agent discovery |
| `GET` | `/a2a/{id}/agent.json` | Get agent's A2A card |
| `POST` | `/a2a/{id}/tasks` | Send A2A task |
| `GET` | `/mcp/servers` | List MCP servers |
| `GET` | `/health` | Health check |

## Quick Start

```bash
# Clone and enter backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your Azure credentials

# Run
uvicorn app.main:app --reload

# Visit docs
open http://localhost:8000/docs
```

## Configuration

All config is via environment variables. See `.env.example` for the full list.

**Required for generation:**
- `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_API_KEY`

**Required for deployment:**
- `AZURE_AI_FOUNDRY_PROJECT_CONNECTION_STRING`
- `COSMOS_DB_ENDPOINT` + `COSMOS_DB_KEY`
- `AZURE_CONTENT_SAFETY_ENDPOINT` + `AZURE_CONTENT_SAFETY_KEY`

## Agent Design System

Every generated agent system includes:

1. **Orchestration** — One orchestrator agent coordinates worker agents
2. **MCP Tools** — All tool integrations via Model Context Protocol servers
3. **A2A Communication** — Agents expose skills via Agent-to-Agent protocol
4. **Memory** — Cosmos DB-backed conversation, semantic, and episodic memory
5. **Evaluation** — Built-in metrics (groundedness, relevance, coherence) + custom evals
6. **Guardrails** — Content safety, PII detection, jailbreak protection

## Testing

```bash
pytest tests/ -v
```
