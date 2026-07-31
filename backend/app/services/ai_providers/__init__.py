"""
GM-012D.4 — AI Provider Abstraction Layer

Provider abstraction layer for AI explanation services.
Supports multiple AI providers with a unified interface.

This layer MUST NOT contain astrology logic.
It MUST NOT modify prompts.
It MUST NOT generate explanations.
It ONLY defines how an AI provider is invoked.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4
import hashlib
import json


class ProviderType(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    LOCAL = "local"
    MOCK = "mock"


class ProviderStatus(str, Enum):
    """Provider status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class AIModel(str, Enum):
    """Supported AI models"""
    # OpenAI
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    # Anthropic
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    # Azure OpenAI
    AZURE_GPT_4O = "azure-gpt-4o"
    AZURE_GPT_4O_MINI = "azure-gpt-4o-mini"
    # Local
    LLAMA_3_1_70B = "llama-3.1-70b"
    LLAMA_3_1_8B = "llama-3.1-8b"
    MIXTRAL_8X7B = "mixtral-8x7b"
    # Mock for testing
    MOCK = "mock"


class ProviderStatusResponse(BaseModel):
    """Provider health status response"""
    provider: str
    status: ProviderStatus
    latency_ms: Optional[float] = None
    last_check: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None


class ProviderRequest(BaseModel):
    """Request to AI provider"""
    prompt_package: dict = Field(..., description="Complete PromptPackage from PromptBuilder")
    model: Optional[str] = None
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=0.0, le=1.0)
    presence_penalty: float = Field(default=0.0, ge=0.0, le=1.0)
    stop: Optional[List[str]] = None
    stream: bool = False
    max_retries: int = 3
    timeout_seconds: int = 60
    request_id: str = Field(default_factory=lambda: str(uuid4()))


class ProviderResponse(BaseModel):
    """Response from AI provider"""
    content: str = Field(..., description="The generated explanation text")
    model: str
    provider: str
    usage: Dict[str, int] = Field(default_factory=dict)
    finish_reason: Optional[str] = None
    citations: List[dict] = Field(default_factory=list)
    confidence: Optional[str] = None
    deterministic_trace: Optional[str] = None
    processing_time_ms: int = 0
    request_id: str
    provider: str
    model: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: Optional[str] = None
    logprobs: Optional[Any] = None
    citations: List[dict] = Field(default_factory=list)
    confidence: Optional[str] = None
    deterministic_trace: Optional[str] = None


class ProviderConfig(BaseModel):
    """Configuration for an AI provider"""
    provider_type: ProviderType
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    organization: Optional[str] = None
    api_version: Optional[str] = None
    default_model: AIModel = AIModel.GPT_4O_MINI
    fallback_models: List[AIModel] = []
    max_retries: int = 3
    timeout_seconds: int = 60
    max_tokens: int = 4000
    temperature: float = 0.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    rate_limit_rpm: int = 60
    timeout_seconds: int = 60
    extra_headers: Dict[str, str] = {}
    extra_params: Dict[str, Any] = {}
    # Health check
    health_check_interval_seconds: int = 60
    health_check_timeout_seconds: int = 10
    # Circuit breaker
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout_seconds: int = 60
    # Retry
    retry_base_delay_seconds: float = 1.0
    retry_max_delay_seconds: float = 30.0
    retry_exponential_base: float = 2.0
    # Cost tracking
    track_cost: bool = True
    cost_per_1k_input_tokens: float = 0.0
    cost_per_1k_output_tokens: float = 0.0
    # Logging
    log_requests: bool = True
    log_responses: bool = False
    log_level: str = "INFO"


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    All AI providers must implement this interface.
    The provider is responsible ONLY for:
    1. Accepting a PromptPackage
    2. Sending the prompt to the configured AI provider
    3. Receiving the raw response
    4. Returning a structured ProviderResponse
    
    The provider MUST NOT:
    - Modify prompts
    - Generate explanations
    - Contain astrology logic
    - Modify prompts
    - Call deterministic engines
    - Access Knowledge Graph directly
    - Perform any astrological calculations
    """
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self._status = ProviderStatus.HEALTHY
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure: Optional[datetime] = None
        self._request_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
    
    @property
    def provider_type(self) -> ProviderType:
        """Return the provider type"""
        return self.config.provider_type
    
    @property
    def status(self) -> ProviderStatus:
        return self._status
    
    @property
    def is_healthy(self) -> bool:
        return self._status == ProviderStatus.HEALTHY
    
    @property
    def is_available(self) -> bool:
        return self._status in (ProviderStatus.HEALTHY, ProviderStatus.DEGRADED)
    
    @abstractmethod
    async def generate(self, request: ProviderRequest) -> ProviderResponse:
        """
        Generate a response from the AI provider.
        
        Args:
            request: The provider request containing the PromptPackage
            
        Returns:
            ProviderResponse with the AI-generated explanation
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> ProviderStatusResponse:
        """
        Perform a health check on the provider.
        
        Returns:
            ProviderStatusResponse with current status
        """
        pass
    
    @abstractmethod
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        """
        Validate that a PromptPackage is well-formed.
        
        Args:
            prompt_package: The PromptPackage to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
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
    
    def _calculate_cost(self, response: "ProviderResponse") -> float:
        """Calculate cost based on token usage"""
        input_cost = (response.prompt_tokens / 1000) * self.config.cost_per_1k_input_tokens
        output_cost = (response.completion_tokens / 1000) * self.config.cost_per_1k_output_tokens
        return input_cost + output_cost
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker should allow request"""
        if self._status == ProviderStatus.UNAVAILABLE:
            # Check if circuit breaker timeout has passed
            if self._circuit_breaker_last_failure:
                elapsed = (datetime.utcnow() - self._circuit_breaker_last_failure).total_seconds()
                if elapsed >= self.config.circuit_breaker_timeout_seconds:
                    self._status = ProviderStatus.DEGRADED
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
    
    @abstractmethod
    async def generate(self, request: "ProviderRequest") -> "ProviderResponse":
        """
        Generate a response from the AI provider.
        
        Args:
            request: The provider request containing the PromptPackage
            
        Returns:
            ProviderResponse with the AI-generated explanation
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> "ProviderStatusResponse":
        """
        Perform a health check on the provider.
        
        Returns:
            ProviderStatusResponse with current status
        """
        pass
    
    @abstractmethod
    async def validate_prompt_package(self, prompt_package: dict) -> bool:
        """
        Validate that a PromptPackage is well-formed.
        
        Args:
            prompt_package: The PromptPackage to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics"""
        return {
            "provider": self.provider_type.value,
            "status": self.status.value,
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "circuit_breaker_failures": self._circuit_breaker_failures,
            "status": self._status.value
        }
    
    def get_config(self) -> ProviderConfig:
        """Get provider configuration"""
        return self.config
    
    async def _execute_with_retry(self, request: "ProviderRequest", generate_func) -> "ProviderResponse":
        """Execute generation with retry logic"""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            if not self._check_circuit_breaker():
                raise Exception("Circuit breaker open - provider unavailable")
            
            try:
                response = await generate_func(request)
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


# Export all public classes
__all__ = [
    "ProviderType",
    "ProviderStatus",
    "AIModel",
    "ProviderStatusResponse",
    "ProviderRequest",
    "ProviderResponse",
    "ProviderConfig",
    "AIProvider",
]