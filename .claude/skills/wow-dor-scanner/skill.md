---
name: wow-dor-scanner
description: >
  Extract SRPOL team data, DoR - STORY/TASK criteria, and active Jira issues from the SRPOL Teams Confluence page.
  Analyzes DoR compliance for each issue and assesses DoR quality per team against industry and company standards.
  Generates Excel report with Summary, DoR Compliance, and DoR quality sheets, plus an HTML dashboard for visual presentation.
  Automatically scans the configured page. Requires Atlassian MCP. Usage: /wow-dor-scanner
---

# WoW DoR Scanner Skill

Extracts team information, Definition of Ready (DoR) - STORY/TASK criteria, and active Jira issues from the SRPOL Teams Confluence page. Analyzes each issue's compliance with team DoR criteria and generates a comprehensive Excel report with actionable feedback.

## Usage

```
/wow-dor-scanner
```

No parameters required. The skill automatically scans the SRPOL Teams page at:
https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams

## What It Does

1. Checks Atlassian MCP authentication
2. Extracts from Confluence:
   - Team page links and sprint board links from directory table
   - Team names from actual Confluence page titles (cleaned by removing "Team", "Team Space" etc.)
   - Definition of Ready (DoR) - STORY/TASK criteria from each team's page (excludes DoR - OFFERING/EPIC)
   - If DoR section is empty but contains a link, follows the link to extract DoR from the referenced page
3. Extracts from Jira:
   - Active issues from each team's sprint board (Stories, Bugs, Tasks with status "In Progress", "Code Review", or "In Development")
   - Excludes Sub-tasks (only analyzes parent-level Stories, Bugs, and Tasks)
   - Uses Jira Team custom field for accurate team-to-issue assignment in shared projects
4. Analyzes DoR Compliance:
   - Compares each Jira issue against team's DoR criteria
   - Binary compliance assessment: "Yes" (green) or "No" (red)
   - Provides feedback only for non-compliant issues explaining why DoR not met
   - Generates Excel report with 2 sheets: Summary (all teams overview) + DoR Compliance (9 columns: Team, Issue Key, Issue Type, URL, Title, Status, Assignee, DoR Compliance, Note)
5. Assesses DoR Quality:
   - Evaluates coverage of each team's DoR document against the DoR Standard (assets/dor-standard.txt) combined with company standard (Confluence page 21735179128)
   - Scores each team 0-100 points representing how many standard criteria are covered
   - Adds "DoR quality" sheet to Report-DoR.xlsx with KPI (average coverage), team coverage scores, and notes listing which standard points are missing
6. Saves all data to absolute path: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\<timestamp>/` where timestamp is in CET format: `YYYYMMDD HH-MM`
   - DoR files: `[team-name]-dor.txt`
   - Jira files: `[team-name]-jira.json` and `[team-name]-jira.txt`
   - Master file: `teams.json`
   - DoR Analysis Report: `Report-DoR.xlsx`
   - HTML Dashboard Report: `Report-DoR.html`
   - Analysis Summary: `DOR_ANALYSIS_SUMMARY.md`

## Instructions

**CRITICAL - FULL AUTOMATION:** This skill must execute all 13 steps automatically without pausing or asking for user confirmation. The entire workflow from data extraction (Steps 1-10) to DoR analysis (Step 11) to DoR quality assessment (Step 12) to HTML report generation (Step 13) should run continuously. Only stop execution if:
- Authentication fails (Step 2)
- Critical errors occur that prevent continuation
- Prerequisites are missing (e.g., no teams found)

Do NOT pause between steps to ask for approval. Do NOT stop after Step 10, Step 11, or Step 12. Proceed directly from Step 10 to Step 11 to Step 12 to Step 13 automatically.

### Execution Constraints - Shell and Python

**RULE: Python scripts longer than 5 lines MUST be written to files before execution.**

When the Python code to execute is more than 5 lines OR contains any quote characters (single or double):
1. Use the Write tool to save the script to `${OUTPUT_DIR}/[descriptive_name].py`
2. Execute with Bash: `cd "${OUTPUT_DIR}" && python3 [descriptive_name].py`

**WHY:** Shell heredocs (`python3 << 'EOF'`) and inline Python (`python3 -c "..."`) fail unpredictably when the code contains quotes, f-strings, or special characters. This causes `unexpected EOF` errors that halt execution mid-skill. Writing to a file eliminates ALL shell escaping issues permanently.

**Exception:** Single-line Python commands without quotes may use `python3 -c` directly:
```bash
# OK - no quotes in Python code
python3 -c "import sys; print(sys.version)"
# FORBIDDEN - has quotes, must use file instead  
python3 -c "data = {'key': 'value'}"
```

**This rule applies to ALL steps including Steps 9, 11, 12, and 13. When in doubt, write to a file.**

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

Then try the /wow-dor-scanner command again.
```

If tools found, attempt a test call:
```
mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources()
```

If this fails, show error:
```
Error: Cannot access Atlassian.

Please check:
- Your authentication token is valid
- You have access to adgear.atlassian.net
- Try accessing the page in your browser first

To re-authenticate:
claude-code config atlassian
```

### Step 3: Calculate CET Timestamp

Calculate the current timestamp in CET (Central European Time):
- Get current UTC time using Bash: `date -u +"%Y-%m-%d %H:%M:%S"`
- Convert to CET (UTC+1 standard, UTC+2 during DST)
- Format as: `YYYYMMDD HH-MM` 
- Example: `20260526 12-38` means 26 May 2026, 12:38 CET
- Store this timestamp for use in all file operations

**CET Conversion:**
- Standard time (Nov-Mar): UTC + 1 hour
- Daylight saving (Mar-Nov): UTC + 2 hours
- Use system timezone conversion or manual calculation

### Step 4: Prepare Output Folder

Create the timestamped output directory using absolute path from project root:
```bash
mkdir -p "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]"
```

Example: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260526 12-38`

**CRITICAL:** Store the full absolute path in a variable for all subsequent file operations:
```
OUTPUT_DIR = "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]"
```

All subsequent file Write operations must use: `${OUTPUT_DIR}/[filename]` to avoid nested folder creation.

### Step 5: Fetch Main SRPOL Teams Page

Use Atlassian MCP to fetch the team directory page:

```
mcp__plugin_atlassian_atlassian__getConfluencePage(
  cloudId: "adgear.atlassian.net",
  pageId: "19470090380",
  contentFormat: "html"
)
```

This returns HTML content containing a table with team data.

### Step 6: Extract Table Data

Parse the HTML to locate and extract the table:

1. Find the `<table>` element in the HTML
2. Locate `<thead>` to identify column positions:
   - First column: "SRPOL Ads Team" (contains team page links)
   - Look for columns containing: "SPRINT board" or "Board"
3. Extract `<tbody>` rows:
   - For each `<tr>` row, extract `<td>` cells
   - From first column: extract team page URL (see MULTI-LINK DISAMBIGUATION RULE below)
   - From SPRINT board column: extract sprint board link
   - Extract page ID from team page URLs (number after `/pages/` or the tiny link ID after `/wiki/x/`)
   - **Do NOT extract team name yet** - it will be retrieved from the actual page title

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

**HTML Parsing Patterns:**
- Table rows: Text between `<tr>` and `</tr>`
- Links: `<a href="URL">TEXT</a>` → capture URL
- Page IDs: Extract from URL patterns:
  - `/pages/[PAGE_ID]/` → numeric ID
  - `/wiki/x/[TINY_ID]` → tiny link ID (e.g., WID6RQU)
- Clean text: Remove HTML tags using pattern `<[^>]+>` → empty string

Build a list of team page references (WITHOUT names yet):
```javascript
[
  {
    pageLink: "https://adgear.atlassian.net/wiki/x/WID6RQU",
    sprintBoardLink: "https://adgear.atlassian.net/jira/...",
    pageId: "WID6RQU"  // or numeric ID
  },
  // ...
]
```

**Note:** Team names will be determined in Step 8 when fetching each team page.

### Step 7: Generate Initial teams.json

Write the master JSON file to `${OUTPUT_DIR}/teams.json` where OUTPUT_DIR is the absolute path from Step 4:

```json
{
  "metadata": {
    "scan_date": "[current ISO-8601 timestamp]",
    "scan_timestamp_cet": "[CET_TIMESTAMP in format YYYYMMDD HH-MM]",
    "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
    "team_count": [number of teams],
    "cloudId": "adgear.atlassian.net",
    "scanner_version": "2.0"
  },
  "teams": []
}
```

The teams array will be populated as extraction progresses.

### Step 8: Extract DoR Per Team

For each team in the list:

1. **Fetch team page and extract name:**
   ```
   mcp__plugin_atlassian_atlassian__getConfluencePage(
     cloudId: "adgear.atlassian.net",
     pageId: [team.pageId],
     contentFormat: "html"
   )
   ```
   
   The response includes a `title` field with the actual page title. Extract and clean it:
   - Get title from response: `response.content.nodes[0].title`
   - Clean the title by removing (case-insensitive):
     - "Team Page"
     - "Team Space"
     - "Team" (only if standalone word, not part of compound names)
     - "Space" (only at the end)
   - Normalize spaces and hyphens
   - **For names with organizational prefix pattern "XX - YYY - Name"** (e.g., "PE - WAW - Abyss"):
     - Extract ONLY the last segment after the final " - " separator as the team name
     - This removes organizational hierarchy prefixes
   - Examples:
     - "Radium Team Space" → "Radium"
     - "PE - WAW - Abyss" → "Abyss" (extract last segment only)
     - "Team Europium" → "Europium"
   - This cleaned title becomes the team name for all outputs

2. **Search for DoR section:**
   Look for headings (`<h1>`, `<h2>`, `<h3>`, `<h4>`) containing:
   - "DEFINITION OF READY (DoR) - STORY/TASK"
   - "DEFINITION OF READY (DoR) - STORY"
   - "Definition of Ready (DoR) - STORY/TASK"
   - "DEFINITION OF READY (DoR)" (without additional description)
   - "Definition of Ready" (plain, without specifying OFFERING/EPIC)
   
   **CRITICAL:** IGNORE and DO NOT extract headings containing:
   - "DEFINITION OF READY (DoR) - OFFERING/EPIC"
   - "- OFFERING/EPIC"
   - "- OFFERING"
   - "- EPIC"
   
   Use case-insensitive matching.

3. **Check for DoR links (ONLY if DoR heading was found in step 2):**
   **CRITICAL PREREQUISITE:** This step ONLY executes if a matching DoR heading was found in step 2. If NO DoR heading exists on the team page, skip directly to step 7 (handle "not found"). Do NOT scan the entire page for DoR-related links without first finding a DoR heading.
   
   After finding the DoR section heading, look for links to external DoR pages:
   - Look for links (`<a href="...">`) ONLY within the content of the found DoR section (between the DoR heading and the next heading)
   - Check if the link URL or link text contains DoR-related keywords:
     - "DoR", "Definition of Ready", "Story", "Task", "Ready", "DoD"
   - If such a link is found:
     - Extract the page ID from the link URL (pattern: `/pages/[PAGE_ID]/` or `/wiki/x/[TINY_ID]`)
     - Fetch the linked page using `mcp__plugin_atlassian_atlassian__getConfluencePage`
     - Search for DoR section in the linked page using the same search criteria as step 2
     - Extract content from the linked page INSTEAD of the current page content
     - Use the linked page content as the DoR source
   
   **BUG PREVENTION:** Never follow links found in other sections of the page (e.g., "Links", "References", "Team Ceremonies"). Only links within the actual DoR section content are valid DoR sources.

4. **Extract content:**
   - Capture all content AFTER the "DoR - STORY/TASK" or plain "DoR" heading
   - Stop at the next major heading (especially "DoR - OFFERING/EPIC") or end of section
   - Convert HTML to plain text:
     - Preserve list structure (`<ul>`, `<ol>`, `<li>`)
     - Remove other HTML tags
     - Normalize whitespace
   - DO NOT include any content from "DoR - OFFERING/EPIC" sections

5. **Convert team name to kebab-case for filename:**
   - Replace spaces and underscores with hyphens
   - Convert to lowercase
   - Examples:
     - "Radium" → "radium-dor.txt"
     - "Abyss" → "abyss-dor.txt"
     - "ML Platform" → "ml-platform-dor.txt"

6. **Save to file:**
   Write to `${OUTPUT_DIR}/[team-name-kebab]-dor.txt` where OUTPUT_DIR is the absolute path from Step 4:
   
   **IMPORTANT: File should contain ONLY the DoR content - no metadata, headers, timestamps, or status notes.**
   
   **Format (clean DoR content only):**
   ```
   [Extracted DoR content - plain text only, no additional formatting or metadata]
   ```
   
   **Examples:**
   
   If DoR is a simple list:
   ```
   - User Story/Requirement Clarity: The user story or requirement is clearly articulated
   - Acceptance Criteria Defined: Specific, testable acceptance criteria are provided
   - Dependencies Identified: All dependencies documented and resolved
   ```
   
   If DoR is a table or structured content:
   ```
   User Story/Requirement Clarity
   The user story or requirement is clearly articulated, concise, and understandable to all team members.
   
   Acceptance Criteria and Measurement Defined
   Specific, testable acceptance criteria are provided for the user story, outlining what constitutes successful completion.
   
   Estimates Provided
   The development team has provided an estimate for the work.
   ```

7. **Handle errors:**
   
   **DoR not found:** Save file with content:
   ```
   DoR - STORY/TASK criteria not found on team page.
   ```
   
   **Page fetch fails:** Save file with content:
   ```
   Error: Could not access team page.
   [Error message from MCP]
   ```

8. **Update teams.json:**
   After processing each team, add entry to teams array:
   ```json
   {
     "name": "[Team Name]",
     "page_link": "[Full URL]",
     "sprint_board_link": "[Sprint Board URL or null]",
     "dor_file": "[team-name-kebab]-dor.txt",
     "page_id": "[Page ID]",
     "extraction_status": "success | not_found | error",
     "extraction_error": null,
     "dor_source": "direct | linked_page | null"
   }
   ```

### Step 9: Extract Jira Issues Per Team (auto-continue after Step 8 without pausing)

**IMPORTANT:** The Team custom field (`customfield_10114`) enables accurate team-specific filtering in shared projects. This field is hardcoded based on verification across multiple Jira projects.

#### Step 9.0: Configure Team Custom Field (Hardcoded)

The Team custom field is essential for accurate team-specific filtering in shared projects (AENW, PEPI, RSW etc).

**Field ID**: `customfield_10114` (verified in Jira instance)

**Validation**:

```javascript
const TEAM_FIELD_ID = "customfield_10114"

console.log(`[INFO] Using Team field: ${TEAM_FIELD_ID}`)
console.log(`[INFO] Filter method: client-side (Team-type fields do NOT support JQL filtering)`)

// Optional: Validate field is present in issue responses
try {
  const testQuery = `project = AENW AND status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task`
  const result = await mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql({
    cloudId: "adgear.atlassian.net",
    jql: testQuery,
    fields: ["key", TEAM_FIELD_ID],
    maxResults: 1
  })
  
  if (result.issues && result.issues.length > 0) {
    const teamFieldValue = result.issues[0].fields?.[TEAM_FIELD_ID]
    if (teamFieldValue && teamFieldValue.name) {
      console.log(`[SUCCESS] Team field validated - sample value: "${teamFieldValue.name}"`)
    } else {
      console.log(`[WARNING] Team field exists but sample issue has null value`)
    }
  } else {
    console.log(`[WARNING] No active issues found in AENW for validation`)
  }
} catch (error) {
  console.log(`[WARNING] Cannot validate Team field: ${error.message}`)
}
```

**Team Name Patterns** (for client-side filtering):

Map skill team names to Team field value patterns for client-side exact matching:

```javascript
const TEAM_NAME_PATTERNS = {
  "Abyss": "PE - WAW - Abyss",
  "Radium": "AE - WAW - Radium",
  "Europium": "AP - WAW - Europium",
  "Copernicium": "AE - WAW - Copernicium",
  "Mouflons": "AS - WAW - Mouflons",
  "Wolves": "AS - WAW - Wolves",
  "Polonium LF": "Polonium",
  "Polonium UF": "AS - WAW - Polonium UF",
  "Bigos": "AS - WAW - Bigos",
  "Capybaras": "AS - WAW - Capybaras",
  "ML Serving Sturgeons": "T - WAW - ML Sturgeons",
  "ML Platform Pandas": "T - WAW - ML Pandas",
  "Zurek": "T - WAW - Zurek",
  "EP Core": "T - WAW - EP Core",
  "Igni": "AP - WAW - Igni",
  "SRE": "T - WAW - Embedded SREs SRPOL"
}
```

**Note:** These patterns MUST exactly match the `customfield_10114.name` values returned in Jira issue responses. The Team field is a Jira Team-type object (not text/select), so matching is performed CLIENT-SIDE after fetching results.

```
+------------------------------------------------------------------------+
| MANDATORY: DO NOT use customfield_10114 = "..." in JQL.                |
| The Team custom field is a Jira Team-type field that does NOT support   |
| JQL equality filtering by name. Queries using this syntax silently      |
| return 0 results even when matching issues exist.                       |
|                                                                         |
| CORRECT APPROACH: Query per project WITHOUT team filter, then filter    |
| results client-side by checking fields.customfield_10114.name value.    |
+------------------------------------------------------------------------+
```

**Project-to-Teams Mapping:**

```javascript
/**
 * PROJECT_TEAMS maps each Jira project key to the SRPOL teams whose issues live there.
 * Used to deduplicate project queries: each project is queried ONCE, results split across teams.
 */
const PROJECT_TEAMS = {
  "MAW":   ["Abyss", "Bigos"],
  "AENW":  ["Radium", "Europium"],
  "AETVP": ["Copernicium"],
  "PEPI":  ["ML Serving Sturgeons"],
  "MOP":   ["Mouflons"],
  "TVPW":  ["Wolves"],
  "MLI":   ["ML Serving Sturgeons", "ML Platform Pandas"],
  "RSW":   ["Polonium UF", "Capybaras"],
  "ML":    ["ML Platform Pandas"],
  "EPCW":  ["EP Core"],
  "PEA":   ["Zurek"],
  "ASPW":  ["Igni"],
  "EEEW":  ["SRE"]
}
```

**Rationale**: The original discovery logic via `getJiraIssueTypeMetaWithFields` has proven unreliable in practice. Hardcoding the verified field ID provides stability while validation confirms the field is accessible. The Team-type custom field does NOT support JQL filtering (equality operator always returns 0 results), so a project-level query with client-side filtering approach is mandatory.

#### Step 9.1: Process Each Team

For each team in the list:

1. **Check for sprint board URL:**
   - Verify team has `sprintBoardLink` from Step 6
   - If null/empty, skip Jira extraction and mark as `jiraStatus: "no_board"`

2. **Extract board ID and project key:**
   Parse the sprint board URL to extract identifiers:
   ```
   URL format: https://adgear.atlassian.net/jira/software/c/projects/[PROJECT]/boards/[BOARD_ID]
   
   Board ID extraction:
   - Pattern: /boards/(\d+)
   - Example: "/boards/8976" → boardId = "8976"
   
   Project key extraction (optional):
   - Pattern: /projects/([A-Z]+)/
   - Example: "/projects/AENW/" → projectKey = "AENW"
   ```
   
   If board ID cannot be extracted, mark as `jiraStatus: "parse_error"` and skip

3. **Build project-level JQL query (NO team filter in JQL):**

   ```
   +------------------------------------------------------------------------+
   | MANDATORY: The query MUST NOT contain customfield_10114 = "..."         |
   | Team-type fields cannot be filtered via JQL. Client-side filtering is   |
   | applied AFTER results are retrieved. See Step 9.0 warning.              |
   |                                                                         |
   | MANDATORY: The query MUST NOT contain `sprint in openSprints()`         |
   | The sprint filter causes data loss for issues that are active but not   |
   | assigned to the current sprint. This is the documented root cause of a  |
   | critical bug that caused 42% of active issues to be missed.             |
   +------------------------------------------------------------------------+
   ```

   For each UNIQUE project key in PROJECT_TEAMS:

   **JQL Template:**
   ```jql
   project = {PROJECT_KEY}
   AND status IN ("In Progress", "Code Review", "In Development")
   AND issuetype IN (Story, Bug, Task)
   AND issuetype != Sub-task
   ```

   **NO ADDITIONAL CLAUSES may be added.** No team filter. No sprint filter. No ORDER BY.

   **CRITICAL - Case Sensitivity:** Jira status names are case-sensitive:
   - "In Progress" (capital I, capital P)
   - "Code Review" (capital C, capital R)
   - "In Development" (capital I, capital D)

   **CRITICAL - Issue Type Filter:** Exclude Sub-tasks:
   - Only parent-level Stories, Bugs, and Tasks are analyzed
   - Sub-tasks are implementation details and should not be assessed against DoR
   - JQL filter: `issuetype != Sub-task`

   **CRITICAL - No Sprint Filter:**
   - NEVER add `sprint in openSprints()` to any query - this causes data loss
   - Issues can be "In Progress" without being in an open sprint

   **Query Type Tracking:**
   Store in metadata which result type applied:
   - `"queryType": "project_wide_with_client_filter"` - Issues found via client-side filtering (normal success)
   - `"queryType": "pattern_mismatch"` - Project has SRPOL issues but team's pattern matched 0
   - `"queryType": "none"` - Project has 0 active issues overall

4. **Execute project queries with pagination and client-side team assignment:**

   Process each unique project key from PROJECT_TEAMS. Projects can be queried
   in parallel (up to 5 concurrent queries recommended).

   **Pagination Loop (MANDATORY for completeness):**
   ```javascript
   for (const [projectKey, teamNames] of Object.entries(PROJECT_TEAMS)) {
     const jql = `project = ${projectKey} AND status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task`

     // Phase 1: Fetch ALL active issues in project (paginated)
     let allProjectIssues = []
     let nextPageToken = null
     let pageCount = 0

     do {
       const result = mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql(
         cloudId: "adgear.atlassian.net",
         jql: jql,
         fields: ["key", "summary", "status", "issuetype", "assignee", "priority", "created", "updated", "customfield_10114"],
         maxResults: 100,
         nextPageToken: nextPageToken  // null on first call
       )

       allProjectIssues = allProjectIssues.concat(result.issues)
       nextPageToken = result.isLast ? null : result.nextPageToken
       pageCount++

       // Safety: cap at 5 pages (500 issues) to prevent infinite loops
       if (pageCount >= 5) {
         console.log(`[WARNING] Project ${projectKey}: capped at 500 issues (${pageCount} pages)`)
         break
       }
     } while (nextPageToken !== null)

     console.log(`[INFO] Project ${projectKey}: fetched ${allProjectIssues.length} total active issues (${pageCount} page(s))`)

     // Phase 2: Client-side filtering - assign issues to teams
     for (const teamName of teamNames) {
       const teamPattern = TEAM_NAME_PATTERNS[teamName]
       
       const teamIssues = allProjectIssues.filter(issue => {
         const teamField = issue.fields?.customfield_10114
         if (!teamField || !teamField.name) return false
         return teamField.name === teamPattern  // EXACT match, case-sensitive
       })

       console.log(`  ${teamName}: ${teamIssues.length} issues matched pattern "${teamPattern}"`)

       // Phase 3: Pattern mismatch detection (replaces old diagnostic query)
       if (teamIssues.length === 0 && allProjectIssues.length > 0) {
         // Check if any SRPOL team (WAW marker) has issues in this project
         const srpolIssues = allProjectIssues.filter(issue => {
           const name = issue.fields?.customfield_10114?.name || ""
           return name.includes("WAW")
         })

         if (srpolIssues.length > 0) {
           // Other SRPOL teams have work, but this team's pattern returned nothing
           // Log observed team names for debugging
           const observedTeams = [...new Set(srpolIssues.map(i => i.fields.customfield_10114.name))]
           console.log(`  [WARNING] Pattern "${teamPattern}" matched 0 issues, but project has SRPOL issues from: ${observedTeams.join(", ")}`)
           console.log(`  [WARNING] Check if team was renamed in Jira or pattern is incorrect`)
           // queryType = "pattern_mismatch"
         } else {
           // No SRPOL teams have work in this project at all
           // queryType = "none"
         }
       }

       // Store results for this team (even if 0 issues - that's valid)
       team.filteredIssues = teamIssues
       team.queryType = teamIssues.length > 0 ? "project_wide_with_client_filter" 
                       : (allProjectIssues.length > 0 ? "pattern_mismatch" : "none")
     }
   }
   ```

   **Key behaviors:**
   - Each project is queried EXACTLY ONCE (deduplication via PROJECT_TEAMS)
   - Pagination ensures no issues are missed due to the 100-result cap
   - Client-side filter uses EXACT string match on `customfield_10114.name`
   - Issues with null/missing team field are silently discarded (not assigned to any team)
   - Pattern mismatch detection replaces the old diagnostic query approach
   - Results for 0-issue teams are still saved (with empty arrays) - this is success, not error

   **Team field validation (inherent in client-side approach):**
   Since issues are assigned to teams based on exact `customfield_10114.name` match,
   validation is inherent - every issue in a team's result set is guaranteed to match.
   
   Log a summary per project for auditability:
   ```javascript
   // After processing all teams in a project:
   const assignedCount = teamNames.reduce((sum, t) => sum + teams[t].filteredIssues.length, 0)
   const unassignedCount = allProjectIssues.length - assignedCount
   
   if (unassignedCount > 0) {
     console.log(`  [INFO] ${projectKey}: ${unassignedCount} issues belong to non-SRPOL teams (discarded)`)
   }
   ```

5. **Process and format results:**
   
   Extract from response for each issue:
   ```javascript
   const issueData = {
     key: issue.key,
     type: fields.issuetype.name,
     summary: fields.summary,
     status: fields.status.name,
     assignee: fields.assignee?.displayName || "Unassigned",
     priority: fields.priority?.name || "None",
     created: fields.created,
     updated: fields.updated,
     url: `https://adgear.atlassian.net/browse/${issue.key}`
   }
   
   // CRITICAL: Extract Team field if available
   const TEAM_FIELD_ID = "customfield_10114"
   if (fields[TEAM_FIELD_ID]) {
     const teamField = fields[TEAM_FIELD_ID]
     
     if (typeof teamField === 'object' && teamField.name) {
       // Store full Team field value
       issueData.teamField = teamField.name
       
       // Extract clean team name (last segment after " - ")
       const segments = teamField.name.split(' - ')
       issueData.teamName = segments[segments.length - 1].trim()
     }
   } else {
     console.log(`[WARNING] Issue ${issue.key} missing Team field`)
   }
   ```
   
   Calculate summary statistics:
   - Total issue count
   - Count by status ("In Progress", "Code Review", "In Development")
   - Count by type (Story, Bug, Task)

6. **Save JSON file:**
   Write to `${OUTPUT_DIR}/[team-name-kebab]-jira.json` where OUTPUT_DIR is the absolute path from Step 4:
   
   **MANDATORY JSON SCHEMA:** The jira.json file MUST include the `query` object with the
   actual JQL used. This is REQUIRED for debugging. Do NOT save bare arrays without metadata.
   If the output is a bare JSON array (e.g., `[{...}, {...}]`) without the wrapping object,
   this is a schema violation that MUST be corrected.
   
   ```json
   {
     "team": "[Team Name]",
     "boardUrl": "[Sprint Board URL]",
     "boardId": "[Board ID]",
     "projectKey": "[Project Key]",
     "extractedAt": "[ISO-8601 timestamp]",
     "teamFieldId": "customfield_10114",
     "query": {
       "jql_executed": "project = AENW AND status IN (\"In Progress\", \"Code Review\", \"In Development\") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task",
       "queryType": "project_wide_with_client_filter | pattern_mismatch | none",
       "filterMethod": "client_side",
       "teamFilterEnabled": true,
       "teamPattern": "AE - WAW - Radium",
       "projectKey": "AENW",
       "totalProjectIssues": 25,
       "matchedTeamIssues": 8,
       "statuses": ["In Progress", "Code Review", "In Development"],
       "issueTypes": ["Story", "Bug", "Task"],
       "pagesRetrieved": 1
     },
     "summary": {
       "total": 15,
       "byStatus": {"In Progress": 10, "Code Review": 3, "In Development": 2},
       "byType": {"Story": 8, "Bug": 4, "Task": 3},
       "truncated": false
     },
     "issues": [
       {
         "key": "AENW-1234",
         "type": "Story",
         "summary": "Implement feature X",
         "status": "In Progress",
         "assignee": "John Doe",
         "priority": "High",
         "created": "2026-05-20T10:00:00Z",
         "updated": "2026-05-25T14:30:00Z",
         "url": "https://adgear.atlassian.net/browse/AENW-1234",
         "teamField": "AE - WAW - Radium",
         "teamName": "Radium"
       }
     ]
   }
   ```
   
   **If results are truncated (100 issues):** Set `"truncated": true` in summary

7. **Save TXT file:**
   Write to `${OUTPUT_DIR}/[team-name-kebab]-jira.txt` where OUTPUT_DIR is the absolute path from Step 4:
   ```
   Team: [Team Name]
   Board: [Sprint Board URL]
   Board ID: [Board ID]
   Project: [Project Key]
   Extracted: [ISO-8601 timestamp]
   Query Strategy: Project-wide + client-side filter (succeeded) | Pattern mismatch (team filter failed) | No active work

   === ACTIVE ISSUES (In Progress, Code Review, In Development) ===

   Summary:
   - Total issues: 15
   - In Progress: 10
   - Code Review: 3
   - In Development: 2

   Issues by type:
   - Stories: 8
   - Bugs: 4
   - Tasks: 3

   === IN PROGRESS (10 issues) ===

   [AENW-1234] Story: Implement feature X
     Assignee: John Doe | Priority: High | Updated: 2026-05-25
     https://adgear.atlassian.net/browse/AENW-1234

   [... list all In Progress issues ...]

   === CODE REVIEW (5 issues) ===

   [AENW-1240] Story: Add validation
     Assignee: Bob Johnson | Priority: Medium | Updated: 2026-05-26
     https://adgear.atlassian.net/browse/AENW-1240

   [... list all Code Review issues ...]

   ---
   Status: success
   ```
   
   **If results truncated:** Add warning at top:
   ```
   WARNING: Results limited to 100 issues. Board may have more active issues.
   ```

8. **Handle errors:**
   
   **No sprint board URL:**
   ```
   Team: [Team Name]
   Board: Not configured
   Extracted: [ISO-8601 timestamp]

   === ACTIVE ISSUES (In Progress, Code Review) ===

   No Jira board URL found for this team.

   ---
   Status: no_board
   ```
   Save as `[team-name]-jira.txt` only (no JSON)
   
   **Parse error (cannot extract board ID):**
   ```
   Team: [Team Name]
   Board: [Sprint Board URL]
   Extracted: [ISO-8601 timestamp]

   === ACTIVE ISSUES (In Progress, Code Review) ===

   Error: Could not extract board ID from URL.
   URL format expected: /boards/[NUMBER]

   ---
   Status: parse_error
   ```
   
   **Access error (API fails):**
   ```
   Team: [Team Name]
   Board: [Sprint Board URL]
   Board ID: [Board ID]
   Extracted: [ISO-8601 timestamp]

   === ACTIVE ISSUES (In Progress, Code Review) ===

   Error: Could not access Jira board.
   [Error message from MCP]

   Possible causes:
   - Insufficient permissions to view board
   - Board does not exist
   - Authentication token lacks required scope

   ---
   Status: access_error
   ```
   
   **Query returns 0 issues:**
   This is SUCCESS (not an error). Save normal JSON/TXT with empty arrays and zero counts.

9. **Update teams.json:**
   After processing each team, add Jira fields to the team entry:
   ```json
   {
     "name": "[Team Name]",
     "page_link": "[Full URL]",
     "sprint_board_link": "[Sprint Board URL]",
     "dor_file": "[team-name-kebab]-dor.txt",
     "page_id": "[Page ID]",
     "extraction_status": "success",
     "extraction_error": null,
     "dor_source": "direct",
     
     "jiraFile": "[team-name-kebab]-jira.json",
     "jiraStatus": "success",
     "jiraIssueCount": 15,
     "jiraBoardId": "8976",
     "jiraProjectKey": "AENW",
     "jiraQueryType": "project_wide_with_client_filter",
     "jiraError": null
   }
   ```
   
   **jiraStatus values:**
   - `"success"` - Issues extracted successfully (even if 0 issues)
   - `"no_board"` - No sprint board URL configured
   - `"parse_error"` - Cannot parse board ID from URL
   - `"access_error"` - Jira API call failed

#### Step 9.2: Query Result Validation

After executing queries for ALL projects and assigning issues to teams:

1. **JQL compliance check:** Verify that NO executed JQL contains `customfield_10114` 
   or `sprint in openSprints()`. If found, this is a critical implementation error.

2. **Cross-team contamination check (inherent guarantee):**
   Client-side filtering by exact `customfield_10114.name` match guarantees that no 
   issue appears in more than one team's results (each issue has exactly one team field 
   value). No explicit check needed - log a confirmation note:
   ```
   [INFO] Cross-team contamination: impossible by design (exact name match filtering)
   ```

3. **Pattern mismatch summary:**
   List all teams where `queryType == "pattern_mismatch"`:
   ```
   [WARNING] Teams with potential pattern mismatch (0 issues but project has SRPOL work):
     - {team}: pattern "{pattern}" not found in {project} (observed teams: [...])
   ```

4. **Result reasonableness check:**
   - Total issues across all teams should be 30-100 (historically observed range)
   - If total < 30: log warning (possible pattern issues or low activity period)
   - If any single team has >30 issues: log info (unusually busy team)
   
5. **Null team field summary:**
   Log how many issues per project had null/missing `customfield_10114` field:
   ```
   [INFO] Issues with null team field (discarded): MAW=2, AENW=0, PEPI=1, ...
   ```

### Step 10: Report Completion

Output a summary:
```
Extraction complete!

Source: SRPOL Teams page
Scan timestamp (CET): [CET_TIMESTAMP]
Teams found: [X]

DoR Extraction:
  - Extracted: [Y]
  - Not found: [Z]
  - Errors: [W]

Jira Extraction:
  - Extracted: [A] teams
  - Total active issues: [B]
  - No board configured: [C]
  - Errors: [D]

Files saved to: ${OUTPUT_DIR}/
- teams.json
- DoR files: [team1]-dor.txt, [team2]-dor.txt, ...
- Jira files: [team1]-jira.json, [team1]-jira.txt, [team2]-jira.json, ...

where OUTPUT_DIR = C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]

Special handling:
- Only extracted "DoR - STORY/TASK" (excluded "DoR - OFFERING/EPIC")
- Jira queries limited to statuses: "In Progress", "Code Review", "In Development" (case-sensitive)
- Jira queries limited to types: Story, Bug, Task (Sub-tasks excluded)
- Jira results capped at 100 issues per team

Failed extractions:
  DoR: [List team names with DoR errors, if any]
  Jira: [List team names with Jira errors, if any]

Proceeding to Step 11: DoR Compliance Analysis...
```

**IMPORTANT:** After outputting the above summary, immediately proceed to Step 11. Do NOT wait for user confirmation. Do NOT ask if the user wants to continue. Execute Step 11 automatically.

### Step 11: DoR Compliance Analysis (AUTO-EXECUTE)

**This step executes automatically after Step 10.** Do not pause or ask for user confirmation before starting Step 11.

```
+================================================================================+
| STEP 11 EXECUTION CONTRACT - BINDING FOR EVERY RUN                             |
|                                                                                 |
| This step produces compliance_data.json. The ONLY valid method is:              |
|                                                                                 |
| 1. FETCH descriptions: Call getJiraIssue for EACH issue (batch 5 per message)   |
| 2. PERSIST descriptions: Write ${OUTPUT_DIR}/issue_descriptions.json            |
| 3. ANALYZE with LLM reasoning: Compare descriptions against DoR criteria        |
| 4. PERSIST results: Write compliance_data.json                                  |
|                                                                                 |
| ORDERING CONSTRAINT (mechanical enforcement):                                   |
| issue_descriptions.json MUST be written to disk BEFORE compliance_data.json.    |
| If you are about to write compliance_data.json and issue_descriptions.json does |
| not yet exist, STOP. You have skipped Step 11.2. Go back and execute it.        |
|                                                                                 |
| FORBIDDEN (violation = invalid output, report must not be generated):           |
| - Writing Python scripts that produce compliance judgments (no analyze_dor.py)  |
| - Producing compliance_data.json without issue_descriptions.json existing first |
| - Using ONLY issue summaries/titles for compliance assessment                   |
| - Keyword/regex/heuristic matching on summaries as substitute for LLM analysis  |
| - Giving "Pass" to issues whose description was never fetched or read           |
| - Assuming "benefit of doubt" or "in-progress means DoR was met"               |
|                                                                                 |
| STATISTICAL INVARIANT:                                                          |
| On 50+ issues, a 0% failure rate is statistically impossible and indicates      |
| the analysis was not performed. If 0 failures are detected after analysis,      |
| output an error and DO NOT proceed to report generation.                        |
|                                                                                 |
| RESOURCE BUDGET:                                                                |
| Step 11 typically requires 20-40 tool calls (fetching + analysis). This is      |
| expected and acceptable. Do NOT optimize by skipping description fetches.       |
| Speed is NOT a goal of Step 11. Accuracy IS the goal.                           |
+================================================================================+
```

**CONTEXT MANAGEMENT for Step 11:**
Step 11 is the most resource-intensive step. To manage context pressure:
- Process teams in batches of 3-4 (fetch descriptions for a batch, analyze, continue)
- It is ACCEPTABLE for Step 11 to span 20+ tool call messages
- NEVER sacrifice accuracy for speed or context conservation
- If only partial teams can be analyzed due to limits, save partial results with `"analysis_status": "partial"` but NEVER mark unfetched issues as "Pass"

After completing all extraction steps, analyze how well each Jira issue meets its team's DoR criteria and generate a comprehensive Excel report.

**CRITICAL - FIXED REPORT FORMAT:** The Report-DoR.xlsx file MUST conform to the exact schema defined below. This format is MANDATORY and MUST NOT be changed, modified, or "improved" between skill executions.

#### Report-DoR.xlsx Schema Specification

**MANDATORY STRUCTURE:**

**Sheet Count:** Exactly TWO sheets  
**Sheet 1 Name:** "Summary" (first sheet, overview of all teams)  
**Sheet 2 Name:** "DoR Compliance" (exact spelling, capital D, capital R, capital C)

---

##### Sheet 1: "Summary"

**Purpose:** Provide a high-level overview of all teams, their DoR status, and number of analyzed Jira issues, with KPI summary at the top.

**KPI Summary Section (rows 1-3, before header):**

Place a short KPI summary at the very top of the sheet (above the table header):

| Row | Column A | Column B | Column C |
|-----|----------|----------|----------|
| 1 | "% Teams with DoR" | "{X}%" (percentage of teams that have DoR defined) | |
| 2 | "% Jira Tasks fitting DoR" | "{Y}%" (percentage of analyzed issues that are DoR compliant) | |
| 3 | *(empty row - separator)* | | |

**KPI Formatting:**
- Row 1-2, Column A: Bold font, left-aligned
- Row 1-2, Column B: Bold font, left-aligned
  - "% Teams with DoR" percentage: Green font color if >= 70%, Orange if 40-69%, Red if < 40%
  - "% Jira Tasks fitting DoR" percentage: Green font color if >= 70%, Orange if 40-69%, Red if < 40%

**KPI Calculation:**
- % Teams with DoR = (count of teams where DoR = "Yes") / (total teams) * 100, rounded to 1 decimal
- % Jira Tasks fitting DoR = (count of compliant issues) / (total analyzed issues) * 100, rounded to 1 decimal

**Table Header Row (row 4):**

**Columns (in exact order):**

| Column | Header Text | Data Type | Description |
|--------|-------------|-----------|-------------|
| A | Team | String | Team name collected from SRPOL Teams page |
| B | DoR | String | "Yes" if team has DoR defined, "No" if not |
| C | Jira Tasks in progress | Integer/String | Number of Jira issues analyzed for DoR compliance. "0" if no issues to analyze |
| D | % Tasks fitting DoR | String | Percentage of this team's Jira issues that pass DoR. Format: "X%" or "-" if no issues |

**Data Source:**
- Column A: ALL team names extracted from the SRPOL Teams Confluence page (not just analyzed teams)
- Column B: "Yes" if team's DoR extraction was successful (dor_source = "direct" or "linked_page"), "No" if DoR was not found (extraction_status = "not_found")
- Column C: Count of Jira issues that were analyzed for DoR compliance for this team. "0" if team had no active issues or was skipped
- Column D: (count of team's issues with DoR Compliance = "Pass") / (total team's issues) * 100, rounded to 0 decimal. "-" if team has 0 issues or no DoR defined

**Header Row Formatting (row 4):**
- Font: Bold, White color (#FFFFFF)
- Background: Dark blue (#366092)
- Alignment: Center horizontal, Center vertical
- Border: Thin borders around all cells

**Data Row Formatting (rows 5+):**
- Alignment: Vertical center for all cells
- Border: Thin borders around all cells
- DoR column conditional fill:
  - "Yes": Green background (#C6EFCE)
  - "No": Red background (#FFC7CE)

**Column Widths:**
- A (Team): 25 characters
- B (DoR): 10 characters
- C (Jira Tasks in progress): 20 characters
- D (% Tasks fitting DoR): 18 characters

**Freeze Panes:** Row 1 (header row)

---

##### Sheet 2: "DoR Compliance"

**Columns (in exact order):**

| Column | Header Text | Data Type | Description | Formatting |
|--------|-------------|-----------|-------------|------------|
| A | Team | String | Team name from teams.json | Default |
| B | Issue Key | String | Jira issue key (e.g., "AENW-1234") | Default |
| C | Issue Type | String | Story, Bug, or Task | Default |
| D | URL | Hyperlink | Full Jira issue URL | Hyperlink format |
| E | Title | String | Issue summary from Jira | Wrap text |
| F | Status | String | Issue status from Jira | Default |
| G | Assignee | String | Assignee display name or "Unassigned" | Default |
| H | DoR Compliance | String | "Pass" or "Fail" only | Conditional fill |
| I | Note | String | Empty if "Pass", reason if "Fail" | Wrap text |

**DoR Compliance Column Formatting:**
- **"Pass" value:** Green background fill (#C6EFCE)
- **"Fail" value:** Red background fill (#FFC7CE)
- **No other values allowed** (not "Yes", "No", "COMPLIANT", "PARTIAL", percentages, etc.)

**Note Column Rules:**
- **If DoR Compliance = "Pass":** Cell MUST be empty (no text, no whitespace)
- **If DoR Compliance = "Fail":** Cell contains brief explanation (1-2 sentences) of WHY issue does not meet DoR
- **Format:** Plain text, no bullet points, no lists
- **Example:** "Missing acceptance criteria and story points not assigned"

**Header Row Formatting:**
- Row 1: Column headers
- Font: Bold, White color (#FFFFFF)
- Background: Dark blue (#366092)
- Alignment: Center horizontal, Center vertical
- Border: Thin borders around all cells

**Data Row Formatting:**
- Alignment: Vertical top alignment for all cells
- Wrap text: Enabled for Title and Note columns
- Border: Thin borders around all cells

**Column Widths:**
- A (Team): 15 characters
- B (Issue Key): 12 characters
- C (Issue Type): 10 characters
- D (URL): 50 characters
- E (Title): 40 characters
- F (Status): 12 characters
- G (Assignee): 15 characters
- H (DoR Compliance): 15 characters
- I (Note): 60 characters

**Freeze Panes:** Row 1 (header row)

**NO ADDITIONAL SHEETS:** Do not create any sheets beyond "Summary" and "DoR Compliance"

**NO ADDITIONAL COLUMNS:** Do not add Priority, Created Date, Updated Date, Compliance %, or any other columns to "DoR Compliance" sheet

**NO SUMMARY ROWS:** Do not add total counts, statistics, or summary rows at bottom of "DoR Compliance" sheet

**VALIDATION:**
After generating Report-DoR.xlsx, verify:
- Exactly 2 sheets: "Summary" (first) and "DoR Compliance" (second)
- Summary sheet has KPI section (rows 1-2) + exactly 4 columns (A through D) starting at row 4
- Summary sheet lists ALL teams from the SRPOL Teams page
- DoR Compliance sheet has exactly 9 columns (A through I): Team, Issue Key, Issue Type, URL, Title, Status, Assignee, DoR Compliance, Note
- All "DoR Compliance" values are "Pass" or "Fail" only
- All "Pass" rows have empty Note column
- All "Fail" rows have non-empty Note column

#### Step 11.1: Validate Prerequisites

Check if DoR compliance analysis should run:

```javascript
// Identify teams that can be analyzed
teams_with_dor = teams.filter(t => t.dorStatus === "found")
teams_with_issues = teams.filter(t => t.jiraIssueCount > 0)
teams_to_analyze = teams_with_dor.filter(t => teams_with_issues.includes(t))

// Skip if no analyzable teams
if (teams_to_analyze.length === 0) {
  console.log("Skipping DoR analysis: No teams have both DoR criteria and active issues")
  // Proceed to Step 10 report
  return
}
```

Output progress:
```
=== Starting DoR Compliance Analysis ===
Teams with DoR criteria: [count]
Teams with active issues: [count]
Teams to analyze: [count]
Total issues to analyze: [count]
```

#### Step 11.2: Fetch and PERSIST Full Issue Details (MANDATORY - NO SHORTCUTS)

**Purpose:** Fetch the full description for every issue and SAVE to disk as an audit artifact.
This file (`issue_descriptions.json`) proves that descriptions were fetched and serves as
input to Step 11.3. Its existence on disk is the enforcement mechanism that prevents shortcuts.

**Output file:** `${OUTPUT_DIR}/issue_descriptions.json`

**Schema:**
```json
{
  "fetched_at": "2026-06-26T14:50:00Z",
  "issues_fetched": 88,
  "issues_with_description": 75,
  "issues_without_description": 13,
  "data": {
    "AENW-1040": {
      "summary": "[SW Test Pro - solution] Marcin Al-Jawahiri",
      "team": "Radium",
      "description": "(No description provided)",
      "has_content": false
    },
    "AENW-1036": {
      "summary": "Changes in DA - outcome task of AENW-1016",
      "team": "Radium",
      "description": "Context: This task implements the DA-side changes required by...",
      "has_content": true
    }
  }
}
```

**Execution procedure:**

1. For each team to analyze, read its `[team]-jira.json` to get the issue list
2. Fetch descriptions in BATCHES of 5 parallel `getJiraIssue` calls per tool-call message:

```javascript
// Batch 5 issues per message for efficiency
mcp__plugin_atlassian_atlassian__getJiraIssue({ cloudId: "adgear.atlassian.net", issueIdOrKey: "AENW-1040", fields: ["description"] })
mcp__plugin_atlassian_atlassian__getJiraIssue({ cloudId: "adgear.atlassian.net", issueIdOrKey: "AENW-1036", fields: ["description"] })
mcp__plugin_atlassian_atlassian__getJiraIssue({ cloudId: "adgear.atlassian.net", issueIdOrKey: "AENW-1035", fields: ["description"] })
mcp__plugin_atlassian_atlassian__getJiraIssue({ cloudId: "adgear.atlassian.net", issueIdOrKey: "AENW-1015", fields: ["description"] })
mcp__plugin_atlassian_atlassian__getJiraIssue({ cloudId: "adgear.atlassian.net", issueIdOrKey: "AENW-943", fields: ["description"] })
```

3. For each response, extract description text:
   - If `fields.description` is a string: use directly
   - If `fields.description` is an object (ADF format): extract text content recursively
   - If `fields.description` is null/missing: store as `"(No description provided)"` with `has_content: false`

4. After ALL issues are fetched, write `issue_descriptions.json` to disk using the Write tool

**ADF text extraction:**
When description is in Atlassian Document Format (object with `type: "doc"` and `content` array):
- Walk the content tree recursively
- Extract text from `paragraph > text` nodes
- Extract items from `bulletList/orderedList > listItem` nodes
- Concatenate all text with newlines
- If resulting text is empty/whitespace: `has_content: false`

**After writing issue_descriptions.json, output confirmation:**
```
[CHECKPOINT] issue_descriptions.json written: X issues fetched, Y with content, Z without content
```

**CRITICAL ORDERING:** Do NOT proceed to Step 11.3 until issue_descriptions.json is physically written to disk. This file is the proof of work for Step 11.2.

**EXPLICITLY FORBIDDEN in Step 11.2:**
- Writing a Python script that "analyzes" issues without fetching descriptions
- Using issue summaries as proxy for descriptions
- Marking all issues as "Pass" because descriptions could not be fetched
- Creating heuristic rules based on summary keywords (TBD, ???, etc.)
- Any approach that produces compliance results WITHOUT reading actual issue content from Jira

#### Step 11.3: Analyze DoR Compliance (LLM-Based - MANDATORY METHOD)

```
+------------------------------------------------------------------------+
| ANALYSIS METHOD: The LLM (Claude) reads descriptions from              |
| issue_descriptions.json and makes SEMANTIC judgments against DoR.       |
| This is NOT automatable by a Python script. The LLM understands         |
| whether text constitutes "acceptance criteria" in a way that regex      |
| cannot. This is WHY the LLM performs this step directly.                |
+------------------------------------------------------------------------+
```

**CALIBRATION RULES - Apply uniformly to ALL issues for consistent results:**

1. **Issue has `has_content: false` in issue_descriptions.json** (empty/no description):
   - If team DoR requires "clear description" or "requirement clarity" → **FAIL**
   - If team DoR requires "acceptance criteria" → **FAIL**
   - Note format: "DoR criterion '[criterion name]': no description provided"
   - This rule is DETERMINISTIC - no LLM judgment needed for empty descriptions

2. **Issue has description but NO identifiable acceptance criteria:**
   Look for ANY of these patterns in the description text:
   - Bullet points or numbered lists labeled as AC/criteria/requirements
   - Sections titled "Acceptance Criteria", "AC", "Done when", "Success criteria", "Expected behavior"
   - Structured conditions (Given/When/Then, or "verify that...", "ensure that...")
   - If NONE found → **FAIL** for AC criterion
   - Note: "DoR criterion '[AC criterion name]': no testable acceptance criteria found in description"

3. **Issue has description AND has identifiable acceptance criteria:**
   → **PASS** for both description and AC criteria

4. **Estimation/Story Points:** Cannot be reliably verified from description alone.
   → Do NOT fail on estimation criteria unless DoR says "estimate visible in description"

5. **Dependencies:** Only fail if DoR requires dependencies AND description explicitly
   mentions unresolved blockers. When unclear → PASS on dependency criteria.

6. **Design/Mockups:** Only fail if DoR requires mockups AND the issue summary/description
   indicates UI work AND no Figma/design link is present in description.

**These calibration rules ensure CONSISTENT results across runs.** The rules make the
"easy cases" deterministic (empty description = Fail) and reserve LLM judgment only for
ambiguous cases (does this text constitute valid AC?).

For each team, analyze all issues in ONE batched LLM call:

**Load DoR criteria:**
```javascript
const dor_text = Read(`${OUTPUT_DIR}/${team.name_kebab}-dor.txt`)

// Skip if DoR not actually found
if (dor_text.includes("DoR - STORY/TASK criteria not found")) {
  console.log(`Skipping ${team.name}: No DoR criteria`)
  continue
}
```

**Construct analysis prompt:**
```javascript
const prompt = `You are a Scrum Master analyzing whether Jira tasks meet their team's Definition of Ready (DoR).

## Team: ${team.name}

## Definition of Ready Criteria:

${dor_text}

## Jira Issues to Analyze:

${JSON.stringify(team.enriched_issues.map(i => ({
  key: i.key,
  type: i.type,
  summary: i.summary,
  description: i.description,
  status: i.status
})), null, 2)}

## Task:

For each issue, determine:
1. Does this issue meet the team's DoR? (Yes/No)
2. If No, list the SPECIFIC DoR criteria that are NOT met, referencing the EXACT criterion name from the team's DoR document above

## Output Format:

Return ONLY a valid JSON array (no markdown, no explanation):

[
  {
    "issue_key": "AENW-1234",
    "meets_dor": true,
    "missing_criteria": []
  },
  {
    "issue_key": "AENW-1235",
    "meets_dor": false,
    "missing_criteria": [
      "DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC provided",
      "DoR criterion 'Dependencies': blocking tasks not identified"
    ]
  }
]

## Analysis Guidelines:

**CRITICAL - Accurate DoR Interpretation:**

1. **User Story Format NOT Always Required:**
   - DoR often says "user story OR requirement" (not AND)
   - Tasks can have requirements/descriptions instead of user story format
   - Only flag if BOTH user story AND requirement are missing
   - Example: "Task should be well described" = description is sufficient

2. **Check for Description Content Carefully:**
   - Read the FULL description field, including all sections (Context, Changes, etc.)
   - Only mark "no description" if field is truly empty or contains only whitespace
   - Descriptions with Context, Changes, or Requirements sections ARE valid
   - Look for content in markdown, HTML, or plain text format

3. **Acceptance Criteria Location:**
   - Check Description field for acceptance criteria
   - Acceptance criteria can be: numbered lists, bullet points, or labeled sections
   - Look for keywords: "Acceptance Criteria", "AC", "Done when", "Success criteria"
   - Criteria in "artifact form" = any structured format (bullets, numbers, table)

4. **Conditional DoR Criteria:**
   - "Mockups" only required if UI changes are involved
   - Backend/API tasks do NOT need mockups if no UI changes
   - Only flag missing mockups if DoR specifically mentions them AND task involves UI

5. **Only Flag Criteria Actually in DoR:**
   - Do NOT invent criteria not present in the team's DoR document
   - If "reproduction steps" not in DoR, do NOT flag it as missing
   - Stick strictly to the criteria listed in the DoR text provided

6. **Feedback Format (CRITICAL - must reference team's DoR):**
   - Each missing_criteria entry MUST start with: "DoR criterion '[exact criterion name from team DoR]':"
   - Then briefly state what's missing or wrong (5-15 words)
   - Example for Mouflons DoR: "DoR criterion 'Measurable/Verifiable Acceptance Criteria': AC not in SMART format"
   - Example for Radium DoR: "DoR criterion 'Dependencies are fulfilled': blocking tasks not declared"
   - The criterion name must match the heading/label used in the team's DoR document
   - Maximum 5 missing criteria per issue

7. **General Guidelines:**
   - Be fair and reasonable in interpretation
   - If a criterion is clearly met through alternative format, mark as compliant
   - Focus on what's genuinely missing, not formatting preferences

## Important:

- Return ONLY the JSON array
- Ensure valid JSON syntax
- No markdown code blocks
- No explanatory text`
```

**Execute analysis:**
```javascript
console.log(`[${team_index}/${teams_to_analyze.length}] Analyzing ${team.name}...`)

try {
  // Analyze using Claude within skill context
  const analysis_response = await analyzeWithClaude(prompt)
  
  // Parse JSON response
  const analysis = JSON.parse(analysis_response)
  
  // Validate structure
  if (!Array.isArray(analysis)) {
    throw new Error("Response is not an array")
  }
  
  team.dor_analysis = analysis
  console.log(`✓ ${team.name} analyzed (${analysis.length} issues)`)
  
} catch (error) {
  console.log(`⚠ ${team.name}: Analysis error, retrying...`)
  
  // Retry with explicit JSON-only instruction
  const retry_prompt = prompt + "\n\nCRITICAL: Return ONLY valid JSON array, no markdown, no text."
  
  try {
    const retry_response = await analyzeWithClaude(retry_prompt)
    // Remove markdown code blocks if present
    const cleaned = retry_response.replace(/```json\n?/g, '').replace(/```\n?/g, '')
    const analysis = JSON.parse(cleaned)
    
    team.dor_analysis = analysis
    console.log(`✓ ${team.name} analyzed (retry succeeded)`)
    
  } catch (retry_error) {
    console.log(`✗ ${team.name}: Analysis failed after retry`)
    team.analysis_failed = true
    team.dor_analysis = []
  }
}
```

#### Step 11.4: Aggregate Report Data (FIXED SCHEMA)

Combine all team analyses into single report dataset matching the FIXED schema (9 columns):

```javascript
const report_data = []

for (const team of teams_to_analyze) {
  // Handle analysis failures
  if (team.analysis_failed) {
    for (const issue of team.enriched_issues) {
      report_data.push({
        team: team.name,
        issue_key: issue.key,
        issue_type: issue.type,
        status: issue.status,
        title: issue.summary,
        url: issue.url,
        assignee: issue.assignee || "Unassigned",
        dor_compliance: "No",
        feedback: "Analysis failed - please review manually"
      })
    }
    continue
  }
  
  // Process successful analysis
  for (const issue of team.enriched_issues) {
    const analysis = team.dor_analysis.find(a => a.issue_key === issue.key)
    
    if (!analysis) {
      // Issue missing from analysis
      report_data.push({
        team: team.name,
        issue_key: issue.key,
        issue_type: issue.type,
        status: issue.status,
        title: issue.summary,
        url: issue.url,
        assignee: issue.assignee || "Unassigned",
        dor_compliance: "No",
        feedback: "Analysis incomplete - please review manually"
      })
      continue
    }
    
    // FIXED SCHEMA: 9 fields
    report_data.push({
      team: team.name,
      issue_key: issue.key,
      issue_type: issue.type,
      status: issue.status,
      title: issue.summary,
      url: issue.url,
      assignee: issue.assignee || "Unassigned",
      dor_compliance: analysis.meets_dor ? "Yes" : "No",
      feedback: analysis.meets_dor ? "" : (analysis.missing_criteria.join("; ") || "Does not meet DoR criteria")
    })
  }
}

// Note: Teams with no DoR are excluded from report (they were skipped in Step 11.1)
// Report only includes teams that have BOTH DoR and active issues
```

#### Step 11.5: Save Compliance and Summary Data Files

**PRE-CONDITION CHECK before saving compliance data:**
Before writing compliance_data.json, verify that issue_descriptions.json exists on disk:
```
Verify: ${OUTPUT_DIR}/issue_descriptions.json exists
If NOT exists → STOP. Step 11.2 was not executed. Go back and execute it.
If exists → proceed with saving compliance results below.
```
This check enforces the ordering constraint from the execution contract.

**This step saves JSON data files that the canonical report generator will consume in Step 13.**

1. Build `summary_data.json` from all teams metadata (schema: see `assets/templates/data-schemas.md`):
   - 15 entries, one per team in fixed order
   - Calculate per-team compliance percentages from compliance results
   - `pct_fitting_dor`: "-" if no issues or no DoR; "X%" otherwise

2. Save to `${OUTPUT_DIR}/compliance_data.json`:
   - Array of all compliance analysis results
   - Each entry has exactly 9 keys: team, issue_key, issue_type, url, title, status, assignee, dor_compliance, note
   - dor_compliance is "Pass" or "Fail" only
   - note is "" for Pass, non-empty explanation for Fail

3. Save to `${OUTPUT_DIR}/summary_data.json`:
   - Array of 15 team entries with keys: team, dor, jira_tasks, pct_fitting_dor

**DO NOT generate Python scripts for report generation.**
**DO NOT write openpyxl code inline.**
**DO NOT create CSV fallbacks.**

Reports will be generated in Step 13 by the canonical template script after quality data is also available.

Proceed immediately to Step 11.6.

**NOTE:** The old Step 11.5 Python code generation (generate_report.py, CSV fallback) has been removed.
All report rendering is now handled by `assets/templates/generate_reports.py` in Step 13.

---

**[LEGACY CODE REMOVED - See assets/templates/generate_reports.py]**

Write to: `${OUTPUT_DIR}/generate_report.py`

```python
#!/usr/bin/env python3
"""
Generate DoR Compliance Excel Report - FIXED SCHEMA
Sheet 1: Summary (all teams overview)
Sheet 2: DoR Compliance (detailed issue analysis)
"""
import json
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# FIXED SCHEMA
COMPLIANCE_SHEET_NAME = "DoR Compliance"
SUMMARY_SHEET_NAME = "Summary"

COMPLIANCE_COLUMNS = [
    ("Team", 15),
    ("Issue Key", 12),
    ("Issue Type", 10),
    ("URL", 50),
    ("Title", 40),
    ("Status", 12),
    ("Assignee", 15),
    ("DoR Compliance", 15),
    ("Note", 60)
]

SUMMARY_COLUMNS = [
    ("Team", 25),
    ("DoR", 10),
    ("Jira Tasks in progress", 20),
    ("% Tasks fitting DoR", 18)
]

def generate_report(data_json, summary_json, output_path):
    """Generate Excel report with Summary + DoR Compliance sheets."""
    data = json.loads(data_json)
    summary_data = json.loads(summary_json)
    
    wb = Workbook()
    
    # Calculate KPIs
    total_teams = len(summary_data)
    teams_without_dor = sum(1 for t in summary_data if t["dor"] == "No")
    teams_with_dor_pct = round((total_teams - teams_without_dor) / total_teams * 100, 1) if total_teams > 0 else 0
    
    total_issues = len(data)
    compliant_issues = sum(1 for d in data if d["dor_compliance"] == "Yes")
    compliance_pct = round(compliant_issues / total_issues * 100, 1) if total_issues > 0 else 0
    
    # Define styles
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    yes_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    no_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # === SHEET 1: Summary ===
    ws_summary = wb.active
    ws_summary.title = SUMMARY_SHEET_NAME
    
    # KPI Summary rows (rows 1-2, row 3 empty separator)
    kpi_bold = Font(bold=True, size=11)
    red_font = Font(bold=True, size=11, color="CC0000")
    green_font = Font(bold=True, size=11, color="006600")
    orange_font = Font(bold=True, size=11, color="CC6600")
    
    # Row 1: % Teams with DoR
    ws_summary.cell(row=1, column=1).value = "% Teams with DoR"
    ws_summary.cell(row=1, column=1).font = kpi_bold
    teams_with_dor_pct = round((total_teams - teams_without_dor) / total_teams * 100, 1) if total_teams > 0 else 0
    ws_summary.cell(row=1, column=2).value = f"{teams_with_dor_pct}%"
    if teams_with_dor_pct >= 70:
        ws_summary.cell(row=1, column=2).font = green_font
    elif teams_with_dor_pct >= 40:
        ws_summary.cell(row=1, column=2).font = orange_font
    else:
        ws_summary.cell(row=1, column=2).font = red_font
    
    # Row 2: % Jira Tasks fitting DoR
    ws_summary.cell(row=2, column=1).value = "% Jira Tasks fitting DoR"
    ws_summary.cell(row=2, column=1).font = kpi_bold
    ws_summary.cell(row=2, column=2).value = f"{compliance_pct}%"
    if compliance_pct >= 70:
        ws_summary.cell(row=2, column=2).font = green_font
    elif compliance_pct >= 40:
        ws_summary.cell(row=2, column=2).font = orange_font
    else:
        ws_summary.cell(row=2, column=2).font = red_font
    
    # Row 3: empty separator
    # Row 4: Table header
    for col_idx, (header, width) in enumerate(SUMMARY_COLUMNS, 1):
        cell = ws_summary.cell(row=4, column=col_idx)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
        ws_summary.column_dimensions[get_column_letter(col_idx)].width = width
    
    # Freeze panes below header
    ws_summary.freeze_panes = 'A5'
    
    # Add Summary data rows (starting from row 5)
    for row_idx, row_data in enumerate(summary_data, start=5):
        # Column A: Team
        ws_summary.cell(row=row_idx, column=1).value = row_data["team"]
        ws_summary.cell(row=row_idx, column=1).border = thin_border
        ws_summary.cell(row=row_idx, column=1).alignment = Alignment(vertical='center')
        
        # Column B: DoR (Yes/No)
        dor_value = row_data["dor"]
        ws_summary.cell(row=row_idx, column=2).value = dor_value
        ws_summary.cell(row=row_idx, column=2).fill = yes_fill if dor_value == "Yes" else no_fill
        ws_summary.cell(row=row_idx, column=2).border = thin_border
        ws_summary.cell(row=row_idx, column=2).alignment = Alignment(horizontal='center', vertical='center')
        
        # Column C: Jira Tasks (count)
        ws_summary.cell(row=row_idx, column=3).value = row_data["jira_tasks"]
        ws_summary.cell(row=row_idx, column=3).border = thin_border
        ws_summary.cell(row=row_idx, column=3).alignment = Alignment(horizontal='center', vertical='center')
        
        # Column D: % Tasks fitting DoR (per team)
        team_pct = row_data.get("pct_fitting_dor", "-")
        ws_summary.cell(row=row_idx, column=4).value = team_pct
        ws_summary.cell(row=row_idx, column=4).border = thin_border
        ws_summary.cell(row=row_idx, column=4).alignment = Alignment(horizontal='center', vertical='center')
    
    # === SHEET 2: DoR Compliance ===
    ws = wb.create_sheet(title=COMPLIANCE_SHEET_NAME)
    
    # Write DoR Compliance header row
    for col_idx, (header, width) in enumerate(COMPLIANCE_COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    
    # Freeze header row
    ws.freeze_panes = 'A2'
    
    # Add DoR Compliance data rows - FIXED SCHEMA (9 columns)
    for row_idx, row_data in enumerate(data, start=2):
        # Column A: Team
        ws.cell(row=row_idx, column=1).value = row_data["team"]
        
        # Column B: Issue Key
        ws.cell(row=row_idx, column=2).value = row_data["issue_key"]
        
        # Column C: Issue Type
        ws.cell(row=row_idx, column=3).value = row_data["issue_type"]
        
        # Column D: URL (as hyperlink)
        ws.cell(row=row_idx, column=4).value = row_data["url"]
        ws.cell(row=row_idx, column=4).hyperlink = row_data["url"]
        ws.cell(row=row_idx, column=4).style = "Hyperlink"
        
        # Column E: Title
        ws.cell(row=row_idx, column=5).value = row_data["title"]
        
        # Column F: Status
        ws.cell(row=row_idx, column=6).value = row_data["status"]
        
        # Column G: Assignee
        ws.cell(row=row_idx, column=7).value = row_data["assignee"]
        
        # Column H: DoR Compliance (Pass/Fail ONLY)
        compliance_value = "Pass" if row_data["dor_compliance"] in ["Yes", "Pass"] else "Fail"
        ws.cell(row=row_idx, column=8).value = compliance_value
        ws.cell(row=row_idx, column=8).fill = yes_fill if compliance_value == "Pass" else no_fill
        
        # Column I: Note (empty if Pass, reason if Fail)
        ws.cell(row=row_idx, column=9).value = row_data.get("note", row_data.get("feedback", ""))
        
        # Apply formatting to all cells in row
        for col in range(1, 10):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = thin_border
            # Wrap text for Title and Note columns
            cell.alignment = Alignment(vertical='top', wrap_text=(col in [5, 9]))
    
    # Save workbook
    wb.save(output_path)
    print(f"[SUCCESS] Excel report saved to: {output_path}")
    
    # Validate schema
    print("\nSCHEMA VALIDATION:")
    print(f"  - Sheet count: {len(wb.sheetnames)} (expected: 2)")
    print(f"  - Sheet 1: '{wb.sheetnames[0]}' (expected: '{SUMMARY_SHEET_NAME}')")
    print(f"  - Sheet 2: '{wb.sheetnames[1]}' (expected: '{COMPLIANCE_SHEET_NAME}')")
    print(f"  - Summary columns: {ws_summary.max_column} (expected: 3)")
    print(f"  - Compliance columns: {ws.max_column} (expected: 9)")
    
    if len(wb.sheetnames) != 2:
        print("  [WARNING] Schema violation: Expected exactly 2 sheets")
    if ws_summary.max_column != 4:
        print(f"  [WARNING] Schema violation: Summary sheet should have 4 columns")
    if ws.max_column != 9:
        print(f"  [WARNING] Schema violation: Compliance sheet should have 9 columns")

if __name__ == "__main__":
    generate_report(sys.argv[1], sys.argv[2], sys.argv[3])
```

**Step 3: Prepare Summary data and execute Python script:**

Build the `summary_data` array from all teams (not just analyzed ones):
```javascript
const summary_data = []

for (const team of all_teams) {
  // Determine if team has DoR
  const has_dor = team.extraction_status === "success" && team.dor_source !== null
  
  // Count analyzed Jira issues for this team
  const team_issues = report_data.filter(r => r.team === team.name)
  const jira_task_count = team_issues.length
  
  // Calculate per-team % fitting DoR
  const team_pass_count = team_issues.filter(r => r.dor_compliance === "Pass" || r.dor_compliance === "Yes").length
  const pct_fitting_dor = (jira_task_count > 0 && has_dor) ? `${Math.round(team_pass_count / jira_task_count * 100)}%` : "-"
  
  summary_data.push({
    team: team.name,
    dor: has_dor ? "Yes" : "No",
    jira_tasks: jira_task_count,  // 0 if no issues analyzed
    pct_fitting_dor: pct_fitting_dor  // "X%" or "-"
  })
}
```

Use both `report_data` and `summary_data` arrays:
```bash
cd "${OUTPUT_DIR}"
python3 generate_report.py '${JSON.stringify(report_data)}' '${JSON.stringify(summary_data)}' 'Report-DoR.xlsx'
```

**Step 4: Fallback to CSV if Python unavailable:**
```javascript
console.log("Python/openpyxl not available, generating CSV fallback...")

// Summary CSV
const summary_csv_lines = ["Team,DoR,Jira Tasks"]
for (const row of summary_data) {
  summary_csv_lines.push([row.team, row.dor, row.jira_tasks].join(','))
}
Write(`${OUTPUT_DIR}/Report_Summary.csv`, summary_csv_lines.join('\n'))

// DoR Compliance CSV - 9 columns
const csv_lines = ["Team,Issue Key,Issue Type,Status,Title,URL,Assignee,DoR Compliance,Feedback"]

for (const row of report_data) {
  const escapeCsv = (str) => {
    if (!str) return ""
    const s = String(str)
    if (s.includes(',') || s.includes('"') || s.includes('\n')) {
      return `"${s.replace(/"/g, '""')}"`
    }
    return s
  }
  
  csv_lines.push([
    escapeCsv(row.team),
    escapeCsv(row.issue_key),
    escapeCsv(row.issue_type),
    escapeCsv(row.status),
    escapeCsv(row.title),
    escapeCsv(row.url),
    escapeCsv(row.assignee),
    row.dor_compliance,
    escapeCsv(row.feedback)
  ].join(','))
}

const csv_content = csv_lines.join('\n')
Write(`${OUTPUT_DIR}/Report.csv`, csv_content)
console.log("CSV reports saved to: ${OUTPUT_DIR}/Report.csv and Report_Summary.csv")
```

#### Step 11.6: Generate Summary Document

Create: `${OUTPUT_DIR}/DOR_ANALYSIS_SUMMARY.md`

```markdown
# DoR Compliance Analysis Summary

**Generated:** ${new Date().toISOString()}
**Scan Directory:** ${OUTPUT_DIR}/

---

## Overall Statistics

- **Total Teams Analyzed:** ${teams_analyzed_count}
- **Total Issues Analyzed:** ${total_issues}
- **Issues Meeting DoR:** ${meeting_count} (${(meeting_count/total_issues*100).toFixed(1)}%)
- **Issues NOT Meeting DoR:** ${not_meeting_count} (${(not_meeting_count/total_issues*100).toFixed(1)}%)
- **Teams Skipped (No DoR):** ${teams_without_dor.length}

---

## Breakdown by Team

| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |
|------|--------------|-----------|---------------|-----------------|
${teams_analyzed.map(t => {
  const meets = t.dor_analysis.filter(a => a.meets_dor).length
  const total = t.dor_analysis.length
  const rate = total > 0 ? (meets/total*100).toFixed(1) : 'N/A'
  return `| ${t.name} | ${total} | ${meets} | ${total - meets} | ${rate}% |`
}).join('\n')}

---

## Most Common DoR Gaps

${getTopGaps(teams_analyzed, 5).map((gap, i) => 
  `${i+1}. **${gap.criteria}** - ${gap.count} occurrences`
).join('\n')}

---

## Teams with No DoR Documentation

The following teams have no documented DoR criteria and were excluded from analysis:

${teams_without_dor.map(t => `- ${t.name}`).join('\n')}

---

## Files Generated

- **Report-DoR.xlsx** (or Report.csv) - Full compliance report
- **DOR_ANALYSIS_SUMMARY.md** - This summary document
- **teams.json** - Updated with analysis metadata

---

## Analysis Method

- **Tool:** Claude Sonnet 4.5 (LLM-based semantic analysis)
- **Approach:** Batched team-level analysis
- **Analysis Duration:** ${analysis_duration}

---

## Recommendations

1. Review all issues marked "No" in the report
2. Address common DoR gaps identified above
3. Teams without DoR should document their criteria
4. Consider refining DoR criteria based on common gaps

---

**Report Location:** \`${OUTPUT_DIR}/Report-DoR.xlsx\`
```

**Helper function:**
```javascript
function getTopGaps(teams, limit) {
  const gap_counts = {}
  
  for (const team of teams) {
    for (const analysis of team.dor_analysis) {
      if (!analysis.meets_dor) {
        for (const criteria of analysis.missing_criteria) {
          gap_counts[criteria] = (gap_counts[criteria] || 0) + 1
        }
      }
    }
  }
  
  return Object.entries(gap_counts)
    .map(([criteria, count]) => ({criteria, count}))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit)
}
```

#### Step 11.7: Update teams.json with Analysis Metadata

```javascript
// Read existing teams.json
const teams_json = Read(`${OUTPUT_DIR}/teams.json`)
const teams_data = JSON.parse(teams_json)

// Calculate statistics
const meeting_count = report_data.filter(r => r.dor_compliance === "Yes").length
const not_meeting_count = report_data.filter(r => r.dor_compliance === "No").length
const total_analyzed = meeting_count + not_meeting_count

// Add analysis metadata
teams_data.metadata.dor_analysis = {
  performed: true,
  timestamp: new Date().toISOString(),
  teams_analyzed: teams_analyzed_count,
  issues_analyzed: total_analyzed,
  issues_meeting_dor: meeting_count,
  issues_not_meeting_dor: not_meeting_count,
  compliance_rate: total_analyzed > 0 ? (meeting_count / total_analyzed * 100).toFixed(1) : "0",
  report_file: python_available ? "Report-DoR.xlsx" : "Report.csv",
  summary_file: "DOR_ANALYSIS_SUMMARY.md",
  analysis_method: "llm_batched"
}

// Add per-team analysis metadata
for (const team of teams_data.teams) {
  const team_analysis = teams_analyzed.find(t => t.name === team.name)
  
  if (team_analysis && !team_analysis.analysis_failed) {
    const meets = team_analysis.dor_analysis.filter(a => a.meets_dor).length
    const total = team_analysis.dor_analysis.length
    
    team.dor_analysis = {
      analyzed: true,
      issues_count: total,
      meets_dor: meets,
      does_not_meet: total - meets,
      compliance_rate: total > 0 ? (meets / total * 100).toFixed(1) : "0"
    }
  } else if (team.dorStatus === "not_found") {
    team.dor_analysis = {
      analyzed: false,
      reason: "no_dor_criteria"
    }
  } else if (team.jiraIssueCount === 0) {
    team.dor_analysis = {
      analyzed: false,
      reason: "no_active_issues"
    }
  } else if (team_analysis && team_analysis.analysis_failed) {
    team.dor_analysis = {
      analyzed: false,
      reason: "analysis_failed"
    }
  }
}

// Write updated teams.json
Write(`${OUTPUT_DIR}/teams.json`, JSON.stringify(teams_data, null, 2))
```

#### Step 11.8: Report DoR Analysis Completion

Output final summary to console:

```
=== DoR Compliance Analysis Complete ===

Teams Analyzed: ${teams_analyzed_count}
Total Issues: ${total_analyzed}
  - Meeting DoR: ${meeting_count} (${(meeting_count/total_analyzed*100).toFixed(1)}%)
  - Not Meeting DoR: ${not_meeting_count} (${(not_meeting_count/total_analyzed*100).toFixed(1)}%)

Report saved to: ${OUTPUT_DIR}/Report-DoR.xlsx

Summary saved to: ${OUTPUT_DIR}/DOR_ANALYSIS_SUMMARY.md

Teams skipped (no DoR criteria): ${teams_without_dor.length}
${teams_without_dor.map(t => `  - ${t.name}`).join('\n')}

Most common gaps:
${getTopGaps(teams_analyzed, 3).map((gap, i) => 
  `  ${i+1}. ${gap.criteria} (${gap.count} issues)`
).join('\n')}

Next steps:
  1. Open Report-DoR.xlsx to review detailed findings
  2. Address high-priority DoR gaps in your team
  3. Consider updating DoR criteria based on findings

Analysis method: LLM-based (Claude Sonnet 4.5)
Analysis duration: ${formatDuration(analysis_duration)}
```

**Error handling for Step 11:**
- If no teams can be analyzed (no DoR + issues), skip Step 11 entirely
- If analysis fails for a team, mark issues as "No" with failure note
- If JSON parse fails twice, mark team as analysis_failed
- If Excel generation fails, fall back to CSV
- Continue with partial results if some teams succeed
- Log all errors to `DOR_ANALYSIS_ERRORS.log`

### Step 12: DoR Quality Assessment (AUTO-EXECUTE after Step 11)

**This step executes automatically after Step 11 completes.** Do not pause or ask for user confirmation. This step assesses the QUALITY of each team's Definition of Ready document itself (not issue compliance).

#### Step 12.0: Load DoR Standard Reference

Read the persistent DoR Standard reference document:
```
Read("C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\dor-standard.txt")
```

If the file does not exist, output warning and skip Step 12 entirely:
```
[WARNING] DoR Standard document not found at assets/dor-standard.txt
Skipping DoR Quality Assessment.
```

Store the content as `dor_standard_text` for use in Step 12.3.

#### Step 12.1: Fetch Company DoR Standard

Fetch the company's Definition of Ready page from Confluence:
```
mcp__plugin_atlassian_atlassian__getConfluencePage(
  cloudId: "adgear.atlassian.net",
  pageId: "21735179128",
  contentFormat: "markdown"
)
```

Parse the response to extract the company DoR text content. Store as `company_dor_text`.

Save to `${OUTPUT_DIR}/company-dor-standard.txt` for traceability.

If fetch fails, log warning but continue using only the industry standard:
```
[WARNING] Could not fetch company DoR page (21735179128). Using industry standard only.
```

#### Step 12.2: Identify Teams to Assess

From the teams data collected in Steps 8-10, identify teams that have a defined DoR:
```javascript
const teams_to_assess = all_teams.filter(t => 
  t.dorStatus === "found" || t.dor_source !== null
)
```

Only teams with extracted DoR criteria (those with a `[team-name]-dor.txt` file) are assessed. Teams without DoR (e.g., ML Serving Sturgeons, SRE) are excluded.

#### Step 12.3: Quality Assessment (LLM-Based)

For EACH team with a defined DoR, evaluate COVERAGE against the DoR Standard. Process all teams in a single batched LLM call for efficiency.

**CRITICAL - FIXED ASSESSMENT METHOD:**
The assessment compares each team's DoR against a FIXED list of standard criteria derived from the industry standard (dor-standard.txt) and company standard (Confluence page). The scoring is purely about COVERAGE: how many of the standard criteria does the team's DoR address?

**Standard Criteria Checklist (10 items):**
These are the 10 essential DoR criteria derived from both standards. Each criterion covered = 10 points. Maximum score = 100.

1. **User Story/Requirement Clarity** - Clear description of what needs to be built, understandable to all team members
2. **Acceptance Criteria** - Specific, testable conditions for successful completion
3. **Estimation/Sizing** - Team has estimated the work (story points, t-shirt sizing, etc.)
4. **Dependencies Identified & Resolved** - External/internal dependencies documented and addressed
5. **Design/UX Specification** - Mockups, wireframes, or technical design provided when applicable
6. **Scope/Sprint Fit** - Work is decomposed to fit within a single sprint
7. **Risks/Blockers Identified** - Known risks and potential blockers documented
8. **Stakeholder Alignment** - PO approval, priority confirmed, business value explained
9. **Technical Feasibility Confirmed** - Technical investigation done, approach validated
10. **Testing Strategy/Approach** - Test cases defined or testing approach documented

**Assessment Prompt:**
```
You are evaluating the COVERAGE of a team's Definition of Ready (DoR) against a standard checklist.

STANDARD CHECKLIST (10 criteria, each worth 10 points):
1. User Story/Requirement Clarity - Clear description of what needs to be built
2. Acceptance Criteria - Specific, testable conditions for completion
3. Estimation/Sizing - Team has estimated the work
4. Dependencies Identified & Resolved - Dependencies documented and addressed
5. Design/UX Specification - Mockups/designs provided when applicable
6. Scope/Sprint Fit - Work decomposed to fit within a sprint
7. Risks/Blockers Identified - Known risks and blockers documented
8. Stakeholder Alignment - PO approval, priority confirmed
9. Technical Feasibility Confirmed - Technical investigation done
10. Testing Strategy/Approach - Test cases or testing approach defined

REFERENCE STANDARDS:
Industry standard:
---
${dor_standard_text}
---

Company standard:
---
${company_dor_text}
---

TEAM DoR TO ASSESS (Team: ${team_name}):
---
${team_dor_text}
---

For this team's DoR, determine which of the 10 standard criteria are COVERED (explicitly addressed in the team's DoR document). A criterion is "covered" if the team's DoR mentions it or addresses it in substance, even if using different wording.

RESPOND IN VALID JSON ONLY:
{
  "team": "Team Name",
  "coverage": <number 0-100, count of covered criteria * 10>,
  "covered_criteria": [<list of covered criterion numbers, e.g. [1, 2, 3, 4]>],
  "missing_criteria": [<list of missing criterion numbers, e.g. [5, 6, 7, 8, 9, 10]>],
  "note": "<list ONLY the missing criteria names, comma-separated>"
}

The "note" field MUST list the NAMES of the missing criteria from the standard checklist.
Format: "Missing: [criterion name 1], [criterion name 2], ..."
If all 10 are covered: "All standard criteria covered"

Examples:
- "Missing: Design/UX Specification, Scope/Sprint Fit, Risks/Blockers Identified, Testing Strategy"
- "Missing: Technical Feasibility Confirmed, Testing Strategy/Approach"
- "All standard criteria covered"
```

**Process ALL teams in one prompt** by including multiple TEAM DoR sections and requesting an array response:
```json
[
  {"team": "Abyss", "coverage": 50, "covered_criteria": [1,2,3,4,5], "missing_criteria": [6,7,8,9,10], "note": "Missing: Scope/Sprint Fit, Risks/Blockers Identified, Stakeholder Alignment, Technical Feasibility, Testing Strategy"},
  ...
]
```

**Parse the JSON response.** If parsing fails, retry once with explicit "RESPOND IN JSON ONLY" instruction.

**Coverage Score Calculation:**
```
coverage = count(covered_criteria) * 10
```
Score is always a multiple of 10 (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100).

#### Step 12.4: Save Quality Data

1. Save quality assessment results to `${OUTPUT_DIR}/quality_data.json`
   - Schema: see `assets/templates/data-schemas.md`
   - Coverage values MUST be multiples of 10 (count of covered criteria * 10)
   - Note MUST list missing criterion names from the 10-criteria standard
   - Criterion names used in Note: User Story/Requirement Clarity, Acceptance Criteria, Estimation/Sizing, Dependencies Identified & Resolved, Design/UX Specification, Scope/Sprint Fit, Risks/Blockers Identified, Stakeholder Alignment, Technical Feasibility Confirmed, Testing Strategy/Approach

2. **DO NOT open Report-DoR.xlsx with load_workbook.** DO NOT write separate openpyxl code. DO NOT create CSV fallbacks.
   The canonical template script (`generate_reports.py`) handles ALL report generation in Step 13.

Proceed immediately to Step 12.5.

#### Step 12.5: Report DoR Quality Assessment Completion

Output final summary to console:

```
=== DoR Quality Assessment Complete ===

Teams Assessed: ${teams_assessed_count}
Average DoR Coverage: ${average_coverage}/100

Top Coverage:
  1. ${top1_team} - ${top1_score}/100
  2. ${top2_team} - ${top2_score}/100
  3. ${top3_team} - ${top3_score}/100

Lowest Coverage:
  1. ${bottom1_team} - ${bottom1_score}/100 (${bottom1_note})
  2. ${bottom2_team} - ${bottom2_score}/100 (${bottom2_note})
  3. ${bottom3_team} - ${bottom3_score}/100 (${bottom3_note})

Results added to: ${OUTPUT_DIR}/Report-DoR.xlsx (sheet "DoR quality")

Standards used:
  - Industry: assets/dor-standard.txt
  - Company: Confluence page 21735179128 (Definition of Ready DOR)
  - Checklist: 10 standard criteria (each = 10 points)
```

**Error handling for Step 12:**
- If dor-standard.txt missing: skip entire Step 12 with warning
- If company DoR page fetch fails: continue with industry standard only
- If LLM evaluation fails: retry once, then mark team as "assessment_failed" with score 0
- If Report-DoR.xlsx cannot be loaded: create standalone DoR-Quality.csv
- If openpyxl unavailable: create standalone DoR-Quality.csv

### Step 13: Generate All Reports via Canonical Template (AUTO-EXECUTE after Step 12)

**This step executes the canonical report generator script. No report code is written by the LLM.**

**This step executes automatically after Step 12 completes.** Do not pause or ask for user confirmation.

#### Step 13.1: Verify Prerequisites

Check that all 3 JSON data files exist in `${OUTPUT_DIR}`:
- `summary_data.json` (saved in Step 11.5)
- `compliance_data.json` (saved in Step 11.5)
- `quality_data.json` (saved in Step 12.4)

If any file is missing, construct it from available data before proceeding.

#### Step 13.2: Verify and Copy Template Script

```bash
test -f "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_reports.py" && echo "OK" || echo "MISSING"
```

If the template script does not exist, output error:
```
ERROR: Template script not found at assets/templates/generate_reports.py
Cannot generate reports without the canonical template.
```
Then skip report generation but do NOT fail the overall skill.

If it exists, copy it to the output directory:
```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_reports.py" "${OUTPUT_DIR}/generate_reports.py"
```

#### Step 13.3: Execute Template Script

```bash
cd "${OUTPUT_DIR}" && python3 generate_reports.py summary_data.json compliance_data.json quality_data.json "." "{SCAN_DATE}"
```

Where `{SCAN_DATE}` is the scan date in YYYY-MM-DD format (e.g., "2026-06-26").

This single command produces BOTH:
- `Report-DoR.xlsx` (3 sheets: Summary, DoR Compliance, DoR quality)
- `Report-DoR.html` (self-contained dashboard)

#### Step 13.4: Validate Reports

```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/validate_reports.py" "${OUTPUT_DIR}/validate_reports.py"
cd "${OUTPUT_DIR}" && python3 validate_reports.py "."
```

If validation fails, output the errors but do NOT attempt to "fix" by regenerating with different code.
The template is canonical - if validation fails, the DATA is wrong, not the renderer.

**Additionally, validate compliance integrity:**
```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/validate_compliance.py" "${OUTPUT_DIR}/validate_compliance.py"
cd "${OUTPUT_DIR}" && python3 validate_compliance.py "."
```

If compliance validation fails, output the errors prominently. If the error is "issue_descriptions.json does not exist", this means Step 11.2 was skipped and the compliance results are INVALID. Note this clearly in the final output.

#### Step 13.5: Report Completion

Output:
```
=== Reports Generated ===

Excel: ${OUTPUT_DIR}/Report-DoR.xlsx
HTML:  ${OUTPUT_DIR}/Report-DoR.html

Validation: PASSED (or list specific errors)
```

**FORBIDDEN in Step 13:**
- DO NOT write Python code to generate reports
- DO NOT create openpyxl scripts
- DO NOT write HTML strings
- DO NOT modify generate_reports.py
- DO NOT add CSS classes, columns, or sections not in the template
- DO NOT generate "fallback" CSV files
- The ONLY actions are: copy template, execute template, validate output

## Error Handling

- **Continue on error:** If one team page fails, continue with remaining teams
- **Track failures:** Record all errors in teams.json metadata
- **Detailed logging:** Include error messages in per-team TXT files
- **Graceful degradation:** Partial data is better than no data
- **Team field unavailable:** If `customfield_10114` is not present in issue responses, all project issues are unassignable to teams; log warning about potential cross-team issues in shared projects (AENW, RSW, PEPI, PEA)
- **Team pattern mismatch:** If client-side filtering matches 0 issues but the project has SRPOL issues from other teams, log pattern mismatch warning (team may have been renamed in Jira)

**Automation Rules:**
- **Only stop for critical failures:** Continue execution through all 13 steps unless:
  - Authentication fails completely (Step 2)
  - No teams found in source page (Step 5)
  - Output directory cannot be created (Step 4)
- **Do not stop for partial failures:** If some teams fail, continue with successful teams
- **Automatic Step 11:** Execute Step 11 (DoR analysis) automatically after Step 10, even if Step 11 has no explicit user request
- **Automatic Step 12:** Execute Step 12 (DoR quality assessment) automatically after Step 11 completes. Skip Step 12 only if assets/dor-standard.txt does not exist
- **Automatic Step 13:** Execute Step 13 (HTML dashboard report) automatically after Step 12 completes. This step is non-critical and should not block completion if it fails

## Tool Requirements

Required tools:
- **ToolSearch** - Check for Atlassian MCP availability
- **mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources** - Verify authentication
- **mcp__plugin_atlassian_atlassian__getConfluencePage** - Fetch Confluence pages
- **mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql** - Query Jira issues
- **mcp__plugin_atlassian_atlassian__getJiraIssue** - Fetch full issue details (for Step 11)
- **mcp__plugin_atlassian_atlassian__getJiraIssueTypeMetaWithFields** - Discover Team custom field ID (Step 9.0)
- **Write** - Create JSON, TXT, Python, and Markdown files
- **Read** - Verify file contents
- **Bash** - Create directories, get current time for CET timestamp calculation, execute Python scripts

Optional tools:
- **Grep** - Search for patterns
- **Glob** - Find files
- **Python 3 + openpyxl** - Generate Excel reports (fallback to CSV if unavailable)

## Important Rules

1. **DoR Scope:** Extract ONLY "DEFINITION OF READY (DoR) - STORY/TASK" or plain "DEFINITION OF READY (DoR)", completely ignore "- OFFERING/EPIC" sections

2. **Team Naming:** Extract team names from actual Confluence page titles, not from table descriptions
   - Fetch each team page to get the title
   - Clean title by removing: "Team", "Team Page", "Team Space", "Space" (case-insensitive)
   - Use cleaned title as team name in all files and metadata

3. **File Naming:** Use kebab-case for all team file names (lowercase with hyphens)

4. **Timestamp Consistency:** Calculate CET timestamp ONCE at the start and use consistently for all file paths

5. **Linked DoR Pages:** ALWAYS check for links in DoR sections. If a link with DoR keywords is found, follow it and extract from the referenced page instead of using inline content

6. **Jira Constraints:**
   - Only query issues with status "In Progress", "Code Review", or "In Development" (case-sensitive)
   - Support fallback queries with alternative case formats if primary queries fail
   - Only query issue types Story, Bug, Task (EXCLUDE Sub-tasks: `issuetype != Sub-task`)
   - Sub-tasks are implementation details and should not be analyzed against DoR
   - Mark truncated results with warning

7. **ISO-8601 Timestamps:** Use ISO-8601 format for all timestamps in files and JSON

8. **Atomic Operations:** Create files in atomic operations (full content at once)

9. **All Files in Timestamped Folder:** No files should be created in parent directory

10. **DoR Compliance Analysis (Step 11):**
   - Only analyze teams that have BOTH DoR criteria and active Jira issues
   - Binary compliance: "Yes" (compliant) or "No" (not compliant)
   - Feedback only for "No" values (brief explanation of why DoR not met)
   - Generate Excel report in FIXED schema (2 sheets: Summary + DoR Compliance) and always named it Report
   - Summary sheet lists ALL teams with DoR status and Jira task count
   - Schema MUST NOT be modified or "improved" between executions
   - Validate report matches schema specification
   - Fall back to CSV if Python/openpyxl unavailable
   - Update teams.json with analysis metadata
   - Continue with partial results if some teams fail analysis

10a. **DoR Analysis Accuracy (CRITICAL):**
   - User story format NOT required for Tasks if DoR says "user story OR requirement"
   - Read FULL description field (all sections: Context, Changes, Requirements, etc.)
   - Only mark "no description" if field is truly empty
   - Acceptance criteria can be in Description field (not separate field)
   - Recognize AC as: numbered lists, bullets, "Done when" sections, structured format
   - Mockups only required if DoR mentions them AND task involves UI changes
   - Backend/API tasks do NOT need mockups if no UI changes
   - Only flag criteria explicitly listed in team's DoR document
   - Do NOT invent criteria not present in DoR (e.g., "reproduction steps" if not in DoR)
   - Interpret DoR fairly and reasonably, not overly strict on format

11. **Team Field Filtering (client-side for shared projects):**
   - Team custom field ID: `customfield_10114` (Jira Team-type field)
   - DO NOT use `customfield_10114` in JQL - Team-type fields do not support JQL filtering
   - Query ALL active issues per project (one query per unique project via PROJECT_TEAMS map)
   - Filter results CLIENT-SIDE by checking `fields.customfield_10114.name` === team pattern
   - Use EXACT string match (case-sensitive) with values from TEAM_NAME_PATTERNS
   - Paginate using `nextPageToken` until `isLast: true` (cap at 5 pages / 500 issues)
   - If pattern matches 0 issues but project has other SRPOL ("WAW") issues: log pattern mismatch warning
   - Issues with null/missing team field are discarded (not assigned to any team)
   - Cross-team contamination is impossible by design (exact name match guarantees uniqueness)
   - NEVER use `sprint in openSprints()` in any query - this filter causes data loss

12. **Report Generation is 100% Deterministic (Template-Based):**
   - Reports are generated ONLY by `assets/templates/generate_reports.py` - NEVER by LLM-written code
   - The LLM's responsibility ends at producing valid JSON data files (summary_data.json, compliance_data.json, quality_data.json)
   - The template script is NEVER modified, NEVER regenerated, NEVER "improved" during skill execution
   - If the template script doesn't exist, the skill outputs an error (doesn't create a replacement)
   - The template produces BOTH Report-DoR.xlsx AND Report-DoR.html in a single execution
   - `src/dor-processor.py` is LEGACY - do not use it for report generation
   - Report-DoR.xlsx schema: EXACTLY 3 sheets ("Summary", "DoR Compliance", "DoR quality")
   - Report-DoR.html schema: Fixed 4-section dashboard (KPI cards, Team Overview, Failed Issues, Quality Assessment)
   - DO NOT write openpyxl code, DO NOT write HTML strings, DO NOT create CSV fallbacks

13. **DoR Quality Assessment (Step 12) - 10 Criteria Binary Model:**
   - Only assesses teams that have defined DoR (excludes teams with dor_source = null)
   - Uses BOTH industry standard (assets/dor-standard.txt) AND company standard (Confluence page 21735179128)
   - Compares team DoR against 10 standard criteria checklist
   - Coverage score = count of covered criteria * 10 (always multiple of 10: 0, 10, 20, ..., 100)
   - The 7-dimension weighted model in src/dor-processor.py (Coverage/Clarity/Measurability/Company/Industry/Actionability/AC) is DEPRECATED
   - Do NOT output weighted sub-scores, do NOT use dimension labels in Note column
   - Criterion names used in Note column MUST come from this list:
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
   - Note format: "Missing: [criterion names comma-separated]" or "All standard criteria covered"
   - Save results to quality_data.json; the template script handles all Excel/HTML rendering

14. **DoR Compliance Integrity (mechanical enforcement):**
   - `issue_descriptions.json` MUST exist in OUTPUT_DIR before `compliance_data.json` is written
   - Every issue in `compliance_data.json` MUST have a corresponding entry in `issue_descriptions.json`
   - Issues where `issue_descriptions.json` shows `has_content: false` MUST be "Fail" in compliance_data.json (an issue with no description cannot pass DoR criteria that require clear description/AC)
   - If compliance_data.json has 0 "Fail" entries across 50+ issues: this is an ERROR condition. Output error message: "ANALYSIS ERROR: 0% failure rate is statistically invalid. Step 11 likely skipped description fetching." Do NOT proceed to Step 13 report generation with invalid data.
   - Historical baseline: 10-25% of issues typically fail DoR compliance
   - Python scripts (*.py) in OUTPUT_DIR are ONLY acceptable for: Jira data processing (Step 9), template copies (generate_reports.py, validate_reports.py, validate_compliance.py). Any file named `analyze_*.py` indicates the LLM wrote a heuristic script instead of performing proper analysis = VIOLATION.

15. **Step 11 Produces Two Artifacts (not one):**
   - `issue_descriptions.json` - proves descriptions were fetched (audit trail)
   - `compliance_data.json` - the actual compliance results
   - Both files are REQUIRED. Missing either = incomplete Step 11.
   - The validation script (`validate_compliance.py`) checks both files post-generation.
