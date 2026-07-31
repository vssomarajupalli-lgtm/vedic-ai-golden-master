"""
GM-012D.4 — OpenAI Provider Implementation

OpenAI provider implementation for the AI Provider abstraction layer.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

import httpx
from openai import AsyncOpenAI

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
                    top_p=params.get("top_p", 1.0),
                    frequency_penalty=params.get("frequency_penalty", 0.0),
                    presence_penalty=params.get("presence_penalty", 0.0),
                    stop=params.get("stop"),
                    stream=request.stream,
                    max_tokens=params.get("max_tokens"),
                    top_p=params.get("top_p", 1.0),
                    frequency_penalty=params.get("frequency_penalty", 0.0),
                    presence_penalty=params.get("presence_penalty", 0.0),
                    stop=params.get("stop"),
                    stream=request.stream,
                )
                
                processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                
                # Extract response
                content = response.choices[0].message.content if response.choices else ""
                finish_reason = response.choices[0].finish_reason if response.choices else None
                usage = response.usage
                
                # Calculate cost
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                total_tokens = usage.total_tokens if usage else 0
                
                cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
                
                # Build response
                response_obj = ProviderResponse(
                    content=content or "",
                    model=model,
                    provider="openai",
                    usage={
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                    },
                    finish_reason=finish_reason,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                    processing_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                    request_id=request.request_id,
                    provider="openai",
                    model=model,
                    timestamp=datetime.utcnow(),
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    finish_reason=finish_reason,
                    logprobs=None,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                )
                
                self._record_success(ProviderResponse(
                    content="",
                    model=model,
                    provider="openai",
                    usage={"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens},
                    finish_reason=finish_reason,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                    processing_time_ms=processing_time_ms,
                    request_id=request.request_id,
                    provider="openai",
                    model=model,
                    timestamp=datetime.utcnow(),
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    finish_reason=finish_reason,
                    logprobs=None,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                ))
                
                return ProviderResponse(
                    content=content or "",
                    model=model,
                    provider="openai",
                    usage={"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens},
                    finish_reason=finish_reason,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                    processing_time_ms=processing_time_ms,
                    request_id=request.request_id,
                    provider="openai",
                    model=model,
                    timestamp=datetime.utcnow(),
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    finish_reason=finish_reason,
                    logprobs=None,
                    citations=[],
                    confidence=None,
                    deterministic_trace=None,
                )
                
            except Exception as e:
                last_exception = e
                logger.warning(f"OpenAI attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.max_retries:
                    delay = self._calculate_backoff(attempt)
                    await asyncio.sleep(delay)
                else:
                    break
        
        raise Exception(f"All retries exhausted. Last error: {last_exception}") from last_exception

    async def health_check(self) -> "ProviderStatusResponse":
        """Perform health check on OpenAI API"""
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
                provider="openai",
                status=ProviderStatus.HEALTHY,
                latency_ms=latency_ms,
                last_check=datetime.utcnow(),
                error_message=None,
                model=self.config.default_model.value,
                version="1.0"
            )
            
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return ProviderStatusResponse(
                provider="openai",
                status=ProviderStatus.UNAVAILABLE,
                latency_ms=0,
                last_check=datetime.utcnow(),
                error_message=str(e),
                model=self.config.default_model.value,
                version="1.0"
            )

    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        """Validate that a PromptPackage is well-formed"""
        try:
            # Check required fields
            required_fields = ["system_prompt", "user_prompt", "evidence_section", "citation_section", "metadata"]
            for field in required_fields:
                if field not in prompt_package:
                    logger.warning(f"Missing required field: {field}")
                    return False
            
            # Check system prompt
            system_prompt = prompt_package.get("system_prompt", "")
            if not system_prompt or len(system_prompt) < 100:
                logger.warning("System prompt too short or missing")
                return False
            
            # Check user prompt
            user_prompt = prompt_package.get("user_prompt", "")
            if not user_prompt or len(user_prompt) < 10:
                logger.warning("User prompt too short or missing")
                return False
            
            # Check evidence section
            evidence = prompt_package.get("evidence_section", {})
            if not evidence or "chain" not in evidence:
                logger.warning("Evidence section missing or malformed")
                return False
            
            # Check citations
            citations = prompt_package.get("citation_section", {})
            if not citations or "citations" not in citations:
                logger.warning("Citations missing")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Prompt package validation failed: {e}")
            return False
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on token usage"""
        costs = self._get_cost_per_1k(model)
        input_cost = (prompt_tokens / 1000) * costs["input"]
        output_cost = (completion_tokens / 1000) * costs["output"]
        return input_cost + output_cost
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay"""
        delay = min(
            self.config.retry_base_delay_seconds * (self.config.retry_exponential_base ** attempt),
            self.config.retry_max_delay_seconds
        )
        return delay
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker allows request"""
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
    
    async def _execute_with_retry(self, request: "ProviderRequest", generate_func) -> "ProviderResponse":
        """Execute generation with retry logic"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            if not self._check_circuit_breaker():
                raise Exception("Circuit breaker open - provider unavailable")
            
            try:
                response = await self.generate(request)
                self._record_success(response)
                return response
            except Exception as e:
                last_exception = e
                self._record_failure(e)
                
                if attempt < self.config.max_retries:
                    delay = self._calculate_backoff(attempt)
                    await asyncio.sleep(delay)
                else:
                    break
        
        raise Exception(f"All retries exhausted. Last error: {last_exception}") from last_exception
    
    def _record_success(self, response: "ProviderResponse") -> None:
        """Record successful request"""
        self._request_count += 1
        self._total_tokens += response.total_tokens
        self._total_cost += self._calculate_cost(response)
        self._circuit_breaker_failures = 0
        self._status = ProviderStatus.HEALTHY
    
    def _record_failure(self, error: Exception) -> None:
        """Record failed request"""
        self._circuit_breaker_failures += 1
        if self._circuit_breaker_failures >= self.config.circuit_breaker_threshold:
            self._status = ProviderStatus.UNAVAILABLE
            self._circuit_breaker_last_failure = datetime.utcnow()
        elif self._circuit_breaker_failures >= self.config.circuit_breaker_threshold // 2:
            self._status = ProviderStatus.DEGRADED
    
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics"""
        return {
            "provider": "openai",
            "status": self._status.value,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "circuit_breaker_failures": self._circuit_breaker_failures,
        }
    
    def get_config(self) -> "ProviderConfig":
        """Get provider configuration"""
        return self.config