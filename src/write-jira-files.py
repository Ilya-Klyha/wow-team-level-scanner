import json
import os

OUTPUT_DIR = 'C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260629 10-08'

# Read the temp file
with open(os.path.join(OUTPUT_DIR, '_team_issues_temp.json'), 'r', encoding='utf-8') as f:
    team_issues = json.load(f)

PROJECT_TEAMS = {
    'MAW': ['Abyss', 'Bigos'],
    'AENW': ['Radium', 'Europium'],
    'AETVP': ['Copernicium'],
    'PEPI': ['Mouflons', 'Wolves', 'ML Serving Sturgeons'],
    'RSW': ['Polonium UF', 'Capybaras'],
    'ML': ['ML Platform Pandas'],
    'EPCW': ['EP Core'],
    'PEA': ['Zurek'],
    'ASPW': ['Igni'],
    'EEEW': ['SRE']
}

# Build team-to-project mapping
team_project = {}
for proj, teams in PROJECT_TEAMS.items():
    for team in teams:
        team_project[team] = proj


def to_kebab(name):
    return name.lower().replace(' ', '-')


jql_template = 'project = {key} AND status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task'

for team_name, issues in team_issues.items():
    kebab = to_kebab(team_name)
    proj_key = team_project[team_name]

    # Write JSON file
    jira_json = {
        'query': {
            'jql': jql_template.format(key=proj_key),
            'project': proj_key,
            'team': team_name,
            'scan_date': '2026-06-29'
        },
        'issues': issues,
        'total': len(issues)
    }

    json_path = os.path.join(OUTPUT_DIR, f'{kebab}-jira.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(jira_json, f, indent=2, ensure_ascii=False)

    # Write TXT file
    txt_path = os.path.join(OUTPUT_DIR, f'{kebab}-jira.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f'Team: {team_name}\n')
        f.write(f'Project: {proj_key}\n')
        f.write(f'Active Issues: {len(issues)}\n')
        f.write(f'Scan Date: 2026-06-29\n')
        f.write('=' * 60 + '\n\n')

        if not issues:
            f.write('No active issues found.\n')
        else:
            for issue in issues:
                f.write(f"{issue['key']} | {issue['issuetype']} | {issue['status']}\n")
                f.write(f"  Summary: {issue['summary']}\n")
                f.write(f"  Assignee: {issue['assignee'] or 'Unassigned'}\n")
                f.write(f"  Priority: {issue['priority']}\n")
                f.write(f"  Updated: {issue['updated']}\n")
                f.write('\n')

# Clean up temp file
os.remove(os.path.join(OUTPUT_DIR, '_team_issues_temp.json'))

print('Jira files written successfully for all 15 teams.')
