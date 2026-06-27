# GOCHARA_TEST_CASES

## 1. PURPOSE
This file defines the validation cases for the gochara engine, scoring logic, and output formatting.

## 2. TEST INPUT RULE
All tests must use dynamic birth profile input.
Hardcoded identity values must not be used as production defaults.

## 3. DATE FORMAT TEST
Verify that all visible dates are rendered only in DD.MM.YYYY format.
Verify that ISO date strings such as YYYY-MM-DD do not appear in final output.

## 4. GOCHARA LOGIC TESTS
Test that:
* Moon nakshatra pada based logic is applied.
* Saturn-based micro gochara follows the authoritative master file.
* Elinati Shani periods are generated with valid start and end dates.
* Dasha-linked overlap windows are included.
* Present planetary transit coverage is complete.

## 5. STRENGTH TESTS
Test that:
* Planet strength scoring includes exaltation, own sign, moolatrikona, uchchabala, and swarashi bala.
* Bhava strength scoring is computed separately where required.
* Vargottama bonus is applied correctly.
* Final score never exceeds 100.

## 6. SUPPRESSION TEST
Verify that the following modules never appear in final output:
* Avakahada Chakra.
* Ghata Chakra.
* Panchadha Maitri Chakra.
* Jaimini Karakas.
* Jaimini Arudhas.

## 7. OUTPUT MODE TESTS
Test both:
* Split PDF mode.
* Single master PDF mode.

Verify that both modes begin with the birth details page and preserve page numbering rules.

## 8. JSON TESTS
Verify that the engine returns JSON-ready structured objects containing:
* Birth profile data.
* Transit snapshot.
* Strength values.
* Timeline windows.
* Report mode metadata.

## 9. NEGATIVE TESTS
Ensure the system does not:
* Show Null or None where a clean Telugu fallback is required.
* Break the template contract.
* Mix archive content into active engine output.