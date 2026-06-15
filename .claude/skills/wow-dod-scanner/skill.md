---
name: wow-dod-scanner
description: >
  Extract SRPOL team data and DoD - STORY/TASK criteria from the SRPOL Teams Confluence page.
  Generates Excel report showing which teams have DoD defined and assesses DoD quality per team
  against industry and company standards. Requires Atlassian MCP. Usage: /wow-dod-scanner
---

# WoW DoD Scanner Skill

Extracts team information and Definition of Done (DoD) - STORY/TASK criteria from the SRPOL Teams Confluence page. Generates a report showing which teams have DoD defined and which do not.

## Usage

```
/wow-dod-scanner
```

No parameters required. The skill automatically scans the SRPOL Teams page at:
https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams

## What It Does

1. Checks Atlassian MCP authentication
2. Extracts from Confluence:
   - Team page links and sprint board links from directory table
   - Team names from actual Confluence page titles (cleaned by removing "Team", "Team Space" etc.)
   - Definition of Done (DoD) - STORY/TASK criteria from each team's page (excludes DoD - OFFERING/EPIC)
   - If DoD section is empty but contains a link, follows the link to extract DoD from the referenced page
3. Generates Report:
   - Excel report with 1 sheet: Summary (Team | DoD) showing which teams have DoD defined
   - KPI: "% Teams with DoD"
4. Saves all data to absolute path: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\<timestamp>/` where timestamp is in CET format: `YYYYMMDD HH-MM`
   - DoD files: `[team-name]-dod.txt`
   - Master file: `teams.json`
   - Report: `Report-DoD.xlsx`

## Instructions

**CRITICAL - FULL AUTOMATION:** This skill must execute all 10 steps automatically without pausing or asking for user confirmation. Only stop execution if:
- Authentication fails (Step 2)
- Critical errors occur that prevent continuation
- Prerequisites are missing (e.g., no teams found)

Do NOT pause between steps to ask for approval.

When invoked:

### Step 1: Configuration

Use the hardcoded SRPOL Teams page configuration:
- **URL**: `https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams`
- **cloudId**: `adgear.atlassian.net`
- **pageId**: `19470090380`
- **Page Title**: `SRPOL Teams`

No user input required.

### Step 2: Check Atlassian MCP Authentication

Before proceeding, verify Atlassian MCP is configured and accessible.

Use ToolSearch to check if Atlassian MCP tools are available:
```
ToolSearch("select:mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources")
```

If tools not found, show error:
```
Error: Atlassian MCP plugin not configured.

To configure Atlassian MCP:
1. Run: claude-code config atlassian
2. Follow the authentication prompts
3. Verify you have access to adgear.atlassian.net

Then try the /wow-dod-scanner command again.
```

If tools found, attempt a test call:
```
mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources()
```

### Step 3: Calculate CET Timestamp

Calculate the current timestamp in CET (Central European Time):
- Get current UTC time using Bash: `date -u +"%Y-%m-%d %H:%M:%S"`
- Convert to CET (UTC+1 standard Nov-Mar, UTC+2 DST Mar-Nov)
- Format as: `YYYYMMDD HH-MM`
- Store this timestamp for use in all file operations

### Step 4: Prepare Output Folder

Create the timestamped output directory:
```bash
mkdir -p "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]"
```

Store full absolute path as OUTPUT_DIR for all subsequent operations.

### Step 5: Fetch Main SRPOL Teams Page

```
mcp__plugin_atlassian_atlassian__getConfluencePage(
  cloudId: "adgear.atlassian.net",
  pageId: "19470090380",
  contentFormat: "html"
)
```

### Step 6: Extract Table Data

Parse the HTML table to extract team page links and sprint board links. Same logic as wow-dor-scanner: extract page IDs from URLs, build list of team references.

### Step 7: Generate Initial teams.json

Write master JSON with metadata and empty teams array to `${OUTPUT_DIR}/teams.json`.

```json
{
  "metadata": {
    "scan_date": "[current ISO-8601 timestamp]",
    "scan_timestamp_cet": "[CET_TIMESTAMP]",
    "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
    "team_count": [number of teams],
    "cloudId": "adgear.atlassian.net",
    "scanner_version": "2.0"
  },
  "teams": []
}
```

### Step 8: Extract DoD Per Team

For each team:

1. **Fetch team page and extract name** (same cleaning rules as wow-dor-scanner)
   - For names with "XX - YYY - Name" pattern, extract ONLY the last segment

2. **Search for DoD section:**
   Look for headings containing:
   - "DEFINITION OF DONE (DoD) - STORY/TASK"
   - "DEFINITION OF DONE (DoD) - STORY"
   - "Definition of Done (DoD) - STORY/TASK"
   - "Definition of Done (DoD)" (without OFFERING/EPIC)
   - "Definition of Done" (plain)
   - "Team DoD"
   - "DoD" (standalone heading)
   
   **CRITICAL:** IGNORE headings containing:
   - "DEFINITION OF DONE (DoD) - OFFERING/EPIC"
   - "- OFFERING/EPIC"
   - "- OFFERING"
   - "- EPIC"

3. **Check for DoD links (ONLY if DoD heading was found):**
   Same logic as wow-dor-scanner: follow links within DoD section to external pages.
   **CRITICAL:** If NO DoD heading exists on the page at all, mark as "not_found". Do NOT follow random links.

4. **Extract content:** Capture all content after DoD heading, stop at next major heading. Convert HTML to plain text.

5. **Save to file:** `${OUTPUT_DIR}/[team-name-kebab]-dod.txt` (DoD content only, no metadata)
   - If DoD not found, save: "DoD - STORY/TASK criteria not found on team page."

6. **Update teams.json** with team entry:
   ```json
   {
     "name": "[Team Name]",
     "page_link": "[Full URL]",
     "sprint_board_link": "[Sprint Board URL or null]",
     "dod_file": "[team-name-kebab]-dod.txt",
     "page_id": "[Page ID]",
     "extraction_status": "success | not_found | error",
     "dod_source": "direct | linked_page | null"
   }
   ```

### Step 9: Generate Report-DoD.xlsx and Report Completion

#### Step 9.1: Generate Report-DoD.xlsx

Use Python/openpyxl to generate Report-DoD.xlsx with EXACTLY 1 sheet.

##### Report-DoD.xlsx Schema Specification

**Sheet Count:** Exactly ONE sheet
**Sheet 1 Name:** "Summary"

**KPI Summary Section (row 1):**

| Row | Column A | Column B |
|-----|----------|----------|
| 1 | "% Teams with DoD" | "{X}%" |
| 2 | *(empty row - separator)* | |

**KPI Formatting:**
- Bold font, left-aligned
- Green font color if >= 70%, Orange if 40-69%, Red if < 40%

**KPI Calculation:**
- % Teams with DoD = (teams with DoD "Yes") / (total teams) * 100, rounded to 1 decimal

**Table Header Row (row 3):**

| Column | Header Text | Width |
|--------|-------------|-------|
| A | Team | 25 |
| B | DoD | 10 |

**Data rows (4+):**
- Column A: ALL team names extracted from SRPOL Teams page
- Column B: "Yes" if team has DoD defined (extraction_status = "success"), "No" if not found
  - "Yes": Green background (#C6EFCE)
  - "No": Red background (#FFC7CE)

**Formatting:**
- Header row: Dark blue background (#366092), white bold font, center aligned
- Data rows: Thin borders, vertical center
- Freeze panes at A4

**Python script structure:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Summary"

# KPI
teams_with_dod = sum(1 for t in teams if t["has_dod"])
total_teams = len(teams)
pct = round(teams_with_dod / total_teams * 100, 1)

ws.cell(1, 1).value = "% Teams with DoD"
ws.cell(1, 1).font = Font(bold=True, size=11)
ws.cell(1, 2).value = f"{pct}%"
if pct >= 70:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="006600")
elif pct >= 40:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="CC6600")
else:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="CC0000")

# Header row 3
header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF", size=11)
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                     top=Side(style='thin'), bottom=Side(style='thin'))

for col, (header, width) in enumerate([("Team", 25), ("DoD", 10)], 1):
    cell = ws.cell(3, col)
    cell.value = header
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = thin_border
    ws.column_dimensions[get_column_letter(col)].width = width

# Data rows
yes_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
no_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

for row_idx, team in enumerate(teams, 4):
    ws.cell(row_idx, 1).value = team["name"]
    ws.cell(row_idx, 1).border = thin_border
    ws.cell(row_idx, 1).alignment = Alignment(vertical='center')

    dod_val = "Yes" if team["has_dod"] else "No"
    cell = ws.cell(row_idx, 2)
    cell.value = dod_val
    cell.fill = yes_fill if dod_val == "Yes" else no_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', vertical='center')

ws.freeze_panes = 'A4'
wb.save(f"{OUTPUT_DIR}/Report-DoD.xlsx")
```

**Fallback:** If openpyxl unavailable, create CSV with same data.

#### Step 9.2: Update teams.json with final metadata

```json
{
  "metadata": {
    ...
    "analysisCompleted": true,
    "reportFile": "Report-DoD.xlsx",
    "kpis": {
      "pctTeamsWithDod": 87
    }
  }
}
```

#### Step 9.3: Output final summary

```
=== DoD Extraction Complete ===

Source: SRPOL Teams page
Scan timestamp (CET): [CET_TIMESTAMP]
Teams found: [X]

DoD Status:
  - Teams with DoD: [Y] ({pct}%)
  - Teams without DoD: [Z]

Teams without DoD:
  - [team names list]

Report saved to: ${OUTPUT_DIR}/Report-DoD.xlsx
Files saved to: ${OUTPUT_DIR}/

All files:
  - teams.json
  - DoD files: [team1]-dod.txt, [team2]-dod.txt, ...
  - Report-DoD.xlsx
```

### Step 10: DoD Quality Assessment (AUTO-EXECUTE after Step 9)

**This step executes automatically after Step 9 completes.** Do not pause or ask for user confirmation. This step assesses the QUALITY of each team's Definition of Done document.

#### Step 10.0: Load DoD Standard Reference

Read the persistent DoD Standard reference document:
```
Read("C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\dod-standard.txt")
```

If the file does not exist, output warning and skip Step 10 entirely:
```
[WARNING] DoD Standard document not found at assets/dod-standard.txt
Skipping DoD Quality Assessment.
```

Store content as `dod_standard_text`.

#### Step 10.1: Fetch Company DoD Standard

Fetch the company's Definition of Done page from Confluence:
```
mcp__plugin_atlassian_atlassian__getConfluencePage(
  cloudId: "adgear.atlassian.net",
  pageId: "21735212005",
  contentFormat: "markdown"
)
```

Store as `company_dod_text`. Save to `${OUTPUT_DIR}/company-dod-standard.txt` for traceability.

If fetch fails, log warning but continue using only the industry standard.

#### Step 10.2: Identify Teams to Assess

Only teams with defined DoD (extraction_status = "success") are assessed. Teams without DoD are excluded.

#### Step 10.3: Quality Assessment (LLM-Based)

For each team with a defined DoD, evaluate quality. Process all teams in a single batched LLM call:

**Assessment Prompt:**
```
You are evaluating the quality of a team's Definition of Done (DoD) document.

INDUSTRY STANDARD (best practices reference):
---
${dod_standard_text}
---

COMPANY STANDARD (organizational DoD guidance):
---
${company_dod_text}
---

TEAM DoD TO ASSESS (Team: ${team_name}):
---
${team_dod_text}
---

Evaluate this team's DoD across 7 dimensions. Score each dimension 0-100:

1. COVERAGE (weight: 25%): How many of these 10 essential areas are addressed?
   - Code Review Completed
   - Unit/Integration Tests Written and Passing
   - Acceptance Criteria Met and Verified
   - CI/CD Pipeline Passing
   - Deployed to Staging/Production
   - Documentation Updated
   - No Known Defects / Technical Debt Documented
   - Performance/Security Validated (if applicable)
   - Monitoring/Alerting Configured
   - PO/Stakeholder Acceptance
   Score: (areas covered / 10) * 100

2. CLARITY & SPECIFICITY (weight: 20%): Are criteria specific and unambiguous?
   - 100 = every criterion is concrete, specific, verifiable
   - 50 = mix of specific and vague criteria
   - 0 = all criteria are generic/copy-paste

3. MEASURABILITY (weight: 15%): Can each criterion be objectively verified?
   - 100 = all criteria have clear pass/fail checks
   - 50 = some criteria are subjective
   - 0 = criteria cannot be consistently evaluated

4. COMPANY STANDARD ALIGNMENT (weight: 15%): Alignment with company DoD page
   - Consistent bar for completeness
   - Reduces hidden work and rework
   - Multi-level DoD (task, story, feature)
   - Visible, achievable, evolutionary
   Score based on how well the team DoD reflects these principles

5. INDUSTRY BEST PRACTICES (weight: 10%): Adherence to Scrum Guide, SAFe
   - 100 = exemplifies industry best practices
   - 50 = follows some practices
   - 0 = contradicts established practices

6. ACTIONABILITY (weight: 10%): Does DoD drive specific behaviors?
   - 100 = clear ownership, workflow integration, verification methods
   - 50 = some actionable guidance
   - 0 = passive checklist with no behavioral guidance

7. EVIDENCE REQUIREMENTS (weight: 5%): Does DoD specify what evidence is needed?
   - 100 = specific evidence requirements for each criterion
   - 50 = mentions evidence for some criteria
   - 0 = no mention of evidence or verification artifacts

RESPOND IN VALID JSON ONLY. Array of objects, one per team:
[
  {
    "team": "Team Name",
    "coverage": <0-100>,
    "clarity": <0-100>,
    "measurability": <0-100>,
    "company_alignment": <0-100>,
    "industry_alignment": <0-100>,
    "actionability": <0-100>,
    "evidence": <0-100>,
    "overall": <weighted average as integer>,
    "note": "<short specific comment on main gaps/weaknesses, max 80 chars>"
  }
]

The "note" field must be SHORT and SPECIFIC. Focus on what is MISSING or WEAK.
Do NOT include positive feedback in the note. Only gaps and weaknesses.
If the DoD is excellent (score >= 90), note can be: "Comprehensive, minor gaps only"
```

**Weighted Average Calculation:**
```
overall = round(
  coverage * 0.25 +
  clarity * 0.20 +
  measurability * 0.15 +
  company_alignment * 0.15 +
  industry_alignment * 0.10 +
  actionability * 0.10 +
  evidence * 0.05
)
```

#### Step 10.4: Add "DoD quality" Sheet to Report-DoD.xlsx

Use Python with openpyxl to open the existing Report-DoD.xlsx and add a second sheet:

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = load_workbook(f"{OUTPUT_DIR}/Report-DoD.xlsx")
ws = wb.create_sheet("DoD quality")

# Row 1: KPI
ws.cell(1, 1).value = "DoD quality lvl"
ws.cell(1, 1).font = Font(bold=True, size=11)
ws.cell(1, 2).value = f"{average_quality}%"
if average_quality >= 70:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="006600")
elif average_quality >= 40:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="CC6600")
else:
    ws.cell(1, 2).font = Font(bold=True, size=11, color="CC0000")

# Row 3: Table header
header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF", size=11)
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                     top=Side(style='thin'), bottom=Side(style='thin'))

for col, (header, width) in enumerate([("Team", 25), ("Quality", 12), ("Note", 60)], 1):
    cell = ws.cell(3, col)
    cell.value = header
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = thin_border
    ws.column_dimensions[get_column_letter(col)].width = width

# Data rows (sorted by quality descending)
green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
orange_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

for row_idx, result in enumerate(sorted_results, 4):
    ws.cell(row_idx, 1).value = result["team"]
    ws.cell(row_idx, 1).border = thin_border

    quality_cell = ws.cell(row_idx, 2)
    quality_cell.value = f"{result['overall']}%"
    quality_cell.border = thin_border
    quality_cell.alignment = Alignment(horizontal='center')
    if result['overall'] >= 70:
        quality_cell.fill = green_fill
    elif result['overall'] >= 40:
        quality_cell.fill = orange_fill
    else:
        quality_cell.fill = red_fill

    note_cell = ws.cell(row_idx, 3)
    note_cell.value = result["note"]
    note_cell.border = thin_border
    note_cell.alignment = Alignment(wrap_text=True)

ws.freeze_panes = 'A4'
wb.save(f"{OUTPUT_DIR}/Report-DoD.xlsx")
```

**CRITICAL:** Use `load_workbook()` to preserve existing "Summary" sheet.
**Fallback:** If openpyxl fails, create standalone DoD-Quality.csv.

#### Step 10.5: Report DoD Quality Assessment Completion

```
=== DoD Quality Assessment Complete ===

Teams Assessed: ${count}
Average DoD Quality: ${average_quality}%

Top Quality DoDs:
  1. ${top1_team} - ${top1_score}%
  2. ${top2_team} - ${top2_score}%
  3. ${top3_team} - ${top3_score}%

Needs Improvement:
  1. ${bottom1_team} - ${bottom1_score}% (${bottom1_note})
  2. ${bottom2_team} - ${bottom2_score}% (${bottom2_note})
  3. ${bottom3_team} - ${bottom3_score}% (${bottom3_note})

Results added to: ${OUTPUT_DIR}/Report-DoD.xlsx (sheet "DoD quality")

Standards used:
  - Industry: assets/dod-standard.txt
  - Company: Confluence page 21735212005 (Definition of Done DoD)
```

**Error handling for Step 10:**
- If dod-standard.txt missing: skip entire Step 10 with warning
- If company DoD page fetch fails: continue with industry standard only
- If LLM evaluation fails: retry once, then mark as "assessment_failed" with score 0
- If Report-DoD.xlsx cannot be loaded: create standalone DoD-Quality.csv

## Error Handling

- **Continue on error:** If one team page fails, continue with remaining teams
- **Track failures:** Record all errors in teams.json metadata
- **Graceful degradation:** Partial data is better than no data

**Automation Rules:**
- **Only stop for critical failures:** Continue execution through all 10 steps unless:
  - Authentication fails completely (Step 2)
  - No teams found in source page (Step 5)
  - Output directory cannot be created (Step 4)
- **Do not stop for partial failures:** If some teams fail, continue with successful teams
- **Automatic Step 10:** Execute Step 10 (DoD quality assessment) automatically after Step 9. Skip only if assets/dod-standard.txt does not exist

## Tool Requirements

Required tools:
- **ToolSearch** - Check for Atlassian MCP availability
- **mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources** - Verify authentication
- **mcp__plugin_atlassian_atlassian__getConfluencePage** - Fetch Confluence pages
- **Write** - Create JSON, TXT, Python files
- **Read** - Verify file contents
- **Bash** - Create directories, get current time, execute Python scripts

Optional tools:
- **Grep** - Search for patterns
- **Glob** - Find files
- **Python 3 + openpyxl** - Generate Excel reports (fallback to CSV if unavailable)

## Important Rules

1. **DoD Scope:** Extract ONLY "DEFINITION OF DONE (DoD) - STORY/TASK" or plain "DEFINITION OF DONE (DoD)", completely ignore "- OFFERING/EPIC" sections

2. **Team Naming:** Same rules as wow-dor-scanner (clean page titles, extract last segment from prefix patterns)

3. **File Naming:** Use kebab-case for all team file names

4. **Timestamp Consistency:** Calculate CET timestamp ONCE and use consistently

5. **Linked DoD Pages:** Follow links in DoD sections to extract from referenced pages. ONLY if DoD heading was found first.

6. **Report-DoD.xlsx Fixed Schema:**
   - Step 9 creates 1 sheet: "Summary" (KPI + Team|DoD table)
   - Step 10 adds a 2nd sheet: "DoD quality" (does not modify Summary sheet)
   - Summary: KPI row "% Teams with DoD" + 2-column table (Team, DoD)
   - DoD quality: KPI row "DoD quality lvl" + 3-column table (Team, Quality, Note)
   - DoD values: "Yes" (green) or "No" (red)

7. **DoD Quality Assessment (Step 10):**
   - Only assesses teams that have defined DoD
   - Uses BOTH industry standard (assets/dod-standard.txt) AND company standard (Confluence page 21735212005)
   - Quality score is 1-100% integer per team
   - Added as 2nd sheet to existing Report-DoD.xlsx
   - "Note" column contains short, specific feedback on what is missing/weak
