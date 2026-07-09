# PHASE 10C: IMPLEMENTATION SEQUENCE

To ensure maximum architectural safety and prevent frontend blockage during backend development, the implementation of the Question Registry must follow this strict bottom-up sequence.

### Step 1: Registry Data Serialization (Backend)
- **Action:** Translate the `docs/status/QUESTION_REGISTRY_MASTER_v1.md` and `docs/architecture/QUESTION_REGISTRY_MAPPING_v1.md` documents into a static configuration format (JSON or YAML).
- **Deliverable:** A single authoritative `registry_config.yaml` or `registry.json` file in the backend repository containing all 200+ question nodes and their boolean logic bounds.
- **Why First:** This file becomes the source of truth for both the Python backend to route logic, and the React frontend to build the UI domains.

### Step 2: Formula Loader & Router Construction (Backend)
- **Action:** Build the `FormulaLoader` class to parse the Registry Config. Build the `QuestionRouter` to intercept `/ask-question` API calls, read the `question_id`, and execute the strict `engine_outputs` extraction logic.
- **Deliverable:** Modification of `queries.py` and `question_engine.py` to support `question_id` lookups.
- **Why Second:** Establishes the mathematical bounds before any NLP fallback logic is introduced.

### Step 3: NLP Fallback Layer (Backend)
- **Action:** Implement the "Dictionary Search Contract" mapping semantic keywords to `question_id` if the user submits a raw text payload instead of an ID.
- **Deliverable:** NLP resolution engine with strict 80% confidence threshold rejection.

### Step 4: Frontend State & Storage Layer (Frontend)
- **Action:** Implement the API fetch to load the 24 Domains from the backend into React Context. Build the `localStorage` hooks to manage Favorites and Recent Questions.
- **Deliverable:** A Headless React state management system capable of tracking recent `question_id` arrays.

### Step 5: Question Browser UI Implementation (Frontend)
- **Action:** Build the Accordion UI, Search Bar, Question Cards, and Sticky Ask Footer based on the `docs/architecture/QUESTION_BROWSER_UI_BLUEPRINT_v1.md`.
- **Deliverable:** Fully functional, interactive React interface replacing the current text box.
- **Why Fifth:** Requires the backend API to be stable so the "Ask" button can successfully submit `question_id` payloads.

### Step 6: Answer Composer Integration (Backend/LLM)
- **Action:** Refactor the final LLM prompt injection logic inside `QuestionEngine.compose_response`. Ensure it only accepts the mapped mathematical variables exported by the Router.
- **Deliverable:** Final generation of deterministic natural language responses. 

---

*Proceed sequentially. Do not begin Frontend UI implementation (Step 5) until the Backend Registry payload (Step 1) is fully accessible.*
