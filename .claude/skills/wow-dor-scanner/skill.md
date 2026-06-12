---
name: wow-dor-scanner
description: >
  Extract SRPOL team data, DoR - STORY/TASK criteria, and active Jira issues from the SRPOL Teams Confluence page.
  Analyzes DoR compliance for each issue and generates Excel report with Summary sheet.
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
5. Saves all data to absolute path: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\<timestamp>/` where timestamp is in CET format: `YYYYMMDD HH-MM`
   - DoR files: `[team-name]-dor.txt`
   - Jira files: `[team-name]-jira.json` and `[team-name]-jira.txt`
   - Master file: `teams.json`
   - DoR Analysis Report: `Report.xlsx`
   - Analysis Summary: `DOR_ANALYSIS_SUMMARY.md`

## Instructions

**CRITICAL - FULL AUTOMATION:** This skill must execute all 11 steps automatically without pausing or asking for user confirmation. The entire workflow from data extraction (Steps 1-10) to DoR analysis and Excel report generation (Step 11) should run continuously. Only stop execution if:
- Authentication fails (Step 2)
- Critical errors occur that prevent continuation
- Prerequisites are missing (e.g., no teams found)

Do NOT pause between steps to ask for approval. Do NOT stop after Step 10. Proceed directly from Step 10 to Step 11 automatically.

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
   - From first column: extract team page URL
   - From SPRINT board column: extract sprint board link
   - Extract page ID from team page URLs (number after `/pages/` or the tiny link ID after `/wiki/x/`)
   - **Do NOT extract team name yet** - it will be retrieved from the actual page title

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
   Look for headings (`<h2>`, `<h3>`, `<h4>`) containing:
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

The Team custom field is essential for accurate team-specific filtering in shared projects (AENW, PEPI, RSW).

**Field ID**: `customfield_10114` (verified in Jira instance)

**Validation**:

```javascript
const TEAM_FIELD_ID = "customfield_10114"

console.log(`[INFO] Using Team field: ${TEAM_FIELD_ID}`)

// Optional: Validate field is accessible
try {
  const testQuery = `project = AENW AND ${TEAM_FIELD_ID} IS NOT EMPTY`
  const result = await mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql({
    cloudId: "adgear.atlassian.net",
    jql: testQuery,
    fields: ["key", TEAM_FIELD_ID],
    maxResults: 1
  })
  
  if (result.total > 0) {
    console.log(`[SUCCESS] Team field validated - found issues with Team data`)
  } else {
    console.log(`[WARNING] Team field exists but may not contain data`)
  }
} catch (error) {
  console.log(`[WARNING] Cannot validate Team field: ${error.message}`)
}
```

**Team Name Patterns** (for JQL filtering):

Map skill team names to Team field value patterns for filtering:

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
  "Zurek": "Zurek",
  "EP Core": "T - WAW - EP Core",
  "Igni": "AP - WAW - Igni",
  "SRE": "T - WAW - Embedded SREs SRPOL"
}
```

**Note:** These patterns use exact matching (`=` operator in JQL) with the full Jira Team field values. The Team field is an object type that requires exact name matching, not fuzzy text search.

**Rationale**: The original discovery logic via `getJiraIssueTypeMetaWithFields` has proven unreliable in practice. Hardcoding the verified field ID provides stability while validation confirms the field is accessible.

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

3. **Build JQL query with team-specific filtering:**
   
   Use a two-tier query strategy with Team field filtering to accurately capture team-specific active work:
   
   **Primary Query (Sprint-based + Team filter):**
   ```jql
   sprint in openSprints() 
   AND project = {PROJECT_KEY} 
   AND {TEAM_FIELD_ID} = "{TEAM_PATTERN}"
   AND status IN ("In Progress", "Code Review", "In Development") 
   AND issuetype IN (Story, Bug, Task)
   AND issuetype != Sub-task
   ```
   
   **Fallback Query (Project-based + Team filter):**
   If sprint query returns 0 results, try:
   ```jql
   project = {PROJECT_KEY} 
   AND {TEAM_FIELD_ID} = "{TEAM_PATTERN}"
   AND status IN ("In Progress", "Code Review", "In Development") 
   AND issuetype IN (Story, Bug, Task)
   AND issuetype != Sub-task
   ```
   
   **No Team Field Fallback:**
   If Team field unavailable (TEAM_FIELD_ID is null), use project-only filter:
   ```jql
   sprint in openSprints() AND project = {PROJECT_KEY} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)
   ```
   
   **Query Strategy:**
   1. If TEAM_FIELD_ID exists, use team-filtered queries (primary + fallback)
   2. If TEAM_FIELD_ID is null, use project-only queries (old behavior)
   3. Store which query type was successful in metadata
   
   **Why Team Field Works:**
   - Each issue has a Team custom field indicating ownership
   - Team field is an object type with a `name` property containing the full team name
   - Using `=` (exact match) operator with the full Jira team name ensures accurate filtering
   - The Team field values follow patterns like "AE - WAW - Radium", "AP - WAW - Igni", "T - WAW - EP Core", etc.
   - Accurately filters team-specific issues even in shared projects (AENW, RSW, PEPI, PEA)
   
   **Examples:**
   - Radium (AENW project): 
     ```
     sprint in openSprints() AND project = AENW AND customfield_10114 = "AE - WAW - Radium" AND status IN ("In Progress", "Code Review")
     ```
     Returns only issues with Team = "AE - WAW - Radium"
   
   - Igni (ASPW project):
     ```
     sprint in openSprints() AND project = ASPW AND customfield_10114 = "AP - WAW - Igni" AND status IN ("In Progress", "Code Review")
     ```
     Returns only issues with Team = "AP - WAW - Igni"
   
   - EP Core (EPCW project):
     ```
     project = EPCW AND customfield_10114 = "T - WAW - EP Core" AND status IN ("In Progress", "Code Review", "In Development")
     ```
     Returns only issues with Team = "T - WAW - EP Core"
   
   **CRITICAL - Case Sensitivity:** Jira status names are case-sensitive:
   - "In Progress" (capital P)
   - "Code Review" (capital C, capital R)
   - "In Development" (capital D)
   
   **CRITICAL - Issue Type Filter:** Exclude Sub-tasks from analysis:
   - Only analyze parent-level Stories, Bugs, and Tasks
   - Sub-tasks are implementation details and should not be assessed against DoR
   - JQL filter: `issuetype != Sub-task`
   
   **Query Type Tracking:**
   Store in metadata which query succeeded:
   - `"queryType": "sprint+team"` - Sprint + team filter worked
   - `"queryType": "project+team"` - Project + team filter worked
   - `"queryType": "sprint"` - Sprint only (no team filter available)
   - `"queryType": "project"` - Project only (no team filter available)
   - `"queryType": "none"` - All queries returned 0

4. **Execute team-filtered query strategy:**
   
   Get team pattern for current team:
   ```javascript
   const teamPattern = TEAM_NAME_PATTERNS[teamName] || teamName
   ```
   
   **If Team field is available (TEAM_FIELD_ID exists):**
   
   a) First attempt - Sprint-based + Team filter:
      ```javascript
      let jql_primary
      let fields_list
      
      if (TEAM_FIELD_ID) {
        jql_primary = `sprint in openSprints() AND project = ${PROJECT_KEY} AND ${TEAM_FIELD_ID} = "${teamPattern}" AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)`
        fields_list = ["key", "summary", "status", "issuetype", "assignee", "priority", "created", "updated", TEAM_FIELD_ID]
      } else {
        jql_primary = `sprint in openSprints() AND project = ${PROJECT_KEY} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)`
        fields_list = ["key", "summary", "status", "issuetype", "assignee", "priority", "created", "updated"]
      }
      
      result = mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql(
        cloudId: "adgear.atlassian.net",
        jql: jql_primary,
        fields: fields_list,
        maxResults: 100
      )
      ```
   
   b) If result.total == 0, try fallback - Project-based + Team filter:
      ```javascript
      let jql_fallback
      
      if (TEAM_FIELD_ID) {
        jql_fallback = `project = ${PROJECT_KEY} AND ${TEAM_FIELD_ID} = "${teamPattern}" AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)`
      } else {
        jql_fallback = `project = ${PROJECT_KEY} AND status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)`
      }
      
      result = mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql(
        cloudId: "adgear.atlassian.net",
        jql: jql_fallback,
        fields: fields_list,
        maxResults: 100
      )
      ```
   
   c) Track which query succeeded:
      - If primary with team filter returns results: `queryType = "sprint+team"`
      - If fallback with team filter returns results: `queryType = "project+team"`
      - If primary without team filter: `queryType = "sprint"` (field unavailable)
      - If fallback without team filter: `queryType = "project"` (field unavailable)
      - If both return 0: `queryType = "none"`
   
   d) Validate Team field in results (if available):
      ```javascript
      if (TEAM_FIELD_ID && result.total > 0) {
        // Check if Team field values match expected pattern
        const teamFieldValues = result.issues.map(i => i.fields[TEAM_FIELD_ID])
        const matchedIssues = teamFieldValues.filter(v => v && v.name === teamPattern).length
        
        console.log(`  Team field validation: ${matchedIssues}/${result.total} issues match team pattern "${teamPattern}"`)
        
        if (matchedIssues < result.total) {
          console.log(`  [WARNING] ${result.total - matchedIssues} issues don't match team pattern (may be shared/unassigned)`)
        }
      }
      ```
   
   **Note:** maxResults is capped at 100. If more issues exist, results will be truncated.

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
   - Count by status ("In Progress", "Code Review")
   - Count by type (Story, Bug, Task)

6. **Save JSON file:**
   Write to `${OUTPUT_DIR}/[team-name-kebab]-jira.json` where OUTPUT_DIR is the absolute path from Step 4:
   ```json
   {
     "team": "[Team Name]",
     "boardUrl": "[Sprint Board URL]",
     "boardId": "[Board ID]",
     "projectKey": "[Project Key]",
     "extractedAt": "[ISO-8601 timestamp]",
     "teamFieldId": "customfield_10114",
     "query": {
       "jql": "[Successful JQL query used]",
       "queryType": "sprint+team | project+team | sprint | project | none",
       "teamFilterEnabled": true,
       "teamPattern": "AE - WAW - Radium",
       "queryAttempted": {
         "primary": "sprint in openSprints() AND project = AENW AND customfield_10114 = \"AE - WAW - Radium\" ...",
         "fallback": "project = AENW AND customfield_10114 = \"AE - WAW - Radium\" ...",
         "primarySuccess": true
       },
       "statuses": ["In Progress", "Code Review", "In Development"],
       "issueTypes": ["Story", "Bug", "Task"]
     },
     "summary": {
       "total": 15,
       "byStatus": {"In Progress": 10, "Code Review": 5},
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
   Query Strategy: Sprint-based (primary succeeded) | Project-based (fallback used) | No active work

   === ACTIVE ISSUES (In Progress, Code Review) ===

   Summary:
   - Total issues: 15
   - In Progress: 10
   - Code Review: 5

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
     "jiraError": null
   }
   ```
   
   **jiraStatus values:**
   - `"success"` - Issues extracted successfully (even if 0 issues)
   - `"no_board"` - No sprint board URL configured
   - `"parse_error"` - Cannot parse board ID from URL
   - `"access_error"` - Jira API call failed

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

After completing all extraction steps, analyze how well each Jira issue meets its team's DoR criteria and generate a comprehensive Excel report.

**CRITICAL - FIXED REPORT FORMAT:** The Report.xlsx file MUST conform to the exact schema defined below. This format is MANDATORY and MUST NOT be changed, modified, or "improved" between skill executions.

#### Report.xlsx Schema Specification

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
After generating Report.xlsx, verify:
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

#### Step 11.2: Fetch Full Issue Details

For each team to analyze, fetch full issue descriptions (needed for DoR analysis):

```javascript
for (const team of teams_to_analyze) {
  // Read existing Jira data
  const jira_json = Read(`${OUTPUT_DIR}/${team.name_kebab}-jira.json`)
  const jira_data = JSON.parse(jira_json)
  
  console.log(`Fetching details for ${team.name} (${jira_data.issues.length} issues)...`)
  
  // Fetch full details for each issue
  for (const issue of jira_data.issues) {
    const full_issue = await mcp__plugin_atlassian_atlassian__getJiraIssue({
      cloudId: "adgear.atlassian.net",
      issueIdOrKey: issue.key,
      fields: ["description"]
    })
    
    // Extract description (handle both string and ADF format)
    if (full_issue.fields.description) {
      if (typeof full_issue.fields.description === 'string') {
        issue.description = full_issue.fields.description
      } else {
        // ADF format - extract text content
        issue.description = extractTextFromADF(full_issue.fields.description)
      }
    } else {
      issue.description = "(No description provided)"
    }
  }
  
  team.enriched_issues = jira_data.issues
}
```

**Helper function for ADF text extraction:**
```javascript
function extractTextFromADF(adf) {
  if (!adf || !adf.content) return "(No description)"
  
  let text = []
  for (const node of adf.content) {
    if (node.type === 'paragraph' && node.content) {
      for (const inline of node.content) {
        if (inline.type === 'text') {
          text.push(inline.text)
        }
      }
    } else if (node.type === 'bulletList' || node.type === 'orderedList') {
      // Extract list items
      if (node.content) {
        for (const listItem of node.content) {
          if (listItem.content) {
            text.push('- ' + extractTextFromADF({content: listItem.content}))
          }
        }
      }
    }
  }
  
  return text.join('\n').trim() || "(No description)"
}
```

#### Step 11.3: Analyze DoR Compliance (LLM-Based)

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

#### Step 11.5: Generate Excel Report (FIXED SCHEMA)

**CRITICAL:** This report MUST match the schema defined at the beginning of Step 11. Do not deviate from the specification.

**Step 1: Check Python availability:**
```bash
python3 -c "import openpyxl; print('OK')" 2>/dev/null
```

**Step 2: Create Python script** (if Python available):

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
python3 generate_report.py '${JSON.stringify(report_data)}' '${JSON.stringify(summary_data)}' 'Report.xlsx'
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

- **Report.xlsx** (or Report.csv) - Full compliance report
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

**Report Location:** \`${OUTPUT_DIR}/Report.xlsx\`
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
  report_file: python_available ? "Report.xlsx" : "Report.csv",
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

Report saved to: ${OUTPUT_DIR}/Report.xlsx

Summary saved to: ${OUTPUT_DIR}/DOR_ANALYSIS_SUMMARY.md

Teams skipped (no DoR criteria): ${teams_without_dor.length}
${teams_without_dor.map(t => `  - ${t.name}`).join('\n')}

Most common gaps:
${getTopGaps(teams_analyzed, 3).map((gap, i) => 
  `  ${i+1}. ${gap.criteria} (${gap.count} issues)`
).join('\n')}

Next steps:
  1. Open Report.xlsx to review detailed findings
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

## Error Handling

- **Continue on error:** If one team page fails, continue with remaining teams
- **Track failures:** Record all errors in teams.json metadata
- **Detailed logging:** Include error messages in per-team TXT files
- **Graceful degradation:** Partial data is better than no data
- **Team field unavailable:** If Team custom field cannot be discovered, proceed with project-level queries but log warning about potential cross-team issues in shared projects (AENW, RSW, PEPI, PEA)
- **Team pattern mismatch:** If fetched issues don't match team pattern, log warning but include issues in results (may indicate unassigned/shared issues)

**Automation Rules:**
- **Only stop for critical failures:** Continue execution through all 11 steps unless:
  - Authentication fails completely (Step 2)
  - No teams found in source page (Step 5)
  - Output directory cannot be created (Step 4)
- **Do not stop for partial failures:** If some teams fail, continue with successful teams
- **Automatic Step 11:** Execute Step 11 (DoR analysis) automatically after Step 10, even if Step 11 has no explicit user request

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

11. **Team Field Filtering (for shared projects):**
   - Use hardcoded Team custom field ID: `customfield_10114`
   - Add Team field filter to JQL queries: `customfield_10114 = "Full Jira Team Name"`
   - Use exact matching (`=` operator) with the full Jira team name from TEAM_NAME_PATTERNS
   - The Team field is an object type that requires exact name matching, not fuzzy text search
   - If Team field filter returns 0, fall back to project-level queries with warning
   - Include Team field in query results for verification
   - Validate that returned issues match expected team pattern

12. **Report.xlsx Fixed Schema:**
   - EXACTLY 2 sheets: "Summary" (first) and "DoR Compliance" (second)
   - Summary sheet: KPI section (rows 1-2: "% Teams with DoR: X%", "% Jira Tasks fitting DoR: Y%") + table with 4 columns (Team, DoR, Jira Tasks in progress, % Tasks fitting DoR) starting at row 4 - lists ALL teams
   - DoR Compliance sheet: 9 columns (Team, Issue Key, Issue Type, URL, Title, Status, Assignee, DoR Compliance, Note)
   - DoR Compliance values: "Pass" (green) or "Fail" (red) ONLY
   - Note column: Empty for "Pass", explanation for "Fail"
   - No additional sheets beyond these two, no additional columns or summary rows
   - Format specification in Step 11 is MANDATORY and immutable
