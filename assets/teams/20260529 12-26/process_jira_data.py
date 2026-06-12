import json
import os
from datetime import datetime, timezone
import sys

# Team mapping with exact Team field values
teams_mapping = {
    "PE-WAW-Abyss": {"name": "PE-WAW-Abyss", "project": "MAW", "board": "9980", "team_field": "PE - WAW - Abyss"},
    "Radium": {"name": "Radium", "project": "AENW", "board": "8976", "team_field": "AE - WAW - Radium"},
    "Europium": {"name": "Europium", "project": "AENW", "board": "8979", "team_field": "AP - WAW - Europium"},
    "Copernicium": {"name": "Copernicium", "project": "AETVP", "board": "9246", "team_field": "AE - WAW - Copernicium"},
    "Mouflons": {"name": "Mouflons", "project": "PEPI", "board": "4503", "team_field": "PE - WAW - Mouflons"},
    "Wolves": {"name": "Wolves", "project": "PEPI", "board": "4504", "team_field": "PE - WAW - Wolves"},
    "Polonium LF": {"name": "Polonium LF", "project": "PEDSP", "board": "8973", "team_field": "PE - WAW - Polonium LF"},
    "Polonium UF": {"name": "Polonium UF", "project": "RSW", "board": "10403", "team_field": "AS - WAW - Polonium UF"},
    "Bigos": {"name": "Bigos", "project": "RSW", "board": "10157", "team_field": "AS - WAW - Bigos"},
    "Capybaras": {"name": "Capybaras", "project": "RSW", "board": "10156", "team_field": "AS - WAW - Capybaras"},
    "ML Serving": {"name": "ML Serving", "project": "PEPI", "board": "4090", "team_field": "T - MTV - ML Serving"},
    "ML Platform": {"name": "ML Platform", "project": "ML", "board": "10470", "team_field": None},
    "EP Core": {"name": "EP Core", "project": "EPCW", "board": "10972", "team_field": None},
    "Zurek": {"name": "Zurek", "project": "PEA", "board": "2881", "team_field": "T - WAW - Zurek"},
    "Igni": {"name": "Igni", "project": "ASPW", "board": "9477", "team_field": None},
    "SRE": {"name": "SRE", "project": "EEEW", "board": "10332", "team_field": None},
}

# Read data from persisted files
file_mappings = {
    "toolu_bdrk_01NR9pamiL6h5WqSnVZF1unz.json": "AENW",
    "toolu_bdrk_01DZ8EzazUvrhHbKAWFgfUM8.json": "MAW",
    "toolu_bdrk_01JM8NYszDSPPGosa1vWcon9.json": "AETVP",
    "toolu_bdrk_01U28JXFWJ4rqQhvYmgp42MS.json": "RSW",
    "toolu_bdrk_019GN9g2EnsjurWRp8Usfa4P.json": "EPCW",
    "toolu_bdrk_01V1aY1GmpxNMm2QRjKVJ8xN.json": "ASPW",
    "toolu_bdrk_019uccj1D4r9HKd7oDmzdbFc.json": "EEEW",
}

base_path = r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\e73da338-927d-4b32-bdd4-f654f453eca8\tool-results"

# Load all project data
project_data = {}
for filename, project in file_mappings.items():
    filepath = os.path.join(base_path, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle persisted output format: [{"type": "text", "text": "..."}]
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "text" in data[0]:
                # Parse the text field which contains the actual JSON
                actual_data = json.loads(data[0]["text"])
                if isinstance(actual_data, dict) and "issues" in actual_data:
                    project_data[project] = actual_data["issues"]
                else:
                    project_data[project] = []
            elif isinstance(data, list):
                project_data[project] = data
            elif isinstance(data, dict):
                project_data[project] = data.get("issues", [])
            else:
                project_data[project] = []
    else:
        project_data[project] = []

# Add ML project data (only 2 issues, inline)
project_data["ML"] = [
    {
        "key": "ML-55",
        "fields": {
            "summary": "Implement Test DAG MLOps based on SDK",
            "issuetype": {"name": "Task"},
            "created": "2026-05-07T09:52:56.776-0400",
            "assignee": {"displayName": "Tomasz Teter"},
            "priority": {"name": "Medium"},
            "updated": "2026-05-20T05:25:04.125-0400",
            "status": {"name": "In Progress"},
            "customfield_10114": None
        }
    },
    {
        "key": "ML-10",
        "fields": {
            "summary": "Support after MWAA upgrade to 2.10.3",
            "issuetype": {"name": "Task"},
            "created": "2026-04-20T13:55:18.034-0400",
            "assignee": {"displayName": "Tomasz Teter"},
            "priority": {"name": "Medium"},
            "updated": "2026-04-23T09:43:19.611-0400",
            "status": {"name": "In Progress"},
            "customfield_10114": None
        }
    }
]

# Add empty data for projects with no results
project_data["PEPI"] = []
project_data["PEA"] = []

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Process each team
results = []
extraction_date = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

for team_key, team_info in teams_mapping.items():
    team_name = team_info["name"]
    project_key = team_info["project"]
    board_id = team_info["board"]
    team_field_value = team_info["team_field"]

    # Get issues for this project
    issues_raw = project_data.get(project_key, [])

    # Filter issues by team field
    team_issues = []
    for issue in issues_raw:
        team_field = issue.get("fields", {}).get("customfield_10114")

        # Special handling for ML Platform (no team field)
        if team_field_value is None and team_field is None:
            team_issues.append(issue)
            continue

        if team_field:
            if isinstance(team_field, dict):
                team_field_name = team_field.get("name", "")
            else:
                team_field_name = str(team_field)

            if team_field_value and team_field_value in team_field_name:
                team_issues.append(issue)

    # Build output data
    issues_output = []
    for issue in team_issues:
        fields = issue.get("fields", {})
        assignee = fields.get("assignee")
        assignee_name = assignee.get("displayName") if assignee else "Unassigned"

        priority = fields.get("priority")
        priority_name = priority.get("name") if priority else "None"

        status = fields.get("status", {})
        status_name = status.get("name", "Unknown")

        issuetype = fields.get("issuetype", {})
        type_name = issuetype.get("name", "Unknown")

        team_field_raw = fields.get("customfield_10114")
        team_field_display = ""
        team_name_parsed = ""
        if team_field_raw:
            if isinstance(team_field_raw, dict):
                team_field_display = team_field_raw.get("name", "")
                # Parse team name (last segment after " - ")
                parts = team_field_display.split(" - ")
                team_name_parsed = parts[-1] if parts else ""
            else:
                team_field_display = str(team_field_raw)
                team_name_parsed = team_field_display

        issues_output.append({
            "key": issue.get("key"),
            "type": type_name,
            "summary": fields.get("summary", ""),
            "status": status_name,
            "assignee": assignee_name,
            "priority": priority_name,
            "created": fields.get("created", ""),
            "updated": fields.get("updated", ""),
            "url": f"https://adgear.atlassian.net/browse/{issue.get('key')}",
            "teamField": team_field_display,
            "teamName": team_name_parsed
        })

    # Create output files
    filename_base = team_name.lower().replace(" ", "-")

    # JSON file
    json_output = {
        "metadata": {
            "team_name": team_name,
            "issue_count": len(issues_output),
            "extraction_date": extraction_date,
            "project_key": project_key,
            "board_id": board_id,
            "team_field_id": "customfield_10114",
            "team_pattern": team_field_value if team_field_value else "N/A",
            "query_type": "project+team" if team_field_value else "project"
        },
        "issues": issues_output
    }

    json_filename = f"{filename_base}-jira.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    # TXT file
    txt_filename = f"{filename_base}-jira.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(f"Team: {team_name}\n")
        f.write(f"Project: {project_key}\n")
        f.write(f"Board ID: {board_id}\n")
        f.write(f"Total Issues: {len(issues_output)}\n")
        f.write(f"Extraction Date: {extraction_date.replace('T', ' ').replace('Z', '')}\n")
        query_type_display = "project+team (Team field filtering enabled)" if team_field_value else "project (No team field)"
        f.write(f"Query Type: {query_type_display}\n\n")
        f.write("=" * 80 + "\n\n")

        if len(issues_output) == 0:
            f.write("No active issues found (In Progress or Code Review status).\n\n")
        else:
            for issue in issues_output:
                f.write(f"[{issue['key']}] {issue['type']}: {issue['summary']}\n")
                f.write(f"  Assignee: {issue['assignee']} | Priority: {issue['priority']} | Status: {issue['status']}\n")
                if issue['teamField']:
                    f.write(f"  Team: {issue['teamField']}\n")
                f.write(f"  Updated: {issue['updated'][:10]}\n")
                f.write(f"  {issue['url']}\n\n")

        f.write("=" * 80 + "\n")
        f.write(f"Status: success\n")
        f.write(f"Total issues: {len(issues_output)}\n")

    # Add to results summary
    results.append({
        "team": team_name,
        "projectKey": project_key,
        "boardId": board_id,
        "issueCount": len(issues_output),
        "queryType": "project+team" if team_field_value else "project",
        "status": "success",
        "filesCreated": [json_filename, txt_filename]
    })

    print(f"✓ {team_name}: {len(issues_output)} issues")

# Print summary as JSON
print("\n" + json.dumps(results, indent=2))
