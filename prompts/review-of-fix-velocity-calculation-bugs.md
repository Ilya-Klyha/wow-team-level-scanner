# Senior Engineering Review: fix-velocity-calculation-bugs.md

**Review date:** 2026-07-17
**Reviewers:** Architecture, Backend, Data Engineering, QA
**Reviewed artifact:** `prompts/fix-velocity-calculation-bugs.md`

---

## Executive Summary

The prompt correctly identifies two real bugs and proposes reasonable fixes. Bug 1 (cross-project contamination) is well-diagnosed with a simple, correct fix. Bug 2 (post-sprint completions) is correctly diagnosed but the proposed fix (Greenhopper API) has significant feasibility risks that are not adequately addressed. The prompt also misses several additional bugs discovered during our codebase analysis that affect the same velocity pipeline.

**Overall assessment: 7/10** - Good root cause analysis, incomplete solution design.

---

## Part 1: Strengths of the Prompt

### 1.1 Bug 1 Analysis - Excellent

- Root cause is precisely identified with specific issue keys (PEA-4234)
- Evidence includes exact SP delta (32 vs 31)
- The fix (project key filter) is minimal, targeted, and correct
- The code snippet provided is directly implementable

### 1.2 Bug 2 Analysis - Good Diagnosis

- The "blind spot" in most-recent-sprint attribution is correctly identified
- The 73 SP vs 50 SP discrepancy is clearly documented
- The explanation of WHY it happens (issues completed after sprint close, never rolled forward) is accurate

### 1.3 Bug 3 (Cleanup) - Well-Scoped

- The "1-5% accuracy" claim falsification is well-evidenced (actual error ~46% for Sprint 19: 73/50)
- The line-by-line cleanup table is actionable
- Implementation order is logical (fix first, clean up after)

---

## Part 2: Weaknesses and Critiques

### 2.1 CRITICAL: Greenhopper API Feasibility is Unresolved

The prompt recommends the Greenhopper sprint report API as the primary fix for Bug 2, but:

1. **The MCP Atlassian plugin does NOT expose arbitrary REST endpoints.** The available tools are a fixed set (`searchJiraIssuesUsingJql`, `getJiraIssue`, etc.). There is no generic "call any Jira REST endpoint" tool. The prompt acknowledges this possibility ("If MCP tools don't support arbitrary REST calls...") but does not resolve it before recommending the approach.

2. **Greenhopper API (`/rest/greenhopper/1.0/`) is an internal/legacy API** on Jira Cloud. It is NOT documented in the official Jira Cloud REST API reference. While it often still works, Atlassian has deprecated it in favor of the Agile REST API (`/rest/agile/1.0/`). Relying on it introduces fragility.

3. **The Agile REST API alternative (`/rest/agile/1.0/sprint/{sprintId}/issue`)** also does NOT distinguish completed-vs-incomplete issues. It returns all issues associated with a sprint. You would still need `statusCategory = Done` filtering, which has the same blind spot.

4. **The prompt should have tested API accessibility BEFORE recommending it.** A simple spike (attempting the call via available MCP tools or `gh api` equivalent) would have resolved this ambiguity.

**Recommendation:** The prompt should present a more concrete decision tree:
- Step 1: Attempt Greenhopper API call via available tools (specify HOW)
- Step 2: If unavailable, specify the concrete fallback algorithm, not vague alternatives
- Step 3: Document the accepted accuracy gap if no API access

### 2.2 CRITICAL: The Prompt Misses a Viable JQL-Based Solution

There IS a JQL function that solves Bug 2 without needing the Greenhopper API:

```jql
project = MAW 
AND sprint = 30218 
AND statusCategory = Done 
AND status WAS NOT IN ("Done", "Closed") BEFORE "2026-06-17"
AND status WAS IN ("Done", "Closed") BEFORE "2026-07-01"
```

The `status WAS` / `status WAS NOT` JQL functions query the issue changelog server-side. Combined with the sprint's `startDate` and `completeDate` (both available in the sprint object), this can identify issues that transitioned to Done DURING the sprint window.

**However**, this approach requires:
- JQL `status changed` or `status WAS` functions to be available (they are on Jira Cloud)
- One query per sprint (6-9 queries for 3 sprints x 2-3 teams per project)
- The sprint start/end dates (already available in `customfield_10115`)

This is a better fit for the current architecture (JQL-based, works with existing MCP tools) than an API that may not be accessible.

### 2.3 MAJOR: Bug 1 Fix May Be Wrong Direction

The prompt proposes filtering OUT cross-project issues. But consider:

- Bigos team operates a **cross-project board** (boardId 11439) that intentionally pulls PEA and RSW issues
- The Confluence page says MAW is the "single project for Bigos" — but Bigos's ACTUAL work spans PEA and RSW
- If the team's real velocity includes PEA/RSW work, filtering it out would UNDERCOUNT velocity

**The real question is:** Does the Jira sprint report for "Bigos Sprint 20" (the one you compare against showing 31 SP) include or exclude PEA-4234?

If the sprint report shows 31 SP (excluding PEA-4234), then the project filter is correct.
If the sprint report shows 32 SP (including PEA-4234), then the current algorithm is correct and the "expected 31 SP" assumption is wrong.

**The prompt assumes the answer without verifying.** The validation section should explicitly include checking the Jira sprint report's actual number.

### 2.4 MAJOR: Missing Bugs Not Addressed

The codebase analysis revealed additional bugs in the same velocity pipeline that the prompt does not address:

#### Missing Bug A: No Issue-Level Deduplication

The `calculate_velocity.py` (July 17) has no deduplication. If pagination produced overlapping results, or if a `toolu_*.txt` file duplicates data from a timestamped file, issues are double-counted. The July 16 implementation had `seen_keys = set()` but it was removed in the July 17 rewrite.

**Impact:** Potential over-counting of SP for any team.

#### Missing Bug B: SPRINT_NAME_PATTERNS Mismatch Between Spec and Implementation

The skill spec says:
```javascript
"ML Serving Sturgeons": /sturgeons/i,
"ML Platform Pandas": /pandas/i,
```

But actual implementations use:
```python
"ML Serving Sturgeons": re.compile(r"ml.?serving", re.IGNORECASE),
"ML Platform Pandas": re.compile(r"ml.?platform", re.IGNORECASE),
```

If sprint names are "ML Serving Sprint 5" the implementation matches but the spec wouldn't. If sprint names are "Sturgeons Sprint 5" the spec matches but implementation wouldn't. This inconsistency means a future implementation following the spec literally will produce different results.

#### Missing Bug C: `toolu_*.txt` Loading Has No Temporal Fence

Pass 2 of `load_velocity_issues()` loads ALL `toolu_*.txt` files matching the URL pattern, with no timestamp filter. While session-specific paths prevent cross-session contamination, within a single session, if velocity queries were re-run (e.g., after a failure), older results would be pooled with newer ones.

### 2.5 MINOR: The "1-5% Accuracy" Claim Falsification is Overstated

The prompt says the error is "~30% for Bigos Sprint 19" (73 vs 50 SP). But:

- This is the error for ONE sprint of ONE team
- The "1-5%" claim in the spec likely referred to the average across all teams/sprints
- Bug 2 specifically affects teams that leave incomplete work in sprints without rolling it forward — this may be rare for most teams
- The claim should be challenged, but calling it "demonstrably false" based on one data point is not rigorous

A proper falsification would require checking the discrepancy across all 15 teams x 3 sprints = 45 data points.

### 2.6 MINOR: Implementation Order Should Include a Spike

The proposed order is:
1. Bug 1 fix
2. Bug 2 investigation
3. Bug 2 fix
4. Bug 3 cleanup

Better order:
1. **Spike: Verify Jira sprint report numbers** for Bigos Sprint 19/20 (confirms Bug 1 and Bug 2 expected values)
2. **Spike: Test Greenhopper API accessibility** via MCP tools
3. Bug 1 fix (project filter)
4. Bug 2 fix (based on spike results: Greenhopper, JQL `status WAS`, or documented limitation)
5. Add deduplication (Missing Bug A)
6. Fix SPRINT_NAME_PATTERNS spec/code mismatch (Missing Bug B)
7. Bug 3 cleanup (update spec to match new approach)

---

## Part 3: Proposed Better Alternatives

### 3.1 Bug 2 Fix: JQL `status changed` Approach (Primary Recommendation)

Replace the "most recent sprint" attribution with a per-sprint JQL query that uses temporal status filtering:

```jql
sprint = {sprintId} 
AND statusCategory = Done 
AND status changed to ("Done") DURING ("{sprintStartDate}", "{sprintCompleteDate}")
```

**Advantages:**
- Works with existing MCP tools (`searchJiraIssuesUsingJql`)
- Server-side evaluation — no client-side guessing about completion time
- No dependency on undocumented/deprecated APIs
- Directly answers "what was completed during this sprint window"

**Disadvantages:**
- Requires `status changed` JQL function (available on Jira Cloud, needs verification on this instance)
- One query per sprint (manageable: 3 sprints per team x ~6 unique projects = ~18 queries)
- May not handle "Done" statuses with different names (need to verify the status name)

**Implementation in the skill:**

```
For each team:
  1. Identify the last 3 closed sprints (from any issue's customfield_10115 that matches team pattern)
  2. For each sprint, query:
     sprint = {sprintId} AND statusCategory = Done 
     AND status changed to Done DURING ("{startDate}", "{completeDate}")
     AND project = {teamProject}
     AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task
  3. Sum customfield_10200 from results
  4. velocity_avg = total / sprints_used
```

### 3.2 Bug 2 Fix: Hybrid Approach (If `status changed` Unavailable)

If JQL `status changed` is not supported or unreliable:

1. Keep current "most recent sprint" attribution as base
2. Add a **"no forward sprint" heuristic**: An issue attributed to Sprint N is ONLY counted if:
   - It appears in Sprint N (most recent closed matching sprint), AND
   - Sprint N+1 exists and is also closed (i.e., we're not looking at the most recent sprint)
   - OR Sprint N IS the most recently closed sprint for this team

The logic: if Sprint 20 closed and you're still attributed to Sprint 19, you were clearly NOT completed in Sprint 19 (otherwise you'd have been rolled or simply wouldn't exist as Done-in-Sprint-19 with Sprint-20-already-closed). This catches the exact scenario described in Bug 2.

```python
# After building sprint_map, for each team:
# Get sorted sprints (newest first)
sorted_sprints = sorted(sprint_map.values(), key=lambda s: s['completeDate'], reverse=True)

# The NEWEST sprint is always "current" -- items there are fine
# For older sprints (position 1, 2, ...): items attributed there that are NOT 
# in any newer sprint were likely completed post-close
# But we can't distinguish without changelog...
```

Actually, this doesn't fully work because the issue may have been completed between Sprint 19 close and Sprint 20 START (a valid scenario). The `status changed DURING` JQL approach is cleaner.

### 3.3 Bug 2 Fix: Greenhopper API (Conditional)

Keep as a FALLBACK, not primary. Add explicit verification step:

```
Step 1: Test if the following call works via available MCP tools:
  GET https://samsung-sbt.atlassian.net/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=11439&sprintId=30218

If accessible: use completedIssues from response
If not accessible: fall back to JQL "status changed" approach
If neither works: document limitation and accept current algorithm with known ~10-30% overcount for teams with poor sprint hygiene
```

---

## Part 4: Comprehensive Test Plan

### 4.1 Pre-Implementation Validation (Spikes)

| # | Test | Expected Result | Purpose |
|---|------|-----------------|---------|
| S1 | Query Jira sprint report UI for Bigos Sprint 19 | Shows 50 SP completed | Confirms Bug 2 expected value |
| S2 | Query Jira sprint report UI for Bigos Sprint 20 | Shows 31 SP completed (not 32) | Confirms Bug 1 expected value |
| S3 | Test JQL `status changed to Done DURING ("2026-06-17", "2026-07-01") AND sprint = 30218 AND project = MAW` | Returns subset of Sprint 19 issues | Validates JQL approach feasibility |
| S4 | Attempt Greenhopper API call via MCP or direct REST | Success or 403/404 | Determines primary vs fallback approach |
| S5 | Check PEA-4234 in Jira Sprint 20 report | Present or absent | Confirms whether project filter is correct behavior |

### 4.2 Bug 1 Tests (Project Filter)

| # | Test | Input | Expected | Verification |
|---|------|-------|----------|--------------|
| B1.1 | Bigos Sprint 20 excludes PEA issues | All velocity issues from MAW + PEA | Sprint 20 SP = 31 (excludes PEA-4234's 1 SP) | Compare with Jira sprint report |
| B1.2 | Bigos Sprint 15-17 excludes PEA/RSW issues | All velocity issues | Sprint 15 = 0 SP from MAW (all were PEA/RSW), Sprint 16 = 0, Sprint 17 = 0 | These sprints should have only MAW-364 (13 SP) attributed to Sprint 18 |
| B1.3 | Teams in shared projects unaffected | AENW project (Europium + Radium) | Each team's issues correctly filtered by team field, no cross-team contamination | Europium and Radium have distinct team field values |
| B1.4 | Single-project teams unaffected | AETVP (Copernicium only) | No change in velocity | Regression check |
| B1.5 | PROJECT_TEAMS mapping used correctly | Dynamic mapping from Step 8B | Filter uses the mapping built from board URLs, not hardcoded | Verify script reads from dynamic source |

### 4.3 Bug 2 Tests (Post-Sprint Completion Exclusion)

| # | Test | Input | Expected | Verification |
|---|------|-------|----------|--------------|
| B2.1 | Bigos Sprint 19 matches Jira report | Sprint 19 issues | 50 SP (not 73) | Direct comparison with Jira UI sprint report |
| B2.2 | Rolled issues still attributed to later sprint | MAW-437, MAW-435, MAW-439 (in both Sprint 19 and 20) | Attributed to Sprint 20 (26 SP) | These have Sprint 20 as most recent closed sprint |
| B2.3 | Issues completed after sprint close excluded | Issues in Sprint 19, Done after Jul 1, no Sprint 20 | NOT counted in Sprint 19 velocity | The 23 SP difference |
| B2.4 | Issues completed during sprint counted | Issues in Sprint 19, Done before Jul 1 | Counted in Sprint 19 velocity | The 50 SP |
| B2.5 | Team with good sprint hygiene unaffected | Team where all items complete during sprint or roll forward | Same velocity as before | Regression check on e.g., Europium |
| B2.6 | Edge case: issue completed same day as sprint close | Done on 2026-07-01 05:00 UTC, sprint closed 2026-07-01 05:04 UTC | Included (completed before close) | Time boundary precision |
| B2.7 | Edge case: issue completed 1 hour after sprint close | Done on 2026-07-01 06:00 UTC, sprint closed 05:04 UTC | Excluded (completed after close) | Time boundary precision |

### 4.4 Integration Tests (Full Pipeline)

| # | Test | Verification Method |
|---|------|-------------------|
| I1 | Full scan produces valid velocity_data.json | Schema validation against spec (Step 9C.6) |
| I2 | All 15 teams have velocity data (or documented null) | Check each team has an entry |
| I3 | Sprint details include correct fields | Each sprint has name, completeDate, sp_completed, issues_completed |
| I4 | Velocity avg computed correctly | Manual check: sum(sprint SP) / count(sprints) for 2-3 teams |
| I5 | Sprint runway correctly derived | velocity_avg > 0 implies runway = dor_ready_sp / velocity_avg |
| I6 | No duplicate issues counted | Add logging: unique issue keys per sprint == total issue count |
| I7 | Cross-validate with Jira sprint reports for 3+ teams | Compare velocity_data.json values with Jira UI for Bigos, Europium, Wolves |

### 4.5 Regression Tests

| # | Test | Risk |
|---|------|------|
| R1 | Teams with 0 SP in recent sprints still get velocity_avg = 0 (not null) | SP=0 vs no-data distinction |
| R2 | Teams with < 3 closed sprints get correct avg (divide by actual count) | Division denominator |
| R3 | New team added to Confluence page gets null velocity (no SPRINT_NAME_PATTERNS entry) with warning | Graceful degradation |
| R4 | Sprint with no matching name pattern logged as warning | Pattern matching edge cases |
| R5 | Issues with null SP contribute 0 to total but increment issue_count | Null handling |
| R6 | 12-week cutoff correctly excludes old sprints | Time boundary |

### 4.6 Performance/Scale Tests

| # | Test | Acceptance Criteria |
|---|------|-------------------|
| P1 | Total API calls for velocity (if using per-sprint queries) | <= 50 calls total (15 teams x 3 sprints, with project dedup) |
| P2 | Pagination handles > 100 issues per sprint query | All pages fetched |
| P3 | Full velocity calculation completes within session limits | No timeout or token exhaustion |

---

## Part 5: Additional Recommendations

### 5.1 Add Deduplication to the Script

```python
seen_issue_keys = set()
for issue in all_issues:
    key = issue.get("key")
    if key in seen_issue_keys:
        continue
    seen_issue_keys.add(key)
    # ... rest of processing
```

### 5.2 Fix SPRINT_NAME_PATTERNS in Skill Spec

Update the spec to match the working implementations:
```javascript
"ML Serving Sturgeons": /ml.?serving/i,   // NOT /sturgeons/i
"ML Platform Pandas": /ml.?platform/i,     // NOT /pandas/i
```

### 5.3 Add Diagnostic Logging

The velocity script should output a diagnostic summary for each team showing:
- Issues loaded (total, by project)
- Issues after team filter
- Issues after sprint attribution
- Issues excluded by project filter (new)
- Issues excluded by post-sprint-completion filter (new)
- Final SP per sprint

This makes future debugging trivial.

### 5.4 Document the "Sprint Hygiene" Factor

Some teams complete work after sprint close without rolling it forward. This is a process issue (not a tool bug). The skill should:
- Log when it detects this pattern
- Report it as a data quality observation in the output
- NOT silently inflate velocity

---

## Part 6: CONFIRMED — Bug 2 Root Cause Clarified

### User Verification (2026-07-17)

The user confirmed via the Jira sprint report UI at:
`https://samsung-sbt.atlassian.net/jira/software/c/projects/MAW/boards/11439/reports/sprint-retrospective?sprint=30218`

**Confirmed facts:**
- Sprint report shows **50 SP completed** (in-sprint)
- **23 SP shown as "Completed outside of sprint"** — these are issues that were in Sprint 19 but completed AFTER the sprint was closed (team process mistake)
- MAW-469, MAW-490, MAW-503 had SP **changed from 0 to 1 SP** after sprint close (SP re-estimation)

### Spike Test S3 Explained

Our JQL `status changed to "Done" DURING ("2026-06-17", "2026-07-01")` returned all 13 issues because it uses calendar-day boundaries (not precise timestamps). The sprint closed on July 1 at 05:04 UTC — issues completed later that same day (after 05:04) still match the `DURING` clause but are NOT counted by Jira's sprint report as "completed in sprint."

**Key insight:** Jira's sprint report uses a point-in-time snapshot at the exact `completeDate` timestamp (2026-07-01T05:04:23.549Z), not a calendar-day boundary. The `DURING` JQL operator is too coarse for this distinction.

### Revised Assessment

| Original Review Concern | Resolution |
|------------------------|------------|
| "Bug 2 may not be a bug" | CONFIRMED as a real bug. 23 SP genuinely completed outside sprint. |
| "The user's 50 SP needs verification" | Verified. 50 SP is the correct sprint velocity. |
| "SP re-estimation" concern | Confirmed: 3 issues had SP changed (0 -> 1 SP each = 3 SP impact) |
| "JQL `status changed DURING` as alternative" | Insufficient — uses calendar-day boundaries, not sprint close timestamp |

### Updated Verdict on Bug 2

**The bug is REAL and the original prompt's diagnosis is CORRECT.** The fix needs to distinguish issues completed before vs after the sprint's exact `completeDate` timestamp. The Greenhopper API remains the most accurate solution (it provides this exact snapshot). The `status changed DURING` JQL fallback needs to use the exact `completeDate` timestamp, not just the date.

---

## Part 7: Conclusion (Updated After User Verification)

Both bugs are confirmed real. The prompt's analysis is correct.

**Verdict: Approve with additions.**

- **Bug 1**: Approve and implement (project filter). Simple, correct, low-risk.
- **Bug 2**: Approve. Root cause confirmed — 23 SP completed outside sprint. Recommended fix: Greenhopper API via direct Python HTTP call (bypasses MCP limitation). Fallback: JQL with precise `completeDate` timestamp (not calendar-day `DURING`).
- **Bug 3 (cleanup)**: Approve. The "1-5% accuracy" claim is false (actual error ~46%). Remove and update spec.
- **Additional fixes** (discovered during review, should be included):
  - Add issue-level deduplication (`seen_keys` set)
  - Fix SPRINT_NAME_PATTERNS spec/code mismatch (`/sturgeons/i` vs `r"ml.?serving"`)
  - Address `toolu_*.txt` temporal fence gap

**Recommended implementation order:**
1. Bug 1 fix (project filter) — immediate, low-risk
2. Add deduplication — immediate, low-risk
3. Fix SPRINT_NAME_PATTERNS in skill spec — immediate, spec-only
4. Bug 2 fix (Greenhopper API or timestamp-precise JQL) — requires credential setup
5. Bug 3 cleanup — update spec after fixes are validated

**Validation checklist:**
- Bigos Sprint 19: 50 SP (not 73)
- Bigos Sprint 20: 31 SP (not 32)
- No regression for other teams (spot-check Europium, Wolves)
- No duplicate issue counting across all teams
