# QUESTION REGISTRY BACKEND CONTRACT v1

## 1. QUESTION ID CONTRACT
Every question executed through the deterministic engine is bound to a strict numeric and string identifier schema.

### Data Structure
- `question_id`: `string` (e.g., `MAR_TIMING_001` or `10.4_GOV_JOB`)
- `domain_id`: `integer` (Corresponds to Master Domains 1-24)
- `child_id`: `integer` (Sequential index within the domain)
- `display_name`: `string` (The user-facing title, e.g., "Marriage Timing" or "Government Job")

**Example Payload Registry:**
```json
{
  "question_id": "7.2",
  "domain_id": 7,
  "child_id": 2,
  "display_name": "Marriage Timing"
}
```

## 2. API CONTRACT
The frontend-to-backend communication layer mapping the `question_id` to the pipeline.

### Frontend Request (POST `/ask-question`)
**Required Fields:**
- `engine_outputs`: `object` (The raw mathematical `ChartProcessResponse` payload containing Dashas, Yogas, Promise).
**Optional Fields:**
- `question_id`: `string` (The specific ID from the Question Browser).
- `question_text`: `string` (The free-text input if `question_id` is null).

### Frontend Response
**Required Fields:**
- `answer_text`: `string` (The synthesized LLM response based ONLY on the mapped formula).
- `resolved_question_id`: `string` (The actual ID evaluated by the backend, useful for tracking if NLP fallback was used).
- `referenced_yogas`: `array[string]`

**Error Responses:**
- `400 Bad Request`: Missing both `question_id` and `question_text`.
- `404 Not Found`: Provided `question_id` does not exist in the Registry.
- `422 Unprocessable Entity`: The provided `engine_outputs` schema is invalid or missing required timing layers.

## 3. SEARCH CONTRACT
Resolves user typestrings to deterministic `question_id` targets.

### Architecture Layers
1. **Search Dictionary Layer:** A pre-computed index mapping common astrological synonyms to Master Domains (e.g., "spouse", "wife", "husband", "partner" -> Domain 7).
2. **Keyword Mapping Layer:** Resolves phonetic variations and typos (e.g., "marrage", "marraige" -> "marriage").
3. **Question ID Resolution:** Returns the closest matching array of child questions for the frontend Accordion UI to auto-expand.

## 4. FAVORITES CONTRACT
Local persistence structure for user-saved queries.

- **Storage Structure:** Initially bounded to `localStorage` on the client.
- **Question ID Persistence:** Stores an array of `question_id` strings (e.g., `["7.2", "10.1", "2.1"]`).
- **Future Synchronization Rules:** Upon account authentication implementation, the string array will be serialized and synced to a remote user profile database.

## 5. RECENT QUESTIONS CONTRACT
Tracks historical execution queries.

- **Storage Format:** Local array of objects: `[{ question_id: "7.2", timestamp: "2026-06-19T22:00:00Z" }]`.
- **Retention Limits:** Capped at the `10` most recently executed queries to prevent storage bloat.
- **Ordering Rules:** Sorted by descending timestamp (newest first). Duplicate queries update the timestamp and bubble to the top.

## 6. FREE TEXT FALLBACK CONTRACT
Maintains NLP flexibility while enforcing mathematical grounding.

- **Routing Hierarchy:** 
  1. If `question_id` is present -> Route exact.
  2. If `question_id` is null AND `question_text` is present -> NLP Router evaluates intent against the 200+ Dictionary Index.
- **Fallback Behavior:** If NLP intent matches a known Domain (e.g., "Will I have kids?" -> Domain 5), it snaps to the closest `question_id` (e.g., `5.1 Childbirth Promise`).
- **Unknown Query Handling:** If NLP fails to resolve to ANY Domain with >80% confidence, the backend rejects the query and gracefully prompts the user: *"Please select a question from the Question Browser."*
