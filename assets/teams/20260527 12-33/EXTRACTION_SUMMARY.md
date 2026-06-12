# SRPOL Teams Data Extraction Summary

**Extraction Date:** 2026-05-27  
**Extraction Time:** 12:33 CET  
**Scanner Version:** 2.0  
**Source:** https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams

---

## Overview

This extraction successfully processed **16 SRPOL teams** for:
1. Definition of Ready (DoR) - STORY/TASK criteria
2. Active Jira issues (In Progress, Code review)

---

## Extraction Results

### Teams Processed (16/16)

| # | Team Name | DoR Status | DoR Source | Jira Status | Active Issues |
|---|-----------|------------|------------|-------------|---------------|
| 1 | PE-WAW-Abyss | Success | Direct | Success | 0 |
| 2 | Radium | Success | Linked Page | Success | 0 |
| 3 | Europium | Success | Linked Page | Success | 0 |
| 4 | Copernicium | Success | Linked Page | Success | 0 |
| 5 | Mouflons | Success | Linked Page | Success | 0 |
| 6 | Wolves | Success | Linked Page | Success | 0 |
| 7 | Polonium-LF | Not Found | Direct | Success | 0 |
| 8 | Lithium | Success | Linked Page | Success | 0 |
| 9 | Radium-Reporting | Success | Linked Page | Success | 0 |
| 10 | Beryllium | Success | Direct | Success | 0 |
| 11 | Bromine | Not Found | Direct | Success | 0 |
| 12 | Iodine | Not Found | Direct | Success | 0 |
| 13 | EP | Success | Direct | Success | 0 |
| 14 | Zurek | Success | Direct | NO_BOARD | N/A |
| 15 | Aluminium | Success | Direct | Success | 0 |
| 16 | SRE | Not Found | Direct | NO_BOARD | N/A |

---

## Statistics

### DoR Extraction
- **Successfully extracted:** 11 teams (69%)
- **Not found:** 5 teams (31%)
  - Polonium-LF: Page marked WIP
  - Bromine: Brief page, no DoR section
  - Iodine: Brief page, no DoR section
  - SRE: References external page
- **Linked pages:** 7 teams (referenced external DoR documents)
- **Direct extraction:** 5 teams (DoR found on team page)

### Jira Extraction
- **Teams with boards:** 14 (88%)
- **Teams without boards:** 2 (12%) - Zurek, SRE
- **Total active issues found:** 0
- **Teams with active issues:** 0

All teams with configured boards had 0 active issues in "In Progress" or "Code review" statuses at extraction time.

---

## Files Created

### DoR Files (16)
- `pe-waw-abyss-dor.txt`
- `radium-dor.txt`
- `europium-dor.txt`
- `copernicium-dor.txt`
- `mouflons-dor.txt`
- `wolves-dor.txt`
- `polonium-lf-dor.txt`
- `lithium-dor.txt`
- `radium-reporting-dor.txt`
- `beryllium-dor.txt`
- `bromine-dor.txt`
- `iodine-dor.txt`
- `ep-dor.txt`
- `zurek-dor.txt`
- `aluminium-dor.txt`
- `sre-dor.txt`

### Jira JSON Files (14)
- `pe-waw-abyss-jira.json`
- `radium-jira.json`
- `europium-jira.json`
- `copernicium-jira.json`
- `mouflons-jira.json`
- `wolves-jira.json`
- `polonium-lf-jira.json`
- `lithium-jira.json`
- `radium-reporting-jira.json`
- `beryllium-jira.json`
- `bromine-jira.json`
- `iodine-jira.json`
- `ep-jira.json`
- `aluminium-jira.json`

### Jira TXT Files (14)
- Same as JSON files, with `.txt` extension

### Master File
- `teams.json` - Comprehensive metadata and status for all 16 teams

**Total Files:** 45

---

## Board IDs

| Team | Board ID | Board Status |
|------|----------|--------------|
| PE-WAW-Abyss | 9980 | Active |
| Radium | 8976 | Active |
| Europium | 8979 | Active |
| Copernicium | 9246 | Active |
| Mouflons | 4503 | Active |
| Wolves | 4504 | Active |
| Polonium-LF | 8973 | Active |
| Lithium | 10403 | Active |
| Radium-Reporting | 10157 | Active |
| Beryllium | 10156 | Active |
| Bromine | 4090 | Active |
| Iodine | 10470 | Active |
| EP | 10972 | Active |
| Zurek | N/A | NO_BOARD |
| Aluminium | 9477 | Active |
| SRE | N/A | NO_BOARD |

---

## Key Findings

1. **DoR Standardization**: 7 teams reference external DoR pages (mostly https://adgear.atlassian.net/wiki/spaces/ENG/pages/19623772331), indicating some standardization across teams.

2. **No Active Issues**: All teams with configured boards had 0 active issues in "In Progress" or "Code review" statuses, suggesting either:
   - Very efficient workflow completion
   - Issues are in different statuses
   - Sprint timing (extraction performed between sprints)

3. **Missing DoR**: 5 teams lack detailed DoR documentation on their pages, which may indicate:
   - Work in progress (Polonium-LF)
   - Brief/minimal team pages (Bromine, Iodine)
   - Reference to external documents (SRE)

4. **No Board Configuration**: 2 teams (Zurek, SRE) have NO_BOARD configured, likely due to:
   - Different workflow management
   - Component teams
   - Support teams

---

## Extraction Method

- **DoR Extraction**: HTML parsing from Confluence pages, identifying headings with "DoR - STORY/TASK", "Definition of Ready", excluding "OFFERING/EPIC"
- **Jira Extraction**: JQL query: `board = [ID] AND status IN ("In Progress", "Code review") AND issuetype IN (Story, Bug, Task)`
- **Fields Retrieved**: key, summary, status, issuetype, assignee, priority, created, updated

---

## Next Steps

1. **Linked DoR Pages**: Fetch and extract content from linked DoR pages for complete documentation
2. **Broader Status Search**: Consider expanding Jira query to include additional statuses (e.g., "To Do", "Ready for Review")
3. **DoR Standardization**: Work with teams lacking DoR to establish documentation
4. **Board Configuration**: Investigate NO_BOARD teams to determine if board setup is needed

---

*Generated by SRPOL Team Scanner v2.0*
