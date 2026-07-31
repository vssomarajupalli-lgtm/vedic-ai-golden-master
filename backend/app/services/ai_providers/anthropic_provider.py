"""
GM-012D.4 — Anthropic Provider Implementation

Anthropic (Claude) provider implementation for the AI Provider abstraction layer.
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


class AnthropicProvider:
    """
    Anthropic (Claude) provider implementation.
    
    Handles communication with Anthropic API.
    Supports Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku models.
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
        
        # Initialize Anthropic client
        self.client = httpx.AsyncClient(
            base_url=config.api_base or "https://api.anthropic.com",
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
                **(config.extra_headers or {})
            },
            timeout=config.timeout_seconds,
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
            "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
            "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
            "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
        }

    def _get_cost_per_1k(self, model: str) -> Dict[str, float]:
        """Get cost per 1k tokens for a model"""
        model_key = model.lower().replace("claude-", "claude-").replace("-", "-")
        if model in self._cost_per_1k:
            return self._cost_per_1k[model]
        # Default to Haiku pricing
        return self._cost_per_1k.get("claude-3-haiku-20240307", {"input": 0.00025, "output": 0.00125})

    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        """Generate a response from Anthropic"""
        from app.services.ai_providers import ProviderRequest, ProviderResponse, ProviderStatus
        import asyncio
        import uuid
        
        start_time = datetime.utcnow()
        
        if not self._check_circuit_breaker():
            raise Exception("Circuit breaker open - provider unavailable")
        
        # Validate prompt package
        if not await self.validate_prompt_package(request.prompt_package):
            raise ValueError("Invalid prompt package")
        
        # Prepare messages
        system_prompt = request.prompt_package.get("system_prompt", "")
        user_prompt = request.prompt_package.get("user_prompt", "")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        # Model selection
        model = request.model or self.config.default_model.value
        
        # Prepare request parameters
        params = {
            "model": model,
            "messages": messages,
            "temperature": request.temperature if request.temperature is not None else self.config.temperature,
            "max_tokens": request.max_tokens or self.config.max_tokens,
            "top_p": request.top_p if request.top_p is not None else self.config.top_p,
            "system": request.prompt_package.get("system_prompt", ""),
        }
        
        if request.stop:
            params["stop_sequences"] = request.stop
        
        # Execute with retry logic
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            if not self._check_circuit_breaker():
                raise Exception("Circuit breaker open - provider unavailable")
            
            try:
                # Make API call
                start_time = datetime.utcnow()
                
                async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                    response = await client.post(
                        f"{self.config.api_base}/v1/messages",
                        headers={
                            "x-api-key": self.config.api_key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json=params,
                        timeout=self.config.timeout_seconds,
                    )
                    
                    processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                    
                    if response.status_code != 200:
                        error_text = await response.text()
                        raise Exception(f"Anthropic API error {response.status_code}: {error_text}")
                    
                    response_data = response.json()
                    content = response_data["content"][0]["text"] if response_data.get("content") else ""
                    
                    usage = response_data.get("usage", {})
                    prompt_tokens = usage.get("input_tokens", 0)
                    completion_tokens = usage.get("output_tokens", 0)
                    total_tokens = usage.get("total_tokens", 0)
                    
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
                    self._status = "healthy"
                    
                    # Build response
                    response_obj = ProviderResponse(
                        content=content,
                        model=model,
                        provider="anthropic",
                        usage={
                            "prompt_tokens": prompt_tokens,
                            "completion_tokens": completion_tokens,
                            "total_tokens": total_tokens
                        },
                        finish_reason=response_data.get("stop_reason"),
                        citations=[],
                        confidence=None,
                        deterministic_trace=None,
                        processing_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                        request_id=str(uuid4()),
                        provider="anthropic",
                        model=model,
                        timestamp=datetime.utcnow(),
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens,
                        finish_reason=response_data.get("stop_reason"),
                        logprobs=None,
                        citations=[],
                        confidence=None,
                        deterministic_trace=None,
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
        """Perform a health check on the Anthropic API"""
        from app.services.ai_providers import ProviderStatusResponse, ProviderStatus
        
        try:
            start_time = datetime.utcnow()
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.config.api_base}/v1/models",
                    headers={"x-api-key": self.config.api_key},
                    timeout=10
                )
                
                if response.status_code == 200:
                    latency_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                    return ProviderStatusResponse(
                        provider="anthropic",
                        status=ProviderStatus.HEALTHY,
                        latency_ms=latency_ms,
                        last_check=datetime.utcnow(),
                        error_message=None,
                        model=self.config.default_model.value,
                        version="1.0"
                    )
            
        except Exception as e:
            logger.error(f"Anthropic health check failed: {e}")
            return ProviderStatusResponse(
                provider="anthropic",
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
            if self._circuit_breaker_last_failure:
                elapsed = (datetime.utcnow() - self._circuit_breaker_last_failure).total_seconds()
                if elapsed >= self.config.circuit_breaker_timeout_seconds:
                    self._status = "healthy"
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
        model_key = model.lower().replace("claude-", "claude-").replace("-", "-")
        if model in self._cost_per_1k:
            return self._cost_per_1k[model]
        # Default to Haiku pricing
        return self._cost_per_1k.get("claude-3-haiku-20240307", {"input": 0.00025, "output": 0.00125})
    
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
            "provider": "anthropic",
            "status": self._status,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "circuit_breaker_failures": self._circuit_breaker_failures,
            "status": self._status
        }
    
    def get_config(self):
        return self.config