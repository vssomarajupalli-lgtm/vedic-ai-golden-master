# YOGA_GOVERNANCE_v1

## Status

Approved Architecture

## Purpose

This document defines the governance rules for Yoga implementation within Vedic AI. It establishes Yoga as a detection and reporting layer, strictly isolating it from Promise scoring mechanics.

---

# ARCHITECTURE RULES

## 1. Yoga = Detection Layer
The Yoga Engine is fundamentally a detection and classification system. It analyzes planetary and house combinations to identify the presence of classical yogas. It does not calculate probabilities, strengths, or weights.

## 2. No Yoga Scoring
Yogas shall not output numeric scores. The result of a yoga evaluation is binary: Present or Absent.

## 3. No Yoga Bonuses
Yogas shall not apply mathematical bonuses to any engine.

## 4. No Yoga Penalties
Yogas shall not apply mathematical penalties to any engine.

## 5. Multi-Bhava Tagging Allowed
A single yoga can be mapped to multiple houses if the classical definition involves combinations across multiple bhavas.

## 6. Universal Yoga Category Allowed
Yogas that affect the entire chart (e.g., Gaja Kesari Yoga) can be tagged as "universal" rather than tied to a specific house.

## 7. Yoga Usage Scope
Yoga Engine outputs shall only be utilized by:
* Reporting and Explanation Layers
* Question Engine
* Frontend UI

Yoga outputs shall **never** be consumed by the NatalPromiseEngine or used to alter the Four Pillar Promise calculation.
