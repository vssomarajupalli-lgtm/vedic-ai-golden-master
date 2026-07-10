# CANONICAL JSON SCHEMA

## Purpose
This file defines how the Samrtha Astro-AI 2.0 engine reads the refined canonical JSON source file and converts it into internal calculation-ready objects.

## Source Confirmation
- The canonical JSON file is the final machine-readable source file.
- The engine must read all required data from this source file only.
- Manual separation of data for each calculation is not required.
- The parser layer must automatically identify and extract data using page number, section name, content block type, heading text, and table rows.
## Template Rule
- The canonical JSON file format is a reusable template used for multiple client profiles.
- The structural format remains the same across files.
- Client-specific values such as native name, date of birth, lagna, mahadasha, planetary data, divisional charts, and timelines change from file to file.
- The engine must never hardcode any client identity or astrological values.
- All calculations must be derived dynamically from the currently loaded canonical JSON file only.
## Batch Safety Rule
- When processing a new client canonical JSON file, the engine must fully clear all previous profile data, temporary calculations, cached values, and report layout objects before loading the next file.
- No client identity, birth constants, planetary values, dasha values, or prior output fragments may persist across file loops.
- Every file execution must start as a fresh isolated runtime pass.