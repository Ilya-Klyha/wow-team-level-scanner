#!/usr/bin/env python3
"""
Generate metadata files: teams.json and DOR_ANALYSIS_SUMMARY.md
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Team info from previous scan
TEAMS = [
    {
        "id": 1,
        "name": "PE-WAW-Abyss",
        "slug": "pe-waw-abyss",
        "board_id": "9980",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AEMP/boards/9980",
        "page_id": "WID6RQU",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22648881240/PE+-+WAW+-+Abyss",
        "dor_file": "pe-waw-abyss-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AEMP",
        "jira_team_pattern": "Abyss"
    },
    {
        "id": 2,
        "name": "Radium",
        "slug": "radium",
        "board_id": "8976",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
        "page_id": "20720615642",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20720615642/Radium+Team+Space",
        "dor_file": "radium-dor.txt",
        "location": "Warsaw/Cracow",
        "has_dor": True,
        "project": "AENW",
        "jira_team_pattern": "AE - WAW - Radium"
    },
    {
        "id": 3,
        "name": "Europium",
        "slug": "europium",
        "board_id": "8979",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
        "page_id": "22431629392",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22431629392/Team+Europium",
        "dor_file": "europium-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AENW",
        "jira_team_pattern": "AP - WAW - Europium"
    },
    {
        "id": 4,
        "name": "Copernicium",
        "slug": "copernicium",
        "board_id": "9246",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246",
        "page_id": "20734247032",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20734247032/Copernicium+Team+Space",
        "dor_file": "copernicium-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AETVP",
        "jira_team_pattern": "AE - WAW - Copernicium"
    },
    {
        "id": 5,
        "name": "Mouflons",
        "slug": "mouflons",
        "board_id": "4503",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/4503",
        "page_id": "22381756417",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22381756417/Team+Mouflons",
        "dor_file": "mouflons-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AENW",
        "jira_team_pattern": "Mouflons"
    },
    {
        "id": 6,
        "name": "Wolves",
        "slug": "wolves",
        "board_id": "4504",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/4504",
        "page_id": "22374940673",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22374940673/Team+Wolves",
        "dor_file": "wolves-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AENW",
        "jira_team_pattern": "Wolves"
    },
    {
        "id": 7,
        "name": "Polonium LF",
        "slug": "polonium-lf",
        "board_id": "8973",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8973",
        "page_id": "22606054953",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606054953/Polonium+LF+WIP",
        "dor_file": "polonium-lf-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "notes": "Page marked as [WIP], minimal DoR info",
        "project": "AENW",
        "jira_team_pattern": "Polonium"
    },
    {
        "id": 8,
        "name": "Polonium UF",
        "slug": "polonium-uf",
        "board_id": "10403",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/10403",
        "page_id": "22606053416",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606053416/Polonium+Upper+Funnel+-+Team+page",
        "dor_file": "polonium-uf-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "notes": "DoR referenced externally",
        "project": "AENW",
        "jira_team_pattern": "Polonium"
    },
    {
        "id": 9,
        "name": "Bigos",
        "slug": "bigos",
        "board_id": "10157",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/10157",
        "page_id": "22695936064",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22695936064/Bigos+-+Team+page",
        "dor_file": "bigos-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "notes": "DoR in separate Confluence page",
        "project": "PEA",
        "jira_team_pattern": "Bigos"
    },
    {
        "id": 10,
        "name": "Capybaras",
        "slug": "capybaras",
        "board_id": "10156",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10156",
        "page_id": "22696132609",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22696132609/Capybaras+-+Team+page",
        "dor_file": "capybaras-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "PEPI",
        "jira_team_pattern": "Capybaras"
    },
    {
        "id": 11,
        "name": "ML Serving",
        "slug": "ml-serving",
        "board_id": "4090",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090",
        "page_id": "21732425749",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732425749/ML+Serving+Sturgeons",
        "dor_file": "ml-serving-dor.txt",
        "location": "Warsaw",
        "has_dor": False,
        "notes": "No explicit DoR documented",
        "project": "PEPI",
        "jira_team_pattern": "ML Serving"
    },
    {
        "id": 12,
        "name": "ML Platform",
        "slug": "ml-platform",
        "board_id": "10470",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10470",
        "page_id": "21732360213",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732360213/ML+Platform+Pandas",
        "dor_file": "ml-platform-dor.txt",
        "location": "Warsaw",
        "has_dor": False,
        "notes": "No explicit DoR documented",
        "project": "PEPI",
        "jira_team_pattern": "ML Platform"
    },
    {
        "id": 13,
        "name": "EP Core",
        "slug": "ep-core",
        "board_id": "10972",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/EP/boards/10972",
        "page_id": "22817472513",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22817472513/WoW+Team+EP+Core",
        "dor_file": "ep-core-dor.txt",
        "location": "Warsaw/Bangalore/Remote",
        "has_dor": True,
        "project": "EP",
        "jira_team_pattern": "EP Core"
    },
    {
        "id": 14,
        "name": "Zurek",
        "slug": "zurek",
        "board_id": "2881",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881",
        "page_id": "21748023571",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21748023571/Ads+Reporting+Bigos+Zurek",
        "dor_file": "zurek-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "notes": "Component team, part of Ads Reporting",
        "project": "PEA",
        "jira_team_pattern": "Zurek"
    },
    {
        "id": 15,
        "name": "Igni",
        "slug": "igni",
        "board_id": "9477",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/9477",
        "page_id": "22435922026",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22435922026/SRPOL+Team+-+Igni",
        "dor_file": "igni-dor.txt",
        "location": "Warsaw",
        "has_dor": True,
        "project": "AENW",
        "jira_team_pattern": "Igni"
    },
    {
        "id": 16,
        "name": "SRE",
        "slug": "sre",
        "board_id": "10332",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEES/boards/10332",
        "page_id": "22719529363",
        "page_url": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22719529363/Team+SRPOL+SRE",
        "dor_file": "sre-dor.txt",
        "location": "Warsaw",
        "has_dor": False,
        "notes": "No explicit DoR documented",
        "project": "PEES",
        "jira_team_pattern": "SRE"
    }
]

# Jira results from scan
JIRA_RESULTS = {
    "Radium": 12,
    "Europium": 3,
    "Copernicium": 5,
    "PE-WAW-Abyss": 0,
    "Mouflons": 0,
    "Wolves": 0,
    "Polonium LF": 0,
    "Polonium UF": 0,
    "Bigos": 0,
    "Capybaras": 0,
    "ML Serving": 0,
    "ML Platform": 0,
    "EP Core": 0,
    "Zurek": 0,
    "Igni": 0,
    "SRE": 0
}

def generate_teams_json(output_dir):
    """Generate teams.json with metadata"""

    # Add Jira extraction results to teams
    for team in TEAMS:
        issue_count = JIRA_RESULTS.get(team['name'], 0)
        team['jira_issues_count'] = issue_count
        team['jira_file'] = f"{team['slug']}-jira.json" if issue_count > 0 else None

    data = {
        "metadata": {
            "scan_date": "2026-05-29T16:28:35+02:00",
            "scan_timestamp_cet": "20260529 16-28",
            "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
            "team_count": 16,
            "cloudId": "adgear.atlassian.net",
            "scanner_version": "2.0",
            "jira_extraction_method": "project_query_with_client_side_team_filtering",
            "total_active_issues": sum(JIRA_RESULTS.values()),
            "teams_with_issues": len([c for c in JIRA_RESULTS.values() if c > 0])
        },
        "teams": TEAMS
    }

    output_file = os.path.join(output_dir, "teams.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Generated: {output_file}")

def generate_analysis_summary(output_dir):
    """Generate DOR_ANALYSIS_SUMMARY.md"""

    total_issues = sum(JIRA_RESULTS.values())
    teams_with_issues = len([c for c in JIRA_RESULTS.values() if c > 0])
    teams_with_dor = len([t for t in TEAMS if t['has_dor']])

    summary = f"""# DoR Compliance Analysis Summary

**Scan Date**: 2026-05-29 16:28 CET
**Scanner Version**: 2.0
**Source**: [SRPOL Teams](https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams)

---

## Overview

- **Total Teams Scanned**: {len(TEAMS)}
- **Teams with Documented DoR**: {teams_with_dor} ({teams_with_dor*100//len(TEAMS)}%)
- **Total Active Issues Analyzed**: {total_issues}
- **Teams with Active Issues**: {teams_with_issues}

---

## Active Issues by Team

| Team | Project | Active Issues | Has DoR |
|------|---------|---------------|---------|
"""

    for team in sorted(TEAMS, key=lambda t: JIRA_RESULTS.get(t['name'], 0), reverse=True):
        issue_count = JIRA_RESULTS.get(team['name'], 0)
        has_dor = "Yes" if team['has_dor'] else "No"
        summary += f"| {team['name']} | {team['project']} | {issue_count} | {has_dor} |\n"

    summary += f"""
---

## Key Findings

### Teams with Active Work (In Progress / Code Review)

1. **Radium** (AENW): 12 issues
   - Has documented DoR criteria
   - Located in Warsaw/Cracow

2. **Copernicium** (AETVP): 5 issues
   - Has documented DoR criteria
   - Located in Warsaw

3. **Europium** (AENW): 3 issues
   - Has documented DoR criteria
   - Located in Warsaw

### Teams with No Active Issues

{len(TEAMS) - teams_with_issues} teams currently have no issues in "In Progress" or "Code Review" status:
"""

    for team in TEAMS:
        if JIRA_RESULTS.get(team['name'], 0) == 0:
            summary += f"- {team['name']}\n"

    summary += f"""
---

## DoR Maturity Assessment

### Teams with Documented DoR ({teams_with_dor}/16)

Teams that have clear Definition of Ready - STORY/TASK criteria documented in their Confluence pages.

### Teams without Documented DoR ({len(TEAMS) - teams_with_dor}/16)

- ML Serving: No explicit DoR documented
- ML Platform: No explicit DoR documented
- SRE: No explicit DoR documented

**Recommendation**: These teams should consider establishing and documenting DoR criteria to improve story readiness and sprint planning quality.

---

## Methodology

### Jira Extraction

- **Query Strategy**: Project-level queries with client-side team filtering
- **Team Identification**: Using Jira custom field `customfield_10114` (Team)
- **Status Filter**: "In Progress" OR "Code Review"
- **Issue Types**: Story, Bug, Task
- **Projects Scanned**: AENW, AETVP, AEMP, PEA, PEPI, EP, PEES

### DoR Compliance Analysis

Each issue was analyzed against its team's DoR criteria:
- **Compliant**: Issue meets all documented DoR requirements
- **Non-Compliant**: Issue missing one or more DoR requirements
- **Feedback**: Specific guidance provided for non-compliant issues

---

## Files Generated

- `Report.xlsx` - Full DoR compliance report (9 columns, {total_issues} issues)
- `teams.json` - Complete team metadata with Jira extraction results
- `[team-name]-dor.txt` - DoR criteria for each team (16 files)
- `DOR_ANALYSIS_SUMMARY.md` - This summary document

---

**Generated by**: WoW Team Scanner v2.0
**Timestamp**: 2026-05-29 16:28:35 CET
"""

    output_file = os.path.join(output_dir, "DOR_ANALYSIS_SUMMARY.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"[SUCCESS] Generated: {output_file}")

if __name__ == "__main__":
    output_dir = Path(__file__).parent
    generate_teams_json(str(output_dir))
    generate_analysis_summary(str(output_dir))
    print("\n[COMPLETE] All metadata files generated")
