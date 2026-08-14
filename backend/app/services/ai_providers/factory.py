"""
GM-012D.4 — OpenAI Provider Implementation

OpenAI provider implementation for the AI Provider abstraction layer.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import httpx

from app.services.ai_providers import (
    AIProvider,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
    ProviderStatusResponse,
    ProviderStatus,
    ProviderType,
    AIModel,
    ProviderStatus,
    ProviderRequest,
    ProviderResponse,
)

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """
    OpenAI provider implementation.
    
    Handles communication with OpenAI API (including Azure OpenAI).
    Supports GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo models.
    """
    
    def __init__(self, config: "ProviderConfig"):
        from app.services.ai_providers import ProviderConfig, ProviderStatus, ProviderType
        from app.services.ai_providers import AIProvider, ProviderStatus

        # Lazy import: the OpenAI SDK is required only when the OpenAI provider
        # is actually instantiated. App import must not require the SDK when the
        # default provider is MockProvider.
        from openai import AsyncOpenAI

        self.config = config
        self._status = ProviderStatus.HEALTHY
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: Optional[datetime] = None
        self._request_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.api_base,
            organization=config.organization,
            default_headers=config.extra_headers or {},
            timeout=config.timeout_seconds,
            max_retries=0,  # We handle retries ourselves
        )
        
        # Cost tracking
        self._request_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        
        # Circuit breaker state
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: Optional[datetime] = None
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.api_base,
            organization=config.organization,
            default_headers=config.extra_headers or {},
            timeout=config.timeout_seconds,
            max_retries=0,  # We handle retries ourselves
        )
        
        # Cost per 1k tokens (approximate, update as needed)
        self._cost_per_1k = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        }

    def _get_cost_per_1k(self, model: str) -> Dict[str, float]:
        """Get cost per 1k tokens for a model"""
        model_key = model.lower().replace("gpt-", "gpt-").replace("-", "-")
        if model in self._cost_per_1k:
            return self._cost_per_1k[model]
        # Default to gpt-4o-mini pricing
        return self._cost_per_1k.get("gpt-4o-mini", {"input": 0.00015, "output": 0.0006})

    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        """Generate a response from OpenAI"""
        from app.services.ai_providers import ProviderRequest, ProviderResponse, ProviderStatus
        import asyncio
        
        start_time = datetime.utcnow()
        
        if not self._check_circuit_breaker():
            raise Exception("Circuit breaker open - provider unavailable")
        
        # Validate prompt package
        if not await self.validate_prompt_package(request.prompt_package):
            raise ValueError("Invalid prompt package")
        
        # Prepare messages
        system_prompt = request.prompt_package.get("system_prompt", "")
        user_prompt = request.prompt_package.get("user_prompt", "")
        
        messages = [
            {"role": "system", "content": request.prompt_package.get("system_prompt", "")},
            {"role": "user", "content": request.prompt_package.get("user_prompt", "")},
        ]
        
        # Model selection
        model = request.model or self.config.default_model.value
        
        # Prepare request parameters
        params = {
            "model": model,
            "messages": messages,
            "temperature": request.temperature if request.temperature is not None else self.config.temperature,
            "max_tokens": request.max_tokens or self.config.max_tokens,
            "top_p": request.top_p if request.top_p is not None else self.config.top_p,
            "frequency_penalty": request.frequency_penalty if request.frequency_penalty is not None else self.config.frequency_penalty,
            "presence_penalty": request.presence_penalty if request.presence_penalty is not None else self.config.presence_penalty,
        }
        
        if request.stop:
            params["stop"] = request.stop
        
        # Execute with retry logic
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            if not self._check_circuit_breaker():
                raise Exception("Circuit breaker open - provider unavailable")
            
            try:
                # Make API call
                start_time = datetime.utcnow()
                
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=params["temperature"],
                    max_tokens=params.get("max_tokens"),
                    top_p=params.get("top_p"),
                    frequency_penalty=params.get("frequency_penalty"),
                    presence_penalty=params.get("presence_penalty"),
                    stop=params.get("stop"),
                )
                
                # Calculate processing time
                processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                
                # Extract response data
                content = response.choices[0].message.content if response.choices else ""
                usage = response.usage
                
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                total_tokens = usage.total_tokens if usage else 0
                
                # Calculate cost
                cost_per_1k = self._get_cost_per_1k(model)
                prompt_cost = (prompt_tokens / 1000) * cost_per_1k.get("input", 0)
                completion_cost = (completion_tokens / 1000) * cost_per_1k.get("output", 0)
                total_cost = prompt_cost + completion_cost
                
                # Update stats
                self._request_count += 1
                self._total_tokens += total_tokens
                self._total_cost += (prompt_cost + completion_cost)
                self._circuit_breaker_failures = 0
                self._status = ProviderStatus.HEALTHY
                
                # Build response
                citations = []
                if hasattr(response.choices[0].message, "citations"):
                    citations = response.choices[0].message.citations or []
                
                response_obj = ProviderResponse(
                    content=response.choices[0].message.content or "",
                    model=model,
                    provider="openai",
                    usage={
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    finish_reason=response.choices[0].finish_reason if response.choices else None,
                    citations=citations,
                    confidence=None,
                    deterministic_trace=None,
                    processing_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                    request_id=str(uuid4()),
                    timestamp=datetime.utcnow(),
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    logprobs=None,
                )
                
                self._record_success(response_obj)
                return response_obj
                
            except Exception as e:
                last_exception = e
                self._record_failure(e)
                
                if attempt < self.config.max_retries:
                    delay = self._calculate_backoff(attempt)
                    await asyncio.sleep(delay)
                else:
                    break
        
        raise Exception(f"All retries exhausted. Last error: {last_exception}") from last_exception

    async def health_check(self) -> "ProviderStatusResponse":
        """Perform a health check on the provider"""
        from app.services.ai_providers import ProviderStatusResponse, ProviderStatus
        
        try:
            # Simple API call to check health
            response = await self.client.models.list()
            if response.data:
                return ProviderStatusResponse(
                    provider="openai",
                    status=ProviderStatus.HEALTHY,
                    latency_ms=0,
                    last_check=datetime.utcnow(),
                    error_message=None,
                    model=self.config.default_model.value,
                    version="1.0"
                )
        except Exception as e:
            return ProviderStatusResponse(
                provider="openai",
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0,
                last_check=datetime.utcnow(),
                error_message=str(e),
                model=None,
                version=None
            )
    
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        """Validate that a PromptPackage is well-formed"""
        required_keys = ["system_prompt", "user_prompt"]
        for key in required_keys:
            if key not in prompt_package:
                return False
            if not prompt_package[key] or not isinstance(prompt_package[key], str):
                return False
        return True
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker allows requests"""
        if self._status == "unavailable":
            # Check if circuit breaker timeout has passed
            if self._circuit_breaker_last_failure:
                elapsed = (datetime.utcnow() - self._circuit_breaker_last_failure).total_seconds()
                if elapsed >= self.config.circuit_breaker_timeout_seconds:
                    self._status = "healthy"
                    self._circuit_breaker_failures = 0
                    return True
            return False
        return True
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay"""
        delay = min(
            self.config.retry_base_delay_seconds * (self.config.retry_exponential_base ** attempt),
            self.config.retry_max_delay_seconds
        )
        return delay
    
    def _get_cost_per_1k(self, model: str) -> Dict[str, float]:
        """Get cost per 1k tokens for a model"""
        model_key = model.lower().replace("gpt-", "gpt-").replace("-", "-")
        if model in self._cost_per_1k:
            return self._cost_per_1k[model]
        # Default to gpt-4o-mini pricing
        return self._cost_per_1k.get("gpt-4o-mini", {"input": 0.00015, "output": 0.0006})
    
    def _calculate_cost(self, response: "ProviderResponse") -> float:
        """Calculate cost based on token usage"""
        input_cost = (response.prompt_tokens / 1000) * self._get_cost_per_1k(response.model).get("input", 0)
        output_cost = (response.completion_tokens / 1000) * self._get_cost_per_1k(response.model).get("output", 0)
        return input_cost + output_cost
    
    def _record_success(self, response: "ProviderResponse") -> None:
        self._request_count += 1
        self._total_tokens += response.total_tokens
        self._total_cost += self._calculate_cost(response)
        self._circuit_breaker_failures = 0
        self._status = "healthy"
    
    def _record_failure(self, e: Exception) -> None:
        self._circuit_breaker_failures += 1
        if self._circuit_breaker_failures >= self.config.circuit_breaker_threshold:
            self._status = "unavailable"
            self._circuit_breaker_last_failure = datetime.utcnow()
        elif self._circuit_breaker_failures >= self.config.circuit_breaker_threshold // 2:
            self._status = "degraded"
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "provider": "openai",
            "status": self._status,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "circuit_breaker_failures": self._circuit_breaker_failures,
            "status": self._status
        }
    
    def get_config(self):
        return self.config


class AzureOpenAIProvider:
    """
    Azure OpenAI provider implementation.
    
    Extends OpenAIProvider with Azure-specific configuration.
    """
    
    def __init__(self, config: "ProviderConfig"):
        # Azure OpenAI uses the same client but with different base URL and auth
        pass
    
    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        # Similar to OpenAIProvider but with Azure-specific config
        pass
    
    async def health_check(self) -> "ProviderStatusResponse":
        pass
    
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        pass


class MockProvider:
    """
    Mock provider for testing without external API calls.
    """
    
    def __init__(self, config: "ProviderConfig"):
        self.config = config
        self._status = "healthy"
        self._request_count = 0
    
    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        """Generate a mock response for testing"""
        from app.services.ai_providers import ProviderResponse
        from datetime import datetime
        from uuid import uuid4
        import json
        
        question = request.prompt_package.get("user_prompt", "")
        
        # Generate deterministic mock response based on question
        if "marriage" in question.lower():
            explanation = "Marriage probability is 61/100 (MODERATE). Natal promise: 45/100. Current transit activation: 78/100. Dasha strength: 65/100."
        elif "career" in question.lower():
            explanation = "Career probability is 72/100 (GOOD). Natal promise: 55/100. Current transit activation: 68/100."
        else:
            explanation = "General probability: 55/100 (MODERATE). Based on natal promise and current transits."
        
        # Return structured JSON response that passes validation
        mock_response = {
            "explanation": explanation,
            "citations": [
                {"type": "engine_output", "path": "master_probability.final_score", "value": "61", "evidence_level": "L4"},
                {"type": "engine_output", "path": "master_probability.breakdown.natal_promise", "value": "45", "evidence_level": "L4"},
                {"type": "engine_output", "path": "master_probability.breakdown.transit", "value": "78", "evidence_level": "L4"},
            ],
            "confidence": "HIGH",
            "deterministic_trace": "master_probability.final_score"
        }
        
        content = json.dumps(mock_response)
        
        return ProviderResponse(
            content=content,
            model="mock-model",
            provider="mock",
            usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            finish_reason="stop",
            citations=[],
            confidence="HIGH",
            deterministic_trace="mock_trace",
            processing_time_ms=10,
            request_id=str(uuid4()),
            timestamp=datetime.utcnow(),
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            logprobs=None,
        )
    
    async def health_check(self):
        from app.services.ai_providers import ProviderStatusResponse, ProviderStatus
        return ProviderStatusResponse(
            provider="mock",
            status=ProviderStatus.HEALTHY,
            latency_ms=1,
            last_check=datetime.utcnow(),
            error_message=None,
            model="mock-model",
            version="1.0"
        )
    
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        return "system_prompt" in prompt_package and "user_prompt" in prompt_package


class ProviderFactory:
    """
    Factory for creating AI providers.
    
    Supports dependency injection and easy provider switching.
    """
    
    def __init__(self):
        self._providers: Dict[str, Any] = {}
        self._default_provider: Optional[str] = None
    
    def register_provider(
        self,
        name: str,
        config: "ProviderConfig",
        is_default: bool = False
    ) -> None:
        """Register a provider with the factory"""
        from app.services.ai_providers import ProviderType, ProviderConfig
        
        if config.provider_type == "openai":
            provider = OpenAIProvider(config)
        elif config.provider_type == ProviderType.ANTHROPIC:
            provider = AnthropicProvider(config)
        elif config.provider_type == ProviderType.AZURE_OPENAI:
            provider = AzureOpenAIProvider(config)
        elif config.provider_type == ProviderType.LOCAL:
            provider = LocalProvider(config)
        elif config.provider_type == ProviderType.MOCK:
            provider = MockProvider(config)
        else:
            raise ValueError(f"Unknown provider type: {config.provider_type}")
        
        self._providers[name] = provider
        
        if is_default or self._default_provider is None:
            self._default_provider = name
    
    def get_provider(self, name: Optional[str] = None) -> Any:
        """Get a provider by name, or the default provider"""
        name = name or self._default_provider
        if not name:
            raise ValueError("No provider specified and no default provider set")
        if name not in self._providers:
            raise ValueError(f"Provider '{name}' not found")
        return self._providers[name]
    
    def get_all_providers(self) -> Dict[str, Any]:
        """Get all registered providers"""
        return self._providers.copy()
    
    def set_default(self, name: str) -> None:
        """Set the default provider"""
        if name not in self._providers:
            raise ValueError(f"Provider '{name}' not registered")
        self._default_provider = name
    
    def remove_provider(self, name: str) -> bool:
        """Remove a provider"""
        if name in self._providers:
            del self._providers[name]
            if self._default_provider == name:
                self._default_provider = None
            return True
        return False
    
    def list_providers(self) -> List[str]:
        """List all registered provider names"""
        return list(self._providers.keys())


# Global factory instance
_provider_factory = None


def get_provider_factory() -> ProviderFactory:
    """Get the global provider factory instance"""
    global _provider_factory
    if _provider_factory is None:
        _provider_factory = ProviderFactory()
    return _provider_factory


def initialize_provider_factory(configs: Dict[str, Dict[str, Any]]) -> ProviderFactory:
    """Initialize the provider factory with configurations"""
    global _provider_factory
    factory = ProviderFactory()
    
    for name, config_dict in configs.items():
        # Create ProviderConfig from dict
        from app.services.ai_providers import ProviderConfig, ProviderType, AIModel
        
        # Convert dict to ProviderConfig
        config = ProviderConfig(
            provider_type=ProviderType(config_dict.get("provider_type", "openai")),
            api_key=config_dict.get("api_key"),
            api_base=config_dict.get("api_base"),
            organization=config_dict.get("organization"),
            api_version=config_dict.get("api_version"),
            default_model=AIModel(config_dict.get("default_model", "gpt-4o-mini")),
            fallback_models=[AIModel(m) for m in config_dict.get("fallback_models", [])],
            max_retries=config_dict.get("max_retries", 3),
            timeout_seconds=config_dict.get("timeout_seconds", 60),
            max_tokens=config_dict.get("max_tokens", 4000),
            temperature=config_dict.get("temperature", 0.0),
            top_p=config_dict.get("top_p", 1.0),
            frequency_penalty=config_dict.get("frequency_penalty", 0.0),
            presence_penalty=config_dict.get("presence_penalty", 0.0),
            rate_limit_rpm=config_dict.get("rate_limit_rpm", 60),
            extra_headers=config_dict.get("extra_headers", {}),
            extra_params=config_dict.get("extra_params", {}),
        )
        
        factory.register_provider(name, ProviderConfig(**config_dict), is_default=(factory._default_provider is None))
    
    _provider_factory = factory
    return factory


def get_provider_factory() -> ProviderFactory:
    """Get the global provider factory instance"""
    global _provider_factory
    if _provider_factory is None:
        _provider_factory = ProviderFactory()
    return _provider_factory


_provider_factory: Optional[ProviderFactory] = None


__all__ = [
    "ProviderFactory",
    "get_provider_factory",
    "initialize_provider_factory",
    "ProviderType",
    "ProviderStatus",
    "AIModel",
    "ProviderStatusResponse",
    "ProviderRequest",
    "ProviderResponse",
    "ProviderConfig",
    "AIProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "AzureOpenAIProvider",
    "LocalProvider",
    "MockProvider",
    "ProviderFactory",
    "get_provider_factory",
    "initialize_provider_factory",
]