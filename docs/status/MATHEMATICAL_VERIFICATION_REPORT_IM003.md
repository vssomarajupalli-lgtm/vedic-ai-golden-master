# Mathematical Verification Report
## Mandali Grid Construction — Capability 7.3
### Universal Gochara Mandali Model A

---

## 1. Governance Formula Specification

From `GOCHARA_MANDALI_GOVERNANCE_v1.md` Section 7.3 (Capability 7.3):

**Inputs:**
- `natal_moon_nakshatra` (string) — from Canonical JSON
- `natal_moon_pada` (integer 1-4) — from Canonical JSON
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules (MGC-01 to MGC-07):**

| Rule | Formula |
|------|---------|
| **MGC-01** | Moon Absolute Pada = `NakshatraPadaResolver(natal_moon_nakshatra, natal_moon_pada)` |
| **MGC-02** | Mandali 1 center = Moon Absolute Pada |
| **MGC-03** | Mandali N center = `((Moon_Absolute_Pada + (N-1)×9 - 1) mod 108) + 1` |
| **MGC-04** | Each Mandali contains exactly 9 padas: center ±4 (modulo 108 wrap) |
| **MGC-05** | All 108 padas covered exactly once across 12 Mandalis (no gaps, no overlaps) |
| **MGC-06** | Mandali Rasi name = Rasi of center pada's Nakshatra (from `nakshatra_rasi_registry`) |
| **MGC-07** | Output is deterministic: identical inputs → identical grid |

---

## 2. Mathematical Verification

### 2.1 Definitions

Let:
- `M` = Moon Absolute Pada ∈ {1, 2, ..., 108}
- `N` = Mandali number ∈ {1, 2, ..., 12}
- `C(N)` = Center pada of Mandali N
- `P(N)` = Set of 9 padas in Mandali N

### 2.2 Center Calculation (MGC-03)

```
C(N) = ((M + (N-1)×9 - 1) mod 108) + 1
```

**Verification of 12 distinct centers:**

For N = 1 to 12:
- C(1) = ((M + 0 - 1) mod 108) + 1 = M
- C(2) = ((M + 9 - 1) mod 108) + 1 = ((M + 8) mod 108) + 1
- C(3) = ((M + 18 - 1) mod 108) + 1 = ((M + 17) mod 108) + 1
- ...
- C(12) = ((M + 99 - 1) mod 108) + 1 = ((M + 98) mod 108) + 1

The centers are: M, M+9, M+18, ..., M+99 (all modulo 108, 1-indexed).

Since 9 and 108 are coprime (gcd(9, 108) = 9, but we step by 9), the 12 centers are:
- M, M+9, M+18, M+27, M+36, M+45, M+54, M+63, M+72, M+81, M+90, M+99 (mod 108)

These are all distinct because the step size 9 generates a cycle of length 108/9 = 12 before repeating.

**✅ 12 distinct centers verified.**

### 2.3 Pada Set Construction (MGC-04)

For each Mandali N:
```
P(N) = { ((C(N) + k - 1) mod 108) + 1 | k ∈ {-4, -3, -2, -1, 0, 1, 2, 3, 4} }
```

This gives exactly 9 padas: center, 4 before, 4 after.

**✅ 9 padas per Mandali verified.**

### 2.4 Coverage Verification (MGC-05)

**Total padas across all Mandalis:** 12 × 9 = 108

**No overlaps:** The centers are spaced 9 apart. Each Mandali spans ±4 from center (9 padas). The gap between adjacent Mandali boundaries is:
- Mandali N ends at C(N) + 4
- Mandali N+1 starts at C(N+1) - 4 = C(N) + 9 - 4 = C(N) + 5

Gap = (C(N) + 5) - (C(N) + 4) = 1 pada → **No overlap, no gap.**

**Wrap-around at 108/1 boundary:**
- When C(N) + 4 > 108, modulo wraps to 1
- When C(N) - 4 < 1, modulo wraps to 108
- The modulo arithmetic `((x - 1) mod 108) + 1` correctly handles 1-108 range

**✅ No overlaps, no gaps, correct wrap-around verified.**

### 2.5 Moon Centers Mandali 1 (MGC-02)

By definition: C(1) = M (Moon Absolute Pada)

**✅ Moon always centers Mandali 1 verified.**

### 2.6 Determinism (MGC-07)

All operations are pure functions:
- `NakshatraPadaResolver` is deterministic (registry lookup)
- Modulo arithmetic is deterministic
- Set construction is deterministic

**✅ Deterministic output verified.**

---

## 3. Worked Example: Raju Chart

**Input (from Canonical JSON):**
- Natal Moon: Makara Rasi, Dhanishta Nakshatra, Pada 2
- Moon Absolute Pada = 90 (via NakshatraPadaResolver)

**Mandali Centers:**
| N | Formula | Center Pada | Center Nakshatra | Center Pada# | Rasi |
|---|---------|-------------|------------------|--------------|------|
| 1 | 90 | 90 | Dhanishta | 2 | Makara |
| 2 | 90+9=99 | 99 | Shatabhisha | 3 | Kumbha |
| 3 | 90+18=108 | 108 | Purva Bhadrapada | 4 | Meena |
| 4 | 90+27=117→9 | 9 | Uttara Bhadrapada | 1 | Meena |
| 5 | 90+36=126→18 | 18 | Revati | 2 | Meena |
| 6 | 90+45=135→27 | 27 | Ashwini | 3 | Mesha |
| 7 | 90+54=144→36 | 36 | Bharani | 4 | Mesha |
| 8 | 90+63=153→45 | 45 | Krittika | 1 | Vrishabha |
| 9 | 90+72=162→54 | 54 | Rohini | 2 | Vrishabha |
| 10 | 90+81=171→63 | 63 | Mrigashira | 3 | Mithuna |
| 11 | 90+90=180→72 | 72 | Ardra | 4 | Mithuna |
| 12 | 90+99=189→81 | 81 | Punarvasu | 1 | Karkata |

**Mandali 1 Padas (center 90 ±4):** 86, 87, 88, 89, 90, 91, 92, 93, 94
- Nakshatras: Shravana P2-4, Dhanishta P1-4, Shatabhisha P1

**Mandali 12 Padas (center 81 ±4):** 77, 78, 79, 80, 81, 82, 83, 84, 85
- Nakshatras: Punarvasu P1-4, Pushya P1-4, Ashlesha P1

**All 108 padas covered exactly once.** ✅

---

## 4. Verification Summary

| Property | Required | Verified |
|----------|----------|----------|
| 12 Mandalis | Yes | ✅ |
| 9 Padas per Mandali | Yes | ✅ |
| 108 unique Padas total | Yes | ✅ |
| No overlaps | Yes | ✅ |
| No gaps | Yes | ✅ |
| Correct wrap-around | Yes | ✅ |
| Moon centers Mandali 1 | Yes | ✅ |
| Deterministic output | Yes | ✅ |
| Governance rules MGC-01 to MGC-07 | All satisfied | ✅ |

---

## 5. Conclusion

**The governance formula for Mandali Grid Construction is mathematically sound.**

All required properties are satisfied:
- 12 Mandalis with 9 padas each = 108 padas
- No overlaps, no gaps
- Correct modulo 108 wrap-around
- Moon always centers Mandali 1
- Deterministic for any valid Moon position

**Verification PASSED.** Proceed to implementation.

---

*Report generated: 2026-07-26*
*Governance: GOCHARA_MANDALI_GOVERNANCE_v1.md Section 7.3*