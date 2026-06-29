import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUTPUT_DIR = 'C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/teams/20260629 10-08'

# Load issue descriptions
with open(os.path.join(OUTPUT_DIR, 'issue_descriptions.json'), 'r', encoding='utf-8') as f:
    issue_descs = json.load(f)

# Load compliance data passed as argument (pre-analyzed)
with open(os.path.join(OUTPUT_DIR, '_compliance_input.json'), 'r', encoding='utf-8') as f:
    compliance_input = json.load(f)

# Write compliance_data.json
with open(os.path.join(OUTPUT_DIR, 'compliance_data.json'), 'w', encoding='utf-8') as f:
    json.dump(compliance_input['compliance_data'], f, indent=2, ensure_ascii=False)

# Write summary_data.json
with open(os.path.join(OUTPUT_DIR, 'summary_data.json'), 'w', encoding='utf-8') as f:
    json.dump(compliance_input['summary_data'], f, indent=2, ensure_ascii=False)

print('compliance_data.json and summary_data.json written successfully.')
