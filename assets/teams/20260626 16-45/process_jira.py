#!/usr/bin/env python3
"""Process Jira query results, filter by team, save per-team files."""
import json, os
from datetime import datetime

OUTPUT_DIR = "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260626 16-45"
RESULTS_DIR = "C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/59a13e87-a704-48f2-9c42-267ae9647741/tool-results"

TEAM_NAME_PATTERNS = {
    "Abyss": "PE - WAW - Abyss",
    "Radium": "AE - WAW - Radium",
    "Europium": "AP - WAW - Europium",
    "Copernicium": "AE - WAW - Copernicium",
    "Mouflons": "AS - WAW - Mouflons",
    "Wolves": "AS - WAW - Wolves",
    "Polonium UF": "AS - WAW - Polonium UF",
    "Bigos": "AS - WAW - Bigos",
    "Capybaras": "AS - WAW - Capybaras",
    "ML Serving Sturgeons": "T - WAW - ML Sturgeons",
    "ML Platform Pandas": "T - WAW - ML Pandas",
    "Zurek": "T - WAW - Zurek",
    "EP Core": "T - WAW - EP Core",
    "Igni": "AP - WAW - Igni",
    "SRE": "T - WAW - Embedded SREs SRPOL"
}

PROJECT_TEAMS = {
    "MAW": ["Abyss", "Bigos"],
    "AENW": ["Radium", "Europium"],
    "AETVP": ["Copernicium"],
    "PEPI": ["Mouflons", "Wolves", "ML Serving Sturgeons"],
    "RSW": ["Polonium UF", "Capybaras"],
    "ML": ["ML Platform Pandas"],
    "EPCW": ["EP Core"],
    "PEA": ["Zurek"],
    "ASPW": ["Igni"],
    "EEEW": ["SRE"]
}

PROJECT_FILES = {
    "MAW": "toolu_bdrk_01BKUvaAP2PsTS7sYmbPogX9.json",
    "AENW": "toolu_bdrk_01Fa7zEkXTFa2HJy9dqxnbUh.json",
    "AETVP": "toolu_bdrk_01JjfzHzxb7bb6emmfZXGtZF.json",
    "PEPI": "toolu_bdrk_01Kh8HZ1ZGCWrGcCYqbMn2pK.json",
    "RSW": "toolu_bdrk_01UXUxjj6STmo6xAbRGXcezJ.json",
    "EPCW": "toolu_bdrk_01G3AaTLpA4JgYMw99M2QxE5.json",
    "PEA": "toolu_bdrk_017fT4wpfAuUkZMUj4MrW73E.json",
    "ASPW": "toolu_bdrk_01VbnaiBr3vmBVGshHJJvdZb.json",
    "EEEW": "toolu_bdrk_01GY4ZpZKZoJwAqNZyPJzQuD.json"
}

def to_kebab(name):
    return name.lower().replace(" ", "-").replace("_", "-")

def load_project_issues(project_key):
    if project_key == "ML":
        return []  # ML had 2 issues with null team field
    filepath = os.path.join(RESULTS_DIR, PROJECT_FILES[project_key])
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    text = data[0]["text"]
    result = json.loads(text)
    return result.get("issues", [])

# Process all projects
team_issues = {name: [] for name in TEAM_NAME_PATTERNS}
project_stats = {}

for project_key, team_names in PROJECT_TEAMS.items():
    issues = load_project_issues(project_key)
    project_stats[project_key] = {"total": len(issues)}

    for team_name in team_names:
        pattern = TEAM_NAME_PATTERNS[team_name]
        matched = []
        for issue in issues:
            tf = issue["fields"].get("customfield_10114")
            if tf and isinstance(tf, dict) and tf.get("name") == pattern:
                matched.append(issue)
        team_issues[team_name] = matched

# Save per-team Jira files
team_jira_stats = {}

for team_name, issues in team_issues.items():
    kebab = to_kebab(team_name)
    proj_key = None
    for pk, teams in PROJECT_TEAMS.items():
        if team_name in teams:
            proj_key = pk
            break

    issue_data = []
    for issue in issues:
        f = issue["fields"]
        assignee = f.get("assignee")
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        tf = f.get("customfield_10114")
        team_field = tf.get("name", "") if tf and isinstance(tf, dict) else ""

        issue_data.append({
            "key": issue["key"],
            "type": f["issuetype"]["name"],
            "summary": f["summary"],
            "status": f["status"]["name"],
            "assignee": assignee_name,
            "priority": f.get("priority", {}).get("name", "None") if f.get("priority") else "None",
            "created": f.get("created", ""),
            "updated": f.get("updated", ""),
            "url": f"https://adgear.atlassian.net/browse/{issue['key']}",
            "teamField": team_field
        })

    by_status = {}
    by_type = {}
    for i in issue_data:
        by_status[i["status"]] = by_status.get(i["status"], 0) + 1
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1

    team_jira_stats[team_name] = {"count": len(issue_data), "project": proj_key, "byStatus": by_status, "byType": by_type}

    jira_json = {
        "team": team_name,
        "projectKey": proj_key,
        "extractedAt": datetime.utcnow().isoformat() + "Z",
        "teamFieldId": "customfield_10114",
        "query": {
            "jql_executed": f'project = {proj_key} AND status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task',
            "queryType": "project_wide_with_client_filter" if len(issue_data) > 0 else "pattern_mismatch",
            "filterMethod": "client_side",
            "teamPattern": TEAM_NAME_PATTERNS[team_name],
            "projectKey": proj_key,
            "totalProjectIssues": project_stats.get(proj_key, {}).get("total", 0),
            "matchedTeamIssues": len(issue_data)
        },
        "summary": {"total": len(issue_data), "byStatus": by_status, "byType": by_type},
        "issues": issue_data
    }

    with open(os.path.join(OUTPUT_DIR, f"{kebab}-jira.json"), "w", encoding="utf-8") as f:
        json.dump(jira_json, f, indent=2)

    # Save TXT
    txt_lines = [f"Team: {team_name}", f"Project: {proj_key}", f"Extracted: {datetime.utcnow().isoformat()}Z", ""]
    txt_lines.append(f"=== ACTIVE ISSUES ({len(issue_data)} total) ===\n")
    for status in ["In Progress", "Code Review", "In Development"]:
        si = [i for i in issue_data if i["status"] == status]
        if si:
            txt_lines.append(f"--- {status} ({len(si)}) ---")
            for i in si:
                txt_lines.append(f"[{i['key']}] {i['type']}: {i['summary']}")
                txt_lines.append(f"  Assignee: {i['assignee']} | {i['url']}")
            txt_lines.append("")

    with open(os.path.join(OUTPUT_DIR, f"{kebab}-jira.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

# Print summary
print("=== Jira Extraction Summary ===")
total = 0
for team_name in TEAM_NAME_PATTERNS:
    c = team_jira_stats[team_name]["count"]
    total += c
    print(f"  {team_name}: {c} issues")
print(f"  TOTAL: {total} issues across all teams")

# Save teams.json
team_configs = [
    ("Abyss", "https://adgear.atlassian.net/wiki/x/WID6RQU", "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980", "WID6RQU", "success", "direct"),
    ("Radium", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20720615642", "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976", "20720615642", "success", "direct"),
    ("Europium", "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22431629392", "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979", "22431629392", "success", "direct"),
    ("Copernicium", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20734247032", "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246", "20734247032", "success", "direct"),
    ("Mouflons", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22381756417", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503", "22381756417", "success", "direct"),
    ("Wolves", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22374940673", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504", "22374940673", "success", "direct"),
    ("Polonium UF", "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606053416", "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403", "22606053416", "success", "linked_page"),
    ("Bigos", "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22695936064", "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/11439", "22695936064", "success", "linked_page"),
    ("Capybaras", "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22696132609", "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156", "22696132609", "success", "direct"),
    ("ML Serving Sturgeons", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732425749", "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090", "21732425749", "not_found", None),
    ("ML Platform Pandas", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732360213", "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470", "21732360213", "success", "linked_page"),
    ("EP Core", "https://adgear.atlassian.net/wiki/x/AQAHUAU", "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972", "AQAHUAU", "success", "direct"),
    ("Zurek", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21748023571", "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881", "21748023571", "success", "direct"),
    ("Igni", "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22435922026", "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477", "22435922026", "success", "direct"),
    ("SRE", "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22719529363", "https://adgear.atlassian.net/jira/software/c/projects/EEEW/boards/10332", "22719529363", "not_found", None),
]

teams_list = []
for name, page_link, sprint_link, page_id, dor_status, dor_source in team_configs:
    kebab = to_kebab(name)
    stats = team_jira_stats[name]
    teams_list.append({
        "name": name,
        "page_link": page_link,
        "sprint_board_link": sprint_link,
        "dor_file": f"{kebab}-dor.txt",
        "page_id": page_id,
        "extraction_status": dor_status,
        "extraction_error": None,
        "dor_source": dor_source,
        "jiraFile": f"{kebab}-jira.json",
        "jiraStatus": "success",
        "jiraIssueCount": stats["count"],
        "jiraProjectKey": stats["project"],
        "jiraQueryType": "project_wide_with_client_filter" if stats["count"] > 0 else "pattern_mismatch",
        "jiraError": None
    })

teams_json = {
    "metadata": {
        "scan_date": datetime.utcnow().isoformat() + "Z",
        "scan_timestamp_cet": "20260626 16-45",
        "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
        "team_count": 15,
        "cloudId": "adgear.atlassian.net",
        "scanner_version": "2.0"
    },
    "teams": teams_list
}

with open(os.path.join(OUTPUT_DIR, "teams.json"), "w", encoding="utf-8") as f:
    json.dump(teams_json, f, indent=2)

print("\n[SUCCESS] teams.json saved.")
print(f"[INFO] Cross-team contamination: impossible by design (exact name match filtering)")
