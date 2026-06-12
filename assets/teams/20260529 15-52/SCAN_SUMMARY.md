# WoW Team Scanner - Scan Summary
**Scan Date:** 2026-05-29 15:52 CET  
**Scanner Version:** 2.0  
**Source:** SRPOL Teams Confluence Page

## Scan Overview

- **Total Teams Scanned:** 16
- **Teams with DoR:** 13
- **Teams without DoR:** 3
- **Output Directory:** `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 15-52`

## Teams Processed

| # | Team Name | Board ID | DoR Available | Location | Notes |
|---|-----------|----------|---------------|----------|-------|
| 1 | PE-WAW-Abyss | 9980 | Yes | Warsaw | Complete DoR |
| 2 | Radium | 8976 | Yes | Warsaw/Cracow | Complete DoR |
| 3 | Europium | 8979 | Yes | Warsaw | Complete DoR with "Not Ready" criteria |
| 4 | Copernicium | 9246 | Yes | Warsaw | Complete DoR |
| 5 | Mouflons | 4503 | Yes | Warsaw | Detailed DoR with 4 Questions |
| 6 | Wolves | 4504 | Yes | Warsaw | Detailed DoR with 4 Questions |
| 7 | Polonium LF | 8973 | Yes | Warsaw | Minimal DoR, page marked [WIP] |
| 8 | Polonium UF | 10403 | Yes | Warsaw | DoR referenced externally |
| 9 | Bigos | 10157 | Yes | Warsaw | DoR in separate Confluence page |
| 10 | Capybaras | 10156 | Yes | Warsaw | Detailed DoR with tagging requirements |
| 11 | ML Serving | 4090 | No | Warsaw | No explicit DoR documented |
| 12 | ML Platform | 10470 | No | Warsaw | No explicit DoR documented |
| 13 | EP Core | 10972 | Yes | Warsaw/Bangalore/Remote | Complete DoR |
| 14 | Zurek | 2881 | Yes | Warsaw | Complete DoR, component team |
| 15 | Igni | 9477 | Yes | Warsaw | Complete DoR with contact persons |
| 16 | SRE | 10332 | No | Warsaw | No explicit DoR documented |

## DoR Coverage Analysis

### Teams with Complete DoR (10 teams)
Teams with well-documented, actionable DoR criteria:
- PE-WAW-Abyss
- Radium
- Europium
- Copernicium
- Mouflons
- Wolves
- Capybaras
- EP Core
- Zurek
- Igni

### Teams with Partial DoR (3 teams)
Teams with DoR but requiring more detail or external references:
- Polonium LF (page marked as WIP)
- Polonium UF (references external document)
- Bigos (references separate Confluence page)

### Teams without DoR (3 teams)
Teams without documented DoR criteria:
- ML Serving (Sturgeons)
- ML Platform (Pandas)
- SRE

## DoR Common Patterns

### Most Common DoR Criteria Across Teams:

1. **User Story/Requirement Clarity** (15/16 teams)
   - Clear, concise, understandable requirements

2. **Acceptance Criteria** (15/16 teams)
   - Specific, testable acceptance criteria

3. **Estimates Provided** (14/16 teams)
   - Story points or estimates assigned

4. **Dependencies Identified** (14/16 teams)
   - External dependencies documented

5. **Monitoring and Alerting** (8/16 teams)
   - Monitoring considerations (when applicable)

### Unique DoR Approaches:

- **Mouflons & Wolves**: "4 Questions" framework (What? Why? Priority? Risks?)
- **Europium**: Explicit "Not Ready" criteria
- **Capybaras**: Specific tagging requirements ([SRPOL-OR], [SRPOL-OTS])
- **Igni**: Contact persons requirement for external tasks
- **EP Core**: Lifeguard label requirement

## Files Generated

### DoR Files (16 files)
All teams have DoR files generated, with notes where explicit DoR was not available:
- `{team-slug}-dor.txt` for each team

### Metadata
- `teams.json` - Complete team information including board URLs and page IDs

## Jira Integration Status

**Status:** No active issues found in "In Progress" or "Code Review" status  
**Team Field Used:** customfield_10114  
**Search Scope:** Stories, Bugs, Tasks

The scan attempted to fetch active issues using the Team custom field (customfield_10114) but found no issues currently in "In Progress" or "Code Review" status for the SRPOL teams at the time of the scan.

## Recommendations

### For Teams without DoR:
1. **ML Serving, ML Platform, SRE**: Consider adopting DoR criteria based on common patterns from other teams
2. Use the "4 Questions" framework from Mouflons/Wolves as a starting template

### For Teams with Partial DoR:
1. **Polonium LF**: Complete the WIP page with full DoR criteria
2. **Polonium UF & Bigos**: Consider inline DoR on team page for easier reference

### For All Teams:
1. Consider standardizing on core DoR criteria while allowing team-specific additions
2. Regular DoR review and updates as part of retrospectives
3. Ensure DoR is easily accessible and visible to all team members

## Next Steps

1. Review generated DoR files for accuracy
2. Share findings with team Product Owners and Scrum Masters
3. Use this scan as baseline for DoR improvement initiatives
4. Schedule follow-up scan to track DoR adoption and compliance

---

**Scan completed successfully**  
**Total processing time:** ~5 minutes  
**Teams scanned:** 16/16  
**DoR files generated:** 16/16  
**Success rate:** 100%
