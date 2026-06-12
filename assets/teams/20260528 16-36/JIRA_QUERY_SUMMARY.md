# Jira Query Summary Report

**Scan Date:** 2026-05-28  
**Scan Time:** 16:36 CET  
**Output Directory:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 16-36

---

## Overview

Successfully queried Jira for active issues (In Progress, Code Review) across all 16 SRPOL teams.

**Query Strategy:** Sprint-based (sprint in openSprints())  
**Statuses Filtered:** In Progress, Code Review  
**Issue Types:** Story, Bug, Task  
**Total Files Created:** 32 (16 JSON + 16 TXT)

---

## Team-by-Team Results

| # | Team | Project Key | Board ID | Issues Found | Status |
|---|------|-------------|----------|--------------|--------|
| 1 | PE-WAW-Abyss | MAW | 9980 | 15 | success |
| 2 | Radium | AENW | 8976 | 16 | success |
| 3 | Europium | AENW | 8979 | 17 | success |
| 4 | Copernicium | AETVP | 9246 | 15 | success |
| 5 | Mouflons | PEPI | 4503 | 0 | success |
| 6 | Wolves | PEPI | 4504 | 0 | success |
| 7 | Polonium LF | PEDSP | 8973 | 0 | success |
| 8 | Polonium UF | RSW | 10403 | 11 | success |
| 9 | Bigos | RSW | 10157 | 16 | success |
| 10 | Capybaras | RSW | 10156 | 8 | success |
| 11 | ML Serving | PEPI | 4090 | 0 | success |
| 12 | ML Platform | ML | 10470 | 1 | success |
| 13 | EP Core | EPCW | 10972 | 25 | success |
| 14 | Zurek | PEA | 2881 | 0 | success |
| 15 | Igni | ASPW | 9477 | 53 | success |
| 16 | SRE | EEEW | 10332 | 19 | success |

**Total Issues Found:** 196 active issues across all teams

---

## Statistics

- **Teams with Active Issues:** 11 teams (68.75%)
- **Teams with Zero Issues:** 5 teams (31.25%)
- **Average Issues per Team:** 12.25
- **Busiest Team:** Igni (53 issues)
- **Projects Queried:** 9 unique Jira projects

### Breakdown by Project

| Project Key | Teams Using | Total Issues |
|-------------|-------------|--------------|
| ASPW | 1 (Igni) | 53 |
| AENW | 2 (Radium, Europium) | 33 |
| EPCW | 1 (EP Core) | 25 |
| EEEW | 1 (SRE) | 19 |
| RSW | 3 (Polonium UF, Bigos, Capybaras) | 35 |
| MAW | 1 (PE-WAW-Abyss) | 15 |
| AETVP | 1 (Copernicium) | 15 |
| PEPI | 3 (Mouflons, Wolves, ML Serving) | 0 |
| PEDSP | 1 (Polonium LF) | 0 |
| PEA | 1 (Zurek) | 0 |
| ML | 1 (ML Platform) | 1 |

---

## Files Created

Each team has two output files:

1. **{team-name-kebab}-jira.json** - Machine-readable JSON with full issue data
2. **{team-name-kebab}-jira.txt** - Human-readable report format

### File Structure

**JSON File Contents:**
- Team metadata (name, board URL, project key)
- Query information (JQL, query type, timestamp)
- Summary statistics (total, by status, by type)
- Full issue details (key, type, summary, status, assignee, priority, dates, URL)

**TXT File Contents:**
- Header with team information
- Summary statistics
- Detailed issue list with all fields

---

## Integration with teams.json

The main teams.json file has been updated with Jira metadata for each team:

- `jiraFile`: Filename of the JSON output
- `jiraStatus`: Query execution status (success)
- `jiraIssueCount`: Number of active issues found

---

## Query Details

**JQL Template Used:**
```
sprint in openSprints() AND project = {PROJECT_KEY} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)
```

**Fields Requested:**
- key
- summary
- status
- issuetype
- assignee
- priority
- created
- updated

**CloudId:** adgear.atlassian.net  
**Max Results per Query:** 100

---

## Notes

1. Teams sharing the same project (AENW, RSW, PEPI) were queried together and issues distributed based on board assignment logic.

2. Five teams currently have zero active issues in the sprint. This could indicate:
   - Sprint has not started yet
   - All work completed
   - Team uses different status values
   - Team not actively using Jira sprints

3. All queries executed successfully with no errors or timeouts.

4. Data extracted matches the sprint state as of 2026-05-28 16:36 CET.

---

**Processing Complete**  
All 16 teams successfully queried and documented.
