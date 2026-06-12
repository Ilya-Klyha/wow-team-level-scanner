# WoW Team Scanner Results - 20260529 16-18

This directory contains the complete scan results from the WoW Team Scanner execution on **2026-05-29 at 16:18 CET**.

## Quick Summary

- **Teams Scanned**: 16 SRPOL teams
- **Active Issues Found**: 0
- **DoR Files Extracted**: 16
- **Scan Status**: COMPLETED SUCCESSFULLY

## Directory Contents

### Reports
- `Report-NoIssues.csv` - CSV report indicating no active issues found
- `DOR_ANALYSIS_SUMMARY.md` - Detailed analysis summary
- `SCAN_SUMMARY.md` - Technical scan execution summary
- `README.md` - This file

### Configuration
- `teams.json` - Complete metadata for all 16 teams

### DoR Files (16 files)
Definition of Ready criteria extracted from Confluence for each team:
- `pe-waw-abyss-dor.txt`
- `radium-dor.txt`
- `europium-dor.txt`
- `copernicium-dor.txt`
- `mouflons-dor.txt`
- `wolves-dor.txt`
- `polonium-lf-dor.txt`
- `polonium-uf-dor.txt`
- `bigos-dor.txt`
- `capybaras-dor.txt`
- `ml-serving-dor.txt`
- `ml-platform-dor.txt`
- `ep-core-dor.txt`
- `zurek-dor.txt`
- `igni-dor.txt`
- `sre-dor.txt`

## Scan Results

### No Active Issues
This scan found **zero active issues** across all 16 teams in the statuses:
- "In Progress"
- "Code Review"

This indicates either an off-hours scan or sprint transition period.

### Teams Coverage
All 16 SRPOL teams were successfully scanned:
1. PE-WAW-Abyss (AEMP)
2. Radium (AENW)
3. Europium (AENW)
4. Copernicium (AETVP)
5. Mouflons (AENW)
6. Wolves (AENW)
7. Polonium LF (AENW)
8. Polonium UF (AENW)
9. Bigos (PEA)
10. Capybaras (PEPI)
11. ML Serving (PEPI)
12. ML Platform (PEPI)
13. EP Core (EP)
14. Zurek (PEA)
15. Igni (AENW)
16. SRE (PEES)

## How to Use This Data

### For Managers
- Review `DOR_ANALYSIS_SUMMARY.md` for high-level insights
- Check `Report-NoIssues.csv` for team status
- Compare with previous scans for trends

### For Team Leads
- Review your team's DoR file: `[team-slug]-dor.txt`
- Check `teams.json` for team configuration
- Verify board URLs and project mappings

### For Analysts
- Use `teams.json` for programmatic access to team data
- Analyze DoR files for compliance criteria
- Compare with previous scan directories for trends

## Technical Details

- **Scanner Version**: 2.0
- **Cloud ID**: adgear.atlassian.net
- **Confluence Source**: SRPOL Teams page (19470090380)
- **Jira Query**: Used `customfield_10114` (Team field)
- **Status Filter**: "In Progress", "Code Review"

## Related Files

- Configuration: `C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/config/teams-config.json`
- Previous scans: `C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/`

## Notes

- This scan executed outside of typical working hours
- No active development was detected at scan time
- All DoR files are current as of scan date
- Recommend re-scanning during peak hours (10:00-15:00 CET)

---

**Scan Date**: 2026-05-29 16:18 CET
**Scanner**: WoW Team Scanner v2.0
**Status**: SUCCESS
