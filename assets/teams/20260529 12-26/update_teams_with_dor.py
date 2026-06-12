#!/usr/bin/env python3
import json

# DoR extraction results
dor_results = [
  {"name": "PE-WAW-Abyss", "pageId": "WID6RQU", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22648881240", "dorStatus": "found", "dorFile": "pe-waw-abyss-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980?atlOrigin=eyJpIjoiZWE4ZjlhZjY3NjlhNDkxOTkxMmZlY2JmNmZlYzc5ODgiLCJwIjoiaiJ9"},
  {"name": "Radium", "pageId": "20720615642", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20720615642", "dorStatus": "found", "dorFile": "radium-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976"},
  {"name": "Europium", "pageId": "22431629392", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22431629392", "dorStatus": "found", "dorFile": "europium-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979"},
  {"name": "Copernicium", "pageId": "20734247032", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20734247032", "dorStatus": "found", "dorFile": "copernicium-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246"},
  {"name": "Mouflons", "pageId": "22381756417", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22381756417", "dorStatus": "found", "dorFile": "mouflons-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503"},
  {"name": "Wolves", "pageId": "22374940673", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22374940673", "dorStatus": "found", "dorFile": "wolves-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504"},
  {"name": "Polonium LF", "pageId": "22606054953", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606054953", "dorStatus": "not_found", "dorFile": "polonium-lf-dor.txt", "dorSource": "none", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEDSP/boards/8973"},
  {"name": "Polonium UF", "pageId": "22606053416", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606053416", "dorStatus": "found", "dorFile": "polonium-uf-dor.txt", "dorSource": "linked_page", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403"},
  {"name": "Bigos", "pageId": "22695936064", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22695936064", "dorStatus": "found", "dorFile": "bigos-dor.txt", "dorSource": "linked_page", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10157"},
  {"name": "Capybaras", "pageId": "22696132609", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22696132609", "dorStatus": "found", "dorFile": "capybaras-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156"},
  {"name": "ML Serving", "pageId": "21732425749", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732425749", "dorStatus": "not_found", "dorFile": "ml-serving-dor.txt", "dorSource": "none", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090"},
  {"name": "ML Platform", "pageId": "21732360213", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732360213", "dorStatus": "not_found", "dorFile": "ml-platform-dor.txt", "dorSource": "none", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470"},
  {"name": "EP Core", "pageId": "AQAHUAU", "pageLink": "https://adgear.atlassian.net/wiki/x/AQAHUAU", "dorStatus": "found", "dorFile": "ep-core-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972"},
  {"name": "Zurek", "pageId": "21748023571", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21748023571", "dorStatus": "found", "dorFile": "zurek-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881"},
  {"name": "Igni", "pageId": "22435922026", "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22435922026", "dorStatus": "found", "dorFile": "igni-dor.txt", "dorSource": "direct", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477"},
  {"name": "SRE", "pageId": "22719529363", "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22719529363", "dorStatus": "not_found", "dorFile": "sre-dor.txt", "dorSource": "none", "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/EEEW/boards/10332"}
]

# Read existing teams.json
with open('teams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update teams array
data["teams"] = []
for team in dor_results:
    data["teams"].append({
        "name": team["name"],
        "page_link": team["pageLink"],
        "sprint_board_link": team.get("sprintBoardLink"),
        "dor_file": team["dorFile"],
        "page_id": team["pageId"],
        "extraction_status": "success" if team["dorStatus"] == "found" else "not_found",
        "extraction_error": None,
        "dor_source": team["dorSource"]
    })

# Update metadata
data["metadata"]["team_count"] = len(data["teams"])

# Save
with open('teams.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated teams.json with {len(data['teams'])} teams")
