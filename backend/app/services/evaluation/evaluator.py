"""
Evaluation Service using Azure AI Evaluation SDK.

Provides built-in and custom evaluation metrics:
- Groundedness: Is the response grounded in the provided context?
- Relevance: Is the response relevant to the user's query?
- Coherence: Is the response logically coherent?
- Fluency: Is the response fluent and natural?
- Custom: User-defined eval prompts scored by LLM

Runs evaluations per-turn, per-session, or on-demand.
"""
import uuid
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.models.agent import EvalConfig, EvalMetric


class EvaluationService:
    """Azure AI Evaluation SDK integration."""

    def __init__(self):
        self._pipelines: dict[str, dict] = {}

    async def create_pipeline(self, graph_id: str, eval_config: EvalConfig) -> str:
        """
        Create an evaluation pipeline for an agent graph.

        Uses azure-ai-evaluation SDK to set up:
        - Built-in evaluators (groundedness, relevance, coherence, fluency)
        - Custom evaluators from user-defined prompt templates
        - Evaluation schedule (per_turn, per_session, on_demand)
        """
        pipeline_id = f"eval-{uuid.uuid4().hex[:12]}"

        evaluator_config = {}

        # Map built-in metrics to Azure AI Evaluation evaluators
        metric_map = {
            EvalMetric.GROUNDEDNESS: "azure_ai_groundedness",
            EvalMetric.RELEVANCE: "azure_ai_relevance",
            EvalMetric.COHERENCE: "azure_ai_coherence",
            EvalMetric.FLUENCY: "azure_ai_fluency",
            EvalMetric.SIMILARITY: "azure_ai_similarity",
        }

        for metric in eval_config.metrics:
            if metric in metric_map:
                evaluator_config[metric.value] = {
                    "type": "builtin",
                    "evaluator": metric_map[metric],
                    "model": settings.azure_openai_deployment,
                }

        # Add custom evaluators
        for custom in eval_config.custom_evaluators:
            evaluator_config[custom.name] = {
                "type": "custom",
                "prompt_template": custom.prompt_template,
                "scoring": custom.scoring,
                "model": settings.azure_openai_deployment,
            }

        self._pipelines[pipeline_id] = {
            "graph_id": graph_id,
            "evaluators": evaluator_config,
            "frequency": eval_config.eval_frequency,
            "threshold": eval_config.threshold,
        }

        logger.info(
            "eval_pipeline_created",
            pipeline_id=pipeline_id,
            metrics=len(evaluator_config),
            frequency=eval_config.eval_frequency,
        )

        return pipeline_id

    async def run_evaluation(
        self,
        pipeline_id: str,
        query: str,
        response: str,
        context: Optional[str] = None,
    ) -> dict[str, float]:
        """
        Run evaluation on a single query-response pair.

        In production, this calls:
            from azure.ai.evaluation import evaluate
            result = evaluate(
                data={"query": query, "response": response, "context": context},
                evaluators=self._get_evaluators(pipeline_id),
                azure_ai_project=settings.azure_ai_foundry_project_connection_string,
            )

        Returns dict of metric_name -> score (0.0 - 1.0)
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {}

        # In production: call Azure AI Evaluation SDK
        # For now, return pipeline config for verification
        logger.info("eval_run", pipeline_id=pipeline_id, query=query[:100])

        return {
            metric: 0.0  # Placeholder — real scores come from Azure AI Evaluation
            for metric in pipeline["evaluators"]
        }

    async def get_pipeline(self, pipeline_id: str) -> Optional[dict]:
        return self._pipelines.get(pipeline_id)


# Singleton
eval_service = EvaluationService()
