#!/usr/bin/env python3
"""
Update teams.json with complete metadata for all 16 teams.
"""

import json
import os
from datetime import datetime, timezone

OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 10-20"

# Complete team data (16 teams from SRPOL Teams page)
TEAMS = [
    {
        "name": "PE-WAW-Abyss",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/MAW/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980",
        "board_id": "9980",
        "project_key": "MAW",
        "dor_file": "pe-waw-abyss-dor.txt",
        "jira_json_file": "pe-waw-abyss-jira.json",
        "jira_txt_file": "pe-waw-abyss-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 14
    },
    {
        "name": "Radium",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/Radium/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/10077",
        "board_id": "10077",
        "project_key": "AENW",
        "dor_file": "radium-dor.txt",
        "jira_json_file": "radium-jira.json",
        "jira_txt_file": "radium-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 31
    },
    {
        "name": "Europium",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/EUROPIUM/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/10089",
        "board_id": "10089",
        "project_key": "AENW",
        "dor_file": "europium-dor.txt",
        "jira_json_file": "europium-jira.json",
        "jira_txt_file": "europium-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 31
    },
    {
        "name": "Copernicium",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/COPERNICIUM/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/10086",
        "board_id": "10086",
        "project_key": "AETVP",
        "dor_file": "copernicium-dor.txt",
        "jira_json_file": "copernicium-jira.json",
        "jira_txt_file": "copernicium-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 15
    },
    {
        "name": "Mouflons",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/MOUF/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/9972",
        "board_id": "9972",
        "project_key": "PEPI",
        "dor_file": "mouflons-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "mouflons-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "no_issues",
        "jira_issue_count": 0
    },
    {
        "name": "Wolves",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/WOLVES/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10090",
        "board_id": "10090",
        "project_key": "PEPI",
        "dor_file": "wolves-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "wolves-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "no_issues",
        "jira_issue_count": 0
    },
    {
        "name": "Polonium LF",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/POLONIUMLF/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEDSP/boards/9976",
        "board_id": "9976",
        "project_key": "PEDSP",
        "dor_file": "polonium-lf-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "polonium-lf-jira.txt",
        "extraction_status": "not_found",
        "dor_source": None,
        "jira_status": "no_issues",
        "jira_issue_count": 0
    },
    {
        "name": "Polonium UF",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/POLONIUMUF/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10093",
        "board_id": "10093",
        "project_key": "RSW",
        "dor_file": "polonium-uf-dor.txt",
        "jira_json_file": "polonium-uf-jira.json",
        "jira_txt_file": "polonium-uf-jira.txt",
        "extraction_status": "success",
        "dor_source": "linked_page",
        "jira_status": "success",
        "jira_issue_count": 35
    },
    {
        "name": "Bigos",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/BIGOS/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/10088",
        "board_id": "10088",
        "project_key": "PEA",
        "dor_file": "bigos-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "bigos-jira.txt",
        "extraction_status": "success",
        "dor_source": "linked_page",
        "jira_status": "no_issues",
        "jira_issue_count": 0
    },
    {
        "name": "Capybaras",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/CAPYBARAS/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156",
        "board_id": "10156",
        "project_key": "RSW",
        "dor_file": "capybaras-dor.txt",
        "jira_json_file": "capybaras-jira.json",
        "jira_txt_file": "capybaras-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 35
    },
    {
        "name": "ML Serving",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/MLS/overview",
        "sprint_board_link": None,
        "board_id": None,
        "project_key": None,
        "dor_file": "ml-serving-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "ml-serving-jira.txt",
        "extraction_status": "not_found",
        "dor_source": None,
        "jira_status": "no_board",
        "jira_issue_count": 0
    },
    {
        "name": "ML Platform",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/MLP/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ML/boards/10180",
        "board_id": "10180",
        "project_key": "ML",
        "dor_file": "ml-platform-dor.txt",
        "jira_json_file": "ml-platform-jira.json",
        "jira_txt_file": "ml-platform-jira.txt",
        "extraction_status": "not_found",
        "dor_source": None,
        "jira_status": "success",
        "jira_issue_count": 1
    },
    {
        "name": "Zurek",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ZUREK/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/10070",
        "board_id": "10070",
        "project_key": "PEA",
        "dor_file": "zurek-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "zurek-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "no_issues",
        "jira_issue_count": 0
    },
    {
        "name": "EP Core",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/EPCORE/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10148",
        "board_id": "10148",
        "project_key": "EPCW",
        "dor_file": "ep-core-dor.txt",
        "jira_json_file": "ep-core-jira.json",
        "jira_txt_file": "ep-core-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 26
    },
    {
        "name": "Igni",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/IGNI/overview",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/10079",
        "board_id": "10079",
        "project_key": "ASPW",
        "dor_file": "igni-dor.txt",
        "jira_json_file": "igni-jira.json",
        "jira_txt_file": "igni-jira.txt",
        "extraction_status": "success",
        "dor_source": "direct",
        "jira_status": "success",
        "jira_issue_count": 53
    },
    {
        "name": "SRE",
        "page_link": "https://adgear.atlassian.net/wiki/spaces/SRE/overview",
        "sprint_board_link": None,
        "board_id": None,
        "project_key": None,
        "dor_file": "sre-dor.txt",
        "jira_json_file": None,
        "jira_txt_file": "sre-jira.txt",
        "extraction_status": "not_found",
        "dor_source": None,
        "jira_status": "no_board",
        "jira_issue_count": 0
    }
]

def main():
    # Calculate statistics
    total_teams = len(TEAMS)
    teams_with_dor = sum(1 for t in TEAMS if t['extraction_status'] == 'success')
    teams_with_issues = sum(1 for t in TEAMS if t['jira_issue_count'] > 0)
    total_issues = sum(t['jira_issue_count'] for t in TEAMS)

    # Create teams.json structure
    teams_json = {
        "metadata": {
            "scan_date": datetime.now(timezone.utc).isoformat(),
            "scan_timestamp_cet": "20260528 10-20",
            "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
            "team_count": total_teams,
            "teams_with_dor": teams_with_dor,
            "teams_with_active_issues": teams_with_issues,
            "total_active_issues": total_issues,
            "cloudId": "adgear.atlassian.net",
            "scanner_version": "2.0"
        },
        "teams": TEAMS
    }

    # Write to file
    output_path = os.path.join(OUTPUT_DIR, 'teams.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(teams_json, f, indent=2, ensure_ascii=False)

    print('Updated teams.json successfully!')
    print(f'Total teams: {total_teams}')
    print(f'Teams with DoR: {teams_with_dor}')
    print(f'Teams with active issues: {teams_with_issues}')
    print(f'Total active issues: {total_issues}')

if __name__ == '__main__':
    main()
