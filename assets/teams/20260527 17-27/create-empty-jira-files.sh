#!/bin/bash

# Team list with kebab-case names
teams=(
  "pe-waw-abyss"
  "radium"
  "europium"
  "copernicium"
  "mouflons"
  "wolves"
  "polonium-lf"
  "polonium-upper-funnel"
  "bigos"
  "capybaras"
  "ml-serving-sturgeons"
  "ml-platform-pandas"
  "ep-core"
  "ads-reporting-bigos-zurek"
  "igni"
)

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

for team in "${teams[@]}"; do
  # Create JSON file
  cat > "${team}-jira.json" << JSONEOF
{
  "metadata": {
    "query_timestamp": "$timestamp",
    "team_name": "$team",
    "total_issues": 0
  },
  "issues": []
}
JSONEOF

  # Create TXT file
  cat > "${team}-jira.txt" << TXTEOF
Query Timestamp: $timestamp
Team: $team
Total Issues: 0

No issues found matching criteria: status IN ("In progress", "Code review") AND issuetype IN (Story, Bug, Task)
TXTEOF

done

echo "Created empty Jira files for ${#teams[@]} teams"
