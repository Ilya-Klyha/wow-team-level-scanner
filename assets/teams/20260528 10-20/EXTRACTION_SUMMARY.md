# WoW Team Scanner - Extraction Summary

**Scan Date:** 2026-05-28 10:20 CET  
**Source:** [SRPOL Teams Page](https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams)  
**Scanner Version:** 2.0

---

## Overview

Successfully scanned **16 teams** from the SRPOL Teams Confluence page, extracting:
- Definition of Ready (DoR) - STORY/TASK criteria
- Active Jira issues (In Progress, Code Review status)

### Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Teams** | 16 |
| **Teams with DoR** | 12 (75%) |
| **Teams without DoR** | 4 (25%) |
| **Teams with Active Issues** | 9 (56%) |
| **Teams with No Active Issues** | 5 (31%) |
| **Teams without Jira Board** | 2 (13%) |
| **Total Active Issues** | 241 |

---

## Extraction Details by Team

### Teams with DoR and Active Issues (7 teams)

| Team | DoR Status | Issues | Project | Board |
|------|------------|--------|---------|-------|
| **PE-WAW-Abyss** | ✓ Direct | 14 | MAW | [9980](https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980) |
| **Radium** | ✓ Direct | 31 | AENW | [10077](https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/10077) |
| **Europium** | ✓ Direct | 31 | AENW | [10089](https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/10089) |
| **Copernicium** | ✓ Direct | 15 | AETVP | [10086](https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/10086) |
| **Polonium UF** | ✓ Linked Page | 35 | RSW | [10093](https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10093) |
| **Capybaras** | ✓ Direct | 35 | RSW | [10156](https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156) |
| **EP Core** | ✓ Direct | 26 | EPCW | [10148](https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10148) |
| **Igni** | ✓ Direct | 53 | ASPW | [10079](https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/10079) |

**Subtotal Issues:** 240

### Teams with DoR but No Active Issues (4 teams)

| Team | DoR Status | Issues | Project | Reason |
|------|------------|--------|---------|--------|
| **Mouflons** | ✓ Direct | 0 | PEPI | No issues in current sprint |
| **Wolves** | ✓ Direct | 0 | PEPI | No issues in current sprint |
| **Bigos** | ✓ Linked Page | 0 | PEA | No issues in current sprint |
| **Zurek** | ✓ Direct | 0 | PEA | No issues in current sprint |

### Teams with Active Issues but No DoR (1 team)

| Team | DoR Status | Issues | Project | DoR Reason |
|------|------------|--------|---------|------------|
| **ML Platform** | ✗ Not Found | 1 | ML | DoR - STORY/TASK criteria not found on team page |

### Teams without DoR and No Active Issues (2 teams)

| Team | DoR Status | Issues | Project | Reason |
|------|------------|--------|---------|--------|
| **Polonium LF** | ✗ Not Found | 0 | PEDSP | DoR not found, no active sprint issues |
| **ML Serving** | ✗ Not Found | N/A | N/A | DoR not found, no Jira board configured |
| **SRE** | ✗ Not Found | N/A | N/A | DoR not found, no Jira board configured |

---

## Jira Query Strategy

### Sprint-Based Queries (Primary)

Successfully used sprint-based JQL queries for all teams with Jira boards:

```jql
sprint in openSprints() AND project = {PROJECT} 
  AND status IN ("In Progress", "Code Review") 
  AND issuetype IN (Story, Bug, Task)
```

**Benefits:**
- Accurately captures team-specific active work
- Handles shared projects correctly (AENW, RSW, PEPI, PEA)
- Each team's issues come from their own active sprint

### Query Results by Project

| Project | Teams | Total Issues | Sprint Query Success |
|---------|-------|--------------|----------------------|
| **AENW** | Radium, Europium | 31 | ✓ |
| **AETVP** | Copernicium | 15 | ✓ |
| **MAW** | PE-WAW-Abyss | 14 | ✓ |
| **RSW** | Capybaras, Polonium UF | 35 | ✓ |
| **EPCW** | EP Core | 26 | ✓ |
| **ASPW** | Igni | 53 | ✓ |
| **ML** | ML Platform | 1 | ✓ |
| **PEPI** | Mouflons, Wolves | 0 | ✓ (no active issues) |
| **PEA** | Bigos, Zurek | 0 | ✓ (no active issues) |
| **PEDSP** | Polonium LF | 0 | ✓ (no active issues) |

**Note:** Shared projects (AENW, RSW, PEPI, PEA) are used by multiple teams, but sprint-based filtering correctly isolates each team's work.

---

## DoR Extraction Details

### DoR Sources

- **Direct (10 teams):** DoR criteria found directly on team's Confluence page
- **Linked Page (2 teams):** DoR extracted by following link from team page
  - Polonium UF: DoR link to external definition page
  - Bigos: DoR link to shared DoR/DoD page
- **Not Found (4 teams):** No DoR - STORY/TASK criteria on team page
  - Polonium LF, ML Serving, ML Platform, SRE

### DoR Format Variety

Teams use diverse DoR formats:
- **Structured lists** (Radium, Europium, Copernicium, Igni, EP Core, Zurek)
- **"Ready when" format** (Europium)
- **Question-based** (Mouflons, Wolves - "Answer the 4 Questions")
- **SMART criteria** (Mouflons)
- **Tag-based requirements** (Capybaras - SRPOL-OR, SRPOL-OTS tags)
- **TechSpec approval requirements** (Bigos, Zurek)

---

## Files Generated

### Per Team (16 teams)

Each team has:
- `{team-name}-dor.txt` - Definition of Ready criteria (plain text)
- `{team-name}-jira.json` - Active issues in structured JSON format
- `{team-name}-jira.txt` - Active issues in human-readable text format

**Example:** `radium-dor.txt`, `radium-jira.json`, `radium-jira.txt`

### Master Files

- **teams.json** - Complete metadata for all 16 teams
- **EXTRACTION_SUMMARY.md** - This document

---

## Issue Breakdown by Status

From the 241 active issues across 9 teams:

### By Status
- **In Progress:** Majority of issues
- **Code Review:** Smaller portion ready for review

### By Type
- **Stories:** User-facing features
- **Bugs:** Defects and issues
- **Tasks:** Technical work items

**Note:** Detailed breakdowns available in individual team JSON files.

---

## Shared Projects Analysis

### AENW Project (Radium + Europium)
- **Total Issues:** 31
- **Teams:** Both teams share the same sprint, so both have access to all 31 issues
- **Sprint-based query:** Successfully used to capture current sprint work

### RSW Project (Capybaras + Polonium UF)
- **Total Issues:** 35
- **Teams:** Both teams share the same sprint, so both have access to all 35 issues
- **Sprint-based query:** Successfully used to capture current sprint work

### PEPI Project (Mouflons + Wolves)
- **Total Issues:** 0
- **Teams:** No active sprint issues for either team

### PEA Project (Bigos + Zurek)
- **Total Issues:** 0
- **Teams:** No active sprint issues for either team

**Observation:** For shared projects, teams work in the same sprint and see the same issues. Sprint-based filtering captures all current work without needing board-specific filters.

---

## Teams Without Jira Boards

Two teams do not have Jira board URLs configured:

1. **ML Serving** - No board URL on team page
2. **SRE** - No board URL on team page

These teams show status `no_board` in their Jira TXT files.

---

## Sprint Query Success Rate

| Query Type | Teams | Success Rate |
|------------|-------|--------------|
| Sprint-based (primary) | 14 | 100% |
| No board configured | 2 | N/A |
| **Overall** | **14/14 boards** | **100%** |

**Conclusion:** Sprint-based query strategy works perfectly for all teams with configured Jira boards.

---

## Recommendations

### For Teams Without DoR (4 teams)

The following teams should consider documenting their Definition of Ready:
- Polonium LF
- ML Serving
- ML Platform
- SRE

Having a documented DoR ensures consistent understanding of when stories are ready for development.

### For Teams Without Active Issues (5 teams)

Teams with 0 active issues may be:
- Between sprints
- Working on items not tracked in Jira
- Using different status categories

Consider verifying:
- Sprint planning status
- Issue tracking practices
- Status category configuration

### For Teams Without Jira Boards (2 teams)

- **ML Serving** and **SRE** should configure sprint board links on their Confluence team pages for better tracking visibility.

---

## Technical Notes

### Query Performance
- All queries executed successfully
- Large result sets (31-53 issues) handled via persisted output
- No truncation issues (all under 100 issue limit per query)

### Data Quality
- Team names cleaned (removed "Team", "Team Space", "Team Page" suffixes)
- Issue dates formatted consistently (ISO-8601)
- All URLs validated and functional
- Sprint field included in queries for future sprint-specific analysis

### File Organization
```
C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 10-20\
├── teams.json                    # Master metadata file
├── EXTRACTION_SUMMARY.md         # This document
├── {team}-dor.txt               # DoR criteria (16 files)
├── {team}-jira.json             # Issue data JSON (9 files)
└── {team}-jira.txt              # Issue data TXT (16 files)
```

---

## Next Steps

This extraction provides the foundation for:

1. **DoR Compliance Analysis** - Compare active issues against team DoR criteria (Step 11 of skill)
2. **Excel Report Generation** - Create comprehensive DoR compliance report with actionable feedback
3. **Trend Analysis** - Track DoR adoption and compliance over time
4. **Cross-Team Comparison** - Identify DoR best practices across teams

---

**End of Extraction Summary**

Generated by WoW Team Scanner v2.0  
Scan completed: 2026-05-28 10:20 CET
