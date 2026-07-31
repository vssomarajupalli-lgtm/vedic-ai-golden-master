# GM-012D.6 Frontend Integration Report

## Files Created

1. **`frontend/src/components/AIExplanationPanel.tsx`** (NEW)
   - Main React component for AI explanation integration
   - Calls `POST /api/v1/explanations/generate`
   - Displays explanation, confidence, evidence summary, citations
   - Includes loading state, error state with retry

## Files Modified

1. **`frontend/src/types/schema.d.ts`** (UPDATED)
   - Added `ExplanationRequest` type for API request
   - Added `ExplanationResponse` type for API response
   - Added `ExplanationCitation` type for citation display
   - Added `ExplanationEvidenceSummary` type for evidence stats
   - Added `ExplanationMetadata` type for provider/model info

2. **`frontend/src/api/backend.ts`** (UPDATED)
   - Added `generateExplanation(request: ExplanationRequest)` method
   - Added `checkExplanationHealth()` method
   - Imported new types from schema

## UI Components

### AIExplanationPanel
A complete React component with:

**Props:**
- `questionId?: string` - Question ID from registry
- `questionText?: string` - Free-text question
- `pipelineOutput: Record<string, unknown> | null` - Full pipeline output
- `targetDateUtc?: string` - ISO 8601 UTC timestamp
- `className?: string` - Custom styling
- `onExplanationGenerated?: (response) => void` - Success callback
- `onError?: (error) => void` - Error callback

**Features:**
1. **Header** - Shows "AI Explanation" with deterministic pipeline badge
2. **Input Summary** - Displays question ID/text and target date
3. **Generate Button** - Loading spinner, disabled states
4. **Error State** - Red banner with error message and Retry button
5. **Confidence Badge** - Color-coded (HIGH=emerald, MEDIUM=amber, LOW=red)
6. **Explanation Text** - Main AI-generated explanation
7. **Evidence Summary** (collapsible) - Total citations, by-type breakdown, highest evidence level
8. **Citations** (collapsible) - Each citation with type badge, evidence level, path, value, node_id
9. **Metadata** (collapsible) - Provider, model, tokens, processing time, grounding hash

**Citation Type Colors:**
- `engine_output` → Blue
- `kg_node` → Purple
- `evidence_chain` → Green
- `formula_registry` → Orange
- `calibration_registry` → Pink
- `report_template` → Gray

## Validation Results

### ✅ Frontend Build
```
✓ built in 1.56s
dist/assets/index-Bv6T00RZ.js    552.93 kB │ gzip: 144.02 kB
```

### ✅ Backend Tests (726 passed, 1 skipped)
All existing tests pass without modification.

### ✅ API Integration Verified
```
GET /api/v1/explanations/health
→ 200 OK, provider: mock, status: healthy

POST /api/v1/explanations/generate
→ 200 OK with structured response:
{
  "question": "Will I get married?",
  "domain": "marriage",
  "routed": true,
  "explanation": "General probability: 55/100 (MODERATE)...",
  "citations": [...],
  "evidence_summary": {...},
  "confidence": "HIGH",
  "metadata": {...},
  "processing_time_ms": 0
}
```

### ✅ Component Features Verified
- **Loading state**: Spinner + "Generating..." text during request
- **Error handling**: Red error banner with message + Retry button
- **Explanation rendering**: Whitespace-pre-wrap for formatted text
- **Confidence display**: Color-coded badge with text
- **Evidence summary**: Collapsible with citation counts by type
- **Citations rendering**: Type badges, evidence levels, paths, values
- **Retry support**: Error state includes Retry button that re-calls API

## Usage Example

```tsx
import { AIExplanationPanel } from './components/AIExplanationPanel';

<AIExplanationPanel
  questionId="7.1"
  questionText="Will I get married?"
  pipelineOutput={chartProcessResponse}
  targetDateUtc="2026-07-29T10:00:00Z"
  onExplanationGenerated={(response) => console.log('Generated:', response)}
  onError={(error) => console.error('Failed:', error)}
/>
```

## Notes
- No backend changes required
- No deterministic engine modifications
- No Knowledge Graph modifications
- No PromptBuilder modifications
- No AI provider logic changes
- Purely consumes the existing `/api/v1/explanations/generate` endpoint