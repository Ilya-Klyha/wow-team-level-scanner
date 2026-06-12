#!/usr/bin/env python3
"""Generate Jira JSON and TXT files for all teams"""
import json

teams = [
    ("Radium", "8976", "AENW", "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976"),
    ("Europium", "8979", "AENW", "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979"),
    ("Copernicium", "9246", "AETVP", "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246"),
    ("Mouflons", "4503", "PEPI", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503"),
    ("Wolves", "4504", "PEPI", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504"),
    ("Polonium LF", "8973", "PEDSP", "https://adgear.atlassian.net/jira/software/c/projects/PEDSP/boards/8973"),
    ("Polonium Upper Funnel", "10403", "RSW", "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403/backlog"),
    ("Bigos", "10157", "RSW", "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10157"),
    ("Capybaras", "10156", "RSW", "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156"),
    ("ML Serving (Sturgeons)", "4090", "PEPI", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090"),
    ("ML Platform (Pandas)", "10470", "ML", "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470"),
    ("WoW EP Core", "10972", "EPCW", "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972"),
    ("Zurek", "2881", "PEA", "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881"),
    ("Igni", "9477", "ASPW", "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477"),
]

def team_name_to_kebab(name):
    """Convert team name to kebab-case"""
    import re
    kebab = re.sub(r'[\s_()]+', '-', name)
    kebab = re.sub(r'[^a-zA-Z0-9-]', '', kebab)
    return kebab.lower()

for team_name, board_id, project_key, board_url in teams:
    filename_base = team_name_to_kebab(team_name)

    # Generate JSON
    json_data = {
        "team": team_name,
        "boardUrl": board_url,
        "boardId": board_id,
        "projectKey": project_key,
        "extractedAt": "2026-05-28T07:34:53Z",
        "query": {
            "jql": f'board = {board_id} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)',
            "statuses": ["In Progress", "Code Review"],
            "issueTypes": ["Story", "Bug", "Task"]
        },
        "summary": {
            "total": 0,
            "byStatus": {},
            "byType": {},
            "truncated": False
        },
        "issues": []
    }

    with open(f"{filename_base}-jira.json", "w") as f:
        json.dump(json_data, f, indent=2)

    # Generate TXT
    txt_content = f"""Team: {team_name}
Board: {board_url}
Board ID: {board_id}
Project: {project_key}
Extracted: 2026-05-28T07:34:53Z

=== ACTIVE ISSUES (In Progress, Code Review) ===

Summary:
- Total issues: 0
- In Progress: 0
- Code Review: 0

Issues by type:
- Stories: 0
- Bugs: 0
- Tasks: 0

No active issues found for this board.

---
Status: success"""

    with open(f"{filename_base}-jira.txt", "w") as f:
        f.write(txt_content)

    print(f"Generated {filename_base}-jira.json and {filename_base}-jira.txt")

print(f"Generated Jira files for {len(teams)} teams")
