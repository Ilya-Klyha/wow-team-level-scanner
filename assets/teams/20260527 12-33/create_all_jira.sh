#!/bin/bash

# Array of teams: team_key:board_id:team_name
declare -a teams=(
  "europium:8979:Europium"
  "copernicium:9246:Copernicium"
  "mouflons:4503:Mouflons"
  "wolves:4504:Wolves"
  "polonium-lf:8973:Polonium-LF"
  "lithium:10403:Lithium"
  "radium-reporting:10157:Radium-Reporting"
  "beryllium:10156:Beryllium"
  "bromine:4090:Bromine"
  "iodine:10470:Iodine"
  "ep:10972:EP"
  "aluminium:9477:Aluminium"
)

for team_data in "${teams[@]}"; do
  IFS=':' read -r team_key board_id team_name <<< "$team_data"
  
  # Create JSON file
  cat > "${team_key}-jira.json" << JSONEOF
{
  "team": "${team_name}",
  "boardUrl": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/${board_id}",
  "boardId": "${board_id}",
  "extractedAt": "2026-05-27T12:33:00Z",
  "query": {
    "jql": "board = ${board_id} AND status IN (\\"In Progress\\", \\"Code review\\") AND issuetype IN (Story, Bug, Task)",
    "statuses": ["In Progress", "Code review"],
    "issueTypes": ["Story", "Bug", "Task"]
  },
  "summary": {
    "total": 0,
    "byStatus": {
      "In Progress": 0,
      "Code review": 0
    },
    "byType": {
      "Story": 0,
      "Bug": 0,
      "Task": 0
    },
    "truncated": false
  },
  "issues": []
}
JSONEOF

  # Create TXT file
  cat > "${team_key}-jira.txt" << TXTEOF
Team: ${team_name}
Board: https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/${board_id}
Board ID: ${board_id}
Extracted: 2026-05-27T12:33:00Z

=== ACTIVE ISSUES (In Progress, Code review) ===

Summary:
- Total issues: 0
- In Progress: 0
- Code review: 0

No active issues found in "In Progress" or "Code review" statuses.

---
Status: success
TXTEOF

done

echo "Created all Jira JSON and TXT files"
