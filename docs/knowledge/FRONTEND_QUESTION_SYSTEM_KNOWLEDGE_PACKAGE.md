# FRONTEND QUESTION SYSTEM KNOWLEDGE PACKAGE

## 1. Executive Summary
The Frontend Question System serves as the primary interactive layer for users to query the Golden Master. It consists of the `QuestionBrowser.tsx` (the registry UI) and the `QuestionEngine.tsx` (the active evaluation UI). It strictly respects the stateless nature of the backend by maintaining user session data locally (via Zustand) and making targeted REST calls to evaluate specific queries.

## 2. Purpose
To provide a beautiful, organized, and searchable UI that allows users to select structured questions and instantly view the corresponding deterministic probability, rather than dealing with raw astrological tables.

## 3. Responsibilities
- Fetch and display the central Question Registry grouped by domains (e.g., Marriage, Career).
- Manage user favorites and recently asked questions.
- Pass the selected `question_id` to the backend Question Engine for evaluation.
- Render the returned `final_score`, `raw_score`, and textual synthesis returned by the backend.

## 4. Architecture
Built using React, Vite, and Tailwind CSS.
- **Store (`useChartStore.ts`):** Manages the `rawOutputs` (the full parsed JSON chart data) and `questionResults` (an array of evaluated question payloads).
- **Question Browser:** Renders a list of available questions from the backend API. It prevents the user from submitting a question if a chart has not yet been processed (enforced via `disabled={!rawOutputs}`).
- **Question Engine:** The display layer for the evaluation result. It shows the qualitative grade, the quantitative percentage, and the textual synthesis (provided by an LLM that reads the deterministic numbers).

## 5. Inputs
- Central Chart Store (`rawOutputs`).
- User interactions (selecting a question, searching).
- Backend API responses (Registry JSON, Question Evaluation JSON).

## 6. Outputs
- Renders React components visualizing the probability data.

## 7. Data Contracts
- The frontend relies on the backend API returning a strictly formatted Question payload, specifically expecting `final_score`, `breakdown`, `synthesis`, and `formula_verification`.

## 8. Implementation Files
- `frontend/src/pages/QuestionBrowser.tsx`
- `frontend/src/pages/QuestionEngine.tsx`
- `frontend/src/store/useChartStore.ts`

## 9. Technical Debt & Recommendations
- Ensure the frontend remains "dumb" regarding astrological math. If a formula needs tweaking, it must happen in the `QuestionEngine` on the Python backend, not in the React presentation layer.
