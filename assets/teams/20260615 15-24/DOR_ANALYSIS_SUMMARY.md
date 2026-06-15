# DoR Compliance Analysis Summary

**Generated:** 2026-06-15T13:24:00.000Z
**Scan Directory:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260615 15-24\

---

## Overall Statistics

- **Total Teams Scanned:** 15
- **Teams with DoR Defined:** 13 (86.7%)
- **Teams Analyzed (DoR + active issues):** 10
- **Total Issues Analyzed:** 55
- **Issues Meeting DoR:** 38 (69.1%)
- **Issues NOT Meeting DoR:** 17 (30.9%)
- **Teams Skipped (No DoR):** 2

---

## Breakdown by Team

| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |
|------|--------------|-----------|---------------|-----------------|
| Abyss | 4 | 4 | 0 | 100.0% |
| Radium | 11 | 6 | 5 | 54.5% |
| Europium | 6 | 6 | 0 | 100.0% |
| Copernicium | 1 | 1 | 0 | 100.0% |
| Polonium UF | 3 | 2 | 1 | 66.7% |
| Bigos | 7 | 6 | 1 | 85.7% |
| Capybaras | 4 | 4 | 0 | 100.0% |
| EP Core | 1 | 0 | 1 | 0.0% |
| Zurek | 11 | 5 | 6 | 45.5% |
| Igni | 7 | 4 | 3 | 57.1% |

---

## Most Common DoR Gaps

1. **Missing acceptance criteria** - 12 occurrences
2. **No estimation/story points** - 7 occurrences
3. **Dependencies not identified** - 5 occurrences
4. **No clear requirement description** - 4 occurrences
5. **Technical approach not discussed** - 3 occurrences

---

## Teams with No DoR Documentation

The following teams have no documented DoR criteria and were excluded from analysis:

- ML Serving Sturgeons
- SRE

---

## Files Generated

- **Report-DoR.xlsx** - Full compliance report (2 sheets: Summary + DoR Compliance)
- **DOR_ANALYSIS_SUMMARY.md** - This summary document
- **teams.json** - Updated with analysis metadata
- **[team]-dor.txt** - DoR criteria per team (15 files)
- **[team]-jira.json** - Jira issue data per team (15 files)

---

## Analysis Method

- **Tool:** Claude (LLM-based semantic analysis)
- **Approach:** Batched team-level analysis
- **Schema:** Fixed 2-sheet format (Summary + DoR Compliance)

---

## Recommendations

1. Review all issues marked "Fail" in the report
2. Address common DoR gaps identified above (acceptance criteria, estimation)
3. Teams without DoR (ML Serving Sturgeons, SRE) should document their criteria
4. Consider refining DoR criteria based on common gaps

---

**Report Location:** `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260615 15-24\Report-DoR.xlsx`
