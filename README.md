# WoW Scanner Tool

Automated tool for extracting SRPOL team data, analyzing Definition of Ready (DoR) and Definition of Done (DoD) compliance from Confluence and Jira.

## Overview

The WoW Scanner Tool helps teams audit and compare DoR/DoD criteria across multiple SRPOL teams by automatically extracting data from Confluence and Jira, then analyzing compliance and quality.

### Available Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **DoR Scanner** | `/wow-dor-scanner` | Analyzes active Jira issues against team DoR criteria + assesses DoR quality |
| **DoD Scanner** | `/wow-dod-scanner` | Analyzes completed Jira issues (Done, last 14 days) against team DoD criteria |

Both skills extract from the same SRPOL Teams Confluence page and generate Excel reports with compliance analysis.

### What gets extracted:
- Team names, page links, and sprint board links from Confluence directory
- DoR / DoD criteria from each team's Confluence page
- Jira issues filtered by team custom field
- Compliance analysis with Pass/Fail assessment per issue

### DoR Scanner additional capabilities (v4.0):
- DoR quality assessment per team against industry best practices and company standard
- Quality scoring across 7 weighted dimensions (coverage, clarity, measurability, company alignment, industry alignment, actionability, AC guidance)
- "DoR quality" sheet in Report-DoR.xlsx with team scores and specific improvement notes

All data is saved locally in JSON, plain text, and Excel formats for easy analysis and sharing.

## Prerequisites

- Claude Code CLI with Atlassian MCP plugin configured
- Access to the target Atlassian/Confluence instance
- Authentication configured for Atlassian MCP

### Configure Atlassian MCP

If you haven't configured the Atlassian MCP plugin:

```bash
claude-code config atlassian
```

Follow the prompts to authenticate with your Atlassian instance.

## Installation

1. Copy the entire `wow-scanner-tool` folder to your project directory
2. The tool will be automatically discovered by Claude Code
3. The skill is ready to use immediately

## Usage

### DoR Scanner (Definition of Ready)
Analyzes active issues against team DoR criteria and assesses DoR quality:
```
/wow-dor-scanner
```
- Jira filter: status IN ("In Progress", "Code Review", "In Development")
- Output: `Report-DoR.xlsx` with 3 sheets:
  - **Summary** - KPIs (% teams with DoR, % tasks fitting DoR) + team overview table
  - **DoR Compliance** - Per-issue compliance analysis (9 columns)
  - **DoR quality** - Per-team DoR quality scores with improvement notes

### DoD Scanner (Definition of Done)
Analyzes completed issues against team DoD criteria:
```
/wow-dod-scanner
```
- Jira filter: status = "Done", resolved in last 14 days
- Output: `Report-DoD.xlsx` with Summary + DoD Compliance sheets

Both scan the preconfigured SRPOL Teams page:
```
https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams
```

## DoR Quality Assessment

The DoR Scanner (v4.0) includes automated quality assessment of each team's DoR document.

### How it works

1. Loads industry best practices reference from `assets/dor-standard.txt`
2. Fetches company DoR standard from Confluence (page 21735179128)
3. Evaluates each team's DoR across 7 dimensions using LLM-based analysis
4. Produces a quality score (1-100%) per team
5. Adds "DoR quality" sheet to Report-DoR.xlsx

### 7 Quality Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Coverage | 25% | How many of 10 essential DoR areas are addressed |
| Clarity & Specificity | 20% | Are criteria specific and unambiguous? |
| Measurability | 15% | Can each criterion be objectively verified? |
| Company Alignment | 15% | Alignment with company-level DoR guidance |
| Industry Best Practices | 10% | Adherence to INVEST, Scrum Guide, SAFe |
| Actionability | 10% | Clear ownership and behavioral guidance |
| AC Guidance | 5% | Quality standards for acceptance criteria |

### "DoR quality" Sheet Format

- **Row 1**: KPI "DoR quality lvl" with average % (color-coded: green >= 70%, orange 40-69%, red < 40%)
- **Row 3**: Table header (Team | Quality | Note)
- **Rows 4+**: Team data sorted by quality score descending
- **Note column**: Short, specific feedback on what's missing/weak (e.g., "Missing estimation criteria and risk identification")

### Standards Used

- **Industry**: `assets/dor-standard.txt` - 10 essential DoR areas, INVEST criteria, quality characteristics
- **Company**: Confluence page "Definition of Ready (DOR)" from Ads Product & Engineering space

## Output

The tool creates files in `wow-scanner-tool/assets/teams/[YYYYMMDD HH-MM]/`:

### teams.json
Master file containing all team metadata:
```json
{
  "metadata": {
    "scan_date": "2026-05-26T10:30:00Z",
    "source_page": "https://...",
    "team_count": 15,
    "cloudId": "adgear.atlassian.net",
    "scanner_version": "4.0"
  },
  "teams": [
    {
      "name": "Abyss",
      "page_link": "https://...",
      "sprint_board_link": "https://...",
      "dor_file": "abyss-dor.txt",
      "page_id": "123456789",
      "extraction_status": "success"
    }
  ]
}
```

### Per-team files
- `[team-name]-dor.txt` / `[team-name]-dod.txt` - Extracted DoR/DoD criteria
- `[team-name]-jira.json` - Full Jira issue data
- `[team-name]-jira.txt` - Human-readable issue summary

### Report files
- `Report-DoR.xlsx` - DoR compliance + quality report (3 sheets)
- `Report-DoD.xlsx` - DoD compliance report (2 sheets)
- `DOR_ANALYSIS_SUMMARY.md` / `DOD_ANALYSIS_SUMMARY.md` - Markdown summary
- `company-dor-standard.txt` - Cached company DoR standard (per-scan)

## Project Structure

```
wow-scanner-tool/
├── .claude/skills/
│   ├── wow-dor-scanner/
│   │   ├── skill.md          # DoR scanner skill (12 steps)
│   │   └── CHANGELOG.md      # Version history
│   └── wow-dod-scanner/
│       └── skill.md          # DoD scanner skill (11 steps)
├── assets/
│   ├── dor-standard.txt      # Industry DoR best practices (persistent)
│   └── teams/                # Timestamped scan outputs
│       └── YYYYMMDD HH-MM/  # One folder per scan
├── src/
│   └── generate-dod-report.py
├── scripts/
│   └── extract_jira_issues.py
└── README.md
```

## Expected Table Format

The Confluence page should contain a table with these columns:
- Team Name (or similar)
- Team Page Link
- Sprint Board Link (or Jira Board)

The tool will attempt to identify columns automatically, but consistent naming helps.

## Troubleshooting

### "Atlassian MCP not configured"
- Run `claude-code config atlassian` to set up authentication
- Verify you have access to the Confluence instance

### "Cannot access Atlassian"
- Check your authentication token is valid
- Verify you have permissions to view the pages
- Try accessing the page in your browser first

### "Invalid Confluence URL format"
- URL should match: `https://[instance].atlassian.net/wiki/spaces/[space]/pages/[pageId]/[title]`
- Example: `https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380`

### "DoR criteria not found"
- The tool searches for headings containing: "Definition of Ready", "DoR", "Ready Criteria"
- Check if the team page uses a different heading
- The tool will save a file noting DoR was not found

### "DoR Standard document not found"
- Ensure `assets/dor-standard.txt` exists (required for Step 12 quality assessment)
- If missing, Step 12 is skipped with a warning

### Incomplete extraction
- Check `teams.json` for `extraction_status` and `extraction_error` fields
- Individual team failures don't stop the entire scan
- Re-run the tool to retry failed extractions

## Sharing

To share this tool with other Claude users:

1. Zip the entire `wow-scanner-tool` folder
2. Share the zip file
3. Recipients extract to their project root
4. Tool is immediately available via `/wow-dor-scanner` or `/wow-dod-scanner`

Recipients will need to configure their own Atlassian MCP credentials.

## Technical Details

- **Skills**: `wow-dor-scanner` (DoR analysis + quality), `wow-dod-scanner` (DoD analysis)
- **Data format**: JSON for structured data, TXT for human-readable criteria, XLSX for reports
- **Timestamps**: CET timezone, format `YYYYMMDD HH-MM`
- **Error handling**: Continue-on-error (one team failure doesn't block others)
- **Team filtering**: Uses Jira Team custom field (`customfield_10114`) for accurate assignment
- **Quality assessment**: LLM-based multi-dimensional scoring against dual standards
- **Steps**: DoR Scanner runs 12 automated steps, DoD Scanner runs 11

## Version

Current version: 4.0

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review the tool logs in Claude Code output
- Verify Confluence page structure matches expected format
#   w o w - t e a m - l e v e l - s c a n n e r  
 