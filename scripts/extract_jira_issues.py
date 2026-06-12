#!/usr/bin/env python3
"""
Extract Jira issues for SRPOL teams.
This script queries Jira for active issues (In Progress, Code Review) for each team.
"""

import json
import re
from datetime import datetime
from pathlib import Path

# Team name to pattern mapping
TEAM_PATTERNS = {
    "PE-WAW-Abyss": "7b3aaae2-20aa-4f06-920d-9eb7ae8e5587",  # Known ID
    "Radium": None,  # Will search by name
    "Europium": None,
    "Copernicium": None,
    "Mouflons": None,
    "Wolves": None,
    "Polonium-LF": None,
    "Polonium-Upper-Funnel": None,
    "Bigos": "5b181ecc-1885-4014-994e-acca018c8c93",  # Known ID
    "Capybaras": None,
    "ML-Serving-Sturgeons": None,
    "ML-Platform-Pandas": None,
    "EP-Core": None,
    "Ads-Reporting-Bigos-Zurek": None,
    "Igni": None,
    "SRPOL-SRE": None
}

def extract_board_info(board_url):
    """Extract board ID and project key from board URL."""
    board_match = re.search(r'/boards/(\d+)', board_url)
    project_match = re.search(r'/projects/([A-Z]+)/', board_url)

    board_id = board_match.group(1) if board_match else None
    project_key = project_match.group(1) if project_match else None

    return board_id, project_key

def extract_team_name(team_field_value):
    """Extract team name from full team field value like 'PE - WAW - Abyss' -> 'Abyss'."""
    if not team_field_value:
        return None
    parts = team_field_value.split(' - ')
    return parts[-1].strip() if parts else team_field_value

def save_json(team, board_url, board_id, project_key, issues, query_info, output_dir):
    """Save Jira issues to JSON file."""
    team_name = team['name']
    kebab_name = team_name.lower().replace('_', '-')

    # Calculate summary stats
    by_status = {}
    by_type = {}
    for issue in issues:
        status = issue['status']
        issue_type = issue['type']
        by_status[status] = by_status.get(status, 0) + 1
        by_type[issue_type] = by_type.get(issue_type, 0) + 1

    data = {
        "team": team_name,
        "boardUrl": board_url,
        "boardId": board_id,
        "projectKey": project_key,
        "extractedAt": datetime.utcnow().isoformat() + 'Z',
        "teamFieldId": "customfield_10114",
        "query": query_info,
        "summary": {
            "total": len(issues),
            "byStatus": by_status,
            "byType": by_type,
            "truncated": len(issues) >= 100
        },
        "issues": issues
    }

    output_path = output_dir / f"{kebab_name}-jira.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return output_path

def save_txt(team, board_url, board_id, project_key, issues, output_dir, status="success", error_msg=None):
    """Save Jira issues to TXT file."""
    team_name = team['name']
    kebab_name = team_name.lower().replace('_', '-')

    lines = []
    lines.append(f"Team: {team_name}")
    lines.append(f"Board: {board_url}" if board_url else "Board: Not configured")
    if board_id:
        lines.append(f"Board ID: {board_id}")
    if project_key:
        lines.append(f"Project: {project_key}")
    lines.append(f"Extracted: {datetime.utcnow().isoformat()}Z")
    lines.append("")

    if error_msg:
        lines.append(f"Error: {error_msg}")
        lines.append("")
        lines.append(f"---")
        lines.append(f"Status: {status}")
    elif not issues:
        lines.append("=== ACTIVE ISSUES (In Progress, Code Review) ===")
        lines.append("")
        lines.append("Summary:")
        lines.append("- Total issues: 0")
        lines.append("")
        lines.append("No active issues found for this team.")
        lines.append("")
        lines.append("---")
        lines.append("Status: success")
    else:
        # Group by status
        by_status = {}
        by_type = {}
        for issue in issues:
            status_name = issue['status']
            type_name = issue['type']
            if status_name not in by_status:
                by_status[status_name] = []
            by_status[status_name].append(issue)
            by_type[type_name] = by_type.get(type_name, 0) + 1

        lines.append("=== ACTIVE ISSUES (In Progress, Code Review) ===")
        lines.append("")
        lines.append("Summary:")
        lines.append(f"- Total issues: {len(issues)}")
        for status_name, count in sorted(by_status.items(), key=lambda x: x[0]):
            lines.append(f"- {status_name}: {len(by_status[status_name])}")
        lines.append("")
        lines.append("Issues by type:")
        for type_name, count in sorted(by_type.items(), key=lambda x: x[0]):
            lines.append(f"- {type_name}s: {count}")
        lines.append("")

        # List issues by status
        for status_name in sorted(by_status.keys()):
            status_issues = by_status[status_name]
            lines.append(f"=== {status_name.upper()} ({len(status_issues)} issues) ===")
            lines.append("")
            for issue in status_issues:
                lines.append(f"[{issue['key']}] {issue['type']}: {issue['summary']}")
                assignee = issue.get('assignee', 'Unassigned')
                priority = issue.get('priority', 'None')
                updated = issue['updated'][:10] if issue.get('updated') else 'N/A'
                lines.append(f"  Assignee: {assignee} | Priority: {priority} | Updated: {updated}")
                if issue.get('teamField'):
                    lines.append(f"  Team: {issue['teamField']}")
                lines.append(f"  {issue['url']}")
                lines.append("")

        if len(issues) >= 100:
            lines.append("WARNING: Results limited to 100 issues. Board may have more active issues.")
            lines.append("")

        lines.append("---")
        lines.append(f"Status: {status}")

    output_path = output_dir / f"{kebab_name}-jira.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path

def main():
    """Main extraction logic."""
    # Load teams.json
    teams_path = Path("C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260610 14-26/teams.json")
    with open(teams_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    teams = data['teams']
    output_dir = teams_path.parent

    print(f"Processing {len(teams)} teams...")
    print()

    # For this script, we'll use manual Jira API calls via mcp_plugin_atlassian
    # Since we can't directly call the MCP tool from Python, this script
    # serves as documentation for what needs to be done manually

    print("This script requires manual Jira API calls.")
    print("Please use the Claude Code MCP Atlassian plugin to query Jira.")
    print()
    print("For each team, run:")
    print("  mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql(")
    print("    cloudId='adgear.atlassian.net',")
    print("    jql='project = {PROJECT_KEY} AND status IN (\"In Progress\", \"Code Review\")',")
    print("    fields=['key', 'summary', 'status', 'issuetype', 'assignee', 'priority', 'created', 'updated', 'customfield_10114'],")
    print("    maxResults=100")
    print("  )")
    print()
    print("Then filter results locally by team field value.")

if __name__ == "__main__":
    main()
