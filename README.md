# WoW Scanner Tool

> Automated audit tool for extracting and analyzing **Definition of Ready (DoR)** and **Definition of Done (DoD)** across SRPOL teams using Confluence and Jira data.

---

## At a Glance

| | DoR Scanner | DoD Scanner |
|---|---|---|
| **Command** | `/wow-dor-scanner` | `/wow-dod-scanner` |
| **Steps** | 13 fully automated | 11 fully automated |
| **Data Sources** | Confluence + Jira | Confluence only |
| **Jira Filter** | In Progress, Code Review, In Development | N/A |
| **Analysis** | Compliance per issue + Quality per team | Quality per team |
| **Output** | `Report-DoR.xlsx` (3 sheets) + HTML | `Report-DoD.xlsx` (2 sheets) + HTML |

---

## How the DoR Scanner Works

The `/wow-dor-scanner` skill runs 13 steps end-to-end without user interaction:

```
Step 1-2    Configuration & Auth check (Atlassian MCP)
    |
Step 3-4    Calculate CET timestamp, create output folder
    |
Step 5-6    Fetch SRPOL Teams page, parse HTML table
    |        (extracts team page links + sprint board links)
    |
Step 7      Write initial teams.json
    |
Step 8      For each team:
    |          - Fetch team page, extract clean name from title
    |          - Locate "DoR - STORY/TASK" heading (ignores OFFERING/EPIC)
    |          - Follow linked DoR pages if section contains links
    |          - Save [team]-dor.txt
    |
Step 9      For each team:
    |          - Query Jira per project (Stories, Bugs, Tasks only)
    |          - Client-side filter by Team field (customfield_10114)
    |          - Paginate up to 500 issues per project
    |          - Save [team]-jira.json + [team]-jira.txt
    |
Step 10     Report extraction summary
    |
Step 11     DoR Compliance Analysis (LLM-based):
    |          11.2 - Fetch full description for EVERY issue via getJiraIssue
    |          11.3 - LLM compares each description against team DoR criteria
    |          11.4 - Aggregate results (Pass/Fail per issue)
    |          11.5 - Save compliance_data.json + summary_data.json
    |
Step 12     DoR Quality Assessment:
    |          - Load industry standard (assets/dor-standard.txt)
    |          - Fetch company standard (Confluence page)
    |          - Score each team's DoR against 10 standard criteria
    |          - Save quality_data.json
    |
Step 13     Generate final reports via template script:
              - Report-DoR.xlsx (3 sheets)
              - Report-DoR.html (self-contained dashboard)
```

### DoR Compliance Analysis (Step 11)

The compliance check fetches the **full Jira issue description** for every active issue, then uses LLM-based semantic analysis to determine whether the issue meets its team's DoR criteria.

**Key rules:**
- Empty descriptions automatically fail if DoR requires "clear description" or "acceptance criteria"
- Acceptance criteria are identified by structure (bullets, numbered lists, Given/When/Then)
- Only criteria explicitly listed in the team's DoR document are checked
- Results: "Pass" or "Fail" with a specific note referencing which DoR criterion was not met

### DoR Quality Assessment (Step 12)

Evaluates how **complete** each team's DoR document is against a standard 10-criteria checklist:

| # | Criterion | Score |
|---|-----------|-------|
| 1 | User Story/Requirement Clarity | 10 pts |
| 2 | Acceptance Criteria | 10 pts |
| 3 | Estimation/Sizing | 10 pts |
| 4 | Dependencies Identified & Resolved | 10 pts |
| 5 | Design/UX Specification | 10 pts |
| 6 | Scope/Sprint Fit | 10 pts |
| 7 | Risks/Blockers Identified | 10 pts |
| 8 | Stakeholder Alignment | 10 pts |
| 9 | Technical Feasibility Confirmed | 10 pts |
| 10 | Testing Strategy/Approach | 10 pts |

Coverage score = (criteria covered) x 10. Assessed against both industry best practices and the company's own DoR standard.

---

## How the DoD Scanner Works

The `/wow-dod-scanner` skill runs 11 steps end-to-end without user interaction:

```
Step 1-2    Configuration & Auth check (Atlassian MCP)
    |
Step 3-4    Calculate CET timestamp, create output folder
    |
Step 5-6    Fetch SRPOL Teams page, parse HTML table
    |
Step 7      Write initial teams.json
    |
Step 8      For each team:
    |          - Fetch team page, extract clean name from title
    |          - Locate "DoD - STORY/TASK" heading (ignores OFFERING/EPIC)
    |          - Follow linked DoD pages if section contains links
    |          - Save [team]-dod.txt
    |
Step 9      Save summary_data.json (all teams with DoD Yes/No status)
    |
Step 10     DoD Quality Assessment (LLM-based):
    |          - Load industry standard (assets/dod-standard.txt)
    |          - Fetch company DoD standard (Confluence page)
    |          - Score across 7 weighted dimensions
    |          - Save quality_data.json
    |
Step 11     Generate final reports via template script:
              - Report-DoD.xlsx (2 sheets)
              - Report-DoD.html (self-contained dashboard)
```

### DoD Quality Assessment (Step 10)

Uses a 7-dimension weighted model to score each team's DoD document:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Coverage | 25% | How many of 10 essential DoD areas are addressed |
| Clarity & Specificity | 20% | Are criteria concrete and unambiguous? |
| Measurability | 15% | Can each criterion be objectively verified? |
| Company Alignment | 15% | Alignment with company-level DoD guidance |
| Industry Best Practices | 10% | Adherence to Scrum Guide, SAFe |
| Actionability | 10% | Clear ownership and behavioral guidance |
| Evidence Requirements | 5% | What artifacts prove "done"? |

Overall score = weighted average (0-100). Results include a short note per team listing specific gaps.

---

## Output Structure

Each scan creates a timestamped folder under `assets/teams/`:

```
assets/teams/20260629 10-08/
  |
  |-- teams.json                  # Master metadata (all teams, statuses, errors)
  |
  |-- [team]-dor.txt              # Extracted DoR criteria (DoR scanner)
  |-- [team]-dod.txt              # Extracted DoD criteria (DoD scanner)
  |-- [team]-jira.json            # Full Jira issue data (DoR scanner only)
  |-- [team]-jira.txt             # Human-readable issue list (DoR scanner only)
  |
  |-- issue_descriptions.json     # Fetched issue descriptions (DoR scanner, audit trail)
  |-- compliance_data.json        # Pass/Fail per issue (DoR scanner)
  |-- summary_data.json           # Team overview data
  |-- quality_data.json           # Quality scores per team
  |
  |-- Report-DoR.xlsx             # Final Excel report (DoR scanner)
  |-- Report-DoR.html             # HTML dashboard (DoR scanner)
  |-- Report-DoD.xlsx             # Final Excel report (DoD scanner)
  |-- Report-DoD.html             # HTML dashboard (DoD scanner)
  |-- DOR_ANALYSIS_SUMMARY.md     # Markdown summary (DoR scanner)
```

### Report Sheets

**Report-DoR.xlsx** contains 3 sheets:

| Sheet | Content |
|-------|---------|
| Summary | KPIs (% teams with DoR, % tasks fitting DoR) + team overview table |
| DoR Compliance | Per-issue analysis: Team, Issue Key, Type, URL, Title, Status, Assignee, Pass/Fail, Note |
| DoR quality | Per-team coverage scores sorted by quality descending + improvement notes |

**Report-DoD.xlsx** contains 2 sheets:

| Sheet | Content |
|-------|---------|
| Summary | KPI (% teams with DoD) + team overview table |
| DoD quality | Per-team quality scores sorted descending + notes on gaps |

---

## Prerequisites

- **Claude Code CLI** with Atlassian MCP plugin configured
- **Python 3** with `openpyxl` package installed
- Access to the target Atlassian/Confluence instance

### Configure Atlassian MCP

```bash
claude-code config atlassian
```

Follow the prompts to authenticate with your Atlassian instance.

---

## Installation

1. Copy the entire `wow-scanner-tool` folder to your project directory
2. Claude Code discovers the skills automatically
3. Run `/wow-dor-scanner` or `/wow-dod-scanner`

---

## Project Structure

```
wow-scanner-tool/
  .claude/skills/
    wow-dor-scanner/
      skill.md              # DoR scanner (13 steps)
    wow-dod-scanner/
      skill.md              # DoD scanner (11 steps)
  assets/
    dor-standard.txt        # Industry DoR best practices (persistent reference)
    dod-standard.txt        # Industry DoD best practices (persistent reference)
    templates/
      generate_reports.py       # Canonical DoR report generator
      generate_dod_reports.py   # Canonical DoD report generator
      validate_reports.py       # DoR report schema validator
      validate_dod_reports.py   # DoD report schema validator
      validate_compliance.py    # Compliance integrity validator
      data-schemas.md           # JSON data schemas reference
      dod-data-schemas.md       # DoD JSON data schemas reference
    teams/                  # Timestamped scan outputs
      YYYYMMDD HH-MM/      # One folder per scan run
  src/
    generate-dod-report.py  # (Legacy - not used by current skills)
  scripts/
    extract_jira_issues.py  # (Legacy utility)
```

---

## Technical Details

| Property | Value |
|----------|-------|
| Scanner version | 4.0 |
| Timestamps | CET timezone, format `YYYYMMDD HH-MM` |
| Team field | Jira `customfield_10114` (client-side filtering) |
| Issue types | Story, Bug, Task (Sub-tasks excluded) |
| Pagination | Up to 500 issues per project (5 pages x 100) |
| Error handling | Continue-on-error (partial results saved) |
| Report generation | Template-based (deterministic, not LLM-generated) |
| Analysis method | LLM semantic analysis (Claude) |

---

## Troubleshooting

<details>
<summary><strong>Atlassian MCP not configured</strong></summary>

Run `claude-code config atlassian` to set up authentication. Verify you have access to the Confluence instance.
</details>

<details>
<summary><strong>Cannot access Atlassian</strong></summary>

- Check your authentication token is valid
- Verify you have permissions to view the pages
- Try accessing the page in your browser first
</details>

<details>
<summary><strong>DoR/DoD criteria not found</strong></summary>

The tool searches for headings containing "Definition of Ready/Done", "DoR/DoD", etc. Check if the team page uses a different heading format. The tool will save a file noting the criteria were not found.
</details>

<details>
<summary><strong>DoR/DoD Standard document not found</strong></summary>

Ensure `assets/dor-standard.txt` and `assets/dod-standard.txt` exist. These are required for quality assessment steps. If missing, quality assessment is skipped with a warning.
</details>

<details>
<summary><strong>Template script not found</strong></summary>

The report generator scripts must exist at `assets/templates/generate_reports.py` (DoR) and `assets/templates/generate_dod_reports.py` (DoD). If missing, reports cannot be generated.
</details>

<details>
<summary><strong>Incomplete extraction</strong></summary>

Check `teams.json` for `extraction_status` and `extraction_error` fields per team. Individual team failures do not stop the entire scan.
</details>

---

## Sharing

1. Zip the entire `wow-scanner-tool` folder
2. Share the zip file
3. Recipients extract to their project root
4. Skills are immediately available via `/wow-dor-scanner` or `/wow-dod-scanner`

Recipients need to configure their own Atlassian MCP credentials.
