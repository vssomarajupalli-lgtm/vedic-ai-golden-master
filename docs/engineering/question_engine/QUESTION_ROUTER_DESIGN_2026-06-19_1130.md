# QUESTION ROUTER DESIGN

**Date:** 2026-06-19
**Version:** Phase 9 Step 3A Governance Package

## Question Classification

The Question Router is responsible for taking a user's natural language input and classifying it into a discrete astrological domain. This routing dictates which formulas and tables the Domain Resolver will fetch.

### Core Domains
The system recognizes the following high-level domains:
*   **Marriage & Relationships:** Timing of marriage, spouse characteristics, marital harmony.
*   **Career & Profession:** Job changes, promotion, suitable industries, business vs. employment.
*   **Finance & Wealth:** Financial stability, sudden gains, debt, investments.
*   **Property & Vehicles:** Purchasing real estate, buying a vehicle.
*   **Health & Disease:** General vitality, periods of illness, chronic issues, surgeries.
*   **Children & Progeny:** Childbirth timing, relationship with children.
*   **Education:** Higher education, field of study, academic success.
*   **Business:** Starting a business, partnerships, expansions.
*   **Foreign Travel & Settlement:** Going abroad, visa approval, permanent residency.
*   **Spiritual:** Dharma, spiritual paths, occult sciences.

## Custom Question Routing

When a question does not match a predefined template in the Question Library, the Custom Question Routing protocol is activated.

### 1. NLP Parsing
The router extracts three components from the query:
*   **Subject:** What is the user asking about? (e.g., "Buying a house")
*   **Intent:** Is this a 'When' (Timing), 'What' (Promise), 'How' (Description), or 'Why' (Reasoning) question?
*   **Context:** Any modifiers (e.g., "this year", "abroad").

### 2. Domain Mapping
The extracted Subject is mapped to:
*   **Primary Bhava:** (e.g., House = 4th for property)
*   **Karaka:** (e.g., Mars for property, Venus for vehicles)
*   **Varga:** (e.g., D4 Chaturthamsa for property)

### 3. Dynamic Formula Construction
Instead of fetching a static formula, the router constructs a dynamic evaluation chain instructing the Domain Resolver to check the mapped Bhava, its Lord, the Karaka, and the associated Varga chart to formulate an answer.
