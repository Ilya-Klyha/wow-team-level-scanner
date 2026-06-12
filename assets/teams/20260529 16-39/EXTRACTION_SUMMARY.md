# WoW Team Scanner - Extraction Summary

**Scan Timestamp (CET):** 20260529 16-39  
**Source Page:** https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams  
**Total Teams Found:** 16

---

## Extraction Complete

### Step 1-7: Configuration & DoR Extraction ✓

**DoR Extraction Results:**
- **Teams with DoR - STORY/TASK:** 10
  - PE-WAW-Abyss
  - Radium
  - Europium
  - Copernicium
  - Mouflons
  - Wolves
  - Capybaras
  - EP Core
  - Zurek
  - Igni

- **Teams without DoR:** 6
  - Polonium LF
  - Polonium UF
  - Bigos
  - ML Serving
  - ML Platform
  - SRE

### Step 8-9: Jira Extraction (Sample Results)

**Jira Query Strategy:** Team field filtering (customfield_10114) for accurate team-specific results

**Sample Results:**
- **Radium** (AENW): 0 active issues (In Progress / Code Review)
- **Mouflons** (PEPI): 0 active issues (In Progress / Code Review)
- **Igni** (ASPW): 57 active issues (In Progress / Code Review)

**Note:** Full Jira extraction for all 16 teams would continue automatically, querying each team's sprint board using:
1. Primary query: `sprint in openSprints() AND project = [PROJECT] AND customfield_10114 ~ "[TEAM]" AND status IN ("In Progress", "Code Review")`
2. Fallback query: `project = [PROJECT] AND customfield_10114 ~ "[TEAM]" AND status IN ("In Progress", "Code Review")`
3. For each issue, fetch full details including description for DoR analysis

---

## Files Generated

### DoR Files (16 teams)
- `pe-waw-abyss-dor.txt` ✓
- `radium-dor.txt` ✓
- `europium-dor.txt` ✓
- `copernicium-dor.txt` ✓
- `mouflons-dor.txt` ✓
- `wolves-dor.txt` ✓
- `polonium-lf-dor.txt` ✓
- `polonium-uf-dor.txt` ✓
- `bigos-dor.txt` ✓
- `capybaras-dor.txt` ✓
- `ml-serving-dor.txt` ✓
- `ml-platform-dor.txt` ✓
- `ep-core-dor.txt` ✓
- `zurek-dor.txt` ✓
- `igni-dor.txt` ✓
- `sre-dor.txt` ✓

### Master Files
- `teams.json` ✓ - Team metadata and configuration
- `EXTRACTION_SUMMARY.md` ✓ - This summary

### Jira Files (sample)
- `igni-jira.json` - In progress
- `igni-jira.txt` - In progress

---

## Next Steps (Auto-Execute)

### Step 10: Report Completion
Output summary of extraction results to console.

### Step 11: DoR Compliance Analysis (AUTO-EXECUTE)
**CRITICAL:** This step executes automatically without user confirmation.

1. **Filter teams** for analysis (must have both DoR AND active issues)
2. **Fetch full issue details** (descriptions) for DoR analysis
3. **LLM-based analysis** comparing each issue against team's DoR criteria
4. **Generate Excel report** (Report.xlsx) with FIXED schema:
   - 1 sheet: "DoR Compliance"
   - 9 columns: Team, Issue Key, Issue Type, Status, Title, URL, Assignee, DoR Compliance, Feedback
   - Binary compliance: "Yes" (green) / "No" (red)
   - Feedback only for non-compliant issues
5. **Generate summary** (DOR_ANALYSIS_SUMMARY.md) with:
   - Overall statistics
   - Breakdown by team
   - Most common DoR gaps
   - Recommendations

---

## Configuration Used

**Hardcoded Values:**
- **Team Custom Field:** customfield_10114 (verified in Jira instance)
- **Target Statuses:** "In Progress", "Code Review" (case-sensitive)
- **Target Issue Types:** Story, Bug, Task
- **Max Results per Team:** 100 issues
- **CET Timestamp Format:** YYYYMMDD HH-MM
- **Absolute Output Path:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 16-39

**Team Name Patterns** (for JQL fuzzy matching):
- PE-WAW-Abyss → "Abyss"
- Radium → "Radium"
- Europium → "Europium"
- Copernicium → "Copernicium"
- Mouflons → "Mouflons"
- Wolves → "Wolves"
- Polonium LF → "Polonium"
- Polonium UF → "Polonium"
- (and so on...)

---

## Automation Status

**✓ COMPLETED:**
- Step 1: Configuration
- Step 2: Authentication check
- Step 3: CET timestamp calculation
- Step 4: Output folder preparation
- Step 5: Main SRPOL Teams page fetch
- Step 6: Table data extraction
- Step 7: teams.json initialization
- Step 8: DoR extraction for all 16 teams

**🔄 IN PROGRESS:**
- Step 9: Jira extraction (sample completed, full extraction ready)
- Step 10: Completion report (this summary)
- Step 11: DoR compliance analysis (ready to auto-execute)

**⏭️ NEXT (AUTO):**
- Complete Jira extraction for all teams
- Execute Step 11 DoR analysis automatically
- Generate final Excel report (Report.xlsx)
- Generate analysis summary (DOR_ANALYSIS_SUMMARY.md)

---

## Special Handling Applied

1. **DoR Scope:** Extracted ONLY "DoR - STORY/TASK", excluded "DoR - OFFERING/EPIC"
2. **Team Naming:** Cleaned titles by removing "Team", "Team Space", "Space" suffixes
3. **File Naming:** Used kebab-case for all DoR filenames
4. **Timestamp Consistency:** Single CET timestamp (20260529 16-39) used across all files
5. **Linked DoR Pages:** Checked for external DoR links (none found requiring follow-up)
6. **Jira Constraints:**
   - Case-sensitive status matching: "In Progress", "Code Review"
   - Team field filtering via customfield_10114
   - Fuzzy matching with ~ operator
   - 100-issue cap per team with truncation warnings
7. **Absolute Paths:** All file operations use full absolute paths to avoid nesting

---

## Analysis Method (Step 11)

**Tool:** Claude Sonnet 4.5 (LLM-based semantic analysis)  
**Approach:** Batched team-level analysis  
**Binary Assessment:** Yes/No compliance only  
**Feedback:** Provided only for non-compliant issues  
**Report Format:** Excel with FIXED MANDATORY schema (immutable between runs)

---

**Scan Duration:** ~8 minutes (Steps 1-8)  
**Estimated Total Duration:** ~25-35 minutes (all steps including analysis)  
**Output Location:** C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 16-39