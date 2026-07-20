# Backlog Readiness Scanner - Report Data Schemas (v2.0)

These schemas define the exact JSON format expected by `generate_backlog_report.py`.
The LLM produces these JSON files; Python renders the reports.

## backlog_data.json

Array of 0+ entries (one per backlog issue, sorted by team then issue_key):

```json
[
  {
    "team": "string - team display name from SRPOL Teams page",
    "issue_key": "string - Jira issue key (e.g., 'AENW-1234')",
    "issue_type": "Story | Bug | Task",
    "url": "string - full Jira URL (https://adgear.atlassian.net/browse/XXX-NNN)",
    "title": "string - issue summary/title from Jira",
    "status": "string - issue status (e.g., 'To Do', 'Backlog', 'Open')",
    "assignee": "string - display name or 'Unassigned'",
    "story_points": "number | null - numeric value or null if not estimated"
  }
]
```

Rules:
- Sorted by `team` (A-Z alphabetical by display name), then `issue_key` (ascending)
- `story_points: 0` is valid and counts as estimated (spikes, investigations)
- `story_points: null` means field is empty (counts as unestimated)
- No entries for teams with 0 backlog items (they are absent from this file)
- `issue_key` is globally unique across the entire array (no duplicates)
- Every entry has exactly 8 keys (no extras, no missing)
- `issue_type` must be one of: "Story", "Bug", "Task"
- `url` must start with `https://adgear.atlassian.net/browse/`
- `assignee` must be non-empty string (use "Unassigned" for null assignees)
- "Polonium UF" team displays as "Polonium" in this file

## summary_data.json

Array of exactly 15 entries (one per SRPOL team, sorted alphabetically by display name):

```json
[
  {
    "team": "string - team display name",
    "backlog_total": "integer - total backlog items for this team",
    "estimated": "integer - items with Story Points value (including 0)",
    "unestimated": "integer - items without Story Points (null)",
    "estimation_rate": "string - 'X%' (rounded to 0 decimal) or '-'",
    "total_story_points": "integer - sum of all Story Points for this team",
    "stories": "integer - count of Story-type issues",
    "bugs": "integer - count of Bug-type issues",
    "tasks": "integer - count of Task-type issues",
    "velocity_avg": "integer | null - average SP/sprint from last 3 sprints",
    "velocity_sprints_used": "integer - how many sprints used (0-3)",
    "velocity_sprints": "array - [{sprint_name, completed_sp}] last 3 sprints",
    "dor_found": "boolean - whether team has a DoR (heading found on page, regardless of whether criteria could be parsed)",
    "dor_checkable_criteria": "integer | null - count of criteria with heuristic checks (null if dor_found=false or Tier 2)",
    "dor_ready_count": "integer | null - estimated issues with DoR compliance >= 75% (null if Tier 2 or dor_found=false)",
    "dor_ready_sp": "integer | null - sum of SP from DoR-ready issues (null if Tier 2 or dor_found=false)",
    "dor_avg_compliance_pct": "integer | null - average compliance % across estimated issues (null if Tier 2 or dor_found=false)",
    "sprint_runway": "number | string - sprints of ready work (numeric), 'N/A' (DoR exists but unparseable OR no velocity data), or 'No DoR' (no DoR heading found)",
    "runway_status": "string - 'Healthy' | 'Attention' | 'Critical' | 'N/A' | 'No DoR'"
  }
]
```

Rules:
- Always exactly 15 entries sorted alphabetically by display name:
  Abyss, Bigos, Capybaras, Copernicium, EP Core, Europium, Igni, ML Platform Pandas, ML Serving Sturgeons, Mouflons, Polonium, Radium, SRE, Wolves, Zurek
- `backlog_total` = `estimated` + `unestimated` (arithmetic invariant)
- `estimation_rate`: "X%" where X = round(estimated / backlog_total * 100) if backlog_total > 0; "-" if backlog_total == 0
- Teams with extraction errors or no board get `backlog_total: 0`, `estimation_rate: "-"`
- `backlog_total`, `estimated`, `unestimated` are always non-negative integers (never null)
- "Polonium UF" internal name displays as "Polonium" in the `team` field
- New v2 fields (velocity_*, dor_*, sprint_runway, runway_status) are nullable for graceful degradation
- `velocity_sprints` array has 0-3 entries, each with `sprint_name` (string) and `completed_sp` (integer)
- `sprint_runway` is numeric when calculable, "N/A" (DoR exists but criteria unparseable for heuristic check, OR no velocity data), or "No DoR" (no DoR heading found for this team)
- `runway_status` thresholds: >= 3.0 "Healthy", >= 1.0 "Attention", < 1.0 "Critical"
- `runway_status` "N/A" = DoR exists but cannot be assessed heuristically, or no velocity data
- `runway_status` "No DoR" = team has no Definition of Ready at all (no heading found on team page)

## dor_criteria.json (NEW in v2)

Array of 15 entries (one per team):

```json
[
  {
    "team": "string - team display name",
    "dor_criteria": [
      {
        "name": "string - criterion name (e.g., 'User Story/Requirement Clarity')",
        "description": "string - criterion description text",
        "check_type": "ESTIMATE | ACCEPTANCE_CRITERIA | DEPENDENCIES | DESCRIPTION_QUALITY | DESIGN | MONITORING | PRIORITY | SCOPE | GENERIC"
      }
    ],
    "dor_source": "team_page | linked_page | not_found",
    "dor_found": "boolean",
    "checkable_criteria_count": "integer - criteria with check_type != GENERIC",
    "total_criteria_count": "integer - total criteria extracted"
  }
]
```

Rules:
- Always 15 entries, one per team
- Three-tier classification:
  - **Tier 1** (criteria parsed): `dor_found: true`, `dor_criteria: [...]`, `dor_source: "team_page" | "linked_page"`
  - **Tier 2** (heading found, no parseable criteria): `dor_found: true`, `dor_criteria: []`, `checkable_criteria_count: 0`, `dor_source: "team_page" | "linked_page"`
  - **Tier 3** (no heading found): `dor_found: false`, `dor_criteria: []`, `dor_source: "not_found"`
- Teams with `dor_found: true` and `dor_criteria: []` represent the case where a DoR heading was found on the team page (and optionally a linked page was followed) but no structured criteria could be extracted. These teams are NOT reported as "No DoR" -- they appear as "N/A" in the runway status.
- `check_type` assigned via keyword matching on criterion name
- GENERIC means criterion cannot be checked heuristically (always passes)

## dor_compliance_backlog.json (NEW in v2)

Array of 0+ entries (one per estimated issue assessed for DoR compliance):

```json
[
  {
    "issue_key": "string - Jira issue key",
    "team": "string - team display name",
    "story_points": "number - SP value (always non-null, only estimated issues assessed)",
    "dor_compliance_pct": "integer - 0-100, percentage of checkable criteria met",
    "criteria_met": "integer - count of checkable criteria met",
    "criteria_total_checkable": "integer - total checkable criteria for this team",
    "criteria_results": [
      {
        "criterion": "string - criterion name",
        "check_type": "string - the heuristic check type",
        "met": "boolean - whether the check passed"
      }
    ]
  }
]
```

Rules:
- Only issues with `story_points != null` are assessed (no null-SP entries)
- Only teams with `dor_found: true` have entries in this file
- `dor_compliance_pct` = round(checkable_met / checkable_total * 100)
- GENERIC criteria always pass but are excluded from the percentage denominator
- Threshold for "DoR ready": compliance_pct >= 75

## velocity_data.json (NEW in v2)

Array of 15 entries (one per team):

```json
[
  {
    "team": "string - team display name",
    "velocity_avg": "integer | null - average SP per sprint",
    "sprints_used": "integer - 0-3",
    "velocity_sprints": [
      {
        "sprint_name": "string - sprint name from Jira",
        "completed_sp": "integer - total SP completed in that sprint"
      }
    ]
  }
]
```

Rules:
- Always 15 entries, one per team
- `velocity_avg` = sum(completed_sp) / sprints_used, or null if sprints_used == 0
- `sprints_used` <= 3 (last 3 completed sprints within 6-week window)
- `velocity_sprints` sorted by most recent first
- Teams with no completed sprint data have velocity_avg: null, sprints_used: 0, velocity_sprints: []
