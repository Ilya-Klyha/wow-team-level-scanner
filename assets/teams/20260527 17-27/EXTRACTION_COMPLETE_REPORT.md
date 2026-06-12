# SRPOL Teams Data Extraction - Complete Report
Generated: 2026-05-27 (Final)

## Executive Summary

All 16 SRPOL teams have been processed. DoR (Definition of Ready) criteria extracted from Confluence pages. Jira data queried using corrected status filters.

## Key Findings

### 1. DoR Extraction: SUCCESS
- 12 teams have documented DoR criteria
- 4 teams have no DoR documentation (Polonium LF, ML Serving Sturgeons, ML Platform Pandas, SRPOL SRE)
- All DoR files created in output directory

### 2. Jira Extraction: COMPLETED (with corrections)

**Issue Discovered:** Previous extraction used incorrect case-sensitive status filter:
- WRONG: "In progress" 
- CORRECT: "In Progress"

**Corrected Results (using project-based queries):**

| Project | Teams | In Progress/Code Review Issues |
|---------|-------|-------------------------------|
| MAW | PE WAW Abyss | 17 |
| AENW | Radium + Europium | 33 |
| AETVP | Copernicium | 16 |
| PEPI | Mouflons + Wolves + ML Serving | 0 |
| PEDSP | Polonium LF | 0 |
| RSW | Polonium UF + Bigos + Capybaras | 47 |
| ML | ML Platform Pandas | 2 |
| EPCW | EP Core | 28 |
| ASPW | Igni | 61 |
| N/A | Ads Reporting | No board |
| N/A | SRPOL SRE | No board |

**TOTAL ACTIVE ISSUES FOUND: 204**

### 3. Technical Limitations Discovered

**Board-Based Queries Don't Work:**
- JQL queries using `board = {ID}` return 0 results
- Appears to be API limitation or permissions issue
- Workaround: Use project-based queries instead

**Shared Projects:**
Multiple teams share same Jira project:
- AENW: Radium (board 8976) + Europium (board 8979)
- PEPI: Mouflons (4503) + Wolves (4504) + ML Serving (4090)  
- RSW: Polonium UF (10403) + Bigos (10157) + Capybaras (10156)

Implication: Cannot differentiate issues by team when they share a project.

## Files Generated

### DoR Files (16 total)
```
pe-waw-abyss-dor.txt
radium-dor.txt
europium-dor.txt
copernicium-dor.txt
mouflons-dor.txt
wolves-dor.txt
polonium-lf-dor.txt (placeholder - no DoR found)
polonium-upper-funnel-dor.txt
bigos-dor.txt
capybaras-dor.txt
ml-serving-sturgeons-dor.txt (placeholder - no DoR found)
ml-platform-pandas-dor.txt (placeholder - no DoR found)
ep-core-dor.txt
ads-reporting-bigos-zurek-dor.txt
igni-dor.txt
srpol-sre-dor.txt (placeholder - no DoR found)
```

### Jira Files (14 teams with boards, 2 JSON + 2 TXT each = 28 files)
```
{team-name}-jira.json  (structured data)
{team-name}-jira.txt   (human-readable report)
```

### Metadata Files
```
teams.json                    - Master index of all teams
SCAN_SUMMARY.txt              - Original scan summary (outdated - used wrong status)
JIRA_QUERY_ANALYSIS.md        - Technical analysis of query issues
EXTRACTION_COMPLETE_REPORT.md - This file
```

## Recommendations

### For Future Extractions:
1. Always use `status IN ("In Progress", "Code Review")` with correct capitalization
2. Use project-based JQL queries, not board-based
3. Accept that teams sharing projects will see combined results
4. Query Confluence links found in DoR sections - some teams reference external pages

### For Consumers of This Data:
1. Teams with "placeholder" DoR files have no documented criteria
2. Teams sharing projects (AENW, PEPI, RSW) see combined Jira results
3. Zero issues doesn't mean no work - could be different workflow states
4. Teams without boards (Ads Reporting, SRPOL SRE) have no Jira data

## Confluence Page Links

Some teams reference external DoR pages:
- Polonium Upper Funnel: Links to https://adgear.atlassian.net/wiki/spaces/ENG/pages/19623772331
- Several teams follow similar patterns

## Status: EXTRACTION COMPLETE

- DoR: 16/16 teams processed
- Jira: 14/14 teams with boards queried (correct status filter applied)
- Metadata: Complete
- Analysis: Complete

All data successfully extracted to:
`C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260527 17-27\`
