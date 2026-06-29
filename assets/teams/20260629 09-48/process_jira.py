#!/usr/bin/env python3
"""
DoR Scanner - Jira Data Processor
Reads persisted Jira tool-result files, performs client-side team filtering,
and writes per-team jira.json and jira.txt files.

Usage:
    python process_jira.py
"""
import json
import os
from datetime import datetime, timezone

# ============================================================
# CONFIGURATION
# ============================================================

TOOL_RESULTS_DIR = os.path.join(
    os.path.expanduser("~"),
    ".claude",
    "projects",
    "C--Users-i-klyha-Desktop-Claude-wow-scanner-tool",
    "84c9f4e2-0e1a-40eb-b54e-cb79829bd196",
    "tool-results",
)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Team name exact match patterns for customfield_10114.name
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
    "SRE": "T - WAW - Embedded SREs SRPOL",
}

# Which projects contain which teams
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
    "EEEW": ["SRE"],
}

# Tool-result file names per project
PROJECT_FILES = {
    "MAW": "toolu_bdrk_01FJviwBRGAU2zWRdCYW95Lp.txt",
    "AENW": "toolu_bdrk_01TNb8BnptdDUyz2eHmBsqbc.txt",
    "AETVP": "toolu_bdrk_017SKSqx3oTB5WWQirPMJr65.txt",
    "PEPI": "toolu_bdrk_01U6N3y276FKX4maAKs82W2A.txt",
    "RSW": "toolu_bdrk_01Px97eTAPeXYNB1cdbzdE6e.txt",
    "EPCW": "toolu_bdrk_01QGgJTBA9MtLJ4apsH42xLw.txt",
    "PEA": "toolu_bdrk_017V8x88brr1dPCjrRbSHgaE.txt",
    "ASPW": "toolu_bdrk_01MygswbjR9zcSPuhjnzbsGy.txt",
    "EEEW": "toolu_bdrk_01T8VajuN6wCPJNYCkGY9wfS.txt",
}

# Team kebab-case names
TEAM_KEBAB = {
    "Abyss": "abyss",
    "Radium": "radium",
    "Europium": "europium",
    "Copernicium": "copernicium",
    "Mouflons": "mouflons",
    "Wolves": "wolves",
    "Polonium UF": "polonium-uf",
    "Bigos": "bigos",
    "Capybaras": "capybaras",
    "ML Serving Sturgeons": "ml-serving-sturgeons",
    "ML Platform Pandas": "ml-platform-pandas",
    "EP Core": "ep-core",
    "Zurek": "zurek",
    "Igni": "igni",
    "SRE": "sre",
}

# Sprint board URLs
BOARD_URLS = {
    "Abyss": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980",
    "Radium": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
    "Europium": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
    "Copernicium": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246",
    "Mouflons": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503",
    "Wolves": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504",
    "Polonium UF": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403",
    "Bigos": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/11439",
    "Capybaras": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156",
    "ML Serving Sturgeons": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090",
    "ML Platform Pandas": "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470",
    "EP Core": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972",
    "Zurek": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881",
    "Igni": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477",
    "SRE": "https://adgear.atlassian.net/jira/software/c/projects/EEEW/boards/10332",
}

# Board IDs extracted from URLs
BOARD_IDS = {
    "Abyss": "9980",
    "Radium": "8976",
    "Europium": "8979",
    "Copernicium": "9246",
    "Mouflons": "4503",
    "Wolves": "4504",
    "Polonium UF": "10403",
    "Bigos": "11439",
    "Capybaras": "10156",
    "ML Serving Sturgeons": "4090",
    "ML Platform Pandas": "10470",
    "EP Core": "10972",
    "Zurek": "2881",
    "Igni": "9477",
    "SRE": "10332",
}

# Hardcoded ML issues (only 2, both with null team field)
ML_ISSUES = [
    {
        "key": "ML-55",
        "fields": {
            "summary": "Implement Test DAG MLOps based on SDK",
            "issuetype": {"name": "Task"},
            "status": {"name": "In Progress"},
            "assignee": {"displayName": "Tomasz Teter"},
            "customfield_10114": None,
            "description": None,
        },
    },
    {
        "key": "ML-10",
        "fields": {
            "summary": "Support after MWAA upgrade to 2.10.3",
            "issuetype": {"name": "Task"},
            "status": {"name": "In Progress"},
            "assignee": {"displayName": "Tomasz Teter"},
            "customfield_10114": None,
            "description": None,
        },
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def get_project_key_for_team(team_name):
    """Get the Jira project key for a team."""
    for project, teams in PROJECT_TEAMS.items():
        if team_name in teams:
            return project
    return None


def load_project_issues(project_key):
    """Load issues from a project's tool-result file."""
    if project_key == "ML":
        return ML_ISSUES

    filename = PROJECT_FILES.get(project_key)
    if not filename:
        print(f"  [WARNING] No file mapping for project {project_key}")
        return []

    filepath = os.path.join(TOOL_RESULTS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  [WARNING] File not found: {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("issues", {}).get("nodes", [])
    return nodes


def filter_issues_for_team(issues, team_name):
    """Filter issues by customfield_10114.name exact match."""
    expected_field_value = TEAM_NAME_PATTERNS[team_name]
    filtered = []

    for issue in issues:
        fields = issue.get("fields", {})
        team_field = fields.get("customfield_10114")

        if team_field is None:
            # For ML project, null team field means it belongs to ML Platform Pandas
            if team_name == "ML Platform Pandas":
                filtered.append(issue)
            continue

        field_name = team_field.get("name", "")
        if field_name == expected_field_value:
            filtered.append(issue)

    return filtered


def extract_issue_data(issue, project_key):
    """Extract standardized issue data from a raw issue node."""
    # Handle both formats (tool-result nodes have 'key' at top level or inside)
    issue_key = issue.get("key", "")
    fields = issue.get("fields", {})

    if not issue_key:
        issue_key = f"{project_key}-?"

    summary = fields.get("summary", "No summary")
    issue_type = fields.get("issuetype", {}).get("name", "Unknown")
    status = fields.get("status", {}).get("name", "Unknown")

    assignee_obj = fields.get("assignee")
    assignee = assignee_obj.get("displayName", "Unassigned") if assignee_obj else "Unassigned"

    description = fields.get("description")
    has_description = description is not None and str(description).strip() != ""

    return {
        "key": issue_key,
        "summary": summary,
        "issueType": issue_type,
        "status": status,
        "assignee": assignee,
        "url": f"https://adgear.atlassian.net/browse/{issue_key}",
        "hasDescription": has_description,
    }


def write_team_jira_json(team_name, issues_data, project_key):
    """Write the team's jira.json file."""
    kebab = TEAM_KEBAB[team_name]
    extracted_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output = {
        "team": team_name,
        "boardUrl": BOARD_URLS[team_name],
        "boardId": BOARD_IDS[team_name],
        "projectKey": project_key,
        "extractedAt": extracted_at,
        "teamFieldId": "customfield_10114",
        "query": {
            "jql": f'project = {project_key} AND status in ("In Progress", "Code Review", "In Development") AND issuetype in (Story, Bug, Task)',
            "filterMethod": "client-side customfield_10114.name exact match",
            "teamFieldValue": TEAM_NAME_PATTERNS[team_name],
        },
        "summary": {
            "totalIssues": len(issues_data),
            "byType": {},
            "byStatus": {},
        },
        "issues": issues_data,
    }

    # Compute summary stats
    for issue in issues_data:
        itype = issue["issueType"]
        output["summary"]["byType"][itype] = output["summary"]["byType"].get(itype, 0) + 1
        istatus = issue["status"]
        output["summary"]["byStatus"][istatus] = output["summary"]["byStatus"].get(istatus, 0) + 1

    filepath = os.path.join(OUTPUT_DIR, f"{kebab}-jira.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return filepath


def write_team_jira_txt(team_name, issues_data, project_key):
    """Write the team's jira.txt file."""
    kebab = TEAM_KEBAB[team_name]
    lines = []
    lines.append(f"TEAM: {team_name}")
    lines.append(f"PROJECT: {project_key}")
    lines.append(f"BOARD: {BOARD_URLS[team_name]}")
    lines.append(f"TOTAL ISSUES: {len(issues_data)}")
    lines.append("")
    lines.append("=" * 70)

    for i, issue in enumerate(issues_data, 1):
        lines.append(f"\n[{i}] {issue['key']} - {issue['issueType']}")
        lines.append(f"    Title: {issue['summary']}")
        lines.append(f"    Status: {issue['status']}")
        lines.append(f"    Assignee: {issue['assignee']}")
        lines.append(f"    URL: {issue['url']}")
        lines.append(f"    Has Description: {'Yes' if issue['hasDescription'] else 'No'}")

    filepath = os.path.join(OUTPUT_DIR, f"{kebab}-jira.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("DoR Scanner - Jira Data Processor")
    print("=" * 70)
    print(f"Tool results dir: {TOOL_RESULTS_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
    print()

    # Cache loaded project data
    project_cache = {}
    team_results = {}

    all_teams = list(TEAM_KEBAB.keys())

    for team_name in all_teams:
        project_key = get_project_key_for_team(team_name)
        if not project_key:
            print(f"  [ERROR] No project mapping for team: {team_name}")
            team_results[team_name] = []
            continue

        # Load project issues (cached)
        if project_key not in project_cache:
            print(f"  Loading project {project_key}...", end=" ")
            project_cache[project_key] = load_project_issues(project_key)
            print(f"({len(project_cache[project_key])} issues)")

        # Filter for this team
        all_project_issues = project_cache[project_key]
        team_issues = filter_issues_for_team(all_project_issues, team_name)

        # Extract standardized data
        issues_data = []
        for issue in team_issues:
            issues_data.append(extract_issue_data(issue, project_key))

        team_results[team_name] = issues_data

        # Write files
        json_path = write_team_jira_json(team_name, issues_data, project_key)
        txt_path = write_team_jira_txt(team_name, issues_data, project_key)

        print(f"  {team_name}: {len(issues_data)} issues -> {os.path.basename(json_path)}, {os.path.basename(txt_path)}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = 0
    for team_name in all_teams:
        count = len(team_results[team_name])
        total += count
        print(f"  {team_name:25s}: {count:3d} issues")

    print(f"  {'TOTAL':25s}: {total:3d} issues")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
