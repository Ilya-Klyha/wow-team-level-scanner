#!/usr/bin/env python3
import json
import re
import os

# Jira extraction results
jira_results = [
    {"team": "PE-WAW-Abyss", "projectKey": "MAW", "boardId": "9980", "issueCount": 4},
    {"team": "Radium", "projectKey": "AENW", "boardId": "8976", "issueCount": 11},
    {"team": "Europium", "projectKey": "AENW", "boardId": "8979", "issueCount": 5},
    {"team": "Copernicium", "projectKey": "AETVP", "boardId": "9246", "issueCount": 5},
    {"team": "Mouflons", "projectKey": "PEPI", "boardId": "4503", "issueCount": 0},
    {"team": "Wolves", "projectKey": "PEPI", "boardId": "4504", "issueCount": 0},
    {"team": "Polonium LF", "projectKey": "PEDSP", "boardId": "8973", "issueCount": 0},
    {"team": "Polonium UF", "projectKey": "RSW", "boardId": "10403", "issueCount": 6},
    {"team": "Bigos", "projectKey": "RSW", "boardId": "10157", "issueCount": 0},
    {"team": "Capybaras", "projectKey": "RSW", "boardId": "10156", "issueCount": 6},
    {"team": "ML Serving", "projectKey": "PEPI", "boardId": "4090", "issueCount": 0},
    {"team": "ML Platform", "projectKey": "ML", "boardId": "10470", "issueCount": 2},
    {"team": "EP Core", "projectKey": "EPCW", "boardId": "10972", "issueCount": 0},
    {"team": "Zurek", "projectKey": "PEA", "boardId": "2881", "issueCount": 0},
    {"team": "Igni", "projectKey": "ASPW", "boardId": "9477", "issueCount": 1},
    {"team": "SRE", "projectKey": "EEEW", "boardId": "10332", "issueCount": 25}
]

def team_name_to_kebab(team_name):
    return team_name.lower().replace(" ", "-").replace("_", "-")

# Read teams.json
with open('teams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update each team with Jira metadata
for team_entry in data["teams"]:
    team_name = team_entry["name"]
    
    # Find matching Jira result
    jira_info = next((j for j in jira_results if j["team"] == team_name), None)
    
    if jira_info:
        kebab_name = team_name_to_kebab(team_name)
        json_file = f"{kebab_name}-jira.json"
        
        if jira_info["issueCount"] > 0:
            team_entry["jiraFile"] = json_file
            team_entry["jiraStatus"] = "success"
            team_entry["jiraIssueCount"] = jira_info["issueCount"]
        else:
            team_entry["jiraFile"] = None
            team_entry["jiraStatus"] = "success"
            team_entry["jiraIssueCount"] = 0
        
        team_entry["jiraBoardId"] = jira_info["boardId"]
        team_entry["jiraProjectKey"] = jira_info["projectKey"]
        team_entry["jiraError"] = None

# Update metadata
data["metadata"]["jira_extraction_completed"] = True
data["metadata"]["total_issues_extracted"] = sum(j["issueCount"] for j in jira_results)

# Save
with open('teams.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated teams.json with Jira metadata")
print(f"Total issues: {sum(j['issueCount'] for j in jira_results)}")
