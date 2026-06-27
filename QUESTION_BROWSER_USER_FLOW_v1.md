# QUESTION BROWSER USER FLOW v1

## 1. Primary Navigation Flow
The user journey transforms an abstract query into a mathematically deterministic API payload.

### Step 1: Entry
User navigates to the "Ask Question" tab in the React frontend.
The UI loads the 24 Master Domains in a collapsed state.
The Search Bar is focused at the top.

### Step 2: Question Discovery (4 Modes)
User discovers their target question via one of four methods:

**Mode A: Direct Exploration (Tap)**
- User scrolls to Domain `7. Marriage (10 Questions)`.
- User taps to expand the accordion.
- User views the 10 child questions and taps `7.2 Marriage Timing`.

**Mode B: Search Resolution**
- User types "marriage" or "when will".
- The UI filters the 200+ list instantly.
- The Accordion auto-expands only the domains containing matching keywords.
- User taps the highlighted result.

**Mode C & D: Favorites & Recents**
- User switches to the "Recent" tab.
- User taps a previously asked question (e.g., `10.1 Career Growth`).

### Step 3: Selection Preview
Once a question card is tapped:
- The UI enters a "Selected" state.
- A sticky "Action Bar" appears at the bottom of the screen displaying the exact text of the chosen question.
- The user is given an opportunity to review the question before committing.

### Step 4: Submission & Execution
- User taps the prominent `[ ASK ]` button in the sticky action bar.
- The UI locks to prevent duplicate submissions.
- A loading overlay with astrological processing animations (e.g., spinning wheels or glowing constellations) appears.
- The frontend extracts the selected `question_id` (e.g., `MAR_TIMING_001`).
- The frontend dispatches the API request containing the `question_id` alongside the raw internal engine outputs (Dashas, Yogas, Promise).

### Step 5: Answer Rendering
- The backend evaluates the mathematical formulas mapped to the `question_id`.
- The LLM formats the deterministic mathematical booleans into a readable response.
- The UI transitions to the "Answer Screen".
- The mathematical synthesis (e.g., *Active dasha: Venus/Jupiter*) is displayed cleanly below the narrative answer.
