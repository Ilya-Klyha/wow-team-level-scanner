---
name: wow-team-backlog-readiness
description: >
  Extract SRPOL team data, DoR criteria, backlog items, velocity, and sprint runway from Jira.
  Detects Stories, Bugs, and Tasks in each team's backlog, checks Story Points estimation,
  assesses DoR compliance via deterministic heuristics, calculates team velocity and sprint runway.
  Generates Report-backlog.xlsx (2 sheets) and Report-backlog.html.
  Requires Atlassian MCP. Usage: /wow-team-backlog-readiness
---

# WoW Team Backlog Readiness Skill v3.0

Extracts team information from the SRPOL Teams Confluence page, queries each team's Jira backlog for unsprinted items (Stories, Bugs, Tasks), checks Story Points estimation, evaluates DoR compliance via deterministic heuristic field checks, calculates team velocity from the last 3 closed sprints, and computes sprint runway. Generates a fixed-schema Excel report (2 sheets), HTML dashboard, and supporting data files.

## Usage

```
/wow-team-backlog-readiness
```

No parameters required. The skill automatically scans the SRPOL Teams page at:
https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams

## What It Does

1. Checks Atlassian MCP authentication
2. Extracts from Confluence:
   - Team page links and sprint board links from directory table
   - Team names from actual Confluence page titles (cleaned)
   - DoR (Definition of Ready) criteria from each team's page
3. Extracts from Jira:
   - Backlog items per team (Stories, Bugs, Tasks not in any active/future sprint)
   - Story Points field value for each item
   - Descriptions for DoR compliance checking
   - Velocity from last 3 closed sprints (sprint field: customfield_10115, name-filtered per team, discovery window: 12w)
4. Analyzes:
   - DoR compliance via heuristic field checks (deterministic, reproducible)
   - Sprint runway per team (dor_ready_sp / velocity_avg)
5. Generates Reports:
   - Excel report: `Report-backlog.xlsx` (2 sheets: "Backlog Readiness" + "Velocity & Runway")
   - HTML dashboard: `Report-backlog.html` (self-contained visual report)
6. Saves all data to: `C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\<timestamp>/`

## Instructions

**CRITICAL - FULL AUTOMATION:** This skill must execute all steps automatically without pausing or asking for user confirmation. Only stop execution if:
- Authentication fails (Step 2)
- Critical errors occur that prevent continuation
- Prerequisites are missing (e.g., no teams found)

Do NOT pause between steps to ask for approval.

### Execution Constraints - Shell and Python

**RULE: Python scripts longer than 5 lines MUST be written to files before execution.**

When the Python code to execute is more than 5 lines OR contains any quote characters:
1. Use the Write tool to save the script to `${OUTPUT_DIR}/[descriptive_name].py`
2. Execute with Bash: `cd "${OUTPUT_DIR}" && python3 [descriptive_name].py`

**This rule applies to ALL steps. When in doubt, write to a file.**

### Execution Model - Sequential with Parallel MCP Calls

This skill executes entirely in the main session. No background agents are spawned.

**Architecture:**
1. MCP calls for data fetching (use parallel tool calls where independent)
2. Save large API responses to files (they auto-save when exceeding inline limits)
3. Python scripts for all data processing, filtering, and calculation
4. Python scripts for report generation

```
+------------------------------------------------------------------------+
| ANTI-PATTERN: DO NOT delegate to Agent tool.                            |
|                                                                         |
| If context feels large after MCP batch responses:                       |
| 1. Write a Python script that extracts needed fields from responses     |
| 2. Execute the script to save extracted data to OUTPUT_DIR              |
| 3. Continue in main session - the raw responses will be forgotten       |
|    naturally as conversation progresses                                  |
|                                                                         |
| NEVER launch Agent() as a "fresh context" workaround.                   |
| Main waiting for agent = pure overhead with zero benefit.               |
+------------------------------------------------------------------------+
```

**Parallel MCP calls:** When multiple independent API queries are needed (e.g., 11 project backlog queries), issue them as multiple tool uses in a single message. The harness executes them concurrently. This provides the same parallelism as agents without the token overhead.

**Batching strategy:**
- Batch up to 5-7 MCP calls per message (more causes response truncation issues)
- For 11 projects: 2 messages of 5-6 calls each
- For 15 team pages: 3 messages of 5 calls each
- Pagination calls: batch all same-page-number calls together

**Python processing rule:** All data filtering, team assignment, velocity calculation, DoR extraction, compliance scoring, and report generation MUST be done via Python scripts written to OUTPUT_DIR and executed with Bash. Never process large datasets (>10 items) inline in the conversation.

**Context window management:** After each MCP batch response, immediately save results to files via a Python script. Do NOT accumulate raw API responses across multiple batches in conversation context. The Python processing scripts read from files, not from conversation history. This prevents context window exhaustion during large scans.

**Progress reporting:** After completing each major phase (team page fetches, backlog queries, velocity queries, DoR compliance), output a progress line:
```
[PROGRESS] Phase: <phase name> (<N>/<total> complete)
```

**Bash error resilience:** If a Bash call fails with exit code 5 and the error contains "add_item", retry once after `sleep 3`. This is a rare Windows MSYS2 edge case that only occurs under unusual system load.

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

Then try the /wow-team-backlog-readiness command again.
```

If tools found, attempt a test call:
```
mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources()
```

If this fails, show authentication error and stop.

### Step 3: Calculate CET Timestamp

Calculate the current timestamp in CET (Central European Time):
- Get current UTC time using Bash: `date -u +"%Y-%m-%d %H:%M:%S"`
- Convert to CET (UTC+1 standard Nov-Mar, UTC+2 DST Mar-Nov)
- Format as: `YYYYMMDD HH-MM`
- Store this timestamp for use in all file operations

**CET Conversion:**
- Standard time (Nov-Mar): UTC + 1 hour
- Daylight saving (Mar-Nov): UTC + 2 hours

### Step 4: Prepare Output Folder

Create the timestamped output directory using absolute path:
```bash
mkdir -p "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]"
```

**CRITICAL:** Store the full absolute path in a variable for all subsequent file operations:
```
OUTPUT_DIR = "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\[CET_TIMESTAMP]"
```

All subsequent file Write operations must use: `${OUTPUT_DIR}/[filename]`.

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
4. Build 15 entries (skip the template/header row if present)

**MULTI-LINK DISAMBIGUATION RULE:**

When a table cell in column 1 (SRPOL Ads Team) contains MULTIPLE `<a>` elements:

1. Filter to ONLY links matching Confluence wiki page URL patterns:
   - Tiny links: URL contains `/wiki/x/[ID]`
   - Full page URLs: URL contains `/wiki/spaces/.../pages/[NUMERIC_ID]`
   - Exclude: Jira links, external links, anchors, non-wiki URLs.

2. From the filtered list, select the FIRST link by DOM/HTML order.
   - Position in HTML is the ONLY selector.
   - Do NOT prefer links based on label text.
   - Do NOT prefer links based on URL format.
   - Inline card links (`data-card-appearance="inline"`) with no visible text ARE valid.

3. Extract page ID from the selected URL:
   - `/wiki/x/[ID]` -> use ID portion directly as pageId
   - `/wiki/spaces/.../pages/[NUMERIC_ID]` -> use NUMERIC_ID as pageId

Build a list of team page references (WITHOUT names yet):
```javascript
[
  {
    pageLink: "https://adgear.atlassian.net/wiki/x/WID6RQU",
    sprintBoardLink: "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
    pageId: "WID6RQU"
  }
]
```

### Step 7: Fetch Team Names and Page Content

For each team, fetch the Confluence page to get the actual title AND store the full page HTML body for DoR extraction in Step 9A:

```
mcp__plugin_atlassian_atlassian__getConfluencePage(
  cloudId: "adgear.atlassian.net",
  pageId: [team.pageId],
  contentFormat: "html"
)
```

Store the full response (title + HTML body) for each team.

Clean the page title:
- Get title from response
- Remove (case-insensitive): "Team Page", "Team Space", "Team" (standalone word), "Space" (at end)
- For "XX - YYY - Name" patterns (e.g., "PE - WAW - Abyss"): extract ONLY the last segment after final " - "
- Normalize spaces and hyphens
- Examples:
  - "Radium Team Space" -> "Radium"
  - "PE - WAW - Abyss" -> "Abyss"
  - "Team Europium" -> "Europium"

**CONTEXT CHECKPOINT after Step 7:**
At this point, N team page HTML bodies have been fetched (where N = number of teams
found in Step 6). This is the largest context accumulation point in the entire skill.

DO NOT delegate remaining work to agents. This is the expected behavior:
1. The HTML content is NEEDED in subsequent steps (Step 8 extracts board metadata
   from URLs already in context, Step 9A extracts DoR sections from the HTML)
2. After each processing step, write results to files via Python scripts
3. Raw HTML leaves context naturally as new MCP responses push it out of the window
4. If context pressure is felt, offload intermediate results to disk -
   NEVER spawn Agent() as a "fresh context" workaround

The pattern "context feels large -> launch Agent" is ALWAYS wrong here.
The pattern "context feels large -> offload to files, continue in main" is ALWAYS correct.

### Step 8: Extract Board Metadata

From each team's sprint board URL, extract:

```
URL format: https://adgear.atlassian.net/jira/software/c/projects/[PROJECT]/boards/[BOARD_ID]

Board ID: /boards/(\d+) -> e.g., "8979"
Project Key: /projects/([A-Z]+)/ -> e.g., "AENW"
```

If board ID cannot be extracted, mark team as `"status": "parse_error"` and skip.
If no sprint board URL, mark team as `"status": "no_board"` and skip.

### Step 8B: Build Dynamic Team-to-Project Mapping

Derive the team-to-project mapping from the board metadata extracted in Step 8.

**Rule: One team = one project.** Each team maps to exactly one Jira project, determined
by the project key extracted from their sprint board URL. A team NEVER spans multiple
projects for backlog query purposes.

```javascript
// Build PROJECT_TEAMS dynamically from board URLs parsed in Step 8
const PROJECT_TEAMS = {}

for (const team of teams) {
  if (!team.project_key) {
    console.log(`[WARNING] Team ${getDisplayName(team.name)}: no project key (status: ${team.status}), excluded from backlog scan`)
    continue
  }

  if (!PROJECT_TEAMS[team.project_key]) {
    PROJECT_TEAMS[team.project_key] = []
  }
  PROJECT_TEAMS[team.project_key].push(team.name)
}

// Log the derived mapping for transparency and debugging
console.log(`[INFO] Dynamic PROJECT_TEAMS mapping (${Object.keys(PROJECT_TEAMS).length} projects, ${teams.filter(t => t.project_key).length} teams):`)
for (const [project, teamNames] of Object.entries(PROJECT_TEAMS).sort()) {
  console.log(`  ${project}: [${teamNames.map(n => getDisplayName(n)).join(", ")}]`)
}
```

**Validation after building:**
- Each team name appears in exactly ONE project entry (enforced by single board URL per team)
- Teams with `status === "no_board"` or `status === "parse_error"` are excluded with a warning
- The mapping is logged to console so discrepancies are visible during review

**Why dynamic:** The SRPOL Teams page is maintained by team leads and can change at any time.
A team might move to a new project, a new team might be added, or a board URL might be updated.
Dynamic extraction ensures the scan always reflects the current state without requiring
manual skill spec maintenance.

### Step 9: Query Backlog Items Per Project

**Goal:** Fetch all backlog items (Stories, Bugs, Tasks) for each project, then assign to teams via client-side filtering.

#### Step 9.0: Configuration

**DISPLAY_NAMES mapping:**

```javascript
const DISPLAY_NAMES = {
  "Polonium UF": "Polonium"
  // All other teams: display_name = internal_name
}

function getDisplayName(name) {
  return DISPLAY_NAMES[name] || name
}
```

All output files, reports, and console output use display names via `getDisplayName()`.
Internal filtering still uses the internal name (e.g., "Polonium UF" for TEAM_NAME_PATTERNS lookup).

**Team Custom Field:** `customfield_10114` (Jira Team-type field)

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

**Project-to-Teams Mapping (DYNAMIC):**

`PROJECT_TEAMS` is NOT hardcoded. It is built dynamically in Step 8B from the sprint board URLs
extracted from the SRPOL Teams page. This ensures the mapping always reflects the current state
of team assignments without requiring manual skill spec updates.

**TEAM-TO-PROJECT RULE:** Each team maps to exactly ONE Jira project, derived from their sprint
board URL on the SRPOL Teams page. The deduplication step in Phase 4 is retained as a safety net
but should not trigger under normal circumstances. If it does trigger (duplicate issue_keys found),
this indicates an unexpected board configuration and should be logged as a warning.

**What is dynamic vs. hardcoded:**
- `PROJECT_TEAMS` (which project to query for which team): DYNAMIC, built in Step 8B from board URLs
- `TEAM_NAME_PATTERNS` (Jira Team field values for client-side filtering): HARDCODED, these are
  Jira-administered team identifiers that change rarely. If a team's Jira Team field name changes,
  update this mapping manually.
- `DISPLAY_NAMES` (output display names): HARDCODED

**Team Name Patterns** (for client-side exact matching):

```javascript
const TEAM_NAME_PATTERNS = {
  "Abyss": "PE - WAW - Abyss",
  "Radium": "AE - WAW - Radium",
  "Europium": "AP - WAW - Europium",
  "Copernicium": "AE - WAW - Copernicium",
  "Mouflons": "AS - WAW - Mouflons",
  "Wolves": "AS - WAW - Wolves",
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

**Orphan Detection:**

During RSW project scanning, if any issues match `customfield_10114.name === "Polonium"` (exact string, not "AS - WAW - Polonium UF"), log a warning and exclude them:
```
[WARNING] Project RSW: Found N issues with team field "Polonium" (orphan - excluded from all teams)
```

These issues belong to the removed "Polonium LF" team and must not be counted toward any team.

#### Step 9.1: JQL for Backlog Items

**Primary JQL Template:**
```jql
project = {PROJECT_KEY}
AND (sprint is EMPTY OR (sprint NOT IN openSprints() AND sprint NOT IN futureSprints()))
AND issuetype IN (Story, Bug, Task)
AND issuetype != Sub-task
AND statusCategory != Done
```

**Explanation of JQL clauses:**
- `sprint is EMPTY` - items never assigned to any sprint
- `sprint NOT IN openSprints() AND sprint NOT IN futureSprints()` - items rolled back from closed sprints (not in any active/future sprint)
- Combined with OR: captures the FULL backlog as shown in the board's backlog view
- `issuetype IN (Story, Bug, Task)` - only these three types
- `issuetype != Sub-task` - exclude sub-tasks
- `statusCategory != Done` - exclude completed items

**NOTE ON sprint FUNCTIONS:**
The wow-dor-scanner bans `sprint in openSprints()` because it caused data loss when FINDING active work (issues can be "In Progress" without a sprint). Here the semantics are INVERTED: we are EXCLUDING sprinted items from the backlog result set. The documented bug does not apply to this use case. This JQL correctly identifies the same set of issues that Jira's backlog view displays.

**Fallback JQL (if primary fails):**
```jql
project = {PROJECT_KEY}
AND sprint is EMPTY
AND issuetype IN (Story, Bug, Task)
AND issuetype != Sub-task
AND statusCategory != Done
```

If the primary JQL throws an error on the first page (e.g., `openSprints()` not supported), fall back to this simpler query and log:
```
[WARNING] Project {KEY}: sprint functions not supported, falling back to 'sprint is EMPTY' only.
Some rolled-over items may be missed.
```

#### Step 9.2: Story Points Field

The Story Points field is **`customfield_10200`**. This was verified empirically against the Jira instance (e.g., MAW-437 has value 13 in this field).

**Fields to request in every backlog query:**
```
fields: ["key", "summary", "status", "issuetype", "assignee", "customfield_10114", "customfield_10200"]
```

**Story Points extraction:**
```javascript
const STORY_POINTS_FIELD = "customfield_10200"

// For each issue:
// issue.fields.customfield_10200 -> numeric value or null
```

No auto-discovery is needed. The field is fixed.

#### Step 9.3: Execute Queries with Pagination and Client-Side Filtering

**CRITICAL - PAGINATION IS MANDATORY:**

The LLM executing this step MUST paginate all project queries to completion. The Jira
API returns max 100 issues per call. Projects commonly have 100-300+ backlog items.

Execution model (sequential, main session only):

  Phase 1 - Initial fetch (parallel MCP calls, batched 5-6 per message):
    Issue searchJiraIssuesUsingJql for each project (maxResults=100, no nextPageToken).
    Batch 5-6 calls per message as parallel tool uses.

  Phase 2 - Pagination (for each project where hasNextPage=true):
    Loop:
      - Read `endCursor` from the previous response at `result.issues.pageInfo.endCursor`
      - Call searchJiraIssuesUsingJql with `nextPageToken=endCursor`
      - Append new `result.issues.nodes` (array) to the accumulated array for that project
      - Check new response's `result.issues.pageInfo.hasNextPage` field
    Until: hasNextPage=false OR endCursor is null OR page count reaches 10

    Pagination for DIFFERENT projects MAY be batched in the same message.
    Pagination for the SAME project MUST be sequential (each call needs prior cursor).

    Context offloading: After each batch of responses, immediately write a Python
    script to extract needed fields and save to disk. Do NOT hold raw API responses
    in conversation context across multiple batches.

  Phase 3 - Process results via Python:
    After all pagination is complete, run Python processing scripts via Bash.
    Python scripts read from saved files on disk, not conversation context.

Defensive rules:
  - If hasNextPage=true but endCursor is null or empty -> STOP pagination for that
    project, log: "[WARNING] Project {KEY}: endCursor null despite hasNextPage=true"
  - Cap at 10 pages (1000 issues) per project to prevent runaway loops
  - If a pagination call fails mid-stream, keep issues already fetched (partial > none)
  - Log page count per project after completion:
    "[INFO] Project {KEY}: {N} backlog issues ({P} pages){fallback_note}"

**API Response Structure:**
```json
{
  "issues": {
    "nodes": [ ...issue objects... ],
    "pageInfo": {
      "hasNextPage": true,
      "endCursor": "Ch0jU3Ry..."
    }
  }
}
```
- `issues.nodes`: array of issue objects (nested under `issues.nodes`, NOT a flat top-level array).
- `issues.pageInfo.hasNextPage`: boolean. `true` = more pages exist. `false` = this is the last page. NOTE: this is INVERTED logic compared to the old `isLast`.
- `issues.pageInfo.endCursor`: string cursor to pass as the `nextPageToken` parameter for the next API call. Null or absent on the last page.

To get next page: pass `result.issues.pageInfo.endCursor` value as the `nextPageToken` parameter in the next `searchJiraIssuesUsingJql` call.
Stop when `result.issues.pageInfo.hasNextPage` is `false` OR `result.issues.pageInfo.endCursor` is null/missing.

**IMPORTANT:** The request parameter name remains `nextPageToken`. Only the response field path differs (`issues.pageInfo.endCursor`). This applies identically to all `searchResultMode` values ("issues", "count", "all").

For each UNIQUE project key in PROJECT_TEAMS:

```javascript
// Phase 0: Initialize accumulators for all teams before any project queries
for (const team of teams) {
  team.backlogIssues = []
  team.status = "pending"
}

for (const [projectKey, teamNames] of Object.entries(PROJECT_TEAMS)) {
  let jql = `project = ${projectKey} AND (sprint is EMPTY OR (sprint NOT IN openSprints() AND sprint NOT IN futureSprints())) AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task AND statusCategory != Done`

  let allProjectIssues = []
  let nextPageToken = null
  let pageCount = 0
  let usedFallback = false

  do {
    try {
      const result = mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql(
        cloudId: "adgear.atlassian.net",
        jql: jql,
        fields: ["key", "summary", "status", "issuetype", "assignee", "customfield_10114", "customfield_10200"],
        maxResults: 100,
        nextPageToken: nextPageToken
      )

      // Response structure: result.issues.nodes (array), result.issues.pageInfo.hasNextPage (bool), result.issues.pageInfo.endCursor (string|null)
      allProjectIssues = allProjectIssues.concat(result.issues.nodes)
      nextPageToken = (result.issues.pageInfo.hasNextPage && result.issues.pageInfo.endCursor)
        ? result.issues.pageInfo.endCursor
        : null
      pageCount++

    } catch (error) {
      if (pageCount === 0 && !usedFallback) {
        console.log(`[WARNING] Project ${projectKey}: Primary JQL failed, using fallback`)
        usedFallback = true
        jql = `project = ${projectKey} AND sprint is EMPTY AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task AND statusCategory != Done`
        continue
      }
      console.log(`[ERROR] Project ${projectKey}: ${error.message}`)
      break
    }

    // Cap at 10 pages (1000 issues)
    if (pageCount >= 10) {
      console.log(`[WARNING] Project ${projectKey}: capped at 1000 issues`)
      break
    }
  } while (nextPageToken !== null)

  console.log(`[INFO] Project ${projectKey}: ${allProjectIssues.length} backlog issues (${pageCount} pages)${usedFallback ? ' [FALLBACK]' : ''}`)

  // Orphan detection for RSW project
  if (projectKey === "RSW") {
    const orphans = allProjectIssues.filter(issue => {
      const teamField = issue.fields?.customfield_10114
      return teamField && teamField.name === "Polonium"  // exact match - old removed team
    })
    if (orphans.length > 0) {
      console.log(`[WARNING] Project RSW: Found ${orphans.length} issues with team field "Polonium" (orphan - excluded from all teams)`)
    }
  }

  // Client-side team assignment
  for (const teamName of teamNames) {
    const teamPattern = TEAM_NAME_PATTERNS[teamName]

    const teamIssues = allProjectIssues.filter(issue => {
      const teamField = issue.fields?.customfield_10114
      if (!teamField || !teamField.name) return false
      return teamField.name === teamPattern  // EXACT match
    })

    console.log(`  ${getDisplayName(teamName)}: +${teamIssues.length} from ${projectKey}`)

    // Extract data per issue
    const processedIssues = teamIssues.map(issue => ({
      team: getDisplayName(teamName),
      issue_key: issue.key,
      issue_type: issue.fields.issuetype.name,
      url: `https://adgear.atlassian.net/browse/${issue.key}`,
      title: issue.fields.summary,
      status: issue.fields.status.name,
      assignee: issue.fields.assignee?.displayName || "Unassigned",
      story_points: issue.fields.customfield_10200 ?? null
    }))

    // Assign results to team
    team.backlogIssues = team.backlogIssues.concat(processedIssues)
    team.usedFallback = team.usedFallback || usedFallback
    team.status = "success"
  }
}

// === PHASE 4: DEDUPLICATION (SAFETY NET) AND FINAL COUNTS ===
// Under normal operation with one-team-one-project rule, no duplicates should exist.
// This step is retained as a defensive guard against unexpected board configurations
// (e.g., a cross-project board filter) or edge cases during team migrations.
for (const team of teams) {
  if (team.status === "success" && team.backlogIssues.length > 0) {
    const beforeCount = team.backlogIssues.length
    const seen = new Set()
    team.backlogIssues = team.backlogIssues.filter(issue => {
      if (seen.has(issue.issue_key)) return false
      seen.add(issue.issue_key)
      return true
    })
    const dupes = beforeCount - team.backlogIssues.length
    if (dupes > 0) {
      console.log(`[WARNING] ${getDisplayName(team.name)}: ${dupes} duplicate issue_keys removed (unexpected)`)
    }
  }
  // Calculate final counts ONLY here (never inside the per-project loop)
  if (team.status === "success") {
    team.backlogTotal = team.backlogIssues.length
    team.estimated = team.backlogIssues.filter(i => i.story_points !== null && i.story_points !== undefined).length
    team.unestimated = team.backlogTotal - team.estimated
  }
}

// Log final counts
console.log(`[INFO] Final backlog counts:`)
for (const team of teams) {
  if (team.status === "success") {
    console.log(`  ${getDisplayName(team.name)}: ${team.backlogTotal} items`)
  }
}
```

**CRITICAL RULES:**
- `backlogTotal`, `estimated`, `unestimated` MUST ONLY be set in the final dedup block (Phase 4)
- They must NOT be set inside the per-project loop (would be overwritten by next project)
- Each team maps to exactly ONE project (one-team-one-project rule from Step 8B)
- Deduplication is a safety net -- if it triggers, log a warning (indicates unexpected state)
- The per-project console.log reports incremental finds (`+N from PROJECT`), not final totals

#### Step 9.4: Validation After All Queries

```javascript
// 1. JQL compliance - verify no customfield_10114 in any executed JQL
console.log(`[INFO] Cross-team contamination: impossible by design (exact name match)`)

// 2. Pattern mismatch warnings
for (const team of teams) {
  if (team.backlogTotal === 0 && team.status === "success") {
    console.log(`[INFO] ${getDisplayName(team.name)}: 0 backlog items (may be normal - all work in sprint)`)
  }
}

// 3. Totals
const totalBacklog = teams.reduce((sum, t) => sum + (t.backlogTotal || 0), 0)
console.log(`[INFO] Total backlog items: ${totalBacklog}`)
console.log(`[INFO] Story Points field: customfield_10200`)

if (totalBacklog < 20) {
  console.log(`[WARNING] Only ${totalBacklog} items found. Verify JQL captures full backlog.`)
}
```

### Step 9A: Extract DoR Per Team

For each team, using the page HTML already fetched in Step 7:

#### 9A.1: Locate DoR Section

Search for DoR headings (h1-h4, case-insensitive **substring** matching) in the team page HTML. A heading matches if its text contains ANY of these patterns as a substring:
- "DEFINITION OF READY (DoR) - STORY/TASK"
- "DEFINITION OF READY (DoR) - STORY"
- "Definition of Ready (DoR) - STORY/TASK"
- "DEFINITION OF READY (DoR)"
- "Definition of Ready"
- "Team DoR"
- "DoR story/task"
- "DoR"

**EXCLUSION RULE (applied BEFORE inclusion):** EXCLUDE any heading where the full heading text contains "OFFERING" or "EPIC" (case-insensitive). A heading like "Definition of Ready (DoR) - OFFERING/EPIC" is excluded even though it contains "Definition of Ready". These are different DoR types not relevant to story/task readiness.

**Match order:** Select the FIRST qualifying heading in DOM order (first match wins).

**REGRESSION GUARD:** Teams where no DoR heading exists anywhere on the team page (such as SRE) must continue to produce `dor_found: false` and `runway_status: "No DoR"`. The link-following and parsing changes below do NOT affect the "no heading found" path.

#### 9A.2: Follow Links If Needed

After finding the DoR section heading, look for links (`<a href="...">`) within the content of that DoR section (between the DoR heading and the next heading of equal or higher level).

Check if the link URL or link text contains ANY of these DoR-related keywords (case-insensitive):
- "DoR"
- "Definition of Ready"
- "Story"
- "Task"
- "Ready"
- "DoD"

**If one or more such links are found:**
- Select the FIRST matching link by DOM order
- Extract the page ID from the link URL using these patterns:
  - `/wiki/spaces/[SPACE]/pages/[NUMERIC_ID]/...` -> use NUMERIC_ID
  - `/pages/[NUMERIC_ID]/...` -> use NUMERIC_ID
  - `/wiki/x/[TINY_ID]` -> use TINY_ID directly as pageId
  - Inline card links (`data-card-appearance="inline"`) with href matching the above patterns are also valid
- Only follow links whose URL contains `/wiki/` (skip external URLs, Jira links, anchor-only links)
- Fetch the linked page using `getConfluencePage(cloudId: "adgear.atlassian.net", pageId, contentFormat: "html")`
- Search for DoR section in the linked page using the same heading patterns and exclusion rules as Step 9A.1
- If DoR content is found on linked page: extract criteria from linked page INSTEAD of the original section content
- If NO DoR section exists on linked page: fall back to extracting criteria from the original section content on the team page
- Max 1 hop -- do NOT follow links found on the linked page

**If NO links with DoR keywords are found in the section:**
- Continue to Step 9A.3 with the original section content

**ERROR HANDLING for link fetch:**
- If `getConfluencePage` fails (API error, 404, permission denied): log the error and fall back to extracting from the original section content. Do NOT mark the team as `dor_found: false` solely due to a link fetch failure.

**BUG PREVENTION:**
- Never follow links found outside the DoR section boundaries (e.g., in "Links", "References", "Team Ceremonies" sections)
- Only links within the actual DoR section content (between the matched heading and the next heading of equal/higher level) are valid candidates

#### 9A.3: Extract Criteria

Extract criteria from the DoR section content:

**From HTML tables:**
- First `<td>` = criterion name
- Second `<td>` = criterion description
- Skip header rows (`<th>`)

**From bullet lists (`<ul>`/`<ol>`):**
- Split each `<li>` on ":" - left part is name, right part is description
- If no ":" found, entire text is both name and description

#### 9A.4: Assign check_type

For each criterion, assign a check_type via keyword matching:

```javascript
function assignCheckType(criterionName) {
  const name = criterionName.toLowerCase()
  if (name.includes("estimate") || name.includes("story point")) return "ESTIMATE"
  if (name.includes("acceptance") || name.includes("criteria") || name.includes("measurement")) return "ACCEPTANCE_CRITERIA"
  if (name.includes("dependenc")) return "DEPENDENCIES"
  if (name.includes("clarity") || name.includes("description") || name.includes("requirement") || name.includes("user story")) return "DESCRIPTION_QUALITY"
  if (name.includes("design") || name.includes("ux") || name.includes("figma") || name.includes("mockup")) return "DESIGN"
  if (name.includes("monitor") || name.includes("alert")) return "MONITORING"
  if (name.includes("priority") || name.includes("prioriti")) return "PRIORITY"
  if (name.includes("scope") || name.includes("fit") || name.includes("size")) return "SCOPE"
  return "GENERIC"
}
```

#### 9A.5: Determine dor_found (Three-Tier Logic)

Determine `dor_found` using a three-tier evaluation:

**TIER 1 -- CRITERIA PARSED (preferred):**
- `dor_found = true`
- Condition: At least 1 criterion was successfully extracted (table row or bullet item) from either the team page or a linked page (Steps 9A.2 + 9A.3)
- `dor_source` = `"team_page"` if criteria found directly on team page, `"linked_page"` if criteria found on a page reached via link-following
- `dor_criteria` = array of extracted criteria objects
- `checkable_criteria_count` = criteria where check_type != "GENERIC"
- `total_criteria_count` = all criteria extracted

**TIER 2 -- HEADING FOUND, NO PARSEABLE CRITERIA:**
- `dor_found = true`
- Condition: A DoR heading was found (Step 9A.1 matched) AND either:
  - (a) A DoR-keyword link was found in the section (regardless of whether the linked page yielded parseable criteria), OR
  - (b) The section contains meaningful content -- defined as: after stripping ALL HTML tags, collapsing whitespace, and removing text that is solely a URL, there remain visible text characters
- `dor_source` = `"team_page"` or `"linked_page"` (whichever was the attempted source)
- `dor_criteria` = `[]` (empty array)
- `checkable_criteria_count` = 0
- `total_criteria_count` = 0

**TIER 3 -- NO HEADING FOUND:**
- `dor_found = false`
- Condition: No DoR heading matched in Step 9A.1 on the team page
- `dor_source` = `"not_found"`
- `dor_criteria` = `[]`
- `checkable_criteria_count` = 0
- `total_criteria_count` = 0

#### 9A.6: Save DoR Criteria

Save to `${OUTPUT_DIR}/dor_criteria.json`:

```json
[
  {
    "team": "Europium",
    "dor_criteria": [
      {
        "name": "Story Points estimated",
        "description": "Each story must have story points assigned before sprint planning",
        "check_type": "ESTIMATE"
      },
      {
        "name": "Acceptance Criteria defined",
        "description": "Clear AC with given/when/then format",
        "check_type": "ACCEPTANCE_CRITERIA"
      }
    ],
    "dor_source": "team_page | linked_page | not_found",
    "dor_found": true,
    "checkable_criteria_count": 4,
    "total_criteria_count": 6
  }
]
```

**Rules:**
- Array of 15 team objects, sorted alphabetically by display name
- `"team"` uses display names (getDisplayName applied)
- `checkable_criteria_count` = criteria where check_type != "GENERIC"
- `total_criteria_count` = all criteria found
- `dor_found`: determined by the three-tier logic in Step 9A.5 above
- `dor_source`: "team_page" if found on team page directly, "linked_page" if followed a link, "not_found" if no DoR heading detected (Tier 3)
- Teams with Tier 2 status have `dor_found: true`, `dor_criteria: []`, `checkable_criteria_count: 0`, `total_criteria_count: 0`

### Step 9B: DoR Compliance via Heuristic Checks

**CRITICAL: This step uses DETERMINISTIC heuristic field checks ONLY. No LLM evaluation. Results must be identical across runs on the same data.**

**TIER 2 SKIP RULE:** For teams where `dor_found=true` BUT `checkable_criteria_count=0` (Tier 2 -- DoR exists but no criteria could be parsed for heuristic checking): SKIP compliance assessment entirely for this team. Do not fetch descriptions, do not run checks. These teams will have:
- `dor_ready_count` = null
- `dor_ready_sp` = null
- `dor_avg_compliance_pct` = null

Only teams with `dor_found=true` AND `checkable_criteria_count > 0` (Tier 1) proceed through Steps 9B.1-9B.4.

#### 9B.1: Description Fetch Strategy

After the bulk backlog query (Step 9.3), for Tier 1 teams (where `dor_found=true` AND `checkable_criteria_count > 0`), fetch descriptions of estimated issues in batches of 20:

```jql
key in (AENW-123, AENW-456, ...)
```

Fields: `["description", "issuelinks"]`

Only fetch for issues that have story_points != null (estimated issues are the primary candidates for DoR readiness).

#### 9B.2: Heuristic Check Definitions

Each check_type maps to a deterministic field-presence check:

| check_type | Passes when |
|---|---|
| ESTIMATE | `story_points != null` |
| ACCEPTANCE_CRITERIA | description contains (case-insensitive): "acceptance criteria" OR "ac:" OR "given " OR "expected result" OR has checkbox lists (`[ ]` or `[x]`) |
| DEPENDENCIES | `issuelinks` array is non-empty OR description mentions (case-insensitive): "depend" OR "blocked by" OR "requires" |
| DESCRIPTION_QUALITY | description length >= 100 characters |
| DESIGN | description mentions (case-insensitive): "figma" OR "mockup" OR "design" OR "wireframe" OR "prototype" |
| MONITORING | description mentions (case-insensitive): "monitor" OR "alert" OR "dashboard" OR "metric" |
| PRIORITY | issue has priority field != "None" and != null |
| SCOPE | `story_points <= 8` |
| GENERIC | always true (cannot check, benefit of doubt) |

#### 9B.3: Scoring

For each issue with dor_found=true team:

```javascript
// Count only checkable criteria (exclude GENERIC)
const checkableCriteria = teamDorCriteria.filter(c => c.check_type !== "GENERIC")
const totalCheckable = checkableCriteria.length

if (totalCheckable === 0) {
  // All criteria are GENERIC - issue is considered compliant
  issue.dor_compliance_pct = 100
} else {
  const metCount = checkableCriteria.filter(c => runCheck(c.check_type, issue)).length
  issue.dor_compliance_pct = Math.round((metCount / totalCheckable) * 100)
}

// Threshold: >= 75% means "DoR ready"
issue.dor_ready = issue.dor_compliance_pct >= 75
```

#### 9B.4: Save Compliance Data

Save to `${OUTPUT_DIR}/dor_compliance_backlog.json`:

```json
[
  {
    "team": "Europium",
    "issue_key": "AENW-1234",
    "story_points": 5,
    "dor_compliance_pct": 80,
    "dor_ready": true,
    "checks": {
      "ESTIMATE": true,
      "ACCEPTANCE_CRITERIA": true,
      "DESCRIPTION_QUALITY": true,
      "DESIGN": false
    }
  }
]
```

**Rules:**
- Only includes issues from teams with dor_found=true
- Only includes estimated issues (story_points != null)
- `"team"` uses display names
- Sorted by team (A-Z), then issue_key (ascending)

### Step 9C: Velocity Calculation (Most Recent Sprint Attribution with Name Filtering)

**Goal:** Calculate average velocity from the last 3 completed sprints per team. Primary source is the Greenhopper velocity API (matches Jira's native velocity chart exactly). Fallback uses "most recent sprint" attribution with sprint name filtering and project key validation.

#### 9C.0: Sprint Field Configuration

**Sprint Field:** `customfield_10115` (Jira Sprint-type field, verified via field metadata)

```javascript
const SPRINT_FIELD = "customfield_10115"
```

This field contains an array of sprint objects with properties: `id`, `name`, `state`, `boardId`, `goal`, `startDate`, `endDate`, `completeDate`.

**CRITICAL:** On this Jira instance, the standard `sprint` field name is NOT recognized by the API response -- sprint data is ONLY available under `customfield_10115`. The JQL function `closedSprints()` still works in query filters (e.g., `sprint in closedSprints()`), but the RESPONSE field containing sprint metadata must be requested as `customfield_10115`.

**Sprint Name Patterns** (for filtering sprints to team's own board):

```javascript
const SPRINT_NAME_PATTERNS = {
  "Abyss": /abyss/i,
  "Radium": /radium/i,
  "Europium": /europium/i,
  "Copernicium": /copernicium/i,
  "Mouflons": /mouflons/i,
  "Wolves": /wolves/i,
  "Polonium UF": /polonium/i,
  "Bigos": /bigos/i,
  "Capybaras": /capybaras/i,
  "ML Serving Sturgeons": /ml.?serving/i,
  "ML Platform Pandas": /ml.?platform/i,
  "Zurek": /zurek/i,
  "EP Core": /ep.?core/i,
  "Igni": /igni/i,
  "SRE": /srpol.*sre/i
}
```

**Why sprint name filtering is needed:** The JQL `sprint in closedSprints()` returns issues from ALL closed sprints across the ENTIRE PROJECT, not just the team's specific board. In shared projects (e.g., ASPW has boards for Igni, Bidder, Platform), an Igni-team issue may carry sprint metadata for "Bidder Sprint 20" in its sprint field array. Without name filtering, phantom sprints from other teams contaminate velocity.

**Pattern matching rules:**
- Case-insensitive matching (`/i` flag)
- Pattern must match as a substring of the sprint name
- Each team's pattern is designed to match ONLY their sprints (e.g., `/igni/i` matches "Igni Sprint 20" but not "Bidder Sprint 20")
- SRE team uses `/srpol.*sre/i` to match their naming convention: "SRPoL SRE Sprint 20", "SRPoL SRE Sprint 19"
- If NO sprints match a team's pattern despite Done issues being found, log: `[WARNING] Team {displayName}: 0 sprints matched name pattern despite {N} Done issues in the project`

#### 9C.0.1: Velocity Query Execution

Issue velocity queries for ALL projects using parallel MCP calls (batch 5-6 per message).
Paginate each project to completion (same rules as backlog queries in Step 9.3).
After all velocity data is fetched, save combined results and run velocity calculation via Python script.

If velocity pagination for a specific query fails mid-stream (cursor expired, network error), retain all pages already fetched for that query and proceed. Log: `[WARNING] Project {KEY}: velocity pagination incomplete ({N} pages fetched, cursor expired). Velocity may be underreported.`

#### 9C.1: Query Completed Work (Single Query Per Project, Client-Side Time Filtering)

**CRITICAL: DO NOT use `resolved >= -Xw` in velocity JQL.**

On this Jira instance, the majority of Done issues have `resolutiondate = null` because the team workflows transition issues to "Done" status without setting the Resolution field. Using `resolved >= -Xw` silently excludes 50-80% of completed work, producing drastically under-reported velocity.

**Verified fact:** The sprint `completeDate` (inside the `customfield_10115` sprint object array) is ALWAYS populated for closed sprints. It is set by Jira when an admin closes the sprint, independent of workflow configuration. Time-bounding MUST use this field client-side, not `resolutiondate` in JQL.

**JQL Template (1 query per project):**

```jql
project = {PROJECT_KEY}
AND sprint in closedSprints()
AND statusCategory = Done
AND issuetype IN (Story, Bug, Task)
AND issuetype != Sub-task
```

No `resolved` clause. No time-bounding in JQL. Time filtering happens client-side after data is fetched.

**Fields to request:**
```
["key", "customfield_10200", "customfield_10114", "customfield_10115"]
```

**Why these fields:**
- `customfield_10200` - Story Points
- `customfield_10114` - Team field (for client-side filtering)
- `customfield_10115` - Sprint objects array (id, name, state, boardId, startDate, endDate, completeDate). NOTE: The standard `sprint` field name is NOT returned by this Jira instance's API; must use `customfield_10115`.

**Why NO `resolutiondate` field:** It is unreliable (null for most Done issues) and is not used for any filtering or attribution logic.

**Why 12 weeks discovery window:** Biweekly teams have ~6 sprints in 12 weeks, guaranteeing at least 3 closed sprints are captured.

**Execution model:**

```javascript
// Fire 1 query per project (all projects in parallel)
const velocityQueries = []
for (const projectKey of Object.keys(PROJECT_TEAMS)) {
  velocityQueries.push({
    project: projectKey,
    jql: `project = ${projectKey} AND sprint in closedSprints() AND statusCategory = Done AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task`
  })
}

// Execute ALL in parallel: maxResults = 100
// Pagination IS expected (200-500 Done issues per project is normal)
```

**Pagination (expected for most projects):**

Each project query will likely return `hasNextPage: true`. Handle as follows:
- Paginate IMMEDIATELY for each project (cursor is fresh since no other work has intervened)
- Same pagination rules as backlog queries: read endCursor, call with nextPageToken
- Cap at 10 pages (1000 issues) per project
- Pagination for DIFFERENT projects MAY run in parallel
- Pagination for the SAME project MUST be sequential
- Log: `[INFO] Project {KEY}: {N} velocity issues ({P} pages)`

**Response overflow handling:**

If a query response exceeds the inline output limit and is saved to a temporary file:
1. Use Grep to extract endCursor: pattern `"endCursor":"([^"]*)"`
2. Use Grep to check hasNextPage: pattern `"hasNextPage":true`
3. If pagination needed, proceed immediately
4. After pagination completes (or if hasNextPage=false), save the accumulated results via Write
5. The main session MUST own pagination calls. All data processing (filtering, calculation)
   happens in the main session via python3 scripts, AFTER all API fetching is complete.

**Client-side time filtering (replaces JQL `resolved >= -Xw`):**

After fetching all issues for a project, during the velocity calculation step (9C.4), only process issues whose MOST RECENT team-matching closed sprint has `completeDate` within the last 12 weeks:

```javascript
const TWELVE_WEEKS_MS = 12 * 7 * 24 * 60 * 60 * 1000
const scanDate = new Date("2026-07-16")  // current scan date
const cutoffDate = new Date(scanDate.getTime() - TWELVE_WEEKS_MS)

// Inside calculateTeamVelocity, after finding targetSprint:
if (new Date(targetSprint.completeDate) < cutoffDate) {
  continue  // Skip - sprint closed more than 12 weeks ago
}
```

This filter is applied INSIDE the velocity calculation function (Step 9C.4), after team filtering and sprint name pattern matching, but before accumulating into sprintMap.

**Fallback:** If `sprint in closedSprints()` fails (syntax error) on the first query for a project, fall back to:
```jql
project = {PROJECT_KEY} AND statusCategory = Done AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task AND updated >= -12w
```
Log: `[WARNING] Project {KEY}: closedSprints() not supported, using updated >= -12w fallback.`

The `updated` field is always non-null for Done issues (Jira updates it on every transition). This is a broader query but client-side sprint `completeDate` filtering still ensures only recent sprint data is used.

**NOTE: Multi-project teams** benefit from velocity discovery across all their mapped projects automatically. The sprintMap accumulator in Step 9C.4 is keyed by sprint ID, so if the same sprint appears in results from two project queries, it accumulates correctly without double-counting (same sprint key -> same map entry).

**Validation after fetch:**
```
[INFO] Velocity data completeness:
  - Projects fully fetched: {N}/{total}
  - Projects with truncated data: {N} (list project keys)
  - Total velocity issues across all projects: {N}
  - Teams with velocity_avg: {N}/15
  - Teams with null velocity: {N}/15 (list team names)
```

If any project had truncated velocity data, add to velocity_data.json metadata:
```json
"truncated_projects": ["AENW"]
```

#### 9C.2: Client-Side Team Filtering (with Project Validation)

Apply TWO filters to assign completed issues to teams:

1. **Team field match:** `customfield_10114.name` must exactly match the team's entry in `TEAM_NAME_PATTERNS`
2. **Project key validation:** The issue's project key (from `issue.fields.project.key` or extracted from the issue key prefix, e.g., "MAW-123" -> "MAW") must match the team's designated project in `PROJECT_TEAMS`

```javascript
// Inside the velocity calculation loop, after team field match:
const issueProject = issue.fields?.project?.key || issue.key.split("-")[0]
const expectedProjects = Object.keys(PROJECT_TEAMS).filter(
  pk => PROJECT_TEAMS[pk].includes(teamName)
)
if (!expectedProjects.includes(issueProject)) {
  // Cross-project contamination — skip this issue
  continue
}
```

**Why this is needed:** Some teams operate cross-project Jira boards (e.g., Bigos board 11439 pulls issues from MAW, PEA, and RSW). These foreign-project issues carry the team's sprint name and team field value, but should NOT count toward velocity because the team's designated project (from SRPOL Teams page board URL) is the authoritative source.

**Diagnostic logging:** When an issue is rejected by the project filter, log:
```
[INFO] Excluded {issue.key} from {displayName} velocity: project {issueProject} not in designated projects {expectedProjects}
```

#### 9C.2.1: Issue Deduplication (MANDATORY)

Before processing issues for velocity calculation, deduplicate by issue key:

```javascript
const seenKeys = new Set()
const uniqueIssues = []
for (const issue of allIssues) {
  if (seenKeys.has(issue.key)) continue
  seenKeys.add(issue.key)
  uniqueIssues.push(issue)
}
if (uniqueIssues.length < allIssues.length) {
  console.log(`[WARNING] ${allIssues.length - uniqueIssues.length} duplicate issues removed from velocity data`)
}
```

This deduplication MUST happen after loading all paginated results and before team filtering/sprint attribution.

#### 9C.3: Sprint Field Parsing

The `customfield_10115` field (Sprint) can be:
- An array of sprint objects: `[{id, name, state, startDate, endDate, completeDate}, ...]`
- A single object: `{id, name, state, ...}`
- null or missing

**Defensive parsing:**
```javascript
function parseSprints(sprintField) {
  if (!sprintField) return []
  if (Array.isArray(sprintField)) return sprintField
  if (typeof sprintField === 'object') return [sprintField]
  if (typeof sprintField === 'string') {
    try { return JSON.parse(sprintField) } catch { return [] }
  }
  return []
}
```

On first successful response, log sprint field format for debugging:
```
[DEBUG] Sprint field (customfield_10115) format sample: <first 200 chars of JSON>
```

If `id` field is missing from sprint objects, use `name` as the deduplication key.

#### 9C.4: Velocity Calculation (Most Recent Sprint Attribution with Name Filtering)

For each team's filtered issues, calculate velocity using "most recent closed team sprint" attribution. This assigns each Done issue to the most recent sprint in its sprint array that (a) is closed, (b) has a completeDate, and (c) matches the team's sprint name pattern. This is the FALLBACK approach used when Greenhopper API is unavailable. It:
- Prevents rollover double-counting (issue can only appear in one sprint)
- Avoids resolution-date comparison inaccuracies
- May overcount for teams that complete work after sprint close (mitigated by Greenhopper API in Step 9C.4.1)

```javascript
function calculateTeamVelocity(teamIssues, teamName) {
  const sprintPattern = SPRINT_NAME_PATTERNS[teamName]
  if (!sprintPattern) {
    console.log(`[WARNING] Team ${getDisplayName(teamName)}: no sprint name pattern defined, velocity will be null`)
    return { velocity_avg: null, sprints_used: 0, velocity_sprints: [] }
  }

  const sprintMap = {}  // key -> {sprint_id, name, completeDate, total_sp, issue_count}

  for (const issue of teamIssues) {
    const sprints = parseSprints(issue.fields[SPRINT_FIELD])
    const sp = issue.fields.customfield_10200
    const spValue = (typeof sp === 'number') ? sp : 0

    // Filter to CLOSED sprints matching team's naming pattern
    const teamSprints = sprints
      .filter(s => s.state === "closed" && s.completeDate && sprintPattern.test(s.name))
      .sort((a, b) => new Date(b.completeDate) - new Date(a.completeDate))

    if (teamSprints.length === 0) continue

    // ================================================================
    // MOST RECENT SPRINT ATTRIBUTION
    // Assign issue to its MOST RECENT closed team-matching sprint.
    //
    // Why this works:
    // - Non-rolled issues: have only 1 closed team sprint -> attributed there
    // - Rolled-over issues: appear in Sprint N and Sprint N+1 (both closed)
    //   -> attributed to Sprint N+1 (most recent) which is where the work
    //      was actually completed. Prevents double-counting.
    //
    // This approximates Jira's velocity chart. For exact match,
    // the Greenhopper API overrides these values in Step 9C.4.1.
    // ================================================================
    const targetSprint = teamSprints[0]  // Most recent by completeDate

    // CLIENT-SIDE TIME FILTER: skip if sprint closed more than 12 weeks ago
    const TWELVE_WEEKS_MS = 12 * 7 * 24 * 60 * 60 * 1000
    const cutoffDate = new Date(new Date(SCAN_DATE).getTime() - TWELVE_WEEKS_MS)
    if (new Date(targetSprint.completeDate) < cutoffDate) {
      continue  // Sprint closed outside 12-week discovery window
    }

    const key = targetSprint.id || targetSprint.name

    if (!sprintMap[key]) {
      sprintMap[key] = {
        sprint_id: targetSprint.id || null,
        name: targetSprint.name,
        completeDate: targetSprint.completeDate,
        total_sp: 0,
        issue_count: 0
      }
    }
    sprintMap[key].total_sp += spValue
    sprintMap[key].issue_count += 1
  }

  // Log warning if no sprints matched despite having issues
  if (Object.keys(sprintMap).length === 0 && teamIssues.length > 0) {
    console.log(`[WARNING] Team ${getDisplayName(teamName)}: 0 sprints matched name pattern despite ${teamIssues.length} Done issues in the project`)
  }

  // Sort by completeDate desc, take last 3 with issues
  const sortedSprints = Object.values(sprintMap)
    .filter(s => s.issue_count > 0)
    .sort((a, b) => new Date(b.completeDate) - new Date(a.completeDate))
    .slice(0, 3)

  if (sortedSprints.length === 0) {
    return { velocity_avg: null, sprints_used: 0, velocity_sprints: [] }
  }

  // CRITICAL: Divide by ACTUAL sprint count (1, 2, or 3) - NOT always 3
  const totalSP = sortedSprints.reduce((sum, s) => sum + s.total_sp, 0)
  const avg = Math.round((totalSP / sortedSprints.length) * 10) / 10

  return {
    velocity_avg: avg,
    sprints_used: sortedSprints.length,
    velocity_sprints: sortedSprints.map(s => ({
      sprint_id: s.sprint_id,
      sprint_name: s.name,
      completed_sp: s.total_sp,
      issue_count: s.issue_count,
      complete_date: s.completeDate
    }))
  }
}
```

**Key design principles:**
- NO `resolutiondate` in JQL or fields (unreliable - most Done issues have null resolutiondate on this instance)
- Time-bounding via sprint `completeDate` client-side (always populated for closed sprints, set by Jira on sprint close)
- Sprint name filtering via `SPRINT_NAME_PATTERNS` (eliminates phantom sprints from shared-project boards)
- Project key validation via `PROJECT_TEAMS` (eliminates cross-project board contamination)
- Issue deduplication by key (prevents double-counting from pagination overlap)
- "Most recent sprint" attribution (eliminates rollover double-counting)
- Single query per project with pagination (no time-windowed partitioning needed)

#### 9C.4.1: Greenhopper Velocity API Verification (Primary Source)

The attribution-based calculation in Step 9C.4 is a FALLBACK. The primary velocity source is the Jira Greenhopper velocity chart API, which returns pre-calculated sprint velocities matching Jira's sprint report exactly.

**API Endpoint:**
```
GET {JIRA_BASE_URL}/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={boardId}
```

**Authentication:** Basic Auth using credentials from `.env` file:
- `JIRA_BASE_URL` (e.g., `https://samsung-sbt.atlassian.net`)
- `JIRA_EMAIL` (Atlassian account email)
- `JIRA_API_TOKEN` (API token from https://id.atlassian.com/manage-profile/security/api-tokens)

**Response structure:**
```json
{
  "sprints": [
    {"id": 30218, "name": "Bigos Sprint 19", "state": "closed", ...},
    {"id": 31148, "name": "Bigos Sprint 20", "state": "closed", ...}
  ],
  "velocityStatEntries": {
    "30218": {"estimated": {"value": 50.0}, "completed": {"value": 50.0}},
    "31148": {"estimated": {"value": 34.0}, "completed": {"value": 31.0}}
  }
}
```

**Implementation in the velocity Python script:**

```python
import os
import requests
from base64 import b64encode

def fetch_greenhopper_velocity(board_id):
    """Fetch velocity data from Greenhopper API. Returns dict of sprint_id -> completed_sp, or None on failure."""
    base_url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    
    if not all([base_url, email, token]):
        print("[WARNING] JIRA credentials not configured (.env). Using fallback attribution-based velocity.")
        return None
    
    url = f"{base_url}/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={board_id}"
    auth = (email, token)
    
    try:
        resp = requests.get(url, auth=auth, timeout=30)
        if resp.status_code != 200:
            print(f"[WARNING] Greenhopper API returned {resp.status_code} for board {board_id}. Using fallback.")
            return None
        data = resp.json()
        result = {}
        for sprint_id_str, entry in data.get("velocityStatEntries", {}).items():
            completed = entry.get("completed", {}).get("value", 0)
            result[int(sprint_id_str)] = completed
        return result
    except Exception as e:
        print(f"[WARNING] Greenhopper API failed for board {board_id}: {e}. Using fallback.")
        return None
```

**Integration with velocity calculation:**

After Step 9C.4 builds `sprintMap` from attribution logic, the script:
1. Extracts the `boardId` from any sprint object (all sprints on a team's board share the same `boardId`)
2. Calls `fetch_greenhopper_velocity(boardId)`
3. If successful: overrides `total_sp` for each sprint with the API's `completed` value
4. If failed: keeps attribution-based values (fallback)

```python
# After building team_sprint_data, before final calculation:
for team, sprints in team_sprint_data.items():
    if not sprints:
        continue
    # Get boardId from first sprint
    board_id = None
    for sprint_data in sprints.values():
        if sprint_data.get("board_id"):
            board_id = sprint_data["board_id"]
            break
    if not board_id:
        continue
    
    # Try Greenhopper API
    velocity_data = fetch_greenhopper_velocity(board_id)
    if velocity_data:
        for sprint_key, sprint_info in sprints.items():
            sprint_id = sprint_info.get("sprint_id")
            if sprint_id and sprint_id in velocity_data:
                old_sp = sprint_info["total_sp"]
                sprint_info["total_sp"] = velocity_data[sprint_id]
                if old_sp != velocity_data[sprint_id]:
                    print(f"  [INFO] {team} {sprint_info['name']}: adjusted {old_sp} -> {velocity_data[sprint_id]} SP (Greenhopper)")
```

**Fallback conditions (use attribution-based velocity):**
- `.env` file missing or credentials not set
- Greenhopper API returns 401/403 (authentication failure)
- Greenhopper API returns 404 (endpoint removed by Atlassian)
- Network timeout or connection error
- Response does not contain `velocityStatEntries`

In all fallback cases, log a warning and proceed with attribution-based values. The attribution logic is retained as a working baseline.

**Known limitation:** The Greenhopper API is an undocumented/internal Jira Cloud API. It is not officially supported by Atlassian and could be removed without notice. The fallback attribution logic ensures the skill continues to function if the API becomes unavailable, albeit with reduced accuracy for teams with poor sprint hygiene.

#### 9C.5: Edge Cases

| Scenario | Handling |
|----------|----------|
| Team has no completed issues in 12 weeks | velocity_avg=null, sprints_used=0 |
| Team has 1 or 2 closed sprints | Divide by actual count (1 or 2), NOT 3 |
| Issue has null SP but is Done | Contributes 0 SP to sprint total |
| Issue has null resolutiondate but is Done | Included normally (time-bounded by sprint completeDate, not resolutiondate) |
| Issue has no sprint field (customfield_10115 is null) | Skipped (cannot determine sprint attribution or time-bounding) |
| Sprint has no completeDate | Excluded from sprint filtering |
| Sprint has no id | Use name as dedup key |
| Sprint completeDate older than 12 weeks | Issue skipped by client-side time filter |
| All issues have null SP | velocity_avg=0 (distinct from null) |
| velocity_avg=0 | Treated same as null for runway (N/A) |
| No sprints match team's name pattern | velocity_avg=null, log warning |
| Sprint name pattern not defined for team | velocity_avg=null, log warning |
| Issue in multiple closed team sprints | Attributed to MOST RECENT only (no double-counting) |
| Sprint appears in both team issues and non-team issues | Counted only for issues matching team filter (client-side) |
| Issue from non-designated project (cross-project board) | Excluded by project key validation (Step 9C.2) |
| Duplicate issue key in loaded data | Deduplicated before processing (Step 9C.2.1) |
| Greenhopper API unavailable (401/403/404/timeout) | Fall back to attribution-based velocity with log warning |
| .env credentials missing | Fall back to attribution-based velocity with log warning |
| Greenhopper returns sprint not in top-3 | Ignored (only top-3 by completeDate are used) |

#### 9C.6: Save Velocity Data

Save to `${OUTPUT_DIR}/velocity_data.json`:

```json
{
  "metadata": {
    "scan_date": "2026-07-16",
    "method": "greenhopper_velocity_api_with_attribution_fallback",
    "method_description": "Primary: Greenhopper velocity API (GET /rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={boardId}) provides exact sprint velocity matching Jira UI. Fallback: attribution-based calculation using most-recent-sprint logic with project key validation and deduplication. Fallback may overcount for teams that complete work after sprint close without rolling forward.",
    "discovery_window": "12w (client-side completeDate filter for fallback)",
    "query_strategy": "greenhopper_api_per_board (fallback: single_query_per_project_with_pagination)",
    "time_filter": "sprint completeDate >= scan_date - 84 days (client-side, fallback only)",
    "max_sprints_per_team": 3,
    "sprint_attribution": "Greenhopper API (primary) or most-recent closed sprint with name pattern + project key validation (fallback)",
    "sprint_field": "customfield_10115",
    "truncated_projects": []
  },
  "teams": {
    "Igni": {
      "velocity_avg": 30.0,
      "sprints_used": 3,
      "velocity_sprints": [
        {"sprint_id": 31200, "sprint_name": "Igni Sprint 20", "completed_sp": 39, "issue_count": 8, "complete_date": "2026-07-15T12:00:00.000Z"},
        {"sprint_id": 31100, "sprint_name": "Igni Sprint 19", "completed_sp": 26, "issue_count": 6, "complete_date": "2026-07-01T12:00:00.000Z"},
        {"sprint_id": 31000, "sprint_name": "Igni Sprint 18", "completed_sp": 25, "issue_count": 5, "complete_date": "2026-06-17T12:00:00.000Z"}
      ]
    }
  }
}
```

**Rules:**
- Object with `metadata` and `teams` keys
- `teams` keyed by display name
- velocity_avg is 1-decimal float (e.g., 30.0) or null
- velocity_avg=null means no sprints found; velocity_avg=0 means sprints exist but 0 SP completed
- Both null and 0 velocity result in runway = "N/A"
- velocity_sprints sorted most recent first
- Each sprint entry includes sprint_id (if available), sprint_name, completed_sp, issue_count, complete_date

**SCHEMA COMPLIANCE GUARD:** The output MUST use this exact schema. Do NOT use alternative key names such as `total_sp_12w`, `avg_sp_per_sprint`, `avg_items_per_sprint`, or any other invented keys. The schema defined here is consumed by downstream report generators and validators.

### Step 9D: Sprint Runway Calculation

For each team, calculate sprint runway:

```javascript
function calculateRunway(team) {
  const velocityAvg = team.velocity_avg
  const dorFound = team.dor_found
  const dorReadySP = team.dor_ready_sp  // null for Tier 2 teams

  // Tier 3: No DoR heading found at all
  if (!dorFound) {
    return { sprint_runway: null, runway_status: "No DoR" }
  }

  // Tier 2: DoR exists but criteria could not be parsed (dor_ready_sp is null)
  if (dorReadySP === null) {
    return { sprint_runway: "N/A", runway_status: "N/A" }
  }

  // No velocity data
  if (velocityAvg === null || velocityAvg === 0) {
    return { sprint_runway: "N/A", runway_status: "N/A" }
  }

  // Tier 1: Full calculation
  const runway = Math.round((dorReadySP / velocityAvg) * 10) / 10  // 1 decimal

  let status
  if (runway >= 3.0) status = "Healthy"
  else if (runway >= 1.0) status = "Attention"
  else status = "Critical"

  return { sprint_runway: runway, runway_status: status }
}
```

**Status thresholds:**
- >= 3.0 sprints: "Healthy"
- >= 1.0 and < 3.0 sprints: "Attention"
- < 1.0 sprints: "Critical"
- velocity_avg null or 0: "N/A"
- dor_found true but dor_ready_sp null (Tier 2 -- DoR exists but unparseable): "N/A"
- dor_found false (Tier 3 -- no DoR heading): "No DoR"

**Three distinct report states:**
- `"No DoR"` = team genuinely has no Definition of Ready (no heading found)
- `"N/A"` = team has a DoR but it could not be assessed heuristically, OR no velocity data
- Numeric = team has DoR, compliance assessed, runway calculated

### Step 10: Save Data Files

#### Step 10.1: Save teams.json

Write `${OUTPUT_DIR}/teams.json`:

```json
{
  "metadata": {
    "scan_date": "[ISO-8601 timestamp]",
    "scan_timestamp_cet": "[YYYYMMDD HH-MM]",
    "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
    "team_count": 15,
    "cloudId": "adgear.atlassian.net",
    "scanner_version": "3.0",
    "scanner_type": "backlog-readiness",
    "story_points_field": "customfield_10200",
    "jql_type": "primary | fallback",
    "total_backlog_items": 245,
    "total_estimated": 180,
    "total_unestimated": 65,
    "estimation_rate_pct": 73.5,
    "dor_compliance_method": "heuristic_field_checks",
    "dor_threshold_pct": 75,
    "velocity_window": "12w",
    "velocity_method": "most_recent_sprint_with_name_filtering",
    "sprint_field": "customfield_10115",
    "velocity_sprints_max": 3
  },
  "teams": [
    {
      "name": "Europium",
      "page_link": "https://...",
      "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
      "board_id": "8979",
      "project_key": "AENW",
      "backlog_total": 30,
      "estimated": 22,
      "unestimated": 8,
      "estimation_rate": "73%",
      "velocity_avg": 21,
      "dor_found": true,
      "dor_ready_count": 15,
      "sprint_runway": 2.1,
      "runway_status": "Attention",
      "status": "success",
      "used_fallback_jql": false,
      "error": null
    }
  ]
}
```

**Team status values:**
- `"success"` - Backlog queried successfully (even if 0 items)
- `"no_board"` - No sprint board URL configured
- `"parse_error"` - Cannot parse board ID/project from URL
- `"access_error"` - Jira API call failed

**Note:** The `"name"` field in the teams array uses display names (getDisplayName applied).

#### Step 10.2: Save backlog_data.json

Write `${OUTPUT_DIR}/backlog_data.json`:

```json
[
  {
    "team": "Europium",
    "issue_key": "AENW-1234",
    "issue_type": "Story",
    "url": "https://adgear.atlassian.net/browse/AENW-1234",
    "title": "Implement feature X",
    "status": "To Do",
    "assignee": "John Doe",
    "story_points": 5
  },
  {
    "team": "Europium",
    "issue_key": "AENW-1235",
    "issue_type": "Bug",
    "url": "https://adgear.atlassian.net/browse/AENW-1235",
    "title": "Fix login issue",
    "status": "Backlog",
    "assignee": "Unassigned",
    "story_points": null
  }
]
```

**Rules:**
- Sorted by: team display name (A-Z), then issue_key (ascending)
- `story_points`: numeric (int or float) OR `null` if not estimated
- `story_points: 0` is valid (counts as estimated - spikes/investigations)
- Every entry has exactly 8 keys
- `issue_key` is globally unique (no duplicates)
- `"team"` field uses display names (getDisplayName applied)

#### Step 10.3: Save summary_data.json

Write `${OUTPUT_DIR}/summary_data.json`:

```json
[
  {
    "team": "Europium",
    "backlog_total": 25,
    "estimated": 16,
    "unestimated": 9,
    "estimation_rate": "64%",
    "total_story_points": 69,
    "stories": 15,
    "bugs": 3,
    "tasks": 7,
    "velocity_avg": 21,
    "velocity_sprints_used": 3,
    "velocity_sprints": [
      {"sprint_name": "Sprint 45", "completed_sp": 21},
      {"sprint_name": "Sprint 44", "completed_sp": 18},
      {"sprint_name": "Sprint 43", "completed_sp": 24}
    ],
    "dor_found": true,
    "dor_checkable_criteria": 4,
    "dor_ready_count": 12,
    "dor_ready_sp": 45,
    "dor_avg_compliance_pct": 78,
    "sprint_runway": 2.1,
    "runway_status": "Attention"
  }
]
```

**Rules:**
- Always exactly 15 entries sorted alphabetically by display name
- `"team"` field uses display names (getDisplayName applied)
- `backlog_total` = `estimated` + `unestimated` (invariant)
- `estimation_rate`: "X%" (rounded, 0 decimal) if backlog_total > 0; "-" if 0
- `total_story_points`: sum of all non-null story_points for the team
- `stories`, `bugs`, `tasks`: count by issue_type
- New velocity/DoR/runway fields are nullable for graceful degradation:
  - `velocity_avg`: number (1-decimal float, e.g. 30.0) or null (no sprints found)
  - `velocity_sprints_used`: 0-3
  - `velocity_sprints`: array of `{sprint_name, completed_sp}` objects (REPORT-CONSUMABLE format, max 3 entries)
  - `dor_found`: boolean
  - `dor_checkable_criteria`: integer or null (if dor_found=false)
  - `dor_ready_count`: integer or null
  - `dor_ready_sp`: integer or null
  - `dor_avg_compliance_pct`: integer (0-100) or null
  - `sprint_runway`: float (1 decimal) or null
  - `runway_status`: "Healthy" | "Attention" | "Critical" | "N/A" | "No DoR"
- Teams with status != "success" get all zeros/nulls

**velocity_sprints format for summary_data.json:**
The `velocity_sprints` array uses the REPORT-CONSUMABLE format (2 fields only):
```json
"velocity_sprints": [
  {"sprint_name": "Igni Sprint 20", "completed_sp": 39},
  {"sprint_name": "Igni Sprint 19", "completed_sp": 26},
  {"sprint_name": "Igni Sprint 18", "completed_sp": 25}
]
```

This is a SUBSET of the full sprint data in `velocity_data.json`. When populating `summary_data.json`, extract only `sprint_name` and `completed_sp` from the velocity calculation result. The report generator (`generate_backlog_report.py`) reads these two fields for Excel columns B-D.

### Step 11: Generate Reports via Canonical Template (AUTO-EXECUTE)

**This step executes the persistent canonical report generator. No report code is written by the LLM.**

#### Step 11.1: Verify Template Exists

```bash
test -f "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_backlog_report.py" && echo "OK" || echo "MISSING"
```

If MISSING:
```
ERROR: Template script not found at assets/templates/generate_backlog_report.py
Cannot generate reports without the canonical template.
```
Skip report generation but do NOT fail the overall skill. Proceed to Step 12.

#### Step 11.2: Copy Template and Execute

```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/generate_backlog_report.py" "${OUTPUT_DIR}/generate_backlog_report.py"
cd "${OUTPUT_DIR}" && python3 generate_backlog_report.py backlog_data.json summary_data.json "." "{SCAN_DATE}"
```

Where `{SCAN_DATE}` is the scan date in YYYY-MM-DD format (e.g., "2026-07-10").

This produces BOTH:
- `Report-backlog.xlsx` (2 sheets: "Backlog Readiness" + "Velocity & Runway")
- `Report-backlog.html` (self-contained dashboard)

#### Step 11.3: Validate Reports

```bash
cp "C:/Users/i.klyha/Desktop/Claude/wow-scanner-tool/assets/templates/validate_backlog_report.py" "${OUTPUT_DIR}/validate_backlog_report.py"
cd "${OUTPUT_DIR}" && python3 validate_backlog_report.py "."
```

If validation fails, output errors but do NOT attempt to fix by regenerating with different code. The template is canonical.

### Step 12: Save Summary Document

Create `${OUTPUT_DIR}/BACKLOG_READINESS_SUMMARY.md`:

```markdown
# Backlog Readiness Summary

**Generated:** [ISO-8601 timestamp]
**Scan Directory:** [OUTPUT_DIR path]

---

## Key Metrics

- **Total Teams Scanned:** 15
- **Total Backlog Items:** [N]
- **Items with Story Points:** [Y] ([rate]%)
- **Items without Story Points:** [Z] ([rate]%)
- **Story Points Field:** customfield_10200
- **JQL Type:** [primary | fallback]
- **DoR Compliance Method:** heuristic field-presence checks
- **DoR Ready Threshold:** >= 75%

---

## Per-Team Breakdown

| Team | Backlog | Estimated | Unestimated | Rate |
|------|---------|-----------|-------------|------|
| [team] | [n] | [y] | [z] | [x]% |
| ... | ... | ... | ... | ... |

---

## Sprint Runway Analysis

| Team | Velocity (avg) | DoR Ready SP | Runway (sprints) | Status |
|------|----------------|--------------|------------------|--------|
| [team] | [v] | [sp] | [r] | [s] |
| ... | ... | ... | ... | ... |

---

## Teams with Critical Runway (< 1.0)

- [Team] - [X] sprints runway (velocity: [V], ready SP: [SP])
- ...

---

## Teams with Healthy Runway (>= 3.0)

- [Team] - [X] sprints runway (velocity: [V], ready SP: [SP])
- ...

---

## Teams with No Runway Data

- [Team] (reason: no DoR / no velocity data / no board)
- ...

---

## Teams Needing Attention (< 50% estimated)

- [Team] - [X]% estimated ([Y] of [Z] items)
- ...

---

## Teams with No Backlog Data

- [Team] (reason: no board / parse error / access error)
- ...

---

## Files Generated

- Report-backlog.xlsx - Excel report (2 sheets: Backlog Readiness, Velocity & Runway)
- Report-backlog.html - HTML dashboard
- backlog_data.json - Per-issue backlog data
- summary_data.json - Team summary with velocity/runway
- teams.json - Scan metadata
- dor_criteria.json - DoR criteria per team
- dor_compliance_backlog.json - Per-issue DoR compliance
- velocity_data.json - Sprint velocity per team

---

## Notes

- Sort order: alphabetical by team display name, then by issue key (not board priority rank)
- Story Points = 0 treated as "estimated" (valid for spikes)
- Backlog = items not in any active or future sprint, not Done
- DoR compliance uses heuristic field-presence checks (deterministic, no LLM evaluation)
- DoR ready threshold: >= 75% of checkable criteria must pass
- Velocity calculated from last 3 closed sprints within 12-week discovery window
- Sprint runway = DoR-ready story points / average velocity
- Sprint cadence assumed uniform (no weighting by sprint length)
- "Polonium UF" displays as "Polonium" in all outputs
```

### Step 13: Report Completion

Output to console:

```
=== Backlog Readiness Scan Complete ===

Source: SRPOL Teams page
Scan timestamp (CET): [CET_TIMESTAMP]
Teams found: 15

Backlog Summary:
  - Total backlog items: [N]
  - Estimated (have Story Points): [Y] ([rate]%)
  - Unestimated (no Story Points): [Z] ([rate]%)
  - Story Points field: customfield_10200
  - DoR compliance method: heuristic field-presence checks

Sprint Runway Summary:
  - Average runway (teams with data): [X.X] sprints
  - Teams with Healthy runway (>=3.0): [N]
  - Teams with Critical runway (<1.0): [N]
  - Teams without runway data: [N]

Per-Team Breakdown:
  Team                  | Backlog | Est. | Velocity | Ready SP | Runway  | Status
  ----------------------|---------|------|----------|----------|---------|--------
  [team]                | [n]     | [y]  | [v]      | [sp]     | [r]     | [s]
  ...

Reports saved to: ${OUTPUT_DIR}/
  - Report-backlog.xlsx (2 sheets: Backlog Readiness, Velocity & Runway)
  - Report-backlog.html
  - BACKLOG_READINESS_SUMMARY.md
  - backlog_data.json, summary_data.json
  - dor_criteria.json, dor_compliance_backlog.json, velocity_data.json

Validation: [PASSED | FAILED with N errors]
```

### Execution Integrity Check

If at any point during this execution, the Agent tool was invoked:
- Append to console output: `[ERROR] Agent delegation detected. This violates Rule #15. Scan results may be incomplete or duplicated.`
- Add to teams.json metadata: `"rule_violations": ["agent_delegation"]`

If no Agent tool was invoked (expected path):
- Append to console output: `[OK] Single-session execution confirmed (no agent delegation)`

## Error Handling

- **Continue on error:** If one team or project fails, continue with remaining teams
- **Track failures:** Record all errors in teams.json per-team entries
- **Graceful degradation:** Partial data is better than no data
- **JQL fallback:** If primary JQL fails, automatically try simpler fallback
- **Team field unavailable:** Issues with null customfield_10114 are silently discarded
- **DoR extraction failure:** If DoR extraction fails for a team, mark dor_found=false, continue with remaining teams
- **Description fetch failure:** If description fetch fails for a batch, skip compliance for those issues, continue
- **Velocity query failure:** If velocity query fails for a project, set velocity_avg=null and runway="N/A" for affected teams, continue
- **Sprint field missing:** If sprint field not in response, log warning, set all velocities to null

**Automation Rules:**
- **Only stop for critical failures:** Authentication fails, no teams found, cannot create output folder
- **Do not stop for partial failures:** If some teams fail, continue with successful teams
- **Automatic Steps 9A-13:** Execute DoR extraction, compliance, velocity, runway, reports, summary, and completion automatically

## Tool Requirements

Required tools:
- **ToolSearch** - Check for Atlassian MCP availability
- **mcp__plugin_atlassian_atlassian__getAccessibleAtlassianResources** - Verify authentication
- **mcp__plugin_atlassian_atlassian__getConfluencePage** - Fetch Confluence pages (team pages, DoR pages)
- **mcp__plugin_atlassian_atlassian__searchJiraIssuesUsingJql** - Query Jira backlog and velocity
- **Write** - Create JSON, TXT, Markdown files
- **Read** - Verify file contents
- **Bash** - Create directories, get current time, execute Python scripts

Optional tools:
- **Grep** - Search for patterns
- **Glob** - Find files

**Execution model:** All work runs in the main session. No background agents.
- MCP tools: parallel calls for data fetching (batch 5-7 per message)
- Bash: Python script execution (sequential, never concurrent)
- Write: save inline API results, create Python scripts
- Read/Grep: check files, extract pagination tokens

## Important Rules

1. **Backlog Scope:** Items NOT in any active or future sprint, NOT in Done status, type Story/Bug/Task only

2. **Team Naming:** Same rules as wow-dor-scanner - clean page titles, extract last segment from prefix patterns. Additionally, apply `getDisplayName()` to all output: "Polonium UF" displays as "Polonium" everywhere.

3. **File Naming:** Use kebab-case for all generated file names

4. **Timestamp Consistency:** Calculate CET timestamp ONCE and use consistently across all files

5. **Team Field Filtering (client-side):**
   - Team custom field ID: `customfield_10114` (Jira Team-type field)
   - DO NOT use `customfield_10114` in JQL
   - Query ALL backlog issues per project (one query per unique project via PROJECT_TEAMS)
   - Filter results CLIENT-SIDE by exact `customfield_10114.name` match
   - Paginate using `nextPageToken` until `hasNextPage: false` (cap at 10 pages / 1000 issues)
   - Issues with null/missing team field are discarded
   - 15 teams total. "Polonium LF" is removed and does not appear anywhere.
   - PROJECT_TEAMS is built dynamically in Step 8B from board URLs (not hardcoded).
   - One team = one project. Query each unique project ONCE, filter results client-side.

6. **Sprint Function Usage (different from wow-dor-scanner):**
   - This skill uses `sprint NOT IN openSprints()` in JQL to EXCLUDE sprinted items
   - This is semantically different from `sprint in openSprints()` which was banned for FINDING active work
   - The ban in wow-dor-scanner addresses a different bug (issues "In Progress" without sprint) that does not apply here
   - If sprint functions fail, fall back to `sprint is EMPTY` only

7. **Story Points Field:**
   - The Story Points field is `customfield_10200` (verified against the Jira instance)
   - No auto-discovery needed - use this field directly in every query
   - `story_points: 0` is valid (estimated)
   - `story_points: null` means not estimated
   - Always request `customfield_10200` in the fields list

8. **Report Generation is 100% Deterministic (Template-Based):**
   - Reports generated ONLY by `assets/templates/generate_backlog_report.py`
   - NEVER write openpyxl code, NEVER write HTML strings, NEVER create CSV fallbacks
   - Template is NEVER modified during execution
   - If template missing, skip reports (don't create replacement)
   - Template produces BOTH .xlsx AND .html in single execution

9. **Report-backlog.xlsx Fixed Schema:**
   - 2 sheets: "Backlog Readiness" + "Velocity & Runway"
   - Sheet 1 "Backlog Readiness": KPI rows 1-2, separator row 3, header row 4, data row 5+
     - 8 columns: Team, Issue Key, Issue Type, URL, Title, Status, Assignee, Story Points
     - Story Points empty cells: red background (#FFC7CE)
     - Story Points numeric cells: default background
     - Sorted by Team (A-Z), then Issue Key (ascending)
   - Sheet 2 "Velocity & Runway": Per-team velocity, DoR readiness, and runway metrics

10. **Data File Ordering:**
    - teams.json written in Step 10.1
    - backlog_data.json written in Step 10.2
    - summary_data.json written in Step 10.3
    - dor_criteria.json written in Step 9A
    - dor_compliance_backlog.json written in Step 9B
    - velocity_data.json written in Step 9C
    - ALL data files must exist before Step 11 execution

11. **DoR Compliance is DETERMINISTIC:**
    - Uses heuristic field checks ONLY
    - No LLM evaluation of issue content
    - Results are identical across runs on the same data
    - GENERIC check_type always passes (benefit of doubt)
    - Threshold is >= 75% for "DoR ready" classification

12. **Velocity uses "most recent sprint" attribution with name filtering:**
    - Sprint field is `customfield_10115` (NOT the standard `sprint` field name)
    - Discovery query: `sprint in closedSprints() AND statusCategory = Done` (NO `resolved` clause)
    - Time filtering: CLIENT-SIDE, sprint `completeDate` >= 12 weeks ago (NOT JQL `resolved >= -Xw`)
    - `resolutiondate` is NOT used anywhere (unreliable - most Done issues have null resolutiondate on this instance)
    - Fields: `["key", "customfield_10200", "customfield_10114", "customfield_10115"]`
    - Sprint field parsed defensively (array/object/string/null)
    - Sprint name filtering: each team's sprints filtered by `SPRINT_NAME_PATTERNS[teamName]` regex to exclude phantom sprints from shared-project boards
    - Attribution: each issue assigned to its MOST RECENT closed team-matching sprint (no resolutiondate comparison, no rollover double-counting)
    - Take last 3 sprints sorted by completeDate descending
    - velocity_avg = total SP / ACTUAL sprints found (1, 2, or 3 - NOT always 3)
    - velocity_avg is 1-decimal float (e.g., 31.5), not integer
    - Fallback if closedSprints() fails: use `statusCategory = Done AND updated >= -12w`
    - Velocity queries use the same API response structure as backlog queries:
      issues at `result.issues.nodes`, pagination via `issues.pageInfo.hasNextPage`
      and `issues.pageInfo.endCursor` passed as `nextPageToken` parameter.

13. **Threshold is >= 75% for DoR "ready" classification.**

14. **Orphan detection:**
    - Log warning for issues matching old "Polonium" (exact string) pattern in RSW project
    - These belong to the removed "Polonium LF" team
    - Exclude from all team counts - do not assign to any team

15. **No Background Agents (STRICT - NO EXCEPTIONS):**
    - This skill NEVER uses the Agent tool - not for "fresh context", not for
      "parallel work", not for any reason
    - If context feels full: offload to files via Python, then continue
    - The pattern "launch agent -> wait for result -> continue" is ALWAYS
      slower than "offload to disk -> continue in main"
    - All MCP calls are made directly from the main session
    - Parallel MCP calls (multiple in one message) provide concurrency
    - Python scripts handle ALL data processing
    - This design saves ~300K+ tokens per run and reduces execution time by 60%
    - VIOLATION OF THIS RULE invalidates the entire scan run

16. **Context Window Management:**
    - After each MCP batch response, immediately offload results to files via Python
    - Do NOT accumulate raw API responses across multiple batches in conversation context
    - Python processing scripts read from disk, not from conversation history
    - This prevents context exhaustion during large scans (15 teams, 10+ projects)
