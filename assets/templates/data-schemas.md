# DoR Scanner - Report Data Schemas

These schemas define the exact JSON format expected by `generate_reports.py`.
The LLM produces these JSON files; Python renders the reports.

## summary_data.json

Array of exactly 15 entries (one per SRPOL team, in order):

```json
[
  {
    "team": "string - team display name",
    "dor": "Yes | No",
    "jira_tasks": "integer - count of issues analyzed for this team",
    "pct_fitting_dor": "string - 'X%' (rounded, no decimal) or '-'"
  }
]
```

Rules:
- Always 15 entries, always in team order (Abyss, Radium, Europium, Copernicium, Mouflons, Wolves, Polonium UF, Bigos, Capybaras, ML Serving Sturgeons, ML Platform Pandas, EP Core, Zurek, Igni, SRE)
- `dor`: "Yes" if team has DoR extracted successfully; "No" otherwise
- `jira_tasks`: 0 if team had no active issues (never negative, never null)
- `pct_fitting_dor`: "-" if jira_tasks==0 OR dor=="No"; otherwise "X%" where X = round(pass/total*100)

## compliance_data.json

Array of 0+ entries (one per analyzed issue, only for teams with DoR AND active issues):

```json
[
  {
    "team": "string - team display name",
    "issue_key": "string - e.g. AENW-1042",
    "issue_type": "Story | Bug | Task",
    "url": "string - full Jira URL (https://adgear.atlassian.net/browse/XXX-NNN)",
    "title": "string - issue summary/title",
    "status": "string - In Progress | Code Review | In Development",
    "assignee": "string - display name or 'Unassigned'",
    "dor_compliance": "Pass | Fail",
    "note": "string - empty if Pass; explanation if Fail"
  }
]
```

Rules:
- Only issues from teams where dor=="Yes" AND jira_tasks > 0
- `dor_compliance`: exactly "Pass" or "Fail" (not Yes/No, not PASS/FAIL)
- `note`: MUST be "" (empty string) when dor_compliance=="Pass"
- `note`: MUST be non-empty when dor_compliance=="Fail"
- Note format: semicolon-separated DoR criteria references

## quality_data.json

Array of entries for teams with DoR defined (excludes teams where dor=="No"):

```json
[
  {
    "team": "string - team display name",
    "coverage": "integer - 0 to 100, always multiple of 10",
    "covered_criteria": "[array of integers 1-10 representing covered criterion numbers]",
    "missing_criteria": "[array of integers 1-10 representing missing criterion numbers]",
    "note": "string - 'Missing: X, Y, Z' or 'All standard criteria covered'"
  }
]
```

Rules:
- `coverage` = len(covered_criteria) * 10 (always 0, 10, 20, ..., 100)
- `covered_criteria` + `missing_criteria` = [1,2,3,4,5,6,7,8,9,10] (complete set)
- `note` format when missing: "Missing: {criterion_name_1}, {criterion_name_2}, ..."
- Criterion names from the standard (must use these exact names in Note):
  1. User Story/Requirement Clarity
  2. Acceptance Criteria
  3. Estimation/Sizing
  4. Dependencies Identified & Resolved
  5. Design/UX Specification
  6. Scope/Sprint Fit
  7. Risks/Blockers Identified
  8. Stakeholder Alignment
  9. Technical Feasibility Confirmed
  10. Testing Strategy/Approach
