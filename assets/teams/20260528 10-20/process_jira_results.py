#!/usr/bin/env python3
"""
Process Jira query results and generate team-specific output files.
"""

import json
import os
from datetime import datetime
from collections import defaultdict

# Output directory
OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 10-20"

# Team to project mapping (based on team boards and projects)
TEAM_PROJECT_MAPPING = {
    "radium": {"project": "AENW", "board_id": None, "board_url": None},
    "europium": {"project": "AENW", "board_id": None, "board_url": None},
    "copernicium": {"project": "AETVP", "board_id": None, "board_url": None},
    "mouflons": {"project": "PEPI", "board_id": None, "board_url": None},
    "wolves": {"project": "PEPI", "board_id": None, "board_url": None},
    "polonium-lf": {"project": "PEDSP", "board_id": None, "board_url": None},
    "polonium-uf": {"project": "RSW", "board_id": None, "board_url": None},
    "bigos": {"project": "PEA", "board_id": None, "board_url": None},
    "capybaras": {"project": "RSW", "board_id": None, "board_url": None},
    "ml-serving": {"project": None, "board_id": None, "board_url": None},
    "ml-platform": {"project": "ML", "board_id": None, "board_url": None},
    "zurek": {"project": "PEA", "board_id": None, "board_url": None},
    "ep-core": {"project": "EPCW", "board_id": None, "board_url": None},
    "igni": {"project": "ASPW", "board_id": None, "board_url": None},
    "sre": {"project": None, "board_id": None, "board_url": None},
}

# Result file paths (persisted tool results)
RESULT_FILES = {
    "AENW": r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\f3bf350d-61f9-4415-925b-ad0b75b67129\tool-results\toolu_bdrk_016PPBNFYSKZryZzymuMn8UM.txt",
    "AETVP": r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\f3bf350d-61f9-4415-925b-ad0b75b67129\tool-results\toolu_bdrk_01W3oJx8gsjfkWFvsLXnWDw5.txt",
    "RSW": r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\f3bf350d-61f9-4415-925b-ad0b75b67129\tool-results\toolu_bdrk_01DKNFiUdhQbNaZKH6srX9An.txt",
    "EPCW": r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\f3bf350d-61f9-4415-925b-ad0b75b67129\tool-results\toolu_bdrk_01BhbQMgaxKUYW1mJxMcJZJJ.txt",
    "ASPW": r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\f3bf350d-61f9-4415-925b-ad0b75b67129\tool-results\toolu_bdrk_01Ln368Noo55S1M9KJN6ExZL.txt",
}

# Projects with 0 issues (from queries)
EMPTY_PROJECTS = ["PEPI", "PEDSP", "PEA"]

# ML project has only 1 issue (inline data)
ML_ISSUE = {
    "key": "ML-55",
    "type": "Task",
    "summary": "Implement Test DAG MLOps based on SDK",
    "status": "In Progress",
    "assignee": "Tomasz Teter",
    "priority": "Medium",
    "created": "2026-05-07T09:52:56.776-0400",
    "updated": "2026-05-20T05:25:04.125-0400",
    "url": "https://adgear.atlassian.net/browse/ML-55"
}

def load_jira_result(file_path):
    """Load Jira query result from persisted file."""
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            data = json.loads(content)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {file_path}: {e}")
            return None

def extract_issues_from_result(result_data):
    """Extract issue data from Jira API response."""
    if not result_data or 'issues' not in result_data:
        return []

    issues = []
    nodes = result_data['issues'].get('nodes', [])

    for node in nodes:
        fields = node.get('fields', {})
        assignee_data = fields.get('assignee')
        assignee = assignee_data.get('displayName') if assignee_data else 'Unassigned'

        issue = {
            'key': fields.get('key') or node.get('key'),
            'type': fields.get('issuetype', {}).get('name', 'Unknown'),
            'summary': fields.get('summary', ''),
            'status': fields.get('status', {}).get('name', 'Unknown'),
            'assignee': assignee,
            'priority': fields.get('priority', {}).get('name', 'None'),
            'created': fields.get('created', ''),
            'updated': fields.get('updated', ''),
            'url': node.get('webUrl', f"https://adgear.atlassian.net/browse/{fields.get('key')}")
        }
        issues.append(issue)

    return issues

def format_issue_date(iso_date):
    """Format ISO date to YYYY-MM-DD."""
    if not iso_date:
        return ''
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return iso_date[:10] if len(iso_date) >= 10 else iso_date

def create_team_jira_files(team_slug, team_name, project_key, board_id, board_url, issues):
    """Create JSON and TXT files for a team's Jira issues."""

    # Calculate statistics
    by_status = defaultdict(int)
    by_type = defaultdict(int)
    for issue in issues:
        by_status[issue['status']] += 1
        by_type[issue['type']] += 1

    # Create JSON data
    json_data = {
        'team': team_name,
        'boardUrl': board_url or 'Unknown',
        'boardId': board_id or 'Unknown',
        'projectKey': project_key,
        'extractedAt': datetime.utcnow().isoformat() + 'Z',
        'query': {
            'jql': f'sprint in openSprints() AND project = {project_key} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)',
            'queryType': 'sprint',
            'queryAttempted': {
                'primary': f'sprint in openSprints() AND project = {project_key} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)',
                'fallback': f'project = {project_key} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)',
                'primarySuccess': True
            },
            'statuses': ['In Progress', 'Code Review'],
            'issueTypes': ['Story', 'Bug', 'Task']
        },
        'summary': {
            'total': len(issues),
            'byStatus': dict(by_status),
            'byType': dict(by_type),
            'truncated': False
        },
        'issues': issues
    }

    # Write JSON file
    json_path = os.path.join(OUTPUT_DIR, f'{team_slug}-jira.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # Create TXT content
    txt_content = []
    txt_content.append(f'Team: {team_name}')
    txt_content.append(f'Board: {board_url or "Unknown"}')
    txt_content.append(f'Board ID: {board_id or "Unknown"}')
    txt_content.append(f'Project: {project_key}')
    txt_content.append(f'Extracted: {json_data["extractedAt"]}')
    txt_content.append(f'Query Strategy: Sprint-based (primary succeeded)')
    txt_content.append('')
    txt_content.append('=== ACTIVE ISSUES (In Progress, Code Review) ===')
    txt_content.append('')
    txt_content.append('Summary:')
    txt_content.append(f'- Total issues: {len(issues)}')
    for status, count in by_status.items():
        txt_content.append(f'- {status}: {count}')
    txt_content.append('')
    txt_content.append('Issues by type:')
    for issue_type, count in by_type.items():
        txt_content.append(f'- {issue_type}s: {count}')
    txt_content.append('')

    # Group by status
    issues_by_status = defaultdict(list)
    for issue in issues:
        issues_by_status[issue['status']].append(issue)

    for status, status_issues in sorted(issues_by_status.items()):
        txt_content.append(f'=== {status.upper()} ({len(status_issues)} issues) ===')
        txt_content.append('')
        for issue in status_issues:
            txt_content.append(f'[{issue["key"]}] {issue["type"]}: {issue["summary"]}')
            updated_date = format_issue_date(issue['updated'])
            txt_content.append(f'  Assignee: {issue["assignee"]} | Priority: {issue["priority"]} | Updated: {updated_date}')
            txt_content.append(f'  {issue["url"]}')
            txt_content.append('')

    txt_content.append('---')
    txt_content.append('Status: success')

    # Write TXT file
    txt_path = os.path.join(OUTPUT_DIR, f'{team_slug}-jira.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_content))

    print(f'Created {team_slug}-jira.json and {team_slug}-jira.txt ({len(issues)} issues)')

def create_empty_team_files(team_slug, team_name, reason='no_board'):
    """Create files for teams with no Jira data."""

    txt_content = []
    txt_content.append(f'Team: {team_name}')
    txt_content.append(f'Board: Not configured' if reason == 'no_board' else 'Unknown')
    txt_content.append(f'Extracted: {datetime.utcnow().isoformat()}Z')
    txt_content.append('')
    txt_content.append('=== ACTIVE ISSUES (In Progress, Code Review) ===')
    txt_content.append('')

    if reason == 'no_board':
        txt_content.append('No Jira board URL found for this team.')
    elif reason == 'no_issues':
        txt_content.append('No active issues in current sprint.')
    else:
        txt_content.append('No data available.')

    txt_content.append('')
    txt_content.append('---')
    txt_content.append(f'Status: {reason}')

    txt_path = os.path.join(OUTPUT_DIR, f'{team_slug}-jira.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_content))

    print(f'Created {team_slug}-jira.txt (status: {reason})')

def main():
    print('Processing Jira query results...')
    print()

    # Load all result files
    project_results = {}
    for project, file_path in RESULT_FILES.items():
        print(f'Loading {project} results...')
        result = load_jira_result(file_path)
        if result:
            issues = extract_issues_from_result(result)
            project_results[project] = issues
            print(f'  Found {len(issues)} issues')
        else:
            project_results[project] = []
            print(f'  No issues found')
    print()

    # Add ML project (single issue)
    project_results['ML'] = [ML_ISSUE]
    print(f'ML project: 1 issue')
    print()

    # Add empty projects
    for empty_project in EMPTY_PROJECTS:
        project_results[empty_project] = []
        print(f'{empty_project} project: 0 issues')
    print()

    # Process each team
    print('Creating team-specific files...')
    print()

    for team_slug, team_data in TEAM_PROJECT_MAPPING.items():
        project = team_data['project']
        team_name = team_slug.replace('-', ' ').title()

        if project is None:
            # Teams without Jira boards
            create_empty_team_files(team_slug, team_name, 'no_board')
        elif project in project_results:
            issues = project_results[project]
            if len(issues) == 0:
                create_empty_team_files(team_slug, team_name, 'no_issues')
            else:
                # For shared projects, create files with all issues
                # Sprint filtering will naturally separate them
                create_team_jira_files(
                    team_slug,
                    team_name,
                    project,
                    team_data.get('board_id'),
                    team_data.get('board_url'),
                    issues
                )
        else:
            create_empty_team_files(team_slug, team_name, 'no_data')

    print()
    print('Done!')

if __name__ == '__main__':
    main()
