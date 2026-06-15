# WoW DoR Scanner - Changelog

## Version 4.0 - 2026-06-15

### New Feature: DoR Quality Assessment (Step 12)

#### Overview
Added automated assessment of each team's Definition of Ready document quality. Evaluates DoR definitions against industry best practices and the company's own DoR standard, producing a quality score (1-100%) per team.

#### New Files
- `assets/dor-standard.txt` - Persistent industry best practices reference document (10 essential DoR areas, INVEST criteria, quality characteristics, scoring guide)
- `${OUTPUT_DIR}/company-dor-standard.txt` - Per-scan cached company DoR standard from Confluence

#### New Step 12 (AUTO-EXECUTE after Step 11)
- **12.0**: Loads industry standard from `assets/dor-standard.txt`
- **12.1**: Fetches company DoR from Confluence page 21735179128
- **12.2**: Identifies teams with defined DoR (excludes teams without DoR)
- **12.3**: LLM-based quality evaluation across 7 weighted dimensions
- **12.4**: Adds "DoR quality" sheet to Report-DoR.xlsx (3rd sheet)
- **12.5**: Reports completion with top/bottom team rankings

#### 7 Quality Dimensions
| Dimension | Weight |
|-----------|--------|
| Coverage (10 essential areas) | 25% |
| Clarity & Specificity | 20% |
| Measurability | 15% |
| Company Standard Alignment | 15% |
| Industry Best Practices | 10% |
| Actionability | 10% |
| AC Guidance | 5% |

#### Report-DoR.xlsx Changes
- **Before**: 2 sheets (Summary + DoR Compliance)
- **After**: 3 sheets (Summary + DoR Compliance + DoR quality)
- **"DoR quality" sheet format**:
  - Row 1: KPI "DoR quality lvl" with average % (color-coded)
  - Row 3: Table header (Team | Quality | Note)
  - Rows 4+: Team data sorted by quality descending
  - Conditional formatting: green >= 70%, orange 40-69%, red < 40%
  - "Note" column: short, specific feedback on DoR gaps/weaknesses

#### Important Rules Updated
- Rule 12 updated to acknowledge 3rd sheet from Step 12
- Rule 13 added for DoR Quality Assessment constraints
- Automation rules updated to include Step 12 auto-execution

---

## Version 3.1 - 2026-06-12

### Bug Fixes and Improvements

#### 1. Fixed Sturgeons DoR Misattribution (Bug Fix)
- **Issue**: Sturgeons team page has NO DoR section, but scanner incorrectly extracted DoR from a linked page (22875865171 "DoR and DoD Team level") that belongs to the Pandas team
- **Root Cause**: Scanner was following DoR-related links found anywhere on the page, not just within a found DoR section
- **Fix**: Step 8.3 now has a CRITICAL PREREQUISITE - DoR link scanning ONLY executes if a DoR heading was found in step 2. If no DoR heading exists, team is immediately marked as "not_found"
- **Impact**: Sturgeons will now correctly report "DoR - STORY/TASK criteria not found"

#### 2. DoR-Specific Feedback in Analysis (Improvement)
- **Issue**: Feedback on non-compliant issues (e.g., PEPI-1139 for Mouflons) was generic and didn't reference the team's specific DoR criteria
- **Fix**: Analysis prompt now requires each missing_criteria entry to start with "DoR criterion '[exact criterion name]':" format
- **Example Before**: "Missing acceptance criteria"
- **Example After**: "DoR criterion 'Measurable/Verifiable Acceptance Criteria': AC not in SMART format as required"
- **Impact**: Feedback is now traceable to specific DoR document entries, making it actionable

#### 3. KPI Summary in Summary Sheet (New Feature)
- **Before**: Summary sheet started directly with the team table
- **After**: Rows 1-2 show KPI percentages before the table:
  - Row 1: "Teams without DoR: X%" (red if > 0%)
  - Row 2: "Issues fitting DoR: Y%" (green >= 70%, orange 40-69%, red < 40%)
  - Row 3: empty separator
  - Row 4: table header (was row 1)
- **Impact**: Quick at-a-glance health metrics visible immediately when opening the report

---

## Version 3.0 - 2026-06-12

### Breaking Changes

#### 1. Skill Renamed from "wow-team-scanner" to "wow-dor-scanner"
- **Command**: `/wow-dor-scanner` (previously `/wow-team-scanner`)
- **Folder**: `.claude/skills/wow-dor-scanner/`
- **Impact**: Old `/wow-team-scanner` command no longer works

#### 2. Abyss Team Name Changed
- **Before**: "PE-WAW-Abyss" in Team column of Report-DoR.xlsx
- **After**: "Abyss" in Team column of Report-DoR.xlsx
- **Logic**: Team names with "XX - YYY - Name" pattern now extract only the last segment
- **Impact**: File naming also changes: `abyss-dor.txt` instead of `pe-waw-abyss-dor.txt`

#### 3. Summary Sheet Added to Report-DoR.xlsx
- **Before**: 1 sheet ("DoR Compliance")
- **After**: 2 sheets ("Summary" as first sheet, "DoR Compliance" as second)
- **Summary sheet columns**:
  - Column A: Team - all team names from SRPOL Teams page
  - Column B: DoR - "Yes" if team has DoR defined, "No" if not
  - Column C: Jira Tasks - number of issues analyzed per team ("0" if none)
- **Impact**: Report schema changed from 1 sheet to 2 sheets

---

## Version 2.1 - 2026-06-10

### Improvements Based on User Feedback

#### 1. Added "In Development" Status
- **Issue**: Only "In Progress" and "Code Review" statuses were analyzed
- **Fix**: Added "In Development" to the list of active statuses
- **Impact**: All JQL queries now include: `status IN ("In Progress", "Code Review", "In Development")`
- **Files Updated**: All JQL query templates, metadata sections, documentation

#### 2. Excluded Sub-tasks from Analysis
- **Issue**: Sub-task MAW-418 was incorrectly analyzed against DoR
- **Fix**: Added explicit Sub-task exclusion in JQL queries: `issuetype != Sub-task`
- **Rationale**: Sub-tasks are implementation details and should not be assessed against DoR
- **Impact**: Only parent-level Stories, Bugs, and Tasks are analyzed
- **Files Updated**: All JQL query templates, documentation

#### 3. Improved User Story Format Interpretation
- **Issue**: Tasks incorrectly flagged for not having "user story format"
- **Fix**: Updated DoR analysis guidelines to recognize "user story OR requirement"
- **Example**: Radium DoR says "user story or requirement is clearly articulated, concise, and understandable"
- **Impact**: Tasks with clear descriptions now pass DoR even without user story format
- **Files Updated**: Analysis Guidelines section (Step 11.3)

#### 4. Fixed Description Content Detection
- **Issue**: Tasks with comprehensive descriptions (Context, Changes) marked as "no description"
- **Examples**: AENW-895, AENW-685, AENW-701 (Europium team)
- **Fix**: Updated guidelines to read FULL description field including all sections
- **Impact**: Only truly empty description fields are flagged as missing
- **Files Updated**: Analysis Guidelines section

#### 5. Improved Acceptance Criteria Recognition
- **Issue**: Acceptance criteria in Description field not recognized
- **Example**: AETVP-528 had comprehensive acceptance criteria but was flagged as missing
- **Fix**: Updated guidelines to check Description field for AC in various formats
- **Recognition Patterns**: Numbered lists, bullet points, "Done when" sections, structured formats
- **Impact**: AC anywhere in Description field (not just separate AC field) now recognized
- **Files Updated**: Analysis Guidelines section

#### 6. Fixed Conditional Mockups Requirement
- **Issue**: Backend task RSW-1038 flagged for missing mockups (no UI changes)
- **Fix**: Added conditional logic for mockup requirements
- **Rule**: Mockups only required if DoR mentions them AND task involves UI changes
- **Impact**: Backend/API tasks without UI changes no longer incorrectly flagged
- **Files Updated**: Analysis Guidelines section

#### 7. Improved "Artifact Form" Recognition
- **Issue**: RSW-1305 acceptance criteria not recognized as "artifact form"
- **Fix**: Updated guidelines to recognize structured formats as "artifact form"
- **Artifact Form Includes**: Numbered lists, bullet points, tables, any structured format
- **Impact**: Broader recognition of properly formatted acceptance criteria
- **Files Updated**: Analysis Guidelines section

#### 8. Fixed Criteria Invention
- **Issue**: ASPW-637 flagged for missing "reproduction steps" not in Igni DoR
- **Fix**: Added explicit rule to only flag criteria actually present in team's DoR
- **Rule**: Do NOT invent criteria not listed in the DoR document
- **Impact**: Analysis now strictly limited to team's documented DoR criteria
- **Files Updated**: Analysis Guidelines section

### Technical Changes

**JQL Query Updates:**
```jql
OLD: status IN ("In Progress", "Code Review") AND issuetype IN (Story, Bug, Task)
NEW: status IN ("In Progress", "Code Review", "In Development") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task
```

**Analysis Guidelines - New Section:**
```
CRITICAL - Accurate DoR Interpretation:

1. User Story Format NOT Always Required
2. Check for Description Content Carefully  
3. Acceptance Criteria Location (check Description field)
4. Conditional DoR Criteria (mockups only if UI changes)
5. Only Flag Criteria Actually in DoR
6. General Guidelines (fair and reasonable interpretation)
```

**Important Rules - New Rule 10a:**
```
DoR Analysis Accuracy (CRITICAL):
- User story format NOT required for Tasks if DoR says "user story OR requirement"
- Read FULL description field (all sections)
- Only mark "no description" if truly empty
- Acceptance criteria can be in Description field
- Mockups only required if DoR mentions them AND task involves UI
- Only flag criteria explicitly listed in team's DoR
- Interpret DoR fairly and reasonably
```

### Expected Impact

**Before Improvements:**
- Overall DoR Compliance: 12.3% (7/57 issues)
- False Negatives: ~40 issues incorrectly flagged

**After Improvements (estimated):**
- Overall DoR Compliance: Expected ~40-50%
- False Negatives: Significantly reduced
- More accurate representation of actual DoR adherence

### Files Modified

1. `skill.md` - Main skill file
   - Line 31: Updated description (added "In Development", excluded Sub-tasks)
   - Lines 436-446: Updated JQL query templates (all occurrences)
   - Lines 456-462: Updated case sensitivity notes
   - Lines 631, 821-822: Updated metadata and documentation
   - Lines 1058-1090: Completely rewrote Analysis Guidelines section
   - Lines 1652-1694: Updated Important Rules sections 6 and 10a

### Validation

To validate these improvements:
1. Re-run `/wow-team-scanner` on the same data
2. Compare new Report-DoR.xlsx with previous version
3. Check specific issues mentioned in feedback:
   - MAW-418 (should be excluded as Sub-task)
   - AENW-939 (should pass with requirement description)
   - AENW-895, AENW-685, AENW-701 (should recognize descriptions)
   - AETVP-528 (should recognize AC in Description)
   - RSW-1038 (should not require mockups for backend)
   - RSW-1305 (should recognize artifact form)
   - ASPW-637 (should not flag non-existent criteria)

### Next Steps

1. Test skill with updated logic
2. Validate against known issues
3. Monitor for new false positives/negatives
4. Iterate on Analysis Guidelines based on feedback

---

**Version**: 2.1  
**Date**: 2026-06-10  
**Author**: Igor Klyha (feedback), Claude Code (implementation)
