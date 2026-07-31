"""
GM-012D.4 — Azure OpenAI Provider Implementation

Azure OpenAI provider implementation for the AI Provider abstraction layer.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from openai import AsyncAzureOpenAI

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


class AzureOpenAIProvider:
    """
    Azure OpenAI provider implementation.
    
    Handles communication with Azure OpenAI API.
    Supports GPT-4o, GPT-4o-mini, GPT-4, GPT-3.5-turbo models deployed on Azure.
    """
    
    def __init__(self, config: "ProviderConfig"):
        from app.services.ai_providers import ProviderConfig, ProviderStatus, ProviderType
        from app.services.ai_providers import AIProvider, ProviderStatus
        
        self.config = config
        self._status = ProviderStatus.HEALTHY
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: Optional[datetime] = None
        self._request_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        
        # Initialize Azure OpenAI client
        self.client = AsyncAzureOpenAI(
            api_key=config.api_key,
            azure_endpoint=config.api_base,
            api_version=config.api_version or "2024-02-15-preview",
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
        
        # Cost per 1k tokens (approximate, update as needed)
        self._cost_per_1k = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4": {"input": 0.03, "output": 0.06},
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
        """Generate a response from Azure OpenAI"""
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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
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
                
                processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                
                # Extract response
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
                self._total_cost += total_cost
                self._circuit_breaker_failures = 0
                self._status = ProviderStatus.HEALTHY
                
                # Build response
                response_obj = ProviderResponse(
                    content=content,
                    model=model,
                    provider="azure_openai",
                    usage={
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    finish_reason=response.choices[0].finish_reason if response.choices else None,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                    processing_time_ms=processing_time_ms,
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
            start_time = datetime.utcnow()
            
            # Simple test request
            response = await self.client.chat.completions.create(
                model=self.config.default_model.value,
                messages=[{"role": "user", "content": "Health check"}],
                max_tokens=5,
                temperature=0,
            )
            
            latency_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            return ProviderStatusResponse(
                provider="azure_openai",
                status=ProviderStatus.HEALTHY,
                latency_ms=latency_ms,
                last_check=datetime.utcnow(),
                error_message=None,
                model=self.config.default_model.value,
                version="1.0"
            )
            
        except Exception as e:
            return ProviderStatusResponse(
                provider="azure_openai",
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
        if self._status == ProviderStatus.UNAVAILABLE:
            if self._circuit_breaker_last_failure:
                elapsed = (datetime.utcnow() - self._circuit_breaker_last_failure).total_seconds()
                if elapsed >= self.config.circuit_breaker_timeout_seconds:
                    self._status = ProviderStatus.DEGRADED
                    self._circuit_breaker_failures = 0
                    return True
            return False
        return True
    
    def _calculate_backoff(self, attempt: int) -> float:
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
        self._status = ProviderStatus.HEALTHY
    
    def _record_failure(self, e: Exception) -> None:
        self._circuit_breaker_failures += 1
        if self._circuit_breaker_failures >= self.config.circuit_breaker_threshold:
            self._status = ProviderStatus.UNAVAILABLE
            self._circuit_breaker_last_failure = datetime.utcnow()
        elif self._circuit_breaker_failures >= self.config.circuit_breaker_threshold // 2:
            self._status = ProviderStatus.DEGRADED
    
    def _calculate_backoff(self, attempt: int) -> float:
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
        self._status = ProviderStatus.HEALTHY
    
    def _record_failure(self, e: Exception) -> None:
        self._circuit_breaker_failures += 1
        if self._circuit_breaker_failures >= self.config.circuit_breaker_threshold:
            self._status = ProviderStatus.UNAVAILABLE
            self._circuit_breaker_last_failure = datetime.utcnow()
        elif self._circuit_breaker_failures >= self.config.circuit_breaker_threshold // 2:
            self._status = ProviderStatus.DEGRADED
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "provider": "azure_openai",
            "status": self._status.value,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "circuit_breaker_failures": self._circuit_breaker_failures,
        }
    
    def get_config(self) -> "ProviderConfig":
        return self.config


class LocalProvider:
    """
    Local provider for running models locally (Ollama, llama.cpp, etc.)
    """
    
    def __init__(self, config: "ProviderConfig"):
        from app.services.ai_providers import ProviderConfig, ProviderStatus, ProviderType
        from app.services.ai_providers import AIProvider, ProviderStatus
        
        self.config = config
        self._status = ProviderStatus.HEALTHY
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: Optional[datetime] = None
        self._request_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        
        # For local models, we'd typically use a local API like Ollama
        self.base_url = config.api_base or "http://localhost:11434"
        self.client = None  # Would be initialized with a local client
    
    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        # Implementation for local model inference
        # This would integrate with Ollama, llama.cpp, or similar
        pass
    
    async def health_check(self) -> "ProviderStatusResponse":
        from app.services.ai_providers import ProviderStatusResponse, ProviderStatus
        return ProviderStatusResponse(
            provider="local",
            status=ProviderStatus.HEALTHY,
            latency_ms=1,
            last_check=datetime.utcnow(),
            error_message=None,
            model=self.config.default_model.value,
            version="1.0"
        )
    
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "provider": "local",
            "status": self._status.value,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
        }
    
    def get_config(self) -> "ProviderConfig":
        return self.config


# Export all provider classes
__all__ = [
    "OpenAIProvider",
    "AzureOpenAIProvider",
    "AnthropicProvider",
    "LocalProvider",
    "MockProvider",
    "ProviderFactory",
    "get_provider_factory",
    "initialize_provider_factory",
]