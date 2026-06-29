import json
import os

OUTPUT_DIR = 'C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260629 10-08'

projects = {
    'MAW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_012AitfA7UTkooznmokgwaQi.txt',
    'AENW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01XctfhFPyLVPfQPeTutbB15.txt',
    'AETVP': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_013QKrDMhofNJpV91LUtixhz.txt',
    'PEPI': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01Brj2zZwX28yD9CjvYgbY6H.txt',
    'RSW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01D45pcWo7SaHUfqKZeawmSP.txt',
    'EPCW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01MG4TF5fQLaxHg4g9uqx5h8.txt',
    'PEA': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01XPGRoBFWdQNMxZEvjBqMnV.txt',
    'ASPW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01HTjFx2P7oYL6RhApdHsNAv.txt',
    'EEEW': 'C:/Users/i.klyha/.claude/projects/C--Users-i-klyha-Desktop-Claude-wow-scanner-tool/d8c97a6f-0662-4ad9-8c18-a2374ccd669a/tool-results/toolu_bdrk_01WKrshP7oHwninZ2mJpXEi6.txt'
}

TEAM_NAME_PATTERNS = {
    'Abyss': 'PE - WAW - Abyss',
    'Radium': 'AE - WAW - Radium',
    'Europium': 'AP - WAW - Europium',
    'Copernicium': 'AE - WAW - Copernicium',
    'Mouflons': 'AS - WAW - Mouflons',
    'Wolves': 'AS - WAW - Wolves',
    'Polonium UF': 'AS - WAW - Polonium UF',
    'Bigos': 'AS - WAW - Bigos',
    'Capybaras': 'AS - WAW - Capybaras',
    'ML Serving Sturgeons': 'T - WAW - ML Sturgeons',
    'ML Platform Pandas': 'T - WAW - ML Pandas',
    'Zurek': 'T - WAW - Zurek',
    'EP Core': 'T - WAW - EP Core',
    'Igni': 'AP - WAW - Igni',
    'SRE': 'T - WAW - Embedded SREs SRPOL'
}

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

# Build a map of issue key -> description from all project files
issue_descriptions = {}

for proj, filepath in projects.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for issue in data['issues']['nodes']:
        key = issue['key']
        desc = issue['fields'].get('description', '')
        summary = issue['fields'].get('summary', '')
        team_field = issue['fields'].get('customfield_10114')
        team_name = None
        if team_field and isinstance(team_field, dict):
            team_name = team_field.get('value') or team_field.get('name')
        elif team_field and isinstance(team_field, str):
            team_name = team_field
        issue_descriptions[key] = {
            'key': key,
            'summary': summary,
            'description': desc or '',
            'team': team_name
        }

# Add ML issues
issue_descriptions['ML-55'] = {
    'key': 'ML-55',
    'summary': 'Implement Test DAG MLOps based on SDK',
    'description': 'Acceptance criteria:\n\n1. Test DAG fully written using SDK\n2. Test DAG successfully running E2E 2.10.3\n\n',
    'team': None
}
issue_descriptions['ML-10'] = {
    'key': 'ML-10',
    'summary': 'Support after MWAA upgrade to 2.10.3',
    'description': 'Provide support and handle issues arising from the MWAA upgrade to version 2.10.3.\n\nThis includes monitoring for compatibility issues, fixing DAG failures caused by the upgrade, and ensuring all pipelines are running correctly on the new version.\n\nAcceptance criteria:\n\nTBD',
    'team': None
}

# Now filter to only the 84 issues we care about
teams_file = os.path.join(OUTPUT_DIR, 'teams.json')
with open(teams_file, 'r', encoding='utf-8') as f:
    teams_data = json.load(f)

# Get list of all team issue keys
all_team_keys = set()
teams_list = ['abyss','radium','europium','copernicium','mouflons','wolves','polonium-uf','bigos','capybaras','ml-serving-sturgeons','ml-platform-pandas','zurek','ep-core','igni','sre']
for t in teams_list:
    fp = os.path.join(OUTPUT_DIR, f'{t}-jira.json')
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for issue in data['issues']:
        all_team_keys.add(issue['key'])

# Filter descriptions to only our team issues
filtered_descriptions = {}
for key in all_team_keys:
    if key in issue_descriptions:
        filtered_descriptions[key] = issue_descriptions[key]
    else:
        filtered_descriptions[key] = {
            'key': key,
            'summary': '',
            'description': '',
            'team': None
        }

# Write issue_descriptions.json
output_path = os.path.join(OUTPUT_DIR, 'issue_descriptions.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_descriptions, f, indent=2, ensure_ascii=False)

print(f'Written {len(filtered_descriptions)} issue descriptions to issue_descriptions.json')
print(f'Issues with non-empty descriptions: {sum(1 for v in filtered_descriptions.values() if v["description"])}')
print(f'Issues with empty/null descriptions: {sum(1 for v in filtered_descriptions.values() if not v["description"])}')
