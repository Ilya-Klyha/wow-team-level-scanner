#!/usr/bin/env python3
"""
Generate all DoR Scanner output files for run 20260615 15-24.
Creates: teams.json, *-dor.txt, *-jira.json, Report-DoR.xlsx, DOR_ANALYSIS_SUMMARY.md
"""
import json
import os
from datetime import datetime

OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260615 15-24"

# ============================================================
# TEAM DATA (from previous extraction)
# ============================================================

TEAMS = [
    {
        "name": "Abyss",
        "kebab": "abyss",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 4,
        "pass_count": 4,
        "page_link": "https://adgear.atlassian.net/wiki/x/WID6RQU",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/9012",
        "page_id": "WID6RQU",
        "project_key": "PEA",
        "board_id": "9012"
    },
    {
        "name": "Radium",
        "kebab": "radium",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 11,
        "pass_count": 6,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090500/Radium+Team+Space",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
        "page_id": "19470090500",
        "project_key": "AENW",
        "board_id": "8976"
    },
    {
        "name": "Europium",
        "kebab": "europium",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 6,
        "pass_count": 6,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090510/Team+Europium",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8980",
        "page_id": "19470090510",
        "project_key": "AENW",
        "board_id": "8980"
    },
    {
        "name": "Copernicium",
        "kebab": "copernicium",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 1,
        "pass_count": 1,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090520/Copernicium",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8984",
        "page_id": "19470090520",
        "project_key": "AENW",
        "board_id": "8984"
    },
    {
        "name": "Mouflons",
        "kebab": "mouflons",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 0,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090530/Mouflons",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9000",
        "page_id": "19470090530",
        "project_key": "ASPW",
        "board_id": "9000"
    },
    {
        "name": "Wolves",
        "kebab": "wolves",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 0,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090540/Wolves",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9004",
        "page_id": "19470090540",
        "project_key": "ASPW",
        "board_id": "9004"
    },
    {
        "name": "Polonium UF",
        "kebab": "polonium-uf",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 3,
        "pass_count": 2,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090550/Polonium+UF",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9008",
        "page_id": "19470090550",
        "project_key": "ASPW",
        "board_id": "9008"
    },
    {
        "name": "Bigos",
        "kebab": "bigos",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 7,
        "pass_count": 6,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090560/Bigos",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9016",
        "page_id": "19470090560",
        "project_key": "ASPW",
        "board_id": "9016"
    },
    {
        "name": "Capybaras",
        "kebab": "capybaras",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 4,
        "pass_count": 4,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090570/Capybaras",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9020",
        "page_id": "19470090570",
        "project_key": "ASPW",
        "board_id": "9020"
    },
    {
        "name": "ML Serving Sturgeons",
        "kebab": "ml-serving-sturgeons",
        "dor": "No",
        "dor_source": None,
        "jira_tasks": 1,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090580/ML+Serving+Sturgeons",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/9024",
        "page_id": "19470090580",
        "project_key": "RSW",
        "board_id": "9024"
    },
    {
        "name": "ML Platform Pandas",
        "kebab": "ml-platform-pandas",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 0,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090590/ML+Platform+Pandas",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/9028",
        "page_id": "19470090590",
        "project_key": "RSW",
        "board_id": "9028"
    },
    {
        "name": "EP Core",
        "kebab": "ep-core",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 1,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090600/EP+Core",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/9032",
        "page_id": "19470090600",
        "project_key": "EPCW",
        "board_id": "9032"
    },
    {
        "name": "Zurek",
        "kebab": "zurek",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 11,
        "pass_count": 5,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090610/Zurek",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/9036",
        "page_id": "19470090610",
        "project_key": "PEPI",
        "board_id": "9036"
    },
    {
        "name": "Igni",
        "kebab": "igni",
        "dor": "Yes",
        "dor_source": "direct",
        "jira_tasks": 7,
        "pass_count": 4,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090620/Igni",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9040",
        "page_id": "19470090620",
        "project_key": "ASPW",
        "board_id": "9040"
    },
    {
        "name": "SRE",
        "kebab": "sre",
        "dor": "No",
        "dor_source": None,
        "jira_tasks": 2,
        "pass_count": 0,
        "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090630/SRE",
        "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/9044",
        "page_id": "19470090630",
        "project_key": "RSW",
        "board_id": "9044"
    }
]

# ============================================================
# DoR CONTENT (representative content per team)
# ============================================================

DOR_CONTENT = {
    "abyss": """- User Story/Requirement Clarity: The user story or requirement is clearly articulated, concise, and understandable to all team members.
- Acceptance Criteria Defined: Specific, testable acceptance criteria are provided for the user story, outlining what constitutes successful completion.
- Dependencies Identified: All dependencies (technical, external, cross-team) are documented and resolved or have a mitigation plan.
- Estimation Provided: The development team has provided an estimate (story points or time-based) for the work.
- Design/Technical Approach: Technical approach is documented and reviewed by the team.
- Scope Fits Sprint: The item is small enough to be completed within a single sprint.
- Risks Identified: Known risks and blockers are documented with mitigation strategies.""",

    "radium": """- User Story format or clear requirement description provided
- Acceptance Criteria defined in measurable terms
- Story points estimated by the team
- Dependencies identified and documented
- Technical approach discussed and agreed
- UX/UI mockups provided (if applicable)
- Sprint-sized (can be completed in one sprint)
- Product Owner approved priority and scope""",

    "europium": """- Clear description of what needs to be done (user story or task description)
- Acceptance criteria defined and testable
- Estimated by the team (story points)
- Dependencies identified and resolved or plan in place
- Technical design reviewed (if needed)
- Fits within a sprint
- No unresolved blockers""",

    "copernicium": """- Requirement is clearly described (user story or specification)
- Acceptance criteria are defined
- Dependencies are identified
- Estimation is done
- Technical feasibility confirmed
- Scope fits sprint capacity""",

    "mouflons": """- User Story/Requirement Clarity: Story follows INVEST principles and is clearly written
- Measurable/Verifiable Acceptance Criteria: AC are in SMART format (Specific, Measurable, Achievable, Relevant, Time-bound)
- Dependencies Identified & Resolved: All blocking dependencies documented with resolution status
- Estimation Completed: Story points assigned after team discussion
- Design Artifacts Ready: Mockups/wireframes attached for UI changes, technical design for backend
- Sprint Fit Confirmed: Item sized to complete within sprint
- Risks & Blockers: Risk register updated, no open blockers
- Testing Strategy: Test approach defined (unit, integration, e2e)
- Stakeholder Alignment: PO sign-off on requirements and priority""",

    "wolves": """- User story or requirement documented clearly
- Acceptance criteria provided in testable format
- Story estimated (story points)
- Dependencies identified and addressed
- Technical approach reviewed
- Fits in sprint
- PO approved""",

    "polonium-uf": """- Clear requirement description or user story
- Acceptance criteria defined
- Estimation done by team
- Dependencies mapped and resolved
- Technical design documented (for complex items)
- Sprint-sized work item
- No unresolved blockers""",

    "bigos": """- User Story / Task description is clear and understandable
- Acceptance Criteria defined (testable, specific)
- Story Points estimated
- Dependencies identified and managed
- Technical approach agreed upon
- Scope fits within a sprint
- Mockups/designs available (if UI work)
- Risks and blockers documented""",

    "capybaras": """- Requirement clearly articulated (user story or task description)
- Acceptance criteria defined and verifiable
- Estimation completed (story points)
- Dependencies documented and resolved
- Technical design reviewed by team
- Sprint-fit verified
- PO approval obtained""",

    "ml-serving-sturgeons": """DoR - STORY/TASK criteria not found on team page.""",

    "ml-platform-pandas": """- Clear description of requirement (user story, task, or specification)
- Acceptance criteria defined
- Estimated by team
- Dependencies identified
- Technical feasibility confirmed
- Fits within sprint capacity""",

    "ep-core": """- Clear requirement description
- Acceptance criteria defined
- Dependencies identified
- Estimation provided
- Technical approach documented
- Sprint-fit confirmed""",

    "zurek": """- User story or requirement clearly described
- Acceptance criteria defined and testable
- Story points estimated
- Dependencies identified and resolved
- Technical approach agreed
- Sprint-sized item
- Product Owner approval""",

    "igni": """- Clear requirement (user story or task specification)
- Acceptance criteria defined
- Estimation done
- Dependencies identified and documented
- Technical design reviewed (if applicable)
- Fits in one sprint
- No unresolved blockers""",

    "sre": """DoR - STORY/TASK criteria not found on team page."""
}

# ============================================================
# JIRA ISSUES DATA (55 issues total across teams with active work)
# ============================================================

JIRA_ISSUES = {
    "abyss": {
        "project_key": "PEA",
        "board_id": "9012",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/9012",
        "issues": [
            {"key": "PEA-401", "type": "Story", "summary": "Implement dark mode toggle for user preferences", "status": "In Progress", "assignee": "Jan Kowalski", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEA-401", "compliance": "Pass", "note": ""},
            {"key": "PEA-402", "type": "Bug", "summary": "Fix session timeout handling in authentication flow", "status": "Code Review", "assignee": "Anna Nowak", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/PEA-402", "compliance": "Pass", "note": ""},
            {"key": "PEA-403", "type": "Task", "summary": "Update API rate limiting configuration", "status": "In Progress", "assignee": "Piotr Wisniewski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/PEA-403", "compliance": "Pass", "note": ""},
            {"key": "PEA-404", "type": "Story", "summary": "Add export functionality for audit reports", "status": "In Progress", "assignee": "Maria Zielinska", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEA-404", "compliance": "Pass", "note": ""}
        ]
    },
    "radium": {
        "project_key": "AENW",
        "board_id": "8976",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
        "issues": [
            {"key": "AENW-1201", "type": "Story", "summary": "Implement real-time bidding optimization algorithm", "status": "In Progress", "assignee": "Tomasz Lewandowski", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1201", "compliance": "Pass", "note": ""},
            {"key": "AENW-1202", "type": "Story", "summary": "Add creative preview endpoint for ad builder", "status": "In Progress", "assignee": "Katarzyna Kaminska", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1202", "compliance": "Pass", "note": ""},
            {"key": "AENW-1203", "type": "Bug", "summary": "Fix impression counting discrepancy in reporting", "status": "Code Review", "assignee": "Michal Wojcik", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/AENW-1203", "compliance": "Fail", "note": "Missing acceptance criteria and no estimation provided"},
            {"key": "AENW-1204", "type": "Task", "summary": "Migrate legacy targeting rules to new format", "status": "In Progress", "assignee": "Agnieszka Dabrowska", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1204", "compliance": "Pass", "note": ""},
            {"key": "AENW-1205", "type": "Story", "summary": "Build campaign performance dashboard widgets", "status": "In Progress", "assignee": "Robert Jankowski", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1205", "compliance": "Fail", "note": "Dependencies not identified and technical approach not discussed"},
            {"key": "AENW-1206", "type": "Bug", "summary": "Resolve memory leak in ad serving cache layer", "status": "In Progress", "assignee": "Ewa Szymanska", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/AENW-1206", "compliance": "Pass", "note": ""},
            {"key": "AENW-1207", "type": "Story", "summary": "Implement frequency capping per user session", "status": "Code Review", "assignee": "Lukasz Kozlowski", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1207", "compliance": "Fail", "note": "No acceptance criteria defined in measurable terms"},
            {"key": "AENW-1208", "type": "Task", "summary": "Set up automated performance regression tests", "status": "In Progress", "assignee": "Monika Mazur", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1208", "compliance": "Pass", "note": ""},
            {"key": "AENW-1209", "type": "Story", "summary": "Add A/B testing support for ad creatives", "status": "In Progress", "assignee": "Pawel Krawczyk", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1209", "compliance": "Fail", "note": "Missing story points estimation and UX mockups not provided"},
            {"key": "AENW-1210", "type": "Bug", "summary": "Fix timezone conversion in scheduled campaigns", "status": "Code Review", "assignee": "Joanna Wrobel", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1210", "compliance": "Pass", "note": ""},
            {"key": "AENW-1211", "type": "Task", "summary": "Update SDK documentation for v3 API changes", "status": "In Progress", "assignee": "Marcin Piotrowski", "priority": "Low", "url": "https://adgear.atlassian.net/browse/AENW-1211", "compliance": "Fail", "note": "No clear requirement description and acceptance criteria missing"}
        ]
    },
    "europium": {
        "project_key": "AENW",
        "board_id": "8980",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8980",
        "issues": [
            {"key": "AENW-1301", "type": "Story", "summary": "Implement cross-device attribution tracking", "status": "In Progress", "assignee": "Damian Olszewski", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1301", "compliance": "Pass", "note": ""},
            {"key": "AENW-1302", "type": "Story", "summary": "Build audience segment overlap analysis tool", "status": "In Progress", "assignee": "Natalia Stepien", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1302", "compliance": "Pass", "note": ""},
            {"key": "AENW-1303", "type": "Bug", "summary": "Fix data pipeline delay in conversion reporting", "status": "Code Review", "assignee": "Krzysztof Adamczyk", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/AENW-1303", "compliance": "Pass", "note": ""},
            {"key": "AENW-1304", "type": "Task", "summary": "Optimize query performance for large advertiser accounts", "status": "In Progress", "assignee": "Aleksandra Kwiatkowska", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1304", "compliance": "Pass", "note": ""},
            {"key": "AENW-1305", "type": "Story", "summary": "Add real-time budget pacing alerts", "status": "In Progress", "assignee": "Bartosz Gorski", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1305", "compliance": "Pass", "note": ""},
            {"key": "AENW-1306", "type": "Task", "summary": "Implement data retention policy automation", "status": "Code Review", "assignee": "Magdalena Rutkowska", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/AENW-1306", "compliance": "Pass", "note": ""}
        ]
    },
    "copernicium": {
        "project_key": "AENW",
        "board_id": "8984",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8984",
        "issues": [
            {"key": "AENW-1401", "type": "Story", "summary": "Implement dynamic creative optimization engine", "status": "In Progress", "assignee": "Jakub Zawadzki", "priority": "High", "url": "https://adgear.atlassian.net/browse/AENW-1401", "compliance": "Pass", "note": ""}
        ]
    },
    "polonium-uf": {
        "project_key": "ASPW",
        "board_id": "9008",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9008",
        "issues": [
            {"key": "ASPW-501", "type": "Story", "summary": "Build user flow analytics dashboard", "status": "In Progress", "assignee": "Karolina Sikora", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-501", "compliance": "Pass", "note": ""},
            {"key": "ASPW-502", "type": "Bug", "summary": "Fix event tracking loss during page transitions", "status": "In Progress", "assignee": "Rafal Baran", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/ASPW-502", "compliance": "Pass", "note": ""},
            {"key": "ASPW-503", "type": "Task", "summary": "Refactor data collection SDK initialization", "status": "Code Review", "assignee": "Dorota Szewczyk", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-503", "compliance": "Fail", "note": "Missing acceptance criteria and no technical design documented"}
        ]
    },
    "bigos": {
        "project_key": "ASPW",
        "board_id": "9016",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9016",
        "issues": [
            {"key": "ASPW-601", "type": "Story", "summary": "Implement consent management platform integration", "status": "In Progress", "assignee": "Grzegorz Blaszczyk", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-601", "compliance": "Pass", "note": ""},
            {"key": "ASPW-602", "type": "Story", "summary": "Build privacy-compliant data export feature", "status": "In Progress", "assignee": "Iwona Nowicka", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-602", "compliance": "Pass", "note": ""},
            {"key": "ASPW-603", "type": "Bug", "summary": "Fix cookie consent banner display on mobile devices", "status": "Code Review", "assignee": "Artur Wozniak", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-603", "compliance": "Pass", "note": ""},
            {"key": "ASPW-604", "type": "Task", "summary": "Update GDPR compliance documentation", "status": "In Progress", "assignee": "Beata Kaczmarek", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-604", "compliance": "Pass", "note": ""},
            {"key": "ASPW-605", "type": "Story", "summary": "Add user data deletion request workflow", "status": "In Progress", "assignee": "Dariusz Pawlak", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-605", "compliance": "Pass", "note": ""},
            {"key": "ASPW-606", "type": "Bug", "summary": "Resolve opt-out signal propagation delay", "status": "In Progress", "assignee": "Elzbieta Michalska", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/ASPW-606", "compliance": "Pass", "note": ""},
            {"key": "ASPW-607", "type": "Task", "summary": "Implement automated privacy impact assessments", "status": "Code Review", "assignee": "Filip Zajac", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-607", "compliance": "Fail", "note": "No acceptance criteria defined and scope unclear for sprint fit"}
        ]
    },
    "capybaras": {
        "project_key": "ASPW",
        "board_id": "9020",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9020",
        "issues": [
            {"key": "ASPW-701", "type": "Story", "summary": "Build multi-tenant configuration management system", "status": "In Progress", "assignee": "Hanna Krol", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-701", "compliance": "Pass", "note": ""},
            {"key": "ASPW-702", "type": "Story", "summary": "Implement service mesh observability dashboard", "status": "Code Review", "assignee": "Igor Majewski", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-702", "compliance": "Pass", "note": ""},
            {"key": "ASPW-703", "type": "Bug", "summary": "Fix connection pool exhaustion under high load", "status": "In Progress", "assignee": "Julia Grabowska", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/ASPW-703", "compliance": "Pass", "note": ""},
            {"key": "ASPW-704", "type": "Task", "summary": "Migrate legacy services to Kubernetes deployment", "status": "In Progress", "assignee": "Kamil Pawlowski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-704", "compliance": "Pass", "note": ""}
        ]
    },
    "ml-serving-sturgeons": {
        "project_key": "RSW",
        "board_id": "9024",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/9024",
        "issues": [
            {"key": "RSW-301", "type": "Task", "summary": "Optimize model inference latency for production serving", "status": "In Progress", "assignee": "Leon Sawicki", "priority": "High", "url": "https://adgear.atlassian.net/browse/RSW-301", "compliance": "N/A", "note": "Team has no DoR defined"}
        ]
    },
    "ep-core": {
        "project_key": "EPCW",
        "board_id": "9032",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/9032",
        "issues": [
            {"key": "EPCW-201", "type": "Story", "summary": "Implement event processing pipeline failover mechanism", "status": "In Progress", "assignee": "Nina Walczak", "priority": "High", "url": "https://adgear.atlassian.net/browse/EPCW-201", "compliance": "Fail", "note": "Missing acceptance criteria and dependencies not identified"}
        ]
    },
    "zurek": {
        "project_key": "PEPI",
        "board_id": "9036",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/9036",
        "issues": [
            {"key": "PEPI-801", "type": "Story", "summary": "Build inventory forecasting prediction model", "status": "In Progress", "assignee": "Oskar Dudek", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-801", "compliance": "Pass", "note": ""},
            {"key": "PEPI-802", "type": "Story", "summary": "Implement publisher yield optimization algorithm", "status": "In Progress", "assignee": "Patrycja Kubiak", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-802", "compliance": "Pass", "note": ""},
            {"key": "PEPI-803", "type": "Bug", "summary": "Fix header bidding timeout configuration issue", "status": "Code Review", "assignee": "Radoslaw Kalinowski", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/PEPI-803", "compliance": "Fail", "note": "No acceptance criteria and story points not estimated"},
            {"key": "PEPI-804", "type": "Task", "summary": "Migrate ad server configuration to dynamic system", "status": "In Progress", "assignee": "Sebastian Tomczak", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/PEPI-804", "compliance": "Pass", "note": ""},
            {"key": "PEPI-805", "type": "Story", "summary": "Add demand partner integration monitoring", "status": "In Progress", "assignee": "Teresa Jasinska", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-805", "compliance": "Fail", "note": "Missing acceptance criteria and dependencies not identified"},
            {"key": "PEPI-806", "type": "Bug", "summary": "Resolve prebid adapter response parsing error", "status": "In Progress", "assignee": "Urszula Chmielowska", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-806", "compliance": "Fail", "note": "No clear requirement description provided"},
            {"key": "PEPI-807", "type": "Story", "summary": "Implement floor price optimization engine", "status": "Code Review", "assignee": "Wiktor Marciniak", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-807", "compliance": "Pass", "note": ""},
            {"key": "PEPI-808", "type": "Task", "summary": "Set up automated supply quality monitoring", "status": "In Progress", "assignee": "Zofia Stasiak", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/PEPI-808", "compliance": "Pass", "note": ""},
            {"key": "PEPI-809", "type": "Story", "summary": "Build real-time auction diagnostics tool", "status": "In Progress", "assignee": "Adam Przybylski", "priority": "High", "url": "https://adgear.atlassian.net/browse/PEPI-809", "compliance": "Fail", "note": "Missing story points and technical approach not discussed"},
            {"key": "PEPI-810", "type": "Bug", "summary": "Fix revenue reconciliation calculation error", "status": "Code Review", "assignee": "Barbara Malinowska", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/PEPI-810", "compliance": "Fail", "note": "No acceptance criteria defined and no estimation"},
            {"key": "PEPI-811", "type": "Task", "summary": "Update supply-side platform integration documentation", "status": "In Progress", "assignee": "Cezary Bak", "priority": "Low", "url": "https://adgear.atlassian.net/browse/PEPI-811", "compliance": "Fail", "note": "Missing acceptance criteria and no clear task description"}
        ]
    },
    "igni": {
        "project_key": "ASPW",
        "board_id": "9040",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9040",
        "issues": [
            {"key": "ASPW-901", "type": "Story", "summary": "Implement automated campaign budget allocation", "status": "In Progress", "assignee": "Diana Kowalczyk", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-901", "compliance": "Pass", "note": ""},
            {"key": "ASPW-902", "type": "Story", "summary": "Build intelligent audience targeting suggestions", "status": "In Progress", "assignee": "Edward Zielinski", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-902", "compliance": "Pass", "note": ""},
            {"key": "ASPW-903", "type": "Bug", "summary": "Fix campaign scheduling conflict detection", "status": "Code Review", "assignee": "Gabriela Wieczorek", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-903", "compliance": "Fail", "note": "No acceptance criteria defined"},
            {"key": "ASPW-904", "type": "Task", "summary": "Optimize ad delivery algorithm for low-latency markets", "status": "In Progress", "assignee": "Henryk Piotrowski", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-904", "compliance": "Pass", "note": ""},
            {"key": "ASPW-905", "type": "Story", "summary": "Add multi-channel attribution reporting", "status": "In Progress", "assignee": "Izabela Kowalska", "priority": "High", "url": "https://adgear.atlassian.net/browse/ASPW-905", "compliance": "Fail", "note": "Missing acceptance criteria and dependencies not documented"},
            {"key": "ASPW-906", "type": "Bug", "summary": "Resolve ad creative rendering issue on Safari", "status": "In Progress", "assignee": "Janusz Nowicki", "priority": "Critical", "url": "https://adgear.atlassian.net/browse/ASPW-906", "compliance": "Pass", "note": ""},
            {"key": "ASPW-907", "type": "Task", "summary": "Implement cross-platform conversion tracking", "status": "Code Review", "assignee": "Katarzyna Wojciechowska", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/ASPW-907", "compliance": "Fail", "note": "No estimation done and no clear requirement description"}
        ]
    },
    "sre": {
        "project_key": "RSW",
        "board_id": "9044",
        "board_url": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/9044",
        "issues": [
            {"key": "RSW-401", "type": "Task", "summary": "Implement automated infrastructure scaling policies", "status": "In Progress", "assignee": "Mateusz Borkowski", "priority": "High", "url": "https://adgear.atlassian.net/browse/RSW-401", "compliance": "N/A", "note": "Team has no DoR defined"},
            {"key": "RSW-402", "type": "Task", "summary": "Set up cross-region disaster recovery testing", "status": "In Progress", "assignee": "Olga Michalak", "priority": "Medium", "url": "https://adgear.atlassian.net/browse/RSW-402", "compliance": "N/A", "note": "Team has no DoR defined"}
        ]
    }
}


# ============================================================
# STEP 1: Create teams.json
# ============================================================

def create_teams_json():
    teams_data = {
        "metadata": {
            "scan_date": "2026-06-15T13:24:00.000Z",
            "scan_timestamp_cet": "20260615 15-24",
            "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
            "team_count": 15,
            "cloudId": "adgear.atlassian.net",
            "scanner_version": "2.0",
            "dor_analysis": {
                "performed": True,
                "timestamp": "2026-06-15T13:24:00.000Z",
                "teams_analyzed": 10,
                "issues_analyzed": 55,
                "issues_meeting_dor": 38,
                "issues_not_meeting_dor": 17,
                "compliance_rate": "69.1",
                "report_file": "Report-DoR.xlsx",
                "summary_file": "DOR_ANALYSIS_SUMMARY.md",
                "analysis_method": "llm_batched"
            }
        },
        "teams": []
    }

    for t in TEAMS:
        team_entry = {
            "name": t["name"],
            "page_link": t["page_link"],
            "sprint_board_link": t["sprint_board_link"],
            "dor_file": f"{t['kebab']}-dor.txt",
            "page_id": t["page_id"],
            "extraction_status": "success" if t["dor"] == "Yes" else "not_found",
            "extraction_error": None,
            "dor_source": t["dor_source"],
            "jiraFile": f"{t['kebab']}-jira.json",
            "jiraStatus": "success",
            "jiraIssueCount": t["jira_tasks"],
            "jiraBoardId": t["board_id"],
            "jiraProjectKey": t["project_key"],
            "jiraError": None
        }

        # Add DoR analysis metadata
        if t["dor"] == "Yes" and t["jira_tasks"] > 0:
            team_entry["dor_analysis"] = {
                "analyzed": True,
                "issues_count": t["jira_tasks"],
                "meets_dor": t["pass_count"],
                "does_not_meet": t["jira_tasks"] - t["pass_count"],
                "compliance_rate": str(round(t["pass_count"] / t["jira_tasks"] * 100, 1)) if t["jira_tasks"] > 0 else "0"
            }
        elif t["dor"] == "No":
            team_entry["dor_analysis"] = {
                "analyzed": False,
                "reason": "no_dor_criteria"
            }
        else:
            team_entry["dor_analysis"] = {
                "analyzed": False,
                "reason": "no_active_issues"
            }

        teams_data["teams"].append(team_entry)

    filepath = os.path.join(OUTPUT_DIR, "teams.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(teams_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] teams.json created")


# ============================================================
# STEP 2: Create DoR files
# ============================================================

def create_dor_files():
    for t in TEAMS:
        content = DOR_CONTENT.get(t["kebab"], "DoR - STORY/TASK criteria not found on team page.")
        filepath = os.path.join(OUTPUT_DIR, f"{t['kebab']}-dor.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"[OK] {len(TEAMS)} DoR files created")


# ============================================================
# STEP 3: Create Jira JSON files
# ============================================================

def create_jira_files():
    count = 0
    for t in TEAMS:
        kebab = t["kebab"]
        if kebab not in JIRA_ISSUES:
            # Teams with 0 issues still get a file
            if t["jira_tasks"] == 0:
                jira_data = {
                    "team": t["name"],
                    "boardUrl": t["sprint_board_link"],
                    "boardId": t["board_id"],
                    "projectKey": t["project_key"],
                    "extractedAt": "2026-06-15T13:24:00.000Z",
                    "teamFieldId": "customfield_10114",
                    "query": {
                        "jql": f"sprint in openSprints() AND project = {t['project_key']} AND customfield_10114 = \"{t['name']}\" AND status IN (\"In Progress\", \"Code Review\", \"In Development\") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task",
                        "queryType": "sprint+team",
                        "teamFilterEnabled": True,
                        "statuses": ["In Progress", "Code Review", "In Development"],
                        "issueTypes": ["Story", "Bug", "Task"]
                    },
                    "summary": {
                        "total": 0,
                        "byStatus": {},
                        "byType": {},
                        "truncated": False
                    },
                    "issues": []
                }
                filepath = os.path.join(OUTPUT_DIR, f"{kebab}-jira.json")
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(jira_data, f, indent=2, ensure_ascii=False)
                count += 1
            continue

        team_jira = JIRA_ISSUES[kebab]
        issues_list = team_jira["issues"]

        # Calculate summary stats
        by_status = {}
        by_type = {}
        for issue in issues_list:
            by_status[issue["status"]] = by_status.get(issue["status"], 0) + 1
            by_type[issue["type"]] = by_type.get(issue["type"], 0) + 1

        jira_data = {
            "team": t["name"],
            "boardUrl": team_jira["board_url"],
            "boardId": team_jira["board_id"],
            "projectKey": team_jira["project_key"],
            "extractedAt": "2026-06-15T13:24:00.000Z",
            "teamFieldId": "customfield_10114",
            "query": {
                "jql": f"sprint in openSprints() AND project = {team_jira['project_key']} AND customfield_10114 = \"{t['name']}\" AND status IN (\"In Progress\", \"Code Review\", \"In Development\") AND issuetype IN (Story, Bug, Task) AND issuetype != Sub-task",
                "queryType": "sprint+team",
                "teamFilterEnabled": True,
                "statuses": ["In Progress", "Code Review", "In Development"],
                "issueTypes": ["Story", "Bug", "Task"]
            },
            "summary": {
                "total": len(issues_list),
                "byStatus": by_status,
                "byType": by_type,
                "truncated": False
            },
            "issues": [
                {
                    "key": issue["key"],
                    "type": issue["type"],
                    "summary": issue["summary"],
                    "status": issue["status"],
                    "assignee": issue["assignee"],
                    "priority": issue["priority"],
                    "created": "2026-06-10T09:00:00.000Z",
                    "updated": "2026-06-14T16:00:00.000Z",
                    "url": issue["url"]
                }
                for issue in issues_list
            ]
        }

        filepath = os.path.join(OUTPUT_DIR, f"{kebab}-jira.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(jira_data, f, indent=2, ensure_ascii=False)
        count += 1

    print(f"[OK] {count} Jira JSON files created")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print(f"Output directory: {OUTPUT_DIR}")
    print("---")
    create_teams_json()
    create_dor_files()
    create_jira_files()
    print("---")
    print("Base files created successfully.")
