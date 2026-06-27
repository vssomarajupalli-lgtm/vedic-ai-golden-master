# QUESTION BROWSER UI BLUEPRINT v1

## 1. Design Philosophy
The Question Browser is designed with a **Mobile-First** approach. It replaces an ambiguous open text field with a deterministic, easily navigable directory of 200+ astrological questions grouped by 24 Master Domains. 

### Core Accessibility Tenets
- **Large Touch Targets:** Minimum 44x44pt click areas for elder-friendly navigation.
- **Readable Typography:** High-contrast fonts with sans-serif dominance (e.g., Inter, Roboto).
- **Low Cognitive Load:** Grouping complex Vedic astrology queries under universally understood life domains.

---

## 2. Screen Layout & Wireframes

### 2.1 Mobile Wireframe Concept
On mobile, vertical real estate is paramount. The layout stacks components sequentially.

```text
[ Sticky Header: "Ask the Stars" ]
----------------------------------
[ Search Bar: "e.g., Marriage" ]
----------------------------------
[ Horizontal Scroll Tabs: ]
[ Favorites ] [ Recent ] [ Browse All ]
----------------------------------
[ Accordion List - Collapsed ]
  ▶ 1. Self & Personality (8)
  ▶ 2. Wealth & Family    (8)
  ▼ 7. Marriage          (10)
    [ 7.1 Marriage Prospects ]
    [ 7.2 Marriage Timing    ]
    [ 7.3 Delay in Marriage  ]
  ▶ 10. Career           (12)
----------------------------------
[ Floating Action Button (FAB) or Sticky Bottom Sheet ]
[ Selected: 7.2 Marriage Timing ]
[         [ ASK QUESTION ]      ]
```

### 2.2 Desktop Wireframe Concept
On desktop, the interface utilizes a two-pane layout to minimize vertical scrolling and leverage horizontal space.

```text
[ Header: "Question Engine" ]
---------------------------------------------------------
| SIDEBAR: NAVIGATION     | MAIN PANEL: SELECTION       |
| [ Search Bar ]          |                             |
|                         | [ Selected Domain Title ]   |
| 1. Self & Personality   |                             |
| 2. Wealth & Family      | [ Question Card 7.1 ]       |
| ...                     | [ Question Card 7.2 ]       |
| 7. Marriage (10) <---   | [ Question Card 7.3 ]       |
| ...                     |                             |
| 10. Career (12)         |                             |
|                         |                             |
|-------------------------------------------------------|
| STICKY FOOTER: [ Selected: 7.2 Marriage Timing ] [ASK]|
---------------------------------------------------------
```

---

## 3. UI Component Specifications

### 3.1 Search Bar
- **Placeholder:** "Search for questions, keywords, or topics..."
- **Behavior:** Live filtering. As the user types, the accordion expands automatically to show matching child questions, hiding non-matching domains.

### 3.2 Accordion Domains (The Browse List)
- **Header Format:** `[Domain Name] ([Question Count])` - e.g., *Marriage (10 Questions)*.
- **Iconography:** Include a subtle icon next to each domain (e.g., rings for marriage, briefcase for career) to improve visual scanning.
- **Behavior:** Tapping a domain expands it, smoothly pushing content down.

### 3.3 Question Cards / List Items
- **Format:** Clean, padded rows containing the child question.
- **Selection State:** When tapped, the card highlights (background color changes, border stroke activates) to indicate it is the active selection.

### 3.4 Favorites & Recent Sections
- **Location:** Pinned to the top of the browser or available via a segmented control tab.
- **Behavior:** Stores the `question_id` locally. Displays the most frequently or recently queried endpoints for quick access.

### 3.5 Selected Question Panel & Ask Button
- **Location:** Sticky at the bottom of the viewport (mobile) or bottom of the pane (desktop).
- **Format:** Shows the currently highlighted question text.
- **Action:** Tapping "Ask" locks the UI, renders a loading spinner, and dispatches the payload to the backend API.
