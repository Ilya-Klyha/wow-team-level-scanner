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
3. Assesses DoD Quality:
   - Evaluates each team's DoD document against industry standard (assets/dod-standard.txt) and company standard (Confluence page 21735212005)
   - 7-dimension weighted scoring: Coverage (25%), Clarity (20%), Measurability (15%), Company Alignment (15%), Industry (10%), Actionability (10%), Evidence (5%)
4. Generates Reports:
   - Excel report: `Report-DoD.xlsx` (2 sheets: Summary + DoD quality)
   - HTML dashboard: `Report-DoD.html` (self-contained visual report)
5. Saves all data to absolute path: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\<timestamp>/` where timestamp is in CET format: `YYYYMMDD HH-MM`
   - DoD files: `[team-name]-dod.txt`
   - Master file: `teams.json`
   - Data files: `summary_data.json`, `quality_data.json`
   - Reports: `Report-DoD.xlsx`, `Report-DoD.html`

## Instructions

**CRITICAL - FULL AUTOMATION:** This skill must execute all 11 steps automatically without pausing or asking for user confirmation. Only stop execution if:
- Authentication fails (Step 2)
- Critical errors occur that prevent continuation
- Prerequisites are missing (e.g., no teams found)

Do NOT pause between steps to ask for approval.

### Execution Constraints - Shell and Python

**RULE: Python scripts longer than 5 lines MUST be written to files before execution.**

When the Python code to execute is more than 5 lines OR contains any quote characters (single or double):
1. Use the Write tool to save the script to `${OUTPUT_DIR}/[descriptive_name].py`
2. Execute with Bash: `cd "${OUTPUT_DIR}" && python3 [descriptive_name].py`

**This rule applies to ALL steps. When in doubt, write to a file.**

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

**MULTI-LINK DISAMBIGUATION RULE:**

When a table cell in column 1 (SRPOL Ads Team) contains MULTIPLE `<a>` elements:

1. Filter to ONLY links matching Confluence wiki page URL patterns:
   - Tiny links: URL contains `/wiki/x/[ID]`
   - Full page URLs: URL contains `/wiki/spaces/.../pages/[NUMERIC_ID]`
   - Exclude: Jira links, external links, anchors, non-wiki URLs.

2. From the filtered list, select the FIRST link by DOM/HTML order.
   - Position in HTML is the ONLY selector.
   - Do NOT prefer links based on label text (e.g., "Team Page", "Team Space").
   - Do NOT prefer links based on URL format (numeric ID vs. tiny link ID).
   - Inline card links (`data-card-appearance="inline"`) with no visible text ARE valid.

3. Extract page ID from the selected URL:
   - `/wiki/x/[ID]` → use ID portion directly as pageId (e.g., "AQAHUAU")
   - `/wiki/spaces/.../pages/[NUMERIC_ID]` → use NUMERIC_ID as pageId

Example - EP Core cell contains:
```
<a href="...wiki/x/AQAHUAU" data-card-appearance="inline">...</a>
<a href="...wiki/spaces/ENG/pages/19133628629"><u>EP Team Page</u></a>
```
Result: Select first link → pageId = "AQAHUAU" (correct WoW team page)

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

### Step 9: Save Summary Data (AUTO-EXECUTE after Step 8)

Write `${OUTPUT_DIR}/summary_data.json` containing all 15 teams with their DoD status.

**Schema** (see `assets/templates/dod-data-schemas.md`):
```json
[
  {"team": "Abyss", "dod": "Yes"},
  {"team": "Radium", "dod": "Yes"},
  {"team": "Europium", "dod": "Yes"},
  ...
  {"team": "SRE", "dod": "No"}
]
```

Rules:
- Always exactly 15 entries in fixed order: Abyss, Radium, Europium, Copernicium, Mouflons, Wolves, Polonium UF, Bigos, Capybaras, ML Serving Sturgeons, ML Platform Pandas, EP Core, Zurek, Igni, SRE
- `dod`: "Yes" if extraction_status = "success"; "No" if extraction_status = "not_found" or "error"

**DO NOT generate any report files in this step.** Only write the JSON data file.

Proceed immediately to Step 10.

### Step 10: DoD Quality Assessment (AUTO-EXECUTE after Step 9)

**This step executes automatically after Step 9 completes.** Do not pause or ask for user confirmation. This step assesses the QUALITY of each team's Definition of Done document.

#### Step 10.0: Load DoD Standard Reference

Read the persistent DoD Standard reference document:
```
Read("C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\dod-standard.txt")
```

If the file does not exist, output warning and skip Step 10 entirely (proceed to Step 11 with empty quality_data.json = `[]`):
```
[WARNING] DoD Standard document not found at assets/dod-standard.txt
Skipping DoD Quality Assessment. Writing empty quality_data.json.
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

Only teams with defined DoD (extraction_status = "success") are assessed. Teams without DoD are excluded from quality_data.json.

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
    "overall": <weighted average, rounded to 1 decimal>,
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
, 1)
```

#### Step 10.4: Save Quality Data

Write `${OUTPUT_DIR}/quality_data.json` with the assessment results.

**Schema** (see `assets/templates/dod-data-schemas.md`):
```json
[
  {
    "team": "Europium",
    "overall": 77.5,
    "coverage": 85,
    "clarity": 85,
    "measurability": 80,
    "company_alignment": 85,
    "industry_alignment": 80,
    "actionability": 80,
    "evidence": 70,
    "note": "Missing explicit performance/security validation and PO acceptance"
  }
]
```

Sort by `overall` descending before writing.

**DO NOT generate any report files in this step.** Only write the JSON data file.
**DO NOT write openpyxl code.** DO NOT open Report-DoD.xlsx with load_workbook.

Proceed immediately to Step 11.

#### Step 10.5: Output Quality Assessment Summary

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

Standards used:
  - Industry: assets/dod-standard.txt
  - Company: Confluence page 21735212005 (Definition of Done DoD)

Proceeding to Step 11: Report Generation...
```

### Step 11: Generate Reports via Canonical Template (AUTO-EXECUTE after Step 10)

**This step executes the canonical report generator script. No report code is written by the LLM.**

**This step executes automatically after Step 10 completes.** Do not pause or ask for user confirmation.

#### Step 11.1: Verify Prerequisites

Check that both JSON data files exist in `${OUTPUT_DIR}`:
- `summary_data.json` (saved in Step 9)
- `quality_data.json` (saved in Step 10.4)

If `quality_data.json` is missing (Step 10 was skipped), create it with empty array `[]` before proceeding.

#### Step 11.2: Verify and Copy Template Script

```bash
test -f "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_dod_reports.py" && echo "OK" || echo "MISSING"
```

If the template script does not exist, output error:
```
ERROR: Template script not found at assets/templates/generate_dod_reports.py
Cannot generate reports without the canonical template.
```
Then skip report generation but do NOT fail the overall skill.

If it exists, copy it to the output directory:
```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_dod_reports.py" "${OUTPUT_DIR}/generate_dod_reports.py"
```

#### Step 11.3: Execute Template Script

```bash
cd "${OUTPUT_DIR}" && python3 generate_dod_reports.py summary_data.json quality_data.json "." "{SCAN_DATE}"
```

Where `{SCAN_DATE}` is the scan date in YYYY-MM-DD format (e.g., "2026-06-29").

This single command produces BOTH:
- `Report-DoD.xlsx` (2 sheets: Summary, DoD quality)
- `Report-DoD.html` (self-contained dashboard)

#### Step 11.4: Validate Reports

```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/validate_dod_reports.py" "${OUTPUT_DIR}/validate_dod_reports.py"
cd "${OUTPUT_DIR}" && python3 validate_dod_reports.py "."
```

If validation fails, output the errors but do NOT attempt to "fix" by regenerating with different code.

#### Step 11.5: Report Completion

Output:
```
=== Reports Generated ===

Excel: ${OUTPUT_DIR}/Report-DoD.xlsx (2 sheets: Summary, DoD quality)
HTML:  ${OUTPUT_DIR}/Report-DoD.html

Validation: PASSED (or list specific errors)

All files saved to: ${OUTPUT_DIR}/
  - teams.json
  - summary_data.json
  - quality_data.json
  - DoD files: [team1]-dod.txt, [team2]-dod.txt, ...
  - Report-DoD.xlsx
  - Report-DoD.html
```

**FORBIDDEN in Step 11:**
- DO NOT write Python code to generate reports
- DO NOT create openpyxl scripts
- DO NOT write HTML strings
- DO NOT modify generate_dod_reports.py
- DO NOT generate "fallback" CSV files
- The ONLY actions are: copy template, execute template, validate output

## Error Handling

- **Continue on error:** If one team page fails, continue with remaining teams
- **Track failures:** Record all errors in teams.json metadata
- **Graceful degradation:** Partial data is better than no data

**Automation Rules:**
- **Only stop for critical failures:** Continue execution through all 11 steps unless:
  - Authentication fails completely (Step 2)
  - No teams found in source page (Step 5)
  - Output directory cannot be created (Step 4)
- **Do not stop for partial failures:** If some teams fail, continue with successful teams
- **Automatic Step 9:** Save summary_data.json immediately after DoD extraction
- **Automatic Step 10:** Execute DoD quality assessment automatically after Step 9. Skip only if assets/dod-standard.txt does not exist
- **Automatic Step 11:** Execute report generation automatically after Step 10

## Tool Requirements

Required tools:
- **ToolSearch** - Check for Atlassian MCP availability
- **mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources** - Verify authentication
- **mcp__plugin_atlassian_atlassian__getConfluencePage** - Fetch Confluence pages
- **Write** - Create JSON, TXT files
- **Read** - Verify file contents
- **Bash** - Create directories, get current time, execute Python scripts

Optional tools:
- **Grep** - Search for patterns
- **Glob** - Find files

## Important Rules

1. **DoD Scope:** Extract ONLY "DEFINITION OF DONE (DoD) - STORY/TASK" or plain "DEFINITION OF DONE (DoD)", completely ignore "- OFFERING/EPIC" sections

2. **Team Naming:** Same rules as wow-dor-scanner (clean page titles, extract last segment from prefix patterns)

3. **File Naming:** Use kebab-case for all team file names

4. **Timestamp Consistency:** Calculate CET timestamp ONCE and use consistently

5. **Linked DoD Pages:** Follow links in DoD sections to extract from referenced pages. ONLY if DoD heading was found first.

6. **Report Generation is 100% Deterministic (Template-Based):**
   - Reports are generated ONLY by `assets/templates/generate_dod_reports.py` - NEVER by LLM-written code
   - The LLM's responsibility ends at producing valid JSON data files (summary_data.json, quality_data.json)
   - The template script is NEVER modified, NEVER regenerated, NEVER "improved" during skill execution
   - If the template script doesn't exist, the skill outputs an error (doesn't create a replacement)
   - The template produces BOTH Report-DoD.xlsx AND Report-DoD.html in a single execution
   - DO NOT write openpyxl code, DO NOT write HTML strings, DO NOT create CSV fallbacks
   - `src/generate-dod-report.py` and inline Python for report generation are LEGACY - do not use

7. **Report-DoD.xlsx Fixed Schema:**
   - EXACTLY 2 sheets: "Summary" (first), "DoD quality" (second)
   - Summary: merged A1:B1 KPI "% Teams with DoD", value in C1 with conditional fill, header row 3, data rows 4-18
   - DoD quality: KPI row "DoD quality lvl", header row 3 (Team | Quality | Note), data sorted by score descending
   - DoD values in Summary: "Yes" (green fill #C6EFCE, font #006100) or "No" (red fill #FFC7CE, font #9C0006)
   - Quality scores: green >= 75%, yellow >= 50%, red < 50%
   - Teams without DoD shown as "N/A" in quality sheet

8. **DoD Quality Assessment (Step 10) - 7 Dimension Weighted Model:**
   - Only assesses teams that have defined DoD
   - Uses BOTH industry standard (assets/dod-standard.txt) AND company standard (Confluence page 21735212005)
   - 7 dimensions: Coverage (25%), Clarity (20%), Measurability (15%), Company Alignment (15%), Industry (10%), Actionability (10%), Evidence (5%)
   - Overall score = weighted average (0-100, 1 decimal)
   - "Note" column contains short, specific feedback on what is missing/weak
   - Results saved to quality_data.json; the template script handles all Excel/HTML rendering

9. **Data File Ordering:**
   - summary_data.json MUST be written BEFORE Step 11 execution
   - quality_data.json MUST be written BEFORE Step 11 execution
   - If Step 10 is skipped, write empty `[]` to quality_data.json before Step 11
