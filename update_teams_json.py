#!/usr/bin/env python3
"""
Update teams.json with Jira extraction metadata.
"""

import json
import os
from pathlib import Path

# Output directory
OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 10-20"
TEAMS_JSON = os.path.join(OUTPUT_DIR, "teams.json")

# Team to project mapping
TEAM_PROJECT_MAPPING = {
    "PE-WAW-Abyss": "MAW",
    "Radium": "AENW",
    "Europium": "AENW",
    "Copernicium": "AETVP",
    "Mouflons": "PEPI",
    "Wolves": "PEPI",
    "Polonium LF": "PEDSP",
    "Polonium UF": "RSW",
    "Bigos": "RSW",
    "Capybaras": "RSW",
    "ML Serving": "PEPI",
    "ML Platform": "ML",
    "EP Core": "EPCW",
    "Zurek": "PEA",
    "Igni": "ASPW",
    "SRE": "EEEW"
}

def team_name_to_filename(team_name):
    """Convert team name to kebab-case filename."""
    return team_name.lower().replace(" ", "-").replace("_", "-")

def extract_board_id(sprint_board_link):
    """Extract board ID from sprint board URL."""
    if not sprint_board_link:
        return None
    try:
        # Pattern: .../boards/[BOARD_ID]
        return sprint_board_link.split("/boards/")[1].split("/")[0] if "/boards/" in sprint_board_link else None
    except:
        return None

def main():
    # Load teams.json
    with open(TEAMS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update each team with Jira metadata
    for team in data["teams"]:
        team_name = team["name"]
        filename_base = team_name_to_filename(team_name)
        jira_json_file = f"{filename_base}-jira.json"
        jira_txt_file = f"{filename_base}-jira.txt"
        jira_json_path = os.path.join(OUTPUT_DIR, jira_json_file)

        # Check if Jira file exists
        if os.path.exists(jira_json_path):
            # Read issue count from Jira JSON
            with open(jira_json_path, 'r', encoding='utf-8') as f:
                jira_data = json.load(f)
                issue_count = jira_data["metadata"]["issue_count"]

            team["jiraFile"] = jira_json_file
            team["jiraStatus"] = "success"
            team["jiraIssueCount"] = issue_count
            team["jiraBoardId"] = extract_board_id(team.get("sprint_board_link"))
            team["jiraProjectKey"] = TEAM_PROJECT_MAPPING.get(team_name)
            team["jiraError"] = None
            print(f"{team_name}: {issue_count} issues extracted")
        else:
            # No Jira file (0 issues or no board)
            if team.get("sprint_board_link"):
                # Has board but 0 issues
                team["jiraFile"] = None
                team["jiraStatus"] = "success"
                team["jiraIssueCount"] = 0
                team["jiraBoardId"] = extract_board_id(team.get("sprint_board_link"))
                team["jiraProjectKey"] = TEAM_PROJECT_MAPPING.get(team_name)
                team["jiraError"] = None
                print(f"{team_name}: 0 issues found")
            else:
                # No board configured
                team["jiraFile"] = None
                team["jiraStatus"] = "no_board"
                team["jiraIssueCount"] = 0
                team["jiraBoardId"] = None
                team["jiraProjectKey"] = None
                team["jiraError"] = "No sprint board link configured"
                print(f"{team_name}: No board configured")

    # Save updated teams.json
    with open(TEAMS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {TEAMS_JSON} with Jira metadata")

if __name__ == "__main__":
    main()
