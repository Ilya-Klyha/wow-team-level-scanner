# DoR Compliance Analysis Summary

**Generated:** 2026-06-18T12:01:00+02:00
**Scan Directory:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260618 12-01

---

## Overall Statistics

- **Total Teams Scanned:** 15
- **Teams with DoR:** 13
- **Teams without DoR:** 2
- **Total Issues Analyzed:** 23
- **Issues Meeting DoR (Pass):** 9 (39.1%)
- **Issues NOT Meeting DoR (Fail):** 14 (60.9%)

---

## Breakdown by Team

| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |
|------|--------------|-----------|---------------|-----------------|
| Abyss | 3 | 3 | 0 | 100.0% |
| Radium | 3 | 0 | 3 | 0.0% |
| Europium | 1 | 0 | 1 | 0.0% |
| Copernicium | 7 | 4 | 3 | 57.1% |
| Polonium UF | 2 | 0 | 2 | 0.0% |
| Bigos | 6 | 2 | 4 | 33.3% |
| Capybaras | 1 | 0 | 1 | 0.0% |

---

## Most Common DoR Gaps

1. **DoR criterion 'Clear & testable Acceptance Criteria': no AC with feature flag/release env info** - 4 occurrences
2. **DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC found** - 3 occurrences
3. **DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC provided** - 3 occurrences
4. **DoR criterion 'Clear Acceptance Criteria': no AC provided** - 2 occurrences
5. **DoR criterion 'Acceptance criteria are defined and testable': no AC found** - 1 occurrences

---

## Teams with No DoR Documentation

The following teams have no documented DoR criteria and were excluded from analysis:

- ML Serving Sturgeons
- SRE

---

## DoR Quality Assessment

Average DoR Coverage: 70/100

| Team | Coverage | Missing |
|------|----------|---------|
| Bigos | 100/100 | All standard criteria covered |
| Radium | 80/100 | Missing: Risks/Blockers Identified, Technical Feasibility Confirmed |
| Europium | 80/100 | Missing: Estimation/Sizing, Risks/Blockers Identified |
| Polonium UF | 80/100 | Missing: User Story/Requirement Clarity, Stakeholder Alignment |
| Copernicium | 70/100 | Missing: Scope/Sprint Fit, Risks/Blockers Identified, Technical Feasibility Confirmed |
| EP Core | 70/100 | Missing: Design/UX Specification, Scope/Sprint Fit, Stakeholder Alignment |
| Igni | 70/100 | Missing: Design/UX Specification, Scope/Sprint Fit, Risks/Blockers Identified |
| Abyss | 60/100 | Missing: Design/UX Specification, Risks/Blockers Identified, Stakeholder Alignment, Technical Feasibility Confirmed |
| Mouflons | 60/100 | Missing: Estimation/Sizing, Design/UX Specification, Scope/Sprint Fit, Testing Strategy/Approach |
| Wolves | 60/100 | Missing: Estimation/Sizing, Design/UX Specification, Scope/Sprint Fit, Testing Strategy/Approach |
| Capybaras | 60/100 | Missing: Design/UX Specification, Risks/Blockers Identified, Stakeholder Alignment, Technical Feasibility Confirmed |
| ML Platform Pandas | 60/100 | Missing: Design/UX Specification, Scope/Sprint Fit, Risks/Blockers Identified, Technical Feasibility Confirmed |
| Zurek | 60/100 | Missing: Design/UX Specification, Scope/Sprint Fit, Stakeholder Alignment, Testing Strategy/Approach |

---

## Files Generated

- **Report-DoR.xlsx** - Full compliance report (3 sheets: Summary, DoR Compliance, DoR quality)
- **DOR_ANALYSIS_SUMMARY.md** - This summary document
- **teams.json** - Updated with analysis metadata

---

## Analysis Method

- **Tool:** Claude Opus 4.6 (LLM-based semantic analysis)
- **Approach:** Batched team-level analysis with local team field filtering
- **Date:** 2026-06-18

---

## Recommendations

1. Review all issues marked "Fail" in the report
2. Address common DoR gaps identified above
3. Teams without DoR (ML Serving Sturgeons, SRE) should document their criteria
4. Consider refining DoR criteria based on common gaps

---

**Report Location:** `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260618 12-01/Report-DoR.xlsx`
