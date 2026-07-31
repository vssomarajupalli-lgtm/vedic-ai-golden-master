# AI Provider Configuration Guide

**Version**: 1.1 (GM-012D)  
**Scope**: Production AI explanation layer configuration  
**Status**: Documentation only — no implementation changes

---

## 1. Supported Providers

| Provider | Type | Models | Status |
|----------|------|--------|--------|
| **OpenAI** | `openai` | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo` | ✅ Production Ready |
| **Anthropic** | `anthropic` | `claude-3-5-sonnet`, `claude-3-opus`, `claude-3-haiku` | ✅ Production Ready |
| **Azure OpenAI** | `azure_openai` | `azure-gpt-4o`, `azure-gpt-4o-mini` | ✅ Production Ready |
| **Local (Ollama/LM Studio)** | `local` | `llama-3.1-70b`, `llama-3.1-8b`, `mixtral-8x7b` | ✅ Production Ready |
| **Mock** | `mock` | `mock-model` | ✅ Testing Only |

---

## 2. Required Environment Variables

### OpenAI
```bash
OPENAI_API_KEY=sk-...
OPENAI_ORGANIZATION=org-...          # Optional
OPENAI_API_BASE=https://api.openai.com/v1  # Optional (custom endpoint)
```

### Anthropic
```bash
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_API_BASE=https://api.anthropic.com  # Optional
```

### Azure OpenAI
```bash
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

### Local (Ollama / LM Studio)
```bash
LOCAL_API_BASE=http://localhost:11434/v1  # Ollama default
LOCAL_API_KEY=not-needed                  # Or your local server key
```

---

## 3. Default Provider

**Default**: `mock` (MockProvider)

The MockProvider is registered as the default provider at factory initialization. It returns deterministic, structured JSON responses that pass governance validation — enabling full pipeline testing without external API dependencies.

To use a real provider in production, register it as default:

```python
from app.services.ai_providers import get_provider_factory, ProviderConfig, ProviderType, AIModel

factory = get_provider_factory()

# Register OpenAI as default
factory.register_provider(
    name="openai-prod",
    config=ProviderConfig(
        provider_type=ProviderType.OPENAI,
        api_key="sk-...",  # or from env
        default_model=AIModel.GPT_4O_MINI,
    ),
    is_default=True
)
```

---

## 4. Fallback Chain

The `ProviderConfig` supports an ordered fallback model list:

```python
ProviderConfig(
    provider_type=ProviderType.OPENAI,
    api_key="...",
    default_model=AIModel.GPT_4O,
    fallback_models=[
        AIModel.GPT_4O_MINI,
        AIModel.GPT_4_TURBO,
        AIModel.GPT_3_5_TURBO,
    ],
    ...
)
```

**Behavior**: On failure (timeout, rate limit, 5xx), the provider automatically retries with the next model in `fallback_models`. If all models fail, the circuit breaker activates.

---

## 5. Timeout Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `timeout_seconds` | 60 | Per-request timeout |
| `health_check_timeout_seconds` | 10 | Health check timeout |
| `health_check_interval_seconds` | 60 | Background health check interval |

All timeouts are configurable per-provider via `ProviderConfig`.

---

## 6. Retry Policy

```python
ProviderConfig(
    max_retries=3,                    # Total attempts = 1 + max_retries
    retry_base_delay_seconds=1.0,     # Initial backoff
    retry_max_delay_seconds=30.0,     # Cap on backoff
    retry_exponential_base=2.0,       # Multiplier per attempt
)
```

**Retry behavior**: Exponential backoff with jitter. Retries on: network errors, 429 (rate limit), 5xx errors. Does NOT retry on 4xx (client errors).

---

## 7. Circuit Breaker

```python
ProviderConfig(
    circuit_breaker_threshold=5,      # Failures before opening
    circuit_breaker_timeout_seconds=60,  # Time before half-open
)
```

**States**:
- **HEALTHY**: Normal operation
- **DEGRADED**: ≥ threshold/2 failures (warns, still accepts requests)
- **UNAVAILABLE**: ≥ threshold failures (rejects requests, returns 503)
- **Half-open**: After timeout, allows probe requests

---

## 8. Rate Limiting

```python
ProviderConfig(
    rate_limit_rpm=60,  # Requests per minute
)
```

Applied per-provider instance. Exceeding limit returns 429 with `Retry-After` header.

---

## 9. Cost Tracking

```python
ProviderConfig(
    track_cost=True,
    cost_per_1k_input_tokens=0.00015,   # gpt-4o-mini pricing
    cost_per_1k_output_tokens=0.0006,
)
```

Access via `provider.get_stats()` → `{"total_cost": 0.042, "total_tokens": 12345, ...}`

---

## 10. Production Initialization Example

```python
# backend/app/main.py or dedicated init module
from app.services.ai_providers import (
    get_provider_factory, ProviderConfig, ProviderType, AIModel
)
import os

def init_ai_providers():
    factory = get_provider_factory()
    
    # OpenAI (production default)
    if os.getenv("OPENAI_API_KEY"):
        factory.register_provider(
            name="openai-prod",
            config=ProviderConfig(
                provider_type=ProviderType.OPENAI,
                api_key=os.getenv("OPENAI_API_KEY"),
                organization=os.getenv("OPENAI_ORGANIZATION"),
                api_base=os.getenv("OPENAI_API_BASE"),
                default_model=AIModel.GPT_4O_MINI,
                fallback_models=[AIModel.GPT_4O, AIModel.GPT_4_TURBO],
                max_retries=3,
                timeout_seconds=60,
                temperature=0.0,
                max_tokens=4000,
                circuit_breaker_threshold=5,
                circuit_breaker_timeout_seconds=60,
                track_cost=True,
                cost_per_1k_input_tokens=0.00015,
                cost_per_1k_output_tokens=0.0006,
            ),
            is_default=True
        )
    
    # Anthropic (fallback)
    if os.getenv("ANTHROPIC_API_KEY"):
        factory.register_provider(
            name="anthropic-prod",
            config=ProviderConfig(
                provider_type=ProviderType.ANTHROPIC,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                default_model=AIModel.CLAUDE_3_5_SONNET,
                fallback_models=[AIModel.CLAUDE_3_HAIKU],
                max_retries=3,
                timeout_seconds=60,
                temperature=0.0,
            ),
            is_default=False
        )
    
    # Local (offline/privacy)
    if os.getenv("LOCAL_API_BASE"):
        factory.register_provider(
            name="local-llama",
            config=ProviderConfig(
                provider_type=ProviderType.LOCAL,
                api_base=os.getenv("LOCAL_API_BASE", "http://localhost:11434/v1"),
                api_key=os.getenv("LOCAL_API_KEY", "not-needed"),
                default_model=AIModel.LLAMA_3_1_8B,
                max_retries=2,
                timeout_seconds=120,  # Local models slower
                temperature=0.0,
            ),
            is_default=False
        )
    
    # Mock always available for testing
    factory.register_provider(
        name="mock",
        config=ProviderConfig(
            provider_type=ProviderType.MOCK,
            default_model=AIModel.MOCK,
        ),
        is_default=False
    )
    
    return factory
```

---

## 11. Health Check Endpoint

```
GET /api/v1/explanations/health
```

**Response**:
```json
{
  "status": "healthy",
  "provider": {
    "name": "openai",
    "status": "healthy",
    "latency_ms": 45.2,
    "model": "gpt-4o-mini"
  },
  "components": {
    "prompt_builder": "ready",
    "question_router": "ready",
    "knowledge_store": "ready"
  }
}
```

---

## 12. Tauri Sidecar Rebuild

After configuring production providers, rebuild the desktop sidecar:

```bash
cd frontend/src-tauri
cargo build --release
# Copies vedic-ai-backend.exe to sidecar/
# Ensure OPENAI_API_KEY etc. are in Tauri env or .env at build time
```

---

## 13. Testing with MockProvider

```python
from app.services.ai_providers import get_provider_factory, ProviderConfig, ProviderType, AIModel

factory = get_provider_factory()
mock = factory.get_provider("mock")

# Or use default (mock)
provider = factory.get_provider()  # Returns mock by default

response = await provider.generate(ProviderRequest(
    prompt_package={"system_prompt": "...", "user_prompt": "Will I get married?"},
    model="mock-model",
    temperature=0.0,
))

# Response.content contains valid JSON with explanation, citations, confidence
# Deterministic: same input → identical output
```

---

## 14. Governance Compliance

All providers must return `ProviderResponse` with:
- `content`: Structured JSON string (validated by `AIExplanationService._validate_response`)
- `citations`: List of citation objects with `type`, `path`, `value`, `evidence_level`
- `confidence`: `HIGH` | `MEDIUM` | `LOW`
- `deterministic_trace`: Reference to engine output for replay verification

The `AIExplanationService` validates every response against governance rules before returning to client.

---

*Generated by GM-013A Release Candidate Cleanup — Documentation only, no code changes.*