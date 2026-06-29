import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUTPUT_DIR = 'C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260629 10-08'

with open(os.path.join(OUTPUT_DIR, 'issue_descriptions.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

teams_list = ['abyss', 'radium', 'europium', 'copernicium', 'mouflons', 'wolves',
              'polonium-uf', 'bigos', 'capybaras', 'ml-serving-sturgeons',
              'ml-platform-pandas', 'zurek', 'ep-core', 'igni', 'sre']

for t in teams_list:
    fp = os.path.join(OUTPUT_DIR, f'{t}-jira.json')
    with open(fp, 'r', encoding='utf-8') as f:
        tdata = json.load(f)
    print(f'=== {tdata["query"]["team"]} ({len(tdata["issues"])} issues) ===')
    for issue in tdata['issues']:
        key = issue['key']
        desc_data = data.get(key, {})
        desc = desc_data.get('description', '') or ''
        desc_preview = desc[:200].replace('\n', ' ') if desc else '[NO DESCRIPTION]'
        print(f'  {key}: {issue["summary"][:80]}')
        print(f'    Desc: {desc_preview}')
    print()
