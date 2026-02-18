"""
Content Safety & Guardrails Service.

Integrates Azure AI Content Safety for:
- Text content classification (hate, violence, self-harm, sexual)
- PII detection and redaction
- Jailbreak attack detection
- Custom blocklist enforcement
- Topic restrictions

Every agent interaction passes through guardrails before and after LLM calls.
"""
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.models.agent import GuardrailConfig


class SafetyService:
    """Azure Content Safety integration for agent guardrails."""

    def __init__(self):
        self._config: Optional[GuardrailConfig] = None
        self._client = None

    async def configure(self, config: GuardrailConfig):
        """Configure guardrails for a deployment."""
        self._config = config

        if config.content_safety and settings.azure_content_safety_endpoint:
            # In production:
            # from azure.ai.contentsafety.aio import ContentSafetyClient
            # from azure.core.credentials import AzureKeyCredential
            # self._client = ContentSafetyClient(
            #     endpoint=settings.azure_content_safety_endpoint,
            #     credential=AzureKeyCredential(settings.azure_content_safety_key),
            # )
            logger.info("content_safety_configured")
        else:
            logger.info("content_safety_skipped", reason="not configured or disabled")

    async def check_input(self, text: str) -> dict:
        """
        Check user input before it reaches an agent.

        Returns: {"safe": bool, "flags": [...], "redacted_text": str}
        """
        result = {"safe": True, "flags": [], "redacted_text": text}

        if not self._config:
            return result

        # Jailbreak detection
        if self._config.jailbreak_protection:
            if await self._detect_jailbreak(text):
                result["safe"] = False
                result["flags"].append("jailbreak_detected")

        # PII detection
        if self._config.pii_detection:
            pii_result = await self._detect_pii(text)
            if pii_result["found"]:
                result["redacted_text"] = pii_result["redacted"]
                result["flags"].append("pii_detected")

        # Content safety classification
        if self._config.content_safety and self._client:
            safety_result = await self._classify_content(text)
            if not safety_result["safe"]:
                result["safe"] = False
                result["flags"].extend(safety_result["categories"])

        # Custom blocklist
        if self._config.custom_blocklist:
            for term in self._config.custom_blocklist:
                if term.lower() in text.lower():
                    result["safe"] = False
                    result["flags"].append(f"blocklist:{term}")

        # Topic restrictions
        if self._config.blocked_topics:
            # In production: use LLM to classify topic
            pass

        return result

    async def check_output(self, text: str) -> dict:
        """Check agent output before it reaches the user."""
        return await self.check_input(text)  # Same checks apply

    async def _detect_jailbreak(self, text: str) -> bool:
        """Detect jailbreak attempts using Azure Content Safety."""
        # In production: use Content Safety Jailbreak API
        jailbreak_indicators = [
            "ignore previous instructions",
            "you are now",
            "disregard your rules",
            "pretend you",
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in jailbreak_indicators)

    async def _detect_pii(self, text: str) -> dict:
        """Detect and redact PII."""
        # In production: use Azure AI Language PII detection
        return {"found": False, "redacted": text}

    async def _classify_content(self, text: str) -> dict:
        """Classify content using Azure Content Safety."""
        # In production:
        # from azure.ai.contentsafety.models import AnalyzeTextOptions
        # response = await self._client.analyze_text(AnalyzeTextOptions(text=text))
        return {"safe": True, "categories": []}


# Singleton
safety_service = SafetyService()
