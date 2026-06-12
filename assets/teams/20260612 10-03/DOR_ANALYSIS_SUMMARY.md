# DoR Compliance Analysis Summary

**Scan Date:** 2026-06-12
**Teams Analyzed:** 12 (of 15 total)
**Total Issues Analyzed:** 76
**Source:** SRPOL Teams Confluence Page

---

## Overall Compliance

| Metric | Value |
|--------|-------|
| Total Issues | 76 |
| DoR Compliant | 37 (48.7%) |
| Non-Compliant | 39 (51.3%) |
| Teams with 100% Compliance | 5 |
| Teams with 0% Compliance | 3 |

---

## Per-Team Breakdown

| Team | Issues | Compliant | Non-Compliant | Rate |
|------|--------|-----------|---------------|------|
| Abyss | 3 | 3 | 0 | 100% |
| Radium | 11 | 7 | 4 | 64% |
| Europium | 6 | 6 | 0 | 100% |
| Copernicium | 5 | 5 | 0 | 100% |
| Mouflons | 1 | 0 | 1 | 0% |
| Polonium Upper Funnel | 3 | 2 | 1 | 67% |
| Bigos | 7 | 6 | 1 | 86% |
| Capybaras | 5 | 5 | 0 | 100% |
| Sturgeons | 1 | 1 | 0 | 100% |
| EP Core | 16 | 2 | 14 | 12% |
| Ads Reporting | 11 | 0 | 11 | 0% |
| Igni | 7 | 0 | 7 | 0% |

---

## Teams Not Analyzed

| Team | Reason |
|------|--------|
| Wolves | Has DoR defined, 0 active issues |
| Pandas | Has DoR defined, 0 active issues |
| SRPOL SRE | No DoR defined |

---

## Common Gaps Identified

### 1. Missing Acceptance Criteria (Most Common - 35 of 39 non-compliant issues)
The most frequent DoR violation is the absence of explicit, testable acceptance criteria. Many tickets describe what needs to be done (task description) but lack clear conditions for acceptance (definition of done).

**Affected teams:** EP Core (14 issues), Ads Reporting (11 issues), Igni (7 issues), Radium (4 issues)

### 2. No Description Provided (2 issues)
Some tickets have completely empty descriptions, violating the most basic DoR requirement of requirement clarity.

**Affected issues:** AENW-906 (Radium), AENW-579 (Radium)

### 3. Missing Clear Definition of Done for Spikes/Investigations (3 issues)
Investigation and spike tickets sometimes lack measurable outcomes that would define when the task is complete.

**Affected teams:** Mouflons, Polonium Upper Funnel, Bigos

---

## Key Observations

1. **High-performing teams (100% compliance):** Abyss, Europium, Copernicium, Capybaras, and Sturgeons demonstrate consistent adherence to their DoR criteria with well-structured descriptions and clear acceptance criteria.

2. **Infrastructure/Platform teams struggle most:** EP Core (12%) has the lowest compliance among teams with multiple issues. Most EP Core tickets are infrastructure migration tasks that describe the work but lack explicit testable acceptance criteria.

3. **Ads Reporting (0% compliance):** All 11 issues from the Ads Reporting team lack explicit acceptance criteria. The ticket titles suggest well-scoped work items, but the descriptions do not include testable conditions for acceptance.

4. **Igni (0% compliance):** All 7 Igni issues lack acceptance criteria. Several appear to be operational/deployment tasks that would benefit from explicit success conditions.

5. **Pattern:** Teams working on product features (Abyss, Europium, Copernicium) tend to have better DoR compliance than teams doing infrastructure/platform work (EP Core, Ads Reporting).

---

## Recommendations

1. **Template enforcement:** Teams with low compliance should adopt ticket templates that include mandatory AC sections.
2. **Infrastructure task guidance:** Create guidelines specifically for infrastructure/migration tasks defining what constitutes proper acceptance criteria (e.g., "service accessible at URL X", "tests pass", "monitoring confirmed").
3. **Sprint planning gates:** Consider blocking tickets from entering sprints without AC during planning ceremonies.
4. **Celebrate high performers:** Abyss, Europium, Copernicium, Capybaras, and Sturgeons serve as good examples for other teams.
