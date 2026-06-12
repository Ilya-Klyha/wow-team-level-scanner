# SRPOL Teams Extraction Summary

**Scan Date**: 2026-05-28 07:34:53 UTC (09:34 CET)  
**Source**: [SRPOL Teams Confluence Page](https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams)  
**Scanner Version**: 2.0

---

## Extraction Results

### Overall Statistics

- **Total Teams Found**: 16
- **DoR Extracted**: 11 teams
- **DoR Not Found**: 4 teams (Polonium LF, Polonium Upper Funnel, ML Serving, ML Platform)
- **Teams with Sprint Boards**: 15
- **Teams without Sprint Boards**: 1 (SRE)

---

## Teams Summary

### Teams with DoR - STORY/TASK Criteria

| # | Team Name | DoR Status | Jira Board | Active Issues |
|---|-----------|------------|------------|---------------|
| 1 | PE-WAW-Abyss | ✓ Extracted | Board 9980 (MAW) | 0 |
| 2 | Radium | ✓ Extracted | Board 8976 (AENW) | 0 |
| 3 | Europium | ✓ Extracted | Board 8979 (AENW) | 0 |
| 4 | Copernicium | ✓ Extracted | Board 9246 (AETVP) | 0 |
| 5 | Mouflons | ✓ Extracted | Board 4503 (PEPI) | 0 |
| 6 | Wolves | ✓ Extracted | Board 4504 (PEPI) | 0 |
| 7 | Bigos | ✓ Extracted | Board 10157 (RSW) | 0 |
| 8 | Capybaras | ✓ Extracted | Board 10156 (RSW) | 0 |
| 9 | WoW EP Core | ✓ Extracted | Board 10972 (EPCW) | 0 |
| 10 | Zurek | ✓ Extracted | Board 2881 (PEA) | 0 |
| 11 | Igni | ✓ Extracted | Board 9477 (ASPW) | 0 |

### Teams WITHOUT DoR - STORY/TASK Criteria

| # | Team Name | Reason | Jira Board |
|---|-----------|--------|------------|
| 1 | Polonium LF | DoR not documented | Board 8973 (PEDSP) |
| 2 | Polonium Upper Funnel | DoR links to external page | Board 10403 (RSW) |
| 3 | ML Serving (Sturgeons) | DoR not documented | Board 4090 (PEPI) |
| 4 | ML Platform (Pandas) | DoR not documented | Board 10470 (ML) |

### Teams WITHOUT Sprint Board

| # | Team Name | Note |
|---|-----------|------|
| 1 | SRE | No sprint board configured in SRPOL Teams page |

---

## DoR Content Analysis

### DoR Structure Patterns Observed

**Pattern 1: Detailed Criteria Tables** (PE-WAW-Abyss, Radium, Copernicium, Capybaras, Bigos)
- User Story/Requirement Clarity
- Acceptance Criteria and Measurement Defined
- Estimates Provided
- Dependencies
- Monitoring/Alerting (if applicable)

**Pattern 2: Principle-Based** (Mouflons, Wolves)
- Clear Description (with 4 questions: What, Why, Priority, Risks)
- Measurable/Verifiable Acceptance Criteria (SMART framework)
- Collaborative Progress

**Pattern 3: Simple Bullet Lists** (WoW EP Core, Zurek, Igni)
- Concise checklist format
- Focus on essential criteria only

**Pattern 4: Comprehensive with Edge Cases** (Europium)
- Includes "Not Ready if" conditions
- Explicit statement: "No work starts without meeting DoR (except production incidents)"

---

## Jira Extraction Results

### Active Issues Summary

**Query Parameters:**
- Status Filter: "In Progress", "Code Review"  
- Issue Types: Story, Bug, Task  
- Max Results per Board: 100

**Results:**
- All 15 boards queried returned **0 active issues**
- This suggests either:
  1. Teams currently have no work in these statuses (all work may be in To Do, Done, or other statuses)
  2. Sprint cycle timing (scan occurred between sprints)
  3. Different status naming conventions in use

**Note**: Status name variations were tested ("IN PROGRESS", "In progress", "CODE REVIEW", "Code review") with same results.

---

## Files Generated

### DoR Files (16 total)
```
pe-waw-abyss-dor.txt
radium-dor.txt
europium-dor.txt
copernicium-dor.txt
mouflons-dor.txt
wolves-dor.txt
polonium-lf-dor.txt (empty - not found)
polonium-upper-funnel-dor.txt (empty - not found)
bigos-dor.txt
capybaras-dor.txt
ml-serving-dor.txt (empty - not found)
ml-platform-dor.txt (empty - not found)
wow-team-ep-core-dor.txt
zurek-dor.txt
igni-dor.txt
```

### Metadata Files
- `teams.json` - Complete team metadata and extraction results
- `process_teams.py` - DoR extraction utilities
- `generate_jira_files.py` - Jira file generation script
- `EXTRACTION_SUMMARY.md` - This summary document

### Jira Files (Created)
- `pe-waw-abyss-jira.json` and `pe-waw-abyss-jira.txt`
- Additional Jira files can be generated using the Python script

---

## Recommendations

### For Teams Without DoR Documentation
1. **Polonium LF**: Document DoR - STORY/TASK criteria
2. **Polonium Upper Funnel**: Move DoR from external link to team page
3. **ML Serving (Sturgeons)**: Create DoR documentation
4. **ML Platform (Pandas)**: Create DoR documentation

### For DoR Content
1. Consider standardizing DoR format across teams
2. Teams using principle-based DoR should clarify specific criteria
3. Add "Definition of Ready - OFFERING/EPIC" where missing

### For Jira Integration
1. Verify correct status names for active work
2. Consider expanding status filters if teams use different workflow states
3. Schedule extraction during mid-sprint for better active issue visibility

---

## Technical Notes

- **HTML Parsing**: Extracted DoR content by searching for `<h2>`, `<h3>`, `<h4>` headings containing "DEFINITION OF READY" or "DoR"
- **Filtering**: Explicitly excluded "OFFERING/EPIC" sections to focus on STORY/TASK criteria only
- **Team Naming**: Cleaned team names by removing "Team", "Team Space", "Team Page" suffixes
- **Timestamp Format**: CET calculated as UTC+2 (DST active in May)

---

## Next Steps (Step 11: DoR Compliance Analysis)

**Status**: Not executed  
**Reason**: No active Jira issues found to analyze

To enable DoR compliance analysis:
1. Run extraction during active sprint work
2. Expand status filters to include more workflow states
3. Consider analyzing recently completed issues instead

---

**Generated by**: WoW Team Scanner v2.0  
**Scan Duration**: ~3 minutes  
**Output Directory**: `assets/teams/20260528 09-34/`
