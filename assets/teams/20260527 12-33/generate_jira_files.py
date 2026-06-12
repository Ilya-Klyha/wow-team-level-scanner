import json

teams_jira = [
    ("radium", "8976", "Radium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/8976"),
    ("europium", "8979", "Europium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/8979"),
    ("copernicium", "9246", "Copernicium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/9246"),
    ("mouflons", "4503", "Mouflons", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503"),
    ("wolves", "4504", "Wolves", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504"),
    ("polonium-lf", "8973", "Polonium-LF", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/8973"),
    ("lithium", "10403", "Lithium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10403"),
    ("radium-reporting", "10157", "Radium-Reporting", "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/10157"),
    ("beryllium", "10156", "Beryllium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10156"),
    ("bromine", "4090", "Bromine", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090"),
    ("iodine", "10470", "Iodine", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10470"),
    ("ep", "10972", "EP", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/10972"),
    ("aluminium", "9477", "Aluminium", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/9477"),
]

for team_key, board_id, team_name, board_url in teams_jira:
    # JSON file
    json_data = {
        "team": team_name,
        "boardUrl": board_url,
        "boardId": board_id,
        "extractedAt": "2026-05-27T12:33:00Z",
        "query": {
            "jql": f'board = {board_id} AND status IN ("In Progress", "Code review") AND issuetype IN (Story, Bug, Task)',
            "statuses": ["In Progress", "Code review"],
            "issueTypes": ["Story", "Bug", "Task"]
        },
        "summary": {
            "total": 0,
            "byStatus": {"In Progress": 0, "Code review": 0},
            "byType": {"Story": 0, "Bug": 0, "Task": 0},
            "truncated": False
        },
        "issues": []
    }
    
    with open(f"{team_key}-jira.json", "w") as f:
        json.dump(json_data, f, indent=2)
    
    # TXT file
    txt_content = f"""Team: {team_name}
Board: {board_url}
Board ID: {board_id}
Extracted: 2026-05-27T12:33:00Z

=== ACTIVE ISSUES (In Progress, Code review) ===

Summary:
- Total issues: 0
- In Progress: 0
- Code review: 0

No active issues found in "In Progress" or "Code review" statuses.

---
Status: success
"""
    
    with open(f"{team_key}-jira.txt", "w") as f:
        f.write(txt_content)

print("Created Jira JSON and TXT files for all teams")
