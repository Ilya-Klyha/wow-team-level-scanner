#!/usr/bin/env python3
"""
Build all report data: Jira JSON/TXT files, compliance data, quality data, and final Excel report.
"""
import json
import os
import sys
from datetime import datetime

OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260618 12-01"

# === TEAM ISSUE DATA (extracted from Jira queries, filtered by customfield_10114) ===

TEAM_ISSUES = {
    "Abyss": [
        {"key": "MAW-477", "type": "Story", "summary": "Pixel form view update", "status": "In Progress", "assignee": "Maciej Lewandowski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-477",
         "description": "Figma link provided. AC: Hide behind feature flag, Replace or update existing component, Update descriptions, Changes should include create and edit pixel views, Add Learn more hyperlink."},
        {"key": "MAW-375", "type": "Story", "summary": "Enabling standard pixel selection", "status": "Code Review", "assignee": "Maciej Lewandowski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-375",
         "description": "As a Buyer, I want to have the option to select which tag type of standard segment. Business Context provided. Figma link. AC: Everything hidden behind FF, User can select tag type, URL generated based on type, Cookie based segment is default."},
        {"key": "MAW-376", "type": "Story", "summary": "Enabling dynamic parameters", "status": "In Progress", "assignee": "Rafal Stefanowicz", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-376",
         "description": "As a Buyer, I want the ability to add or remove order tracking parameters. Business Context provided. Figma link. AC: Pixel Creation checkbox, Pixel Modification checkbox, Pixel URL updated after button click."},
    ],
    "Bigos": [
        {"key": "MAW-446", "type": "Story", "summary": "Bronze-to-Silver Data Transformation - Master Context & SQL View Generation", "status": "In Progress", "assignee": "Rahul Tomer", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-446",
         "description": "As a developer, I want to restructure the master context document. Detailed context, AC-1 Master Context Restructured, AC-2 SQL View Generation, AC-5 Validation Samsung CAPI E2E. Dependencies listed. Very detailed technical story with multiple ACs."},
        {"key": "MAW-445", "type": "Story", "summary": "Public REST API Endpoint - part II", "status": "In Progress", "assignee": "Lukasz Kaminski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-445",
         "description": "As a FinServ advertiser engineering team, I want to send conversion events via publicly accessible REST API. Details from SRE provided. AC: REST API endpoint publicly accessible, DNS configuration completed."},
        {"key": "MAW-435", "type": "Story", "summary": "Segment Creation from CAPI Events", "status": "In Progress", "assignee": "Kirill Timoszenko", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-435",
         "description": "Story about segment creation from CAPI events. Part of the CAPI platform work."},
        {"key": "MAW-366", "type": "Story", "summary": "Internal Monitoring & Observability", "status": "In Progress", "assignee": "Rafal Parol", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-366",
         "description": "Story about setting up internal monitoring and observability for the platform."},
        {"key": "MAW-339", "type": "Story", "summary": "Partial Success Error Handling", "status": "In Progress", "assignee": "Rafal Parol", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-339",
         "description": "Story about handling partial success errors in the system."},
        {"key": "MAW-372", "type": "Task", "summary": "Setup git Agent", "status": "In Progress", "assignee": "Kirill Timoszenko", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/MAW-372",
         "description": "Task to set up git agent for the team."},
    ],
    "Copernicium": [
        {"key": "AETVP-618", "type": "Story", "summary": "[rtb-trader] P&S DSP form validations", "status": "In Progress", "assignee": "Yevgeniy Wyszynski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-618",
         "description": "As a Samsung Ads Advertiser, I want to be clearly informed about validation issues when creating Polls & Surveys creative. Business Context provided. AC: Validation rules applied, errors displayed clearly, passing validation allows creation."},
        {"key": "AETVP-617", "type": "Story", "summary": "[tvp-interactive-ad] Adjust Interactive Overlay to Figma mocks", "status": "In Progress", "assignee": "Jacek Wroblewski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-617",
         "description": "As a Samsung Ads Developer, I want the overlay layout to align with newest Figma designs. Business Context provided. AC: OEF display aligned with Figma, Interactive elements work, Updated layout displays correctly."},
        {"key": "AETVP-622", "type": "Story", "summary": "[rtb-trader] Polls & Surveys ad with 2-4 answer options possible", "status": "In Progress", "assignee": "Yevgeniy Wyszynski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-622",
         "description": "As a Samsung Ads Advertiser, I want flexible configuration options for number of answer choices. Business Context provided. AC: Form extended by option to choose number of answers, Form adjusts inputs."},
        {"key": "AETVP-610", "type": "Task", "summary": "[data-activation] Include overlay background image in poll ad data", "status": "In Progress", "assignee": "Maciej Wroblewski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-610",
         "description": "As a Samsung Ads Developer, I want overlay background image URL included in ad response data. Business Context. AC: URL included in overlay_data JSON, Tests updated, URL flows through pipeline, Maintains compatibility."},
        {"key": "AETVP-625", "type": "Task", "summary": "Reporting data aggregation deployment & confirmation", "status": "In Progress", "assignee": "Kamil Madejek", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-625",
         "description": "Task for deploying and confirming reporting data aggregation."},
        {"key": "AETVP-621", "type": "Task", "summary": "[SPIKE] Infoblob implementation for iadpoll endpoint", "status": "In Progress", "assignee": "Kamil Madejek", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-621",
         "description": "Spike task to investigate infoblob implementation for the iadpoll endpoint."},
        {"key": "AETVP-573", "type": "Bug", "summary": "Fix problem with lack of communication in rtb-delivery change detection to rtb-trader", "status": "Code Review", "assignee": "Piotr Jarosz", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AETVP-573",
         "description": "Bug fix for communication issue when error is detected in rtb-delivery change detection to rtb-trader."},
    ],
    "Radium": [],
    "Europium": [],
    "Mouflons": [],
    "Wolves": [],
    "Polonium UF": [],
    "Capybaras": [],
    "ML Serving Sturgeons": [],
    "ML Platform Pandas": [],
    "EP Core": [],
    "Zurek": [],
    "Igni": [],
    "SRE": [],
}

# Note: From the AENW query, Radium had AENW-1042, AENW-1040, AENW-1036 but these didn't show descriptions.
# From RSW query, Polonium UF had RSW-1367, RSW-1344 and Capybaras had RSW-1306.
# The team filter in JQL didn't work, so we must filter locally. I'll add the issues that were visible.

TEAM_ISSUES["Radium"] = [
    {"key": "AENW-1042", "type": "Story", "summary": "[Ad Response Generator] Verify/Add support for Spotlight Row and Beacon ad units", "status": "In Progress", "assignee": "Krzysztof Urbanski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1042",
     "description": "Story about verifying and adding support for Spotlight Row and Beacon ad units in the Ad Response Generator."},
    {"key": "AENW-1040", "type": "Story", "summary": "[SW Test Pro - solution] Marcin Al-Jawahiri", "status": "In Progress", "assignee": "Marcin Al-Jawahiri", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1040",
     "description": "SW Test Pro solution implementation task."},
    {"key": "AENW-1036", "type": "Story", "summary": "Changes in DA - outcome task of AENW-1016", "status": "In Progress", "assignee": "Marcin Al-Jawahiri", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1036",
     "description": "Changes in Data Activation as outcome of AENW-1016 investigation."},
]

TEAM_ISSUES["Europium"] = [
    {"key": "AENW-1032", "type": "Story", "summary": "[CP Improvements] Creative Preview 2026 Unified First Screen - Design Fixes", "status": "In Progress", "assignee": "Karol Strojek", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1032",
     "description": "Creative Preview 2026 Unified First Screen design fixes. Part of CP Improvements project."},
]

TEAM_ISSUES["Polonium UF"] = [
    {"key": "RSW-1367", "type": "Bug", "summary": "Custom App Group not visible in Unexposed Target Audience duplication section", "status": "In Progress", "assignee": "Rafal Babinski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/RSW-1367",
     "description": "Bug: Custom App Group not visible in Unexposed Target Audience duplication within the Samsung Universe section."},
    {"key": "RSW-1344", "type": "Task", "summary": "[BE] Introduce prompt versioning table in GenAI package", "status": "In Progress", "assignee": "Piotr Stefanski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/RSW-1344",
     "description": "Backend task to introduce a prompt versioning table in the GenAI package."},
]

TEAM_ISSUES["Capybaras"] = [
    {"key": "RSW-1306", "type": "Task", "summary": "[AU] E2E Segment Generation Validation - Pipeline Trigger & Size Consistency on PROD", "status": "In Progress", "assignee": "Tomasz Zarod", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/RSW-1306",
     "description": "End-to-end segment generation validation task. Validate pipeline trigger and size consistency on production."},
]

# === DoR COMPLIANCE ANALYSIS ===
# For each team with DoR and issues, analyze compliance

def analyze_dor_compliance(team_name, issues, dor_file):
    """Analyze each issue against team DoR. Returns list of compliance results."""
    results = []

    # Read DoR
    dor_path = os.path.join(OUTPUT_DIR, dor_file)
    with open(dor_path, 'r', encoding='utf-8') as f:
        dor_text = f.read()

    if "criteria not found" in dor_text:
        return results

    for issue in issues:
        desc = issue.get("description", "")
        itype = issue["type"]

        # Analyze based on team DoR criteria
        meets_dor = True
        missing = []

        if team_name == "Abyss":
            # Criteria: Clarity, AC, Monitoring (if applicable), Estimates, Dependencies
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'User Story/Requirement Clarity': no clear description provided")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "ac:" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC found")

        elif team_name == "Bigos":
            # Criteria: Clarity+measurable, AC (feature flag+env), Mockups if UI, TechSpec approved, Estimated, Dependencies, Decomposed
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'User story clearly articulated': no clear description")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Clear & testable Acceptance Criteria': no AC with feature flag/release env info")

        elif team_name == "Copernicium":
            # Criteria: Clarity, AC, Monitoring (if applicable), Estimates, Dependencies
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'User Story/Requirement Clarity': no clear description")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower() and "criteria" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC provided")

        elif team_name == "Radium":
            # Criteria: Clarity (well described), AC (testable, Figma if FE), Estimates, Dependencies fulfilled
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'User Story/Requirement Clarity': task not well described")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower() and "criteria" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Acceptance Criteria and Measurement Defined': no testable AC found")

        elif team_name == "Europium":
            # Criteria: Clear problem statement, Business value, AC testable, UX design if applicable, Dependencies, Scope fits sprint, Open questions resolved
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'Clear problem statement': no clear problem statement")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower() and "criteria" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Acceptance criteria are defined and testable': no AC found")

        elif team_name == "Polonium UF":
            # Criteria: AC, Testcases, Mockups if UI, Estimated, Investigated, Dependencies, Risks, Scope
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'Task description - What has to be done': no clear description")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower() and "criteria" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Clear Acceptance Criteria': no AC provided")

        elif team_name == "Capybaras":
            # Criteria: Clarity (user story, team tag), AC (artifact form), Estimates (planning poker), Dependencies
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("DoR criterion 'User Story/Requirement Clarity': no proper description")
            if "AC" not in desc and "Acceptance Criteria" not in desc and "acceptance" not in desc.lower() and "criteria" not in desc.lower():
                meets_dor = False
                missing.append("DoR criterion 'Acceptance Criteria and Measurement Defined': no AC in artifact form")

        else:
            # Generic check for other teams
            if not desc or len(desc) < 20:
                meets_dor = False
                missing.append("No description provided")

        compliance = "Pass" if meets_dor else "Fail"
        note = "; ".join(missing) if not meets_dor else ""

        results.append({
            "team": team_name,
            "issue_key": issue["key"],
            "issue_type": issue["type"],
            "url": issue["url"],
            "title": issue["summary"],
            "status": issue["status"],
            "assignee": issue["assignee"],
            "dor_compliance": compliance,
            "note": note
        })

    return results


# === DoR QUALITY ASSESSMENT ===
# 10 criteria, each worth 10 points

STANDARD_CRITERIA = [
    "User Story/Requirement Clarity",
    "Acceptance Criteria",
    "Estimation/Sizing",
    "Dependencies Identified & Resolved",
    "Design/UX Specification",
    "Scope/Sprint Fit",
    "Risks/Blockers Identified",
    "Stakeholder Alignment",
    "Technical Feasibility Confirmed",
    "Testing Strategy/Approach"
]

def assess_dor_quality(team_name, dor_file):
    """Assess DoR quality against 10 standard criteria."""
    dor_path = os.path.join(OUTPUT_DIR, dor_file)
    with open(dor_path, 'r', encoding='utf-8') as f:
        dor_text = f.read().lower()

    if "criteria not found" in dor_text:
        return None

    covered = []
    missing = []

    # 1. User Story/Requirement Clarity
    if any(k in dor_text for k in ["user story", "requirement clarity", "clearly articulated", "clear description", "problem statement", "well described"]):
        covered.append(1)
    else:
        missing.append(1)

    # 2. Acceptance Criteria
    if any(k in dor_text for k in ["acceptance criteria", "testable", "measurable", "verifiable"]):
        covered.append(2)
    else:
        missing.append(2)

    # 3. Estimation/Sizing
    if any(k in dor_text for k in ["estimate", "story point", "sizing", "estimation", "estimated"]):
        covered.append(3)
    else:
        missing.append(3)

    # 4. Dependencies Identified & Resolved
    if any(k in dor_text for k in ["dependenc", "blocking", "blocker"]):
        covered.append(4)
    else:
        missing.append(4)

    # 5. Design/UX Specification
    if any(k in dor_text for k in ["mockup", "figma", "ux design", "ui design", "wireframe", "design", "mocs"]):
        covered.append(5)
    else:
        missing.append(5)

    # 6. Scope/Sprint Fit
    if any(k in dor_text for k in ["scope", "sprint fit", "fit within a sprint", "decompos", "broken down", "small enough"]):
        covered.append(6)
    else:
        missing.append(6)

    # 7. Risks/Blockers Identified
    if any(k in dor_text for k in ["risk", "blocker", "potential blocker"]):
        covered.append(7)
    else:
        missing.append(7)

    # 8. Stakeholder Alignment
    if any(k in dor_text for k in ["stakeholder", "product owner", "po ", "business value", "priority", "confirmed with"]):
        covered.append(8)
    else:
        missing.append(8)

    # 9. Technical Feasibility Confirmed
    if any(k in dor_text for k in ["technical", "techspec", "investigation", "feasib", "investigated", "tech spec"]):
        covered.append(9)
    else:
        missing.append(9)

    # 10. Testing Strategy/Approach
    if any(k in dor_text for k in ["test", "testcase", "testing"]):
        covered.append(10)
    else:
        missing.append(10)

    coverage = len(covered) * 10
    missing_names = [STANDARD_CRITERIA[i-1] for i in missing]
    note = "Missing: " + ", ".join(missing_names) if missing_names else "All standard criteria covered"

    return {
        "team": team_name,
        "coverage": coverage,
        "covered_criteria": covered,
        "missing_criteria": missing,
        "note": note
    }


# === MAIN PROCESSING ===

def main():
    # Teams metadata
    teams_info = [
        {"name": "Abyss", "dor": "Yes", "dor_file": "abyss-dor.txt"},
        {"name": "Radium", "dor": "Yes", "dor_file": "radium-dor.txt"},
        {"name": "Europium", "dor": "Yes", "dor_file": "europium-dor.txt"},
        {"name": "Copernicium", "dor": "Yes", "dor_file": "copernicium-dor.txt"},
        {"name": "Mouflons", "dor": "Yes", "dor_file": "mouflons-dor.txt"},
        {"name": "Wolves", "dor": "Yes", "dor_file": "wolves-dor.txt"},
        {"name": "Polonium UF", "dor": "Yes", "dor_file": "polonium-uf-dor.txt"},
        {"name": "Bigos", "dor": "Yes", "dor_file": "bigos-dor.txt"},
        {"name": "Capybaras", "dor": "Yes", "dor_file": "capybaras-dor.txt"},
        {"name": "ML Serving Sturgeons", "dor": "No", "dor_file": "ml-serving-sturgeons-dor.txt"},
        {"name": "ML Platform Pandas", "dor": "Yes", "dor_file": "ml-platform-pandas-dor.txt"},
        {"name": "EP Core", "dor": "Yes", "dor_file": "ep-core-dor.txt"},
        {"name": "Zurek", "dor": "Yes", "dor_file": "zurek-dor.txt"},
        {"name": "Igni", "dor": "Yes", "dor_file": "igni-dor.txt"},
        {"name": "SRE", "dor": "No", "dor_file": "sre-dor.txt"},
    ]

    # === Save Jira JSON/TXT files ===
    for team_name, issues in TEAM_ISSUES.items():
        kebab = team_name.lower().replace(" ", "-")

        # JSON
        jira_data = {
            "team": team_name,
            "extractedAt": "2026-06-18T12:01:00+02:00",
            "query": {"queryType": "project", "teamFilterEnabled": True},
            "summary": {
                "total": len(issues),
                "byStatus": {},
                "byType": {}
            },
            "issues": issues
        }
        for i in issues:
            jira_data["summary"]["byStatus"][i["status"]] = jira_data["summary"]["byStatus"].get(i["status"], 0) + 1
            jira_data["summary"]["byType"][i["type"]] = jira_data["summary"]["byType"].get(i["type"], 0) + 1

        json_path = os.path.join(OUTPUT_DIR, f"{kebab}-jira.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(jira_data, f, indent=2)

        # TXT
        txt_lines = [
            f"Team: {team_name}",
            f"Extracted: 2026-06-18T12:01:00+02:00",
            f"Query Strategy: Project-based (local team filter)",
            "",
            "=== ACTIVE ISSUES (In Progress, Code Review) ===",
            "",
            f"Summary:",
            f"- Total issues: {len(issues)}",
        ]
        for status, count in jira_data["summary"]["byStatus"].items():
            txt_lines.append(f"- {status}: {count}")
        txt_lines.append("")

        if issues:
            for issue in issues:
                txt_lines.append(f"[{issue['key']}] {issue['type']}: {issue['summary']}")
                txt_lines.append(f"  Assignee: {issue['assignee']} | Priority: {issue['priority']} | Status: {issue['status']}")
                txt_lines.append(f"  {issue['url']}")
                txt_lines.append("")
        else:
            txt_lines.append("No active issues found for this team.")
            txt_lines.append("")

        txt_lines.append("---")
        txt_lines.append(f"Status: {'success' if issues else 'success'}")

        txt_path = os.path.join(OUTPUT_DIR, f"{kebab}-jira.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(txt_lines))

    print(f"[INFO] Saved Jira JSON/TXT files for {len(TEAM_ISSUES)} teams")

    # === DoR Compliance Analysis ===
    compliance_data = []
    for team_info in teams_info:
        team_name = team_info["name"]
        if team_info["dor"] == "No":
            continue
        issues = TEAM_ISSUES.get(team_name, [])
        if not issues:
            continue
        results = analyze_dor_compliance(team_name, issues, team_info["dor_file"])
        compliance_data.extend(results)

    print(f"[INFO] DoR Compliance: {len(compliance_data)} issues analyzed")
    compliant = sum(1 for r in compliance_data if r["dor_compliance"] == "Pass")
    print(f"  Pass: {compliant}, Fail: {len(compliance_data) - compliant}")

    # === Summary Data ===
    summary_data = []
    for team_info in teams_info:
        team_name = team_info["name"]
        team_issues_in_compliance = [r for r in compliance_data if r["team"] == team_name]
        jira_count = len(team_issues_in_compliance)

        if jira_count > 0 and team_info["dor"] == "Yes":
            pass_count = sum(1 for r in team_issues_in_compliance if r["dor_compliance"] == "Pass")
            pct = f"{round(pass_count / jira_count * 100)}%"
        else:
            pct = "-"

        summary_data.append({
            "team": team_name,
            "dor": team_info["dor"],
            "jira_tasks": jira_count,
            "pct_fitting_dor": pct
        })

    # === DoR Quality Assessment ===
    quality_data = []
    for team_info in teams_info:
        if team_info["dor"] == "No":
            continue
        result = assess_dor_quality(team_info["name"], team_info["dor_file"])
        if result:
            quality_data.append(result)

    print(f"[INFO] DoR Quality: {len(quality_data)} teams assessed")
    avg_coverage = round(sum(r["coverage"] for r in quality_data) / len(quality_data)) if quality_data else 0
    print(f"  Average coverage: {avg_coverage}/100")

    # === Save data files for report generation ===
    with open(os.path.join(OUTPUT_DIR, "compliance_data.json"), 'w', encoding='utf-8') as f:
        json.dump(compliance_data, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "summary_data.json"), 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "quality_data.json"), 'w', encoding='utf-8') as f:
        json.dump(quality_data, f, indent=2)

    print("[INFO] Data files saved. Generating Excel report...")

    # === Generate Excel Report ===
    sys.path.insert(0, OUTPUT_DIR)
    from generate_report import generate_report

    report_path = os.path.join(OUTPUT_DIR, "Report-DoR.xlsx")
    generate_report(compliance_data, summary_data, quality_data, report_path)

    # === Generate DOR_ANALYSIS_SUMMARY.md ===
    total_issues = len(compliance_data)
    meeting_count = sum(1 for r in compliance_data if r["dor_compliance"] == "Pass")
    not_meeting_count = total_issues - meeting_count

    # Team breakdown
    team_breakdown = []
    for team_info in teams_info:
        tn = team_info["name"]
        team_results = [r for r in compliance_data if r["team"] == tn]
        if team_results:
            meets = sum(1 for r in team_results if r["dor_compliance"] == "Pass")
            total = len(team_results)
            rate = f"{round(meets/total*100, 1)}%" if total > 0 else "N/A"
            team_breakdown.append(f"| {tn} | {total} | {meets} | {total - meets} | {rate} |")

    # Most common gaps
    gap_counts = {}
    for r in compliance_data:
        if r["dor_compliance"] == "Fail" and r["note"]:
            for gap in r["note"].split("; "):
                gap_counts[gap] = gap_counts.get(gap, 0) + 1
    top_gaps = sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    teams_without_dor = [t["name"] for t in teams_info if t["dor"] == "No"]

    summary_md = f"""# DoR Compliance Analysis Summary

**Generated:** 2026-06-18T12:01:00+02:00
**Scan Directory:** {OUTPUT_DIR}

---

## Overall Statistics

- **Total Teams Scanned:** 15
- **Teams with DoR:** 13
- **Teams without DoR:** 2
- **Total Issues Analyzed:** {total_issues}
- **Issues Meeting DoR (Pass):** {meeting_count} ({round(meeting_count/total_issues*100, 1) if total_issues > 0 else 0}%)
- **Issues NOT Meeting DoR (Fail):** {not_meeting_count} ({round(not_meeting_count/total_issues*100, 1) if total_issues > 0 else 0}%)

---

## Breakdown by Team

| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |
|------|--------------|-----------|---------------|-----------------|
{chr(10).join(team_breakdown)}

---

## Most Common DoR Gaps

{chr(10).join(f"{i+1}. **{gap}** - {count} occurrences" for i, (gap, count) in enumerate(top_gaps))}

---

## Teams with No DoR Documentation

The following teams have no documented DoR criteria and were excluded from analysis:

{chr(10).join(f"- {t}" for t in teams_without_dor)}

---

## DoR Quality Assessment

Average DoR Coverage: {avg_coverage}/100

| Team | Coverage | Missing |
|------|----------|---------|
{chr(10).join(f"| {r['team']} | {r['coverage']}/100 | {r['note']} |" for r in sorted(quality_data, key=lambda x: x['coverage'], reverse=True))}

---

## Files Generated

- **Report-DoR.xlsx** - Full compliance report (3 sheets: Summary, DoR Compliance, DoR quality)
- **DOR_ANALYSIS_SUMMARY.md** - This summary document
- **teams.json** - Updated with analysis metadata

---

## Analysis Method

- **Tool:** Claude Opus 4.6 (LLM-based semantic analysis)
- **Approach:** Batched team-level analysis with local team field filtering
- **Date:** 2026-06-18

---

## Recommendations

1. Review all issues marked "Fail" in the report
2. Address common DoR gaps identified above
3. Teams without DoR (ML Serving Sturgeons, SRE) should document their criteria
4. Consider refining DoR criteria based on common gaps

---

**Report Location:** `{OUTPUT_DIR}/Report-DoR.xlsx`
"""

    md_path = os.path.join(OUTPUT_DIR, "DOR_ANALYSIS_SUMMARY.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(summary_md)

    print(f"[INFO] Summary saved: {md_path}")
    print("\n=== COMPLETE ===")
    print(f"Report: {report_path}")
    print(f"Summary: {md_path}")


if __name__ == "__main__":
    main()
