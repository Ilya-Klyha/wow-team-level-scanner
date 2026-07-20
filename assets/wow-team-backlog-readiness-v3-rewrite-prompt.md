# Skill Rewrite Prompt: wow-team-backlog-readiness v3.0

## Objective

Rewrite the "Agent and Bash Execution Rules" section and related execution model in `.claude/skills/wow-team-backlog-readiness/skill.md` to eliminate background agents entirely. Replace with a sequential main-session architecture that uses parallel MCP calls and Python processing scripts.

## Problem Statement

The current v2.0 skill has an "Agent and Bash Execution Rules" section that was added to prevent a Windows Git Bash race condition (`add_item` fatal error, exit code 5). This rule:
- Bans background agents from using Bash
- Bans the main session from calling Bash while agents are running
- Forces "temporal separation" between API fetching and data processing

### Measured Impact (2026-07-16 run)

| Metric | Current (v2.0 with agents) | Expected (no agents) |
|--------|---------------------------|---------------------|
| Total execution time | 35+ minutes | 10-15 minutes |
| Token consumption (agents) | ~391,000 tokens | 0 (agents eliminated) |
| Token consumption (total) | ~450K+ (agents + main session) | 80-150K (main session only) |
| Agent reliability | 2/3 agents failed or hit limits | N/A |
| Backlog agent | 213K tokens, died without output | N/A |
| DoR agent | Hit 429 budget limit at 353 tokens in | N/A |
| Velocity agent | 178K tokens, 18 min for work doable in 3 min | N/A |
| Main session idle time | ~15 min waiting for agents | 0 |
| Fallback recovery work | Main session redid all backlog queries | N/A |

### Why Agents Fail for This Workload

1. **Context bloat**: Each Jira API response is 140-250KB. An agent reading those into its context burns tokens at 10-50x the rate of the main session (which can save results to files and process with Python).

2. **No Python access**: Agents banned from Bash cannot process data. They can only fetch and save. But the main session must wait idle during this time, then do all processing anyway.

3. **Unreliable**: Agents hit budget limits, time out, fail to write output files, or produce incomplete data. Every failure requires the main session to redo the work sequentially - the exact thing agents were supposed to avoid.

4. **The race condition is rare and narrow**: The `add_item` bash error only occurs when multiple `bash.exe` processes start simultaneously on Windows (MSYS2 shared memory init). MCP calls are NOT bash processes. The main session making sequential Python script calls has zero risk.

5. **No parallelism gain**: MCP calls can already be parallelized in a single message (multiple tool uses). This gives the same throughput as agents without the overhead.

## What to Change

### DELETE entirely:

1. The "Agent and Bash Execution Rules" section (lines ~64-107 in current skill.md)
2. The "Agent Failure Recovery" section
3. The "Bash Failure Safety Net" section
4. All references to background agents in Step 9.3 (Phase 1/2/3 agent delegation)
5. The "Agent-specific tool restrictions" in Tool Requirements section
6. The `CONSTRAINT: Do NOT use the Bash tool` pattern references
7. Step 9C.0.1 "Velocity Execution Priority" section (ordering is natural in sequential model)

### REPLACE WITH:

A new section called "Execution Model" that describes:

```markdown
### Execution Model - Sequential with Parallel MCP Calls

This skill executes entirely in the main session. No background agents are spawned.

**Architecture:**
1. MCP calls for data fetching (use parallel tool calls where independent)
2. Save large API responses to files (they auto-save when exceeding inline limits)
3. Python scripts for all data processing, filtering, and calculation
4. Python scripts for report generation

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

**Bash error resilience:** If a Bash call fails with exit code 5 containing "add_item", retry once after `sleep 3`. This is a Windows MSYS2 edge case that occurs rarely and only under unusual system load.
```

### REWRITE Step 9.3 execution model:

Current: Complex Phase 1/2/3 with agent delegation, waiting, fallback recovery.

New simplified version:

```markdown
#### Step 9.3: Execute Queries with Pagination

For each unique project in PROJECT_TEAMS, query backlog items using MCP calls from the main session.

**Execution:**
1. Issue first-page queries for ALL projects (batch 5-6 per message, parallel MCP calls)
2. Save response files, check `isLast` and `nextPageToken` for each
3. For projects needing page 2+: issue pagination queries (batch by page number)
4. Continue until all projects have `isLast: true` or cap at 10 pages
5. Run `combine_backlog.py` to merge all pages into `backlog_raw.json`
6. Run `process_backlog.py` to filter by team and generate `backlog_data.json`

**Response handling:** Large API responses (>100KB) are automatically saved to tool-results files. The Python combine script reads these files directly. No need to read them into conversation context.

**Context offloading:** After each batch of MCP responses is received, immediately write a Python script to extract and save the needed fields to disk. Do NOT hold raw API responses in conversation context across multiple batches. This prevents context window exhaustion when processing 10+ projects with pagination.
```

### REWRITE Step 9C.1 velocity execution:

Same pattern - main session makes MCP calls, Python script processes:

```markdown
#### Step 9C.1: Query Completed Work

Issue velocity queries for ALL projects (batch 5-6 per message, parallel MCP calls).
Paginate same as backlog queries.
Save combined results to `velocity_raw.json`.
Run `process_velocity.py` to calculate per-team velocity.
```

### REWRITE Step 7 (team page fetches for DoR):

```markdown
#### Step 7: Fetch Team Names and Page Content

Issue getConfluencePage calls for all 15 team pages (batch 5 per message, 3 messages).
Save each page body to `dor_page_{N}.html` via a Python script that processes the tool-result files.
Extract team names from page titles.
```

### UPDATE Tool Requirements section:

Remove "Agent-specific tool restrictions" and replace with:

```markdown
**Execution model:** All work runs in the main session. No background agents.
- MCP tools: parallel calls for data fetching
- Bash: Python script execution (sequential, never concurrent)
- Write: save inline API results, create Python scripts
- Read/Grep: check files, extract pagination tokens
```

### ADD to Important Rules:

```markdown
15. **No Background Agents:**
    - This skill does NOT use the Agent tool
    - All MCP calls are made directly from the main session
    - Parallel MCP calls (multiple in one message) provide concurrency without agent overhead
    - Python scripts handle ALL data processing
    - This design saves ~300K+ tokens per run and reduces execution time by 60%

16. **Context Window Management:**
    - After each MCP batch response, immediately offload results to files via Python
    - Do NOT accumulate raw API responses across multiple batches in conversation context
    - Python processing scripts read from disk, not from conversation history
    - This prevents context exhaustion during large scans (15 teams, 10+ projects)
```

## Expected Outcome After Rewrite

| Metric | Before (v2.0) | After (v3.0) |
|--------|---------------|--------------|
| Execution time | 35+ min | 10-15 min |
| Token consumption | ~400K+ (agents) + main session | Main session only (80-150K depending on backlog size) |
| Reliability | 2/3 agents failed | No agents = no agent failures |
| Complexity | Complex temporal separation rules | Simple sequential pipeline |
| Pagination handling | Agent must paginate without Python | Main session paginates with cursor extraction |
| Skill spec size | Very large (agent rules + recovery) | Smaller (removed ~100 lines of agent rules) |

## Constraints on the Rewrite

1. **Do NOT change the data logic** - JQL queries, team patterns, field IDs, velocity calculation, DoR extraction algorithm, report schema all stay identical
2. **Do NOT change output file formats** - All JSON schemas, Excel schema, HTML dashboard remain the same
3. **Do NOT change the processing Python scripts** - `process_backlog.py`, `process_velocity.py`, `process_dor.py`, `process_compliance.py`, `generate_backlog_report.py` templates are canonical
4. **DO remove all agent-related instructions** - No Agent tool, no temporal separation, no "agent must not use Bash"
5. **DO add parallel MCP call batching guidance** - How many calls per message, how to handle response files
6. **DO keep the "Bash Failure Safety Net" as a one-liner** - Just "retry once after sleep 3 on exit code 5" - not the elaborate agent-avoidance architecture
7. **DO add context window management rule** - Offload API responses to files immediately after each batch; Python scripts read from files, not conversation history
8. **DO add progress reporting** - Output `[PROGRESS]` lines after each major phase completes

**NOTE:** The ML team sprint name pattern bug (`sturgeons` -> `ml.?serving`, `pandas` -> `ml.?platform`) found during the 2026-07-16 run is a DATA LOGIC fix and should be addressed in a separate, focused change -- not mixed into this architectural rewrite. This keeps the rewrite purely structural and simplifies regression testing.

## Files to Modify

- `.claude/skills/wow-team-backlog-readiness/skill.md` - Main skill specification (the only file to change)

## Verification After Rewrite

### Phase 1: Structural Validation (before execution)

| # | Check | Method | Pass Criteria |
|---|-------|--------|---------------|
| 1.1 | No agent references | `grep -i "background agent\|Agent tool\|spawn agent" skill.md` | Zero matches |
| 1.2 | No temporal separation | `grep -i "temporal" skill.md` | Zero matches |
| 1.3 | Parallel MCP guidance present | `grep -i "parallel.*mcp\|batch.*mcp" skill.md` | At least 3 occurrences |
| 1.4 | Execution model section | `grep "Execution Model" skill.md` | Section exists |
| 1.5 | No CONSTRAINT pattern | `grep "CONSTRAINT: Do NOT use Bash" skill.md` | Zero matches |
| 1.6 | Context management rule | `grep -i "context.*management\|offload.*file" skill.md` | Present |
| 1.7 | Progress reporting rule | `grep "PROGRESS" skill.md` | Present |
| 1.8 | Rule 15 exists | `grep "No Background Agents" skill.md` | Present |
| 1.9 | Rule 16 exists | `grep "Context Window Management" skill.md` | Present |
| 1.10 | Data logic unchanged | Compare JQL templates, field IDs, TEAM_NAME_PATTERNS | Identical to v2.0 |
| 1.11 | Output schemas unchanged | Compare JSON schema definitions | Identical to v2.0 |
| 1.12 | File size reduced | `wc -l skill.md` | < 1750 lines (down from ~1860) |

### Phase 2: Functional Validation (full execution)

Run `/wow-team-backlog-readiness` and verify:

| # | Check | Pass Criteria |
|---|-------|---------------|
| 2.1 | No Agent tool calls | Zero Agent tool invocations during run |
| 2.2 | MCP calls batched | Multiple MCP calls per message (2+ for project queries) |
| 2.3 | Python handles processing | All data processing via `python3 *.py` Bash calls |
| 2.4 | No concurrent bash | Never more than 1 Bash call per message |
| 2.5 | Context offloading | API results saved to files after each batch |
| 2.6 | Progress lines emitted | `[PROGRESS]` output after each major phase |
| 2.7 | 15 teams discovered | `teams.json` has `team_count: 15` |
| 2.8 | Backlog data populated | `backlog_data.json` non-empty |
| 2.9 | Velocity data populated | `velocity_data.json` has 10+ teams with non-null velocity |
| 2.10 | DoR criteria extracted | `dor_criteria.json` has 15 entries |
| 2.11 | Reports generated | `Report-backlog.xlsx` and `.html` exist |
| 2.12 | Validation passes | `validate_backlog_report.py` exits with code 0 |

### Phase 3: Performance Validation

| # | Check | Pass Criteria |
|---|-------|---------------|
| 3.1 | Execution time | < 20 minutes wall-clock |
| 3.2 | Token consumption | < 200K total (target: 80-150K) |
| 3.3 | No timeout errors | Zero 429/timeout responses or graceful recovery |
| 3.4 | No bash exit code 5 | Zero occurrences |
| 3.5 | Full pagination | All projects reach `hasNextPage: false` |

### Phase 4: Regression Check (compare against v2.0 baseline)

| # | Check | Pass Criteria |
|---|-------|---------------|
| 4.1 | Same team set | Identical 15 team names |
| 4.2 | Similar backlog counts | Within +/- 10% per team (real-time variance) |
| 4.3 | Same output file set | Identical file names in output directory |
| 4.4 | Velocity values reasonable | Within +/- 20% of v2.0 baseline |
| 4.5 | No data loss | Total backlog items within 5% of v2.0 |

### Acceptance Criteria

The v3.0 rewrite is accepted when ALL of:
1. All Phase 1 structural checks pass
2. All Phase 2 functional checks pass
3. Phase 3.1 passes (< 20 minutes)
4. Phase 3.2 passes (< 200K tokens)
5. `validate_backlog_report.py` passes with 0 errors
6. At least 12/15 teams have complete data (backlog + velocity + runway)
