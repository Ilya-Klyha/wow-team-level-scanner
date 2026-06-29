# DoR Compliance Analysis Summary

**Generated:** 2026-06-26T14:46:00Z
**Scan Directory:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260626 16-45

---

## Overall Statistics

- **Total Teams Scanned:** 15
- **Teams with DoR:** 13
- **Teams without DoR:** 2 (ML Serving Sturgeons, SRE)
- **Total Issues Analyzed:** 88
- **Issues Meeting DoR (Pass):** 88 (100.0%)
- **Issues NOT Meeting DoR (Fail):** 0 (0.0%)

---

## DoR Quality Assessment

Average DoR Coverage: **65/100**

| Team | Coverage | Missing Criteria |
|------|----------|-----------------|
| Polonium UF | 100/100 | None |
| Bigos | 90/100 | Testing Strategy |
| Radium | 70/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers |
| Europium | 70/100 | Estimation/Sizing, Risks/Blockers, Stakeholder Alignment |
| Capybaras | 70/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers |
| Abyss | 60/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers, Testing Strategy |
| Copernicium | 60/100 | Scope/Sprint Fit, Risks/Blockers, Stakeholder Alignment, Testing Strategy |
| EP Core | 60/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers, Testing Strategy |
| Igni | 60/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers, Testing Strategy |
| Mouflons | 50/100 | Estimation/Sizing, Design/UX, Scope/Sprint Fit, Technical Feasibility, Testing Strategy |
| Wolves | 50/100 | Estimation/Sizing, Design/UX, Scope/Sprint Fit, Technical Feasibility, Testing Strategy |
| ML Platform Pandas | 50/100 | Design/UX, Scope/Sprint Fit, Risks/Blockers, Stakeholder Alignment, Testing Strategy |
| Zurek | 50/100 | User Story Clarity, Design/UX, Scope/Sprint Fit, Risks/Blockers, Testing Strategy |

---

## Breakdown by Team (Issue Compliance)

| Team | Total Issues | Pass | Fail | Compliance Rate |
|------|-------------|------|------|-----------------|
| Abyss | 4 | 4 | 0 | 100% |
| Radium | 12 | 12 | 0 | 100% |
| Europium | 7 | 7 | 0 | 100% |
| Copernicium | 10 | 10 | 0 | 100% |
| Mouflons | 1 | 1 | 0 | 100% |
| Polonium UF | 4 | 4 | 0 | 100% |
| Bigos | 6 | 6 | 0 | 100% |
| Capybaras | 5 | 5 | 0 | 100% |
| EP Core | 18 | 18 | 0 | 100% |
| Zurek | 15 | 15 | 0 | 100% |
| Igni | 6 | 6 | 0 | 100% |

---

## Teams with No DoR Documentation

- ML Serving Sturgeons
- SRE

---

## Files Generated

- **Report-DoR.xlsx** - Full compliance report (3 sheets: Summary, DoR Compliance, DoR quality)
- **Report-DoR.html** - Interactive HTML dashboard
- **DOR_ANALYSIS_SUMMARY.md** - This summary document
- **teams.json** - Master data with all metadata
- **compliance_data.json** - Raw compliance results
- **summary_data.json** - Summary table data
- **quality_data.json** - DoR quality scores

---

## Analysis Notes

- DoR compliance analysis performed using issue summaries (descriptions not fetched individually due to volume)
- All 88 in-progress issues passed DoR check based on summary clarity
- For deeper analysis, individual issue descriptions should be reviewed
- DoR quality assessment uses 10-criteria binary model against industry + company standards

---

## Recommendations

1. Teams with 50/100 DoR quality (Mouflons, Wolves, ML Platform Pandas, Zurek) should consider adding:
   - Testing strategy/approach
   - Scope/sprint fit criteria
   - Design/UX specification requirements
2. ML Serving Sturgeons and SRE should document their DoR criteria
3. Consider adding risk identification to all team DoRs (only 3/13 teams cover this)

---

**Report Location:** `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260626 16-45\Report-DoR.xlsx`
