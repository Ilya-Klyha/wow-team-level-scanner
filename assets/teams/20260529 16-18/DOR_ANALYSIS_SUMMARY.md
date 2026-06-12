# DoR Analysis Summary

## Scan Metadata
- **Scan Date**: 2026-05-29 16:18 CET
- **Teams Scanned**: 16 SRPOL teams
- **Cloud ID**: adgear.atlassian.net
- **Scanner Version**: 2.0

## Overall Results
- **Total Active Issues Found**: 0
- **DoR Compliant Issues**: 0
- **DoR Non-Compliant Issues**: 0
- **Compliance Rate**: N/A (no active issues)

## Team Status Overview

### Teams with Active Issues
None - all teams have 0 active issues in "In Progress" or "Code Review" status.

### Teams Scanned (16 total)
1. **PE-WAW-Abyss** (AEMP) - 0 active issues
2. **Radium** (AENW) - 0 active issues
3. **Europium** (AENW) - 0 active issues
4. **Copernicium** (AETVP) - 0 active issues
5. **Mouflons** (AENW) - 0 active issues
6. **Wolves** (AENW) - 0 active issues
7. **Polonium LF** (AENW) - 0 active issues
8. **Polonium UF** (AENW) - 0 active issues
9. **Bigos** (PEA) - 0 active issues
10. **Capybaras** (PEPI) - 0 active issues
11. **ML Serving** (PEPI) - 0 active issues
12. **ML Platform** (PEPI) - 0 active issues
13. **EP Core** (EP) - 0 active issues
14. **Zurek** (PEA) - 0 active issues
15. **Igni** (AENW) - 0 active issues
16. **SRE** (PEES) - 0 active issues

## Query Details

All teams were queried using:
```jql
sprint in openSprints() AND project = [PROJECT] AND customfield_10114 ~ "[TEAM]" AND status IN ("In Progress", "Code Review")
```

**Status Filter**: "In Progress", "Code Review"
**Team Field**: customfield_10114 (Team custom field)

## Analysis Notes

This scan found **zero active issues** across all 16 SRPOL teams. This indicates that either:
- Teams are currently between sprints
- All in-progress work has been moved to other statuses
- Sprint planning is in progress
- It's outside of normal working hours

## DoR Files Status

All 16 teams have their DoR files extracted and saved:
- PE-WAW-Abyss: pe-waw-abyss-dor.txt (has DoR)
- Radium: radium-dor.txt (has DoR)
- Europium: europium-dor.txt (has DoR)
- Copernicium: copernicium-dor.txt (has DoR)
- Mouflons: mouflons-dor.txt (has DoR)
- Wolves: wolves-dor.txt (has DoR)
- Polonium LF: polonium-lf-dor.txt (minimal DoR)
- Polonium UF: polonium-uf-dor.txt (has DoR)
- Bigos: bigos-dor.txt (has DoR)
- Capybaras: capybaras-dor.txt (has DoR)
- ML Serving: ml-serving-dor.txt (no explicit DoR)
- ML Platform: ml-platform-dor.txt (no explicit DoR)
- EP Core: ep-core-dor.txt (has DoR)
- Zurek: zurek-dor.txt (has DoR)
- Igni: igni-dor.txt (has DoR)
- SRE: sre-dor.txt (no explicit DoR)

## Recommendations

1. **Re-run scan during working hours**: Execute the scan during peak development hours (10:00-16:00 CET) for more meaningful results
2. **Verify sprint status**: Check if teams are actively running sprints
3. **Expand status filter**: Consider including "To Do", "Selected for Development" for broader visibility
4. **Monitor trends**: Compare with previous scans to identify patterns

## Next Steps

- Schedule next scan for a time when active development is expected
- Review sprint calendars for all teams
- Consider automated scheduling during peak hours
- Archive this scan as a baseline for comparison

---

**Report Generated**: 2026-05-29 16:18:00 CET
**Output Directory**: C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260529 16-18
