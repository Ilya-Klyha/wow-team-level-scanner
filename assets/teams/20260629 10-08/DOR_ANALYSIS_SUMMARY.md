# DoR Analysis Summary

## Scan Details
- **Date**: 2026-06-29
- **Teams Analyzed**: 15
- **Teams with DoR**: 13 (86.7%)
- **Teams without DoR**: ML Serving Sturgeons, SRE

## DoR Compliance Results
- **Issues Analyzed**: 79
- **Pass**: 63 (79.7%)
- **Fail**: 16 (20.3%)

### Failure Breakdown by Team
| Team | Issues | Failures | Pass Rate |
|------|--------|----------|-----------|
| Radium | 12 | 5 | 58% |
| Zurek | 13 | 6 | 54% |
| Igni | 6 | 2 | 67% |
| Mouflons | 1 | 1 | 0% |
| Bigos | 6 | 1 | 83% |
| Polonium UF | 3 | 1 | 67% |

### Common Failure Reasons
1. **No description or description too brief** (AENW-910, AENW-913, AENW-906, AENW-796, PEA-4226) - Empty or minimal descriptions
2. **Missing Acceptance Criteria** (ASPW-386, ASPW-733, PEA-4160, PEA-4161, PEA-4215, PEA-4219) - Description exists but no identifiable AC
3. **Placeholder/TODO AC** (AENW-1015) - AC marked as needing update

## DoR Quality Assessment
- **Average Coverage**: 63/100
- **Highest**: Polonium UF (90), Bigos (90)
- **Lowest**: Mouflons (40), Wolves (40)

### Most Common Missing Criteria
1. Risks/Blockers Identified - missing in 10/13 teams
2. Design/UX Specification - missing in 8/13 teams
3. Scope/Sprint Fit - missing in 7/13 teams
4. Stakeholder Alignment - missing in 7/13 teams
5. Technical Feasibility Confirmed - missing in 6/13 teams
