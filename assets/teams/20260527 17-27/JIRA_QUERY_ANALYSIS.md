# JIRA Query Analysis - SRPOL Teams
Generated: 2026-05-27

## Issue Identified
Previous extraction used incorrect status filter:
- INCORRECT: status IN ("In progress", "Code review")  
- CORRECT: status IN ("In Progress", "Code Review")

The case-sensitive difference caused all queries to return 0 results.

## Test Results (Using Correct Status)

### Project-Based Queries (WORKING)
- MAW (PE WAW Abyss): 17 issues found
- AENW (Radium + Europium): 33 issues found  
- AETVP (Copernicium): 16 issues found
- PEPI (Mouflons + Wolves + ML Serving): 0 issues (legitimately empty)

### Board-Based Queries (NOT WORKING)
- All board-based queries return 0 results
- Appears to be an API limitation or configuration issue
- Recommendation: Use project-based queries instead

## Recommended Approach

For each team, use project key instead of board ID:
```
project = {PROJECT_KEY} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)
```

## Team-to-Project Mapping

1. PE WAW Abyss → MAW (board 9980)
2. Radium → AENW (board 8976)
3. Europium → AENW (board 8979)  
4. Copernicium → AETVP (board 9246)
5. Mouflons → PEPI (board 4503)
6. Wolves → PEPI (board 4504)
7. Polonium LF → PEDSP (board 8973)
8. Polonium Upper Funnel → RSW (board 10403)
9. Bigos → RSW (board 10157)
10. Capybaras → RSW (board 10156)
11. ML Serving Sturgeons → PEPI (board 4090)
12. ML Platform Pandas → ML (board 10470)
13. EP Core → EPCW (board 10972)
14. Ads Reporting → NO BOARD
15. Igni → ASPW (board 9477)
16. SRPOL SRE → NO BOARD

## Issue: Shared Projects

Multiple teams share the same project key:
- AENW: Radium (board 8976) + Europium (board 8979)
- PEPI: Mouflons (4503) + Wolves (4504) + ML Serving (4090)
- RSW: Polonium Upper Funnel (10403) + Bigos (10157) + Capybaras (10156)

**Problem**: Project-based query cannot differentiate between teams on the same project.

**Solution**: Either:
1. Accept that teams sharing projects will see all project issues
2. Manually filter by assignee/component after fetching
3. Note in documentation that board-specific filtering is not available via API

## Status

DoR files: ✓ Complete (all extracted properly)
Jira files: ✗ Incomplete (need re-extraction with correct status and project-based queries)
