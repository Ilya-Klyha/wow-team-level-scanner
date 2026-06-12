#!/usr/bin/env python3
"""
Extract Jira data for all SRPOL teams with correct status filters
"""
import json
from datetime import datetime

# Team configuration: (team_name_kebab, jira_project_key, jira_board_id)
TEAMS = [
    ("pe-waw-abyss", "MAW", "9980"),
    ("radium", "AENW", "8976"),
    ("europium", "AENW", "8979"),
    ("copernicium", "AETVP", "9246"),
    ("mouflons", "PEPI", "4503"),
    ("wolves", "PEPI", "4504"),
    ("polonium-lf", "PEDSP", "8973"),
    ("polonium-upper-funnel", "RSW", "10403"),
    ("bigos", "RSW", "10157"),
    ("capybaras", "RSW", "10156"),
    ("ml-serving-sturgeons", "PEPI", "4090"),
    ("ml-platform-pandas", "ML", "10470"),
    ("ep-core", "EPCW", "10972"),
    ("ads-reporting-bigos-zurek", None, None),  # No board
    ("igni", "ASPW", "9477"),
    ("srpol-sre", None, None),  # No board
]

def generate_jql_query(project_key):
    """Generate JQL query using project key (not board)"""
    return f'project = {project_key} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)'

def main():
    print("JIRA Extraction Configuration")
    print("="*60)
    for team, project, board in TEAMS:
        if project:
            jql = generate_jql_query(project)
            print(f"\nTeam: {team}")
            print(f"  Project: {project}")
            print(f"  Board: {board}")
            print(f"  JQL: {jql}")
        else:
            print(f"\nTeam: {team}")
            print(f"  Status: NO BOARD - Skip Jira extraction")

if __name__ == "__main__":
    main()
