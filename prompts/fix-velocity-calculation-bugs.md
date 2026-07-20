# Fix Velocity Calculation Bugs in wow-team-backlog-readiness Skill

## Context

Analysis date: 2026-07-17
Affected skill: `.claude/skills/wow-team-backlog-readiness/skill.md` (Step 9C: Velocity Calculation)
Verified against: Bigos team, Sprint 19 and Sprint 20

## Bug 1: Cross-Project Issue Contamination

### Problem

The velocity calculation loads issues from ALL 11 Jira projects, then filters only by:
1. Team name field (`customfield_10114`) 
2. Sprint name pattern (regex match)

It does NOT enforce that counted issues belong to the team's designated project.

### Evidence

- Bigos team is mapped to project **MAW** (per Confluence SRPOL Teams page)
- But 162 PEA issues and 5 RSW issues also carry `customfield_10114 = "AS - WAW - Bigos"` and have "Bigos Sprint XX" in their sprint field
- **Sprint 20 result:** 32 SP reported (should be 31 SP). Extra 1 SP from PEA-4234 (PEA project, "DSP - App Insights - Missing Data") which carries "Bigos Sprint 20" on boardId 11439

### Root Cause

Bigos team operates a cross-project board (boardId 11439) that pulls issues from PEA and RSW into Bigos sprints. These foreign-project issues pass all current filters because they have the Bigos team field and Bigos sprint names.

### Fix

After team field matching, add a **project key filter**: only count issues whose `project.key` matches the team's designated project(s) from `PROJECT_TEAMS` mapping.

In the skill spec (Step 9C.2 or 9C.4), add:
```
For each issue attributed to a team, verify issue.fields.project.key is in the 
PROJECT_TEAMS mapping for that team. Discard issues from non-designated projects.
```

In the Python script, at line ~157 in `calculate_velocity()`:
```python
# After determining team, verify project matches
expected_projects = [k for k, teams in PROJECT_TEAMS.items() if team in teams]
if project_key not in expected_projects:
    continue
```

---

## Bug 2: "Completed Outside Sprint" Issues Incorrectly Counted as Sprint Velocity

### Problem

The algorithm counts ALL currently-Done issues attributed to a sprint, regardless of WHEN they became Done. Issues that were in Sprint 19 but completed AFTER the sprint closed (shown as "Completed outside of sprint" in Jira's sprint report) are incorrectly counted toward Sprint 19's velocity.

Additionally, the algorithm uses CURRENT story point values. Jira's sprint report uses SP values at the time of sprint close. Issues whose SP were changed after sprint close (e.g., from 0 to 1 SP) show inflated values in the algorithm.

### Evidence

- **Sprint 19 reported by algorithm:** 73 SP (13 issues)
- **Sprint 19 actual (Jira sprint report, confirmed 2026-07-17):** 50 SP completed
- **Difference:** 23 SP = issues "Completed outside of sprint" (team mistake — done after sprint close)
- **SP changes:** MAW-469, MAW-490, MAW-503 had SP changed from 0 to 1 SP each after sprint close
- **Sprint report URL:** https://samsung-sbt.atlassian.net/jira/software/c/projects/MAW/boards/11439/reports/sprint-retrospective?sprint=30218

These issues were never moved to Sprint 20 (their most recent closed sprint remains Sprint 19), so the "most recent sprint" attribution logic cannot distinguish them from issues genuinely completed during the sprint.

### Root Cause

Two sub-issues:

1. **Post-sprint completions counted:** The JQL `statusCategory = Done` checks current status, not historical status at sprint close time. The "most recent closed sprint" attribution method cannot detect WHEN an issue transitioned to Done relative to the sprint's close date.

2. **SP values not snapshotted:** The algorithm uses current `customfield_10200` values. Jira's sprint report snapshots SP at sprint close. Post-close SP re-estimations inflate the count.

### Important context on JQL `status changed DURING`

A spike test confirmed that `status changed to "Done" DURING ("2026-06-17", "2026-07-01")` returns the same 13 issues (73 SP). This is because the JQL uses CURRENT SP values and because issues completed outside the sprint DID have their status changed to Done during that calendar period — they just weren't completed before the sprint was closed (sprint closed on July 1 at 05:04 UTC; some issues were done after this timestamp but within the same calendar day).

The key distinction: Jira's sprint report considers an issue "completed in sprint" only if it was Done AT THE MOMENT the sprint was closed (a point-in-time snapshot), not just during the date range.

### Fix: Use Jira Sprint Report API (Greenhopper)

**Primary approach (recommended):** The Jira Greenhopper API provides a sprint report endpoint that returns pre-separated lists of completed vs incomplete issues as a point-in-time snapshot at sprint close:

```
GET /rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={boardId}&sprintId={sprintId}
```

Response structure:
```json
{
  "contents": {
    "completedIssues": [...],                      // Done AT THE MOMENT sprint was closed
    "issuesNotCompletedInCurrentSprint": [...],    // Still open when sprint closed
    "puntedIssues": [...],                         // Removed from sprint before close
    "issuesCompletedInAnotherSprint": [...],       // "Completed outside of sprint"
    "issueKeysAddedDuringSprint": {"MAW-503": true, ...}  // Mid-sprint additions (object, not array)
  }
}
```

Each issue in `completedIssues` includes TWO SP fields:
- `estimateStatistic.statFieldValue.value` — SP at sprint START (committed estimate)
- `currentEstimateStatistic.statFieldValue.value` — SP at sprint CLOSE (final estimate, used for velocity)

The velocity report companion endpoint:
```
GET /rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={boardId}
```
Returns pre-calculated velocity:
```json
{"velocityStatEntries": {"30218": {"estimated": {"value": 50.0}, "completed": {"value": 50.0}}}}
```

**Required data (already available in `customfield_10115` sprint objects):**
- `boardId`: 11439 (for Bigos) — the `boardId` field in sprint objects
- `sprintId`: e.g., 30218 (Sprint 19) — the `id` field in sprint objects

**API constraints:**
- Undocumented/internal API on Jira Cloud (no formal deprecation timeline, but no stability guarantees)
- Works with Basic Auth (email + API token) and OAuth 2.0
- Does NOT work with Connect add-ons or Forge apps
- The MCP Atlassian plugin does NOT expose arbitrary REST endpoints — this API CANNOT be called via `searchJiraIssuesUsingJql` or any other available MCP tool
- Must be called via direct HTTP request (e.g., `curl` with stored credentials)

**Implementation approach:**

1. During velocity data fetch (Step 9C.0.1), after identifying closed sprints per team via name patterns, call the sprint report endpoint for each sprint
2. For each team, get the last 3 closed sprints from the sprint field data (boardId and sprintId from `customfield_10115`)
3. For each sprint, call: `GET /rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={boardId}&sprintId={sprintId}`
4. Sum SP from `completedIssues` only (using `estimateStatistic.statFieldValue.value`)
5. Apply project filter from Bug 1 fix (exclude issues from non-designated projects)
6. This gives the exact same number as Jira's sprint report/velocity chart

**Fallback approach (if Greenhopper API unavailable):**

Since the MCP plugin cannot call Greenhopper directly, and `status changed DURING` JQL still uses current SP values (not snapshot), the practical fallback is:

1. **Exclude "completed outside sprint" heuristically:**
   - After attributing issues to sprints, check if the issue's `statusCategory` became "Done" BEFORE the sprint's `completeDate` timestamp
   - Use JQL: `sprint = {sprintId} AND status changed to "Done" BEFORE "{sprintCompleteDate}"` 
   - This approximates the sprint report's "completed in sprint" by using the exact `completeDate` timestamp as boundary (not just the date)

2. **Accept SP value discrepancy as known limitation:**
   - Document that current SP values are used (not historical snapshot)
   - Log when SP changes are detected (if changelog is fetched)
   - For the 3 SP difference in Sprint 19 (MAW-469/490/503 re-estimated from 0 to 1), this is minor

3. **Direct HTTP call via Python script:**
   - The velocity calculation already runs as a Python script post-fetch
   - Add direct `requests.get()` calls to the Greenhopper API using stored credentials
   - This bypasses MCP limitations entirely
   - Requires: Jira API token stored securely (e.g., environment variable or `.env` file)

**Recommended implementation path:**
1. First attempt: Direct HTTP call in Python script (most accurate, matches Jira UI exactly)
2. If no credentials available: Use `status changed to "Done" BEFORE "{completeDate}"` JQL as approximation
3. Document remaining SP-snapshot limitation in either case

---

## Bug 3 (Cleanup): Remove Dead resolutiondate References from Skill

### Problem

The skill spec contains extensive documentation about NOT using `resolutiondate` (lines 990-994, 1018, 1058, 1135, 1171, 1231, 1244, 1265, 1270, 1812-1813, 1817). While the warnings are correct, they:
1. Add significant noise to the spec
2. Reference a "1-5% accuracy" claim that is now proven wrong (actual error is ~30% for Bigos Sprint 19)
3. May confuse future implementations into thinking the current approach is accurate

### Fix

1. Remove all "produces values within 1-5% of Jira velocity chart" claims — this is demonstrably false
2. Consolidate the `resolutiondate` warnings into a single block at the top of Step 9C
3. Remove redundant repetitions of "resolutiondate is not used" throughout the spec
4. Update the method description to reflect the new sprint report API approach
5. Remove the old `calculateTeamVelocity` pseudocode (lines 1139-1227) and replace with the new API-based approach

### Specific lines to clean up in skill.md:

| Line(s) | Content | Action |
|---------|---------|--------|
| 935 | "within 1-5%" claim | Remove or replace with accuracy note |
| 990-994 | CRITICAL resolutiondate warning | Keep but simplify to 2 lines |
| 1018 | "Why NO resolutiondate field" | Keep as single line |
| 1058 | "Client-side time filtering (replaces JQL resolved >= -Xw)" | Simplify header |
| 1135 | "Avoids resolution-date comparison inaccuracies" | Remove |
| 1171 | "resolutiondate-based attribution (within 1-5% empirically)" | Remove — claim is false |
| 1231 | Repeated resolutiondate mention | Remove |
| 1244 | Edge case row about null resolutiondate | Keep but simplify |
| 1265 | Method description with resolutiondate mention | Rewrite for new approach |
| 1270 | sprint_attribution field | Update |
| 1812-1813 | Summary bullets about resolutiondate | Consolidate |
| 1817 | Attribution summary | Update |

---

## Implementation Order

1. **Bug 1 fix** (project filter) — Simple, low-risk, immediate improvement
2. **Bug 2 investigation** — Test Greenhopper sprint report API accessibility via MCP or direct REST call
3. **Bug 2 fix** — Implement sprint report API approach (or fallback)
4. **Bug 3 cleanup** — Update skill spec to reflect new approach, remove dead code/claims

## Validation

After fix, re-run velocity calculation for Bigos and verify:
- Sprint 19: 50 SP (matches Jira sprint report)
- Sprint 20: 31 SP (matches Jira sprint report, excludes PEA-4234)
- Velocity avg: (50 + 31 + Sprint18) / 3

Also spot-check 2-3 other teams to ensure no regression.
