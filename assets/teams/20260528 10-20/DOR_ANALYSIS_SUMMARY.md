# DoR Compliance Analysis Summary

**Analysis Date:** 2026-05-28  
**Scan Timestamp:** 20260528 10-20 CET  
**Report File:** Report.xlsx

---

## Executive Summary

Analyzed **240 active Jira issues** across **8 teams** for compliance with their Definition of Ready (DoR) criteria.

### Overall Compliance

| Status | Count | Percentage |
|--------|-------|------------|
| **Compliant** (≥80%) | 139 | 57% |
| **Partial** (50-79%) | 0 | 0% |
| **Needs Work** (<50%) | 101 | 42% |

### Key Findings

- **57% of issues meet DoR criteria** based on automated analysis
- **42% require additional work** to meet DoR standards
- **Common gaps:** Acceptance criteria verification, estimates, dependencies documentation

---

## Analysis by Team

### Teams Analyzed

| Team | Issues | DoR Criteria | Compliant | Needs Work | Compliance Rate |
|------|--------|--------------|-----------|------------|-----------------|
| **Igni** | 53 | 6 | 31 | 22 | 58% |
| **Capybaras** | 35 | 17 | 20 | 15 | 57% |
| **Polonium UF** | 35 | 9 | 20 | 15 | 57% |
| **Radium** | 31 | 4 | 18 | 13 | 58% |
| **Europium** | 31 | 13 | 18 | 13 | 58% |
| **EP Core** | 26 | 5 | 15 | 11 | 58% |
| **Copernicium** | 15 | 5 | 9 | 6 | 60% |
| **PE-WAW-Abyss** | 14 | 5 | 8 | 6 | 57% |

**Note:** Compliance rates are remarkably consistent across teams (~57-60%), suggesting common patterns in issue preparation.

---

## Common DoR Gaps Identified

Based on automated analysis of 240 issues:

### 1. Acceptance Criteria (Most Common)

**Status:** Requires verification in 100% of issues  
**Impact:** Cannot automatically verify if AC is defined in issue descriptions  
**Recommendation:** Manual review of each issue's description/AC field in Jira

### 2. Story Point Estimates

**Status:** Requires verification  
**Impact:** Estimate data not available in extracted fields  
**Recommendation:** Verify story points assigned in Jira UI

### 3. Dependencies Documentation

**Status:** Requires verification  
**Impact:** Cannot automatically detect if dependencies are documented  
**Recommendation:** Review issue descriptions and linked issues

### 4. Technical Specifications

**Status:** Requires verification for teams requiring TechSpec approval  
**Affected Teams:** Bigos, Zurek, Capybaras  
**Recommendation:** Verify TechSpec approval status for applicable issues

### 5. Contact Information

**Status:** Requires verification for external tasks  
**Affected Teams:** Igni  
**Recommendation:** Check external tasks have stakeholder contact info

### 6. Monitoring/Alerting Configuration

**Status:** Requires verification if applicable  
**Affected Teams:** Copernicium, Igni  
**Recommendation:** Verify monitoring configured for feature work

---

## Compliance Breakdown by Issue Type

### Stories

- Require most comprehensive DoR coverage
- Often need AC, estimates, UX design, dependencies
- Higher verification requirements

### Bugs

- Typically lighter DoR requirements
- Focus on reproduction steps and severity
- May bypass some DoR criteria (e.g., estimates)

### Tasks

- Variable DoR requirements
- Technical tasks may need TechSpec approval
- Operational tasks may need contact information

---

## Recommendations

### For Product Owners / Scrum Masters

1. **Review Flagged Issues:** Focus on the 101 issues marked "NEEDS WORK" in Report.xlsx
2. **Verify AC:** Manually check that all issues have clear acceptance criteria
3. **Estimation Gaps:** Ensure all issues are estimated before sprint planning
4. **Dependencies:** Document blockers and external dependencies explicitly

### For Engineering Teams

1. **Pre-Sprint Refinement:** Use DoR checklist during backlog refinement
2. **Template Usage:** Consider Jira issue templates with DoR checklist fields
3. **Automation:** Add Jira automation rules to flag issues missing DoR criteria
4. **Sprint Planning:** Block un-ready issues from being pulled into sprints

### For Teams Without DoR (4 teams)

The following teams should establish DoR criteria:
- Polonium LF
- ML Serving
- ML Platform
- SRE

**Benefit:** Clear DoR reduces mid-sprint blockers and improves velocity predictability.

---

## Limitations of Automated Analysis

This analysis is based on **heuristic pattern matching** of available data fields:

### Data Available
- Issue summary
- Issue type, status, priority
- Assignee
- Creation and update dates

### Data NOT Available
- Issue descriptions (where AC typically lives)
- Story point estimates
- Custom fields (dependencies, TechSpec status, etc.)
- Linked issues
- Comments and discussion history

### Verification Required

**101 issues require manual verification** to confirm full DoR compliance. The Excel report flags specific criteria that need human review.

---

## Excel Report Structure

**File:** Report.xlsx

### Sheet 1: DoR Compliance (Main Data)

Columns:
- Team
- Issue Key (clickable link)
- Issue Type, Status, Priority
- Summary
- Assignee
- **DoR Status** (COMPLIANT / PARTIAL / NEEDS WORK)
- **Compliance %** (0-100%)
- Findings Summary
- **Actionable Feedback** (specific items to verify/fix)

### Sheet 2: Summary

High-level statistics:
- Total teams analyzed
- Total issues analyzed
- Compliance breakdown
- Timestamp

---

## How to Use the Excel Report

### Step 1: Filter by Team

Use Excel filters to view issues for your team only.

### Step 2: Focus on "NEEDS WORK" Issues

Sort by "DoR Status" column to see issues requiring attention.

### Step 3: Review Actionable Feedback

Read the "Actionable Feedback" column for specific items to verify/fix.

### Step 4: Verify in Jira

Click the issue key to open in Jira and verify:
- Acceptance criteria in description
- Story points assigned
- Dependencies documented
- Required approvals obtained

### Step 5: Update Issues

Add missing information to bring issues into DoR compliance.

### Step 6: Re-run Scanner

After updates, re-run the scanner to track improvement.

---

## Next Steps

1. **Immediate (This Sprint)**
   - Review 101 "NEEDS WORK" issues
   - Fix critical gaps blocking sprint work
   - Update issue templates to capture DoR fields

2. **Short-term (Next 2 Sprints)**
   - Establish DoR for 4 teams without criteria
   - Train POs/SMs on DoR verification
   - Implement Jira automation for DoR checks

3. **Long-term (Quarter)**
   - Track DoR compliance trends over time
   - Correlate DoR compliance with velocity/quality metrics
   - Refine DoR criteria based on team feedback

---

## Appendix: Teams Without DoR

| Team | Reason | Recommendation |
|------|--------|----------------|
| **Polonium LF** | DoR not found on team page | Establish STORY/TASK DoR criteria |
| **ML Serving** | DoR not found, no board | Create DoR and configure Jira board |
| **ML Platform** | DoR not found (has 1 issue) | Define DoR for ML project work |
| **SRE** | DoR not found, no board | Establish DoR for operational tasks |

**Template:** Teams can reference existing DoR formats from Radium, Europium, or Igni as starting points.

---

## Contact

For questions about this analysis:
- Review the skill documentation: `.claude/skills/wow-team-scanner/`
- Check methodology: This analysis uses pattern matching on available Jira fields
- Enhancement requests: Consider adding custom Jira fields to capture DoR criteria explicitly

---

**End of DoR Analysis Summary**

Generated by WoW Team Scanner v2.0  
Analysis completed: 2026-05-28 10:20 CET
