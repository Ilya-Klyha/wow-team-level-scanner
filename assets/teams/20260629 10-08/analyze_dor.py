#!/usr/bin/env python3
"""
DoR Compliance Analysis and Quality Assessment
Produces: compliance_data.json, summary_data.json, quality_data.json
"""
import json
import re
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
with open(os.path.join(OUTPUT_DIR, "issue_descriptions.json"), "r", encoding="utf-8") as f:
    issues = json.load(f)

with open(os.path.join(OUTPUT_DIR, "teams.json"), "r", encoding="utf-8") as f:
    teams_config = json.load(f)

# Team name pattern to team name mapping
TEAM_PATTERN_MAP = {
    "PE - WAW - Abyss": "Abyss",
    "AE - WAW - Radium": "Radium",
    "AP - WAW - Europium": "Europium",
    "AE - WAW - Copernicium": "Copernicium",
    "AS - WAW - Mouflons": "Mouflons",
    "AS - WAW - Wolves": "Wolves",
    "AS - WAW - Polonium UF": "Polonium UF",
    "AS - WAW - Bigos": "Bigos",
    "AS - WAW - Capybaras": "Capybaras",
    "T - WAW - ML Sturgeons": "ML Serving Sturgeons",
    "T - WAW - ML Pandas": "ML Platform Pandas",
    "T - WAW - Zurek": "Zurek",
    "T - WAW - EP Core": "EP Core",
    "AP - WAW - Igni": "Igni",
    "T - WAW - Embedded SREs SRPOL": "SRE",
}

# Teams without DoR (excluded from compliance)
TEAMS_WITHOUT_DOR = {"ML Serving Sturgeons", "SRE"}

# Load DoR files for teams that have them
team_dors = {}
for team in teams_config["teams"]:
    if team["dor_status"] == "found" and team["dor_file"]:
        dor_path = os.path.join(OUTPUT_DIR, team["dor_file"])
        if os.path.exists(dor_path):
            with open(dor_path, "r", encoding="utf-8") as f:
                team_dors[team["name"]] = f.read()


def has_acceptance_criteria(description):
    """Check if description contains identifiable acceptance criteria."""
    if not description or not description.strip():
        return False

    desc_lower = description.lower()

    # Check for explicit AC sections
    ac_patterns = [
        r'acceptance\s+criteria',
        r'\bac\b[:\s]',
        r'definition\s+of\s+done',
        r'given\s+.*\s+when\s+.*\s+then',
        r'condition\s+to\s+complete',
    ]
    for pattern in ac_patterns:
        if re.search(pattern, desc_lower):
            return True

    # Check for bullet list patterns that look like AC
    # Look for checkbox patterns like "* [ ]" or "- [ ]"
    if re.search(r'[\*\-]\s*\[[\sx]\]', description):
        return True

    # Check for "Requirements" section with MUST/SHOULD/COULD verifiable statements
    # This is a common alternative to explicit AC in infrastructure/platform teams
    if re.search(r'#{1,4}\s*requirements', desc_lower) or re.search(r'\*\*requirements?\*\*', desc_lower):
        # Must have verifiable bullets (We MUST, We SHOULD, etc.)
        if re.search(r'we\s+(must|should|could|have\s+to)', desc_lower):
            return True
    # Also catch "Requirements" as a standalone line followed by verifiable statements
    if re.search(r'requirements', desc_lower) and re.search(r'we\s+must', desc_lower):
        return True

    return False


def has_clear_description(description):
    """Check if the issue has a meaningful description."""
    if not description or not description.strip():
        return False
    # Very short descriptions are not meaningful
    if len(description.strip()) < 30:
        return False
    return True


def analyze_compliance(issue_key, issue_data, team_name, team_dor_text):
    """Analyze whether an issue meets its team's DoR. Returns (pass/fail, note)."""
    description = issue_data.get("description", "")

    # Check 1: Does the issue have a clear description?
    if not has_clear_description(description):
        return "Fail", "No description or description too brief to meet DoR requirements"

    # Check 2: Does the team's DoR require AC?
    dor_lower = team_dor_text.lower()
    dor_requires_ac = any(term in dor_lower for term in [
        "acceptance criteria", "measurable ac", "verifiable ac",
        "testable acceptance", "clear ac", "defined ac"
    ])

    if dor_requires_ac:
        if not has_acceptance_criteria(description):
            return "Fail", "Missing identifiable Acceptance Criteria (required by team DoR)"

    # Check 3: Does the DoR require clear user story/requirement?
    dor_requires_clarity = any(term in dor_lower for term in [
        "user story", "requirement clarity", "clearly articulated",
        "clear description", "well described", "clear problem statement"
    ])

    if dor_requires_clarity:
        # Check if description has some structure (user story format, headers, etc.)
        has_structure = bool(
            re.search(r'(as\s+a|i\s+want|so\s+that|context|requirement|goal|problem)', description.lower())
            or re.search(r'(##|###|\*\*)', description)  # markdown headers or bold
            or len(description.strip()) > 100  # substantial description
        )
        if not has_structure:
            return "Fail", "Description lacks clarity/structure required by team DoR"

    # Check 4: Dependencies mentioned as unresolved blockers
    desc_lower = description.lower()
    if re.search(r'(blocked\s+by|waiting\s+for|depends\s+on.*not\s+ready|unresolved\s+dependency)', desc_lower):
        return "Fail", "Description mentions unresolved blocking dependencies"

    # Check 5: Placeholder/TODO AC
    if re.search(r'\[TODO\]\s*update', description) and not has_acceptance_criteria(description):
        return "Fail", "Acceptance Criteria marked as TODO/placeholder - not yet defined"

    return "Pass", ""


# Build compliance data
compliance_data = []
team_issue_counts = {}  # team_name -> {total: N, pass: N}

for issue_key, issue_data in issues.items():
    team_pattern = issue_data.get("team")
    if not team_pattern:
        continue  # Skip issues without team assignment

    team_name = TEAM_PATTERN_MAP.get(team_pattern)
    if not team_name:
        continue

    # Skip teams without DoR
    if team_name in TEAMS_WITHOUT_DOR:
        continue

    # Skip if team has no DoR text loaded
    if team_name not in team_dors:
        continue

    # Analyze compliance
    result, note = analyze_compliance(issue_key, issue_data, team_name, team_dors[team_name])

    # Build URL
    url = f"https://adgear.atlassian.net/browse/{issue_key}"

    compliance_entry = {
        "team": team_name,
        "issue_key": issue_key,
        "issue_type": "Story",  # Default since we don't have type info in descriptions
        "url": url,
        "title": issue_data.get("summary", ""),
        "status": "In Progress",
        "assignee": "",
        "dor_compliance": result,
        "note": note,
    }
    compliance_data.append(compliance_entry)

    # Track counts per team
    if team_name not in team_issue_counts:
        team_issue_counts[team_name] = {"total": 0, "pass": 0}
    team_issue_counts[team_name]["total"] += 1
    if result == "Pass":
        team_issue_counts[team_name]["pass"] += 1

# Sort compliance data by team
compliance_data.sort(key=lambda x: (x["team"], x["issue_key"]))

# Build summary data (all 15 teams)
all_team_names = [t["name"] for t in teams_config["teams"]]
summary_data = []
for team_name in all_team_names:
    has_dor = team_name not in TEAMS_WITHOUT_DOR
    counts = team_issue_counts.get(team_name, {"total": 0, "pass": 0})

    if has_dor and counts["total"] > 0:
        pct = round(counts["pass"] / counts["total"] * 100)
        pct_str = f"{pct}%"
    else:
        pct_str = "-"

    summary_data.append({
        "team": team_name,
        "dor": "Yes" if has_dor else "No",
        "jira_tasks": counts["total"],
        "pct_fitting_dor": pct_str,
    })

# DoR Quality Assessment
# 10 criteria mapping
QUALITY_CRITERIA = [
    "User Story/Requirement Clarity",
    "Acceptance Criteria",
    "Estimation/Sizing",
    "Dependencies Identified & Resolved",
    "Design/UX Specification",
    "Scope/Sprint Fit",
    "Risks/Blockers Identified",
    "Stakeholder Alignment",
    "Technical Feasibility Confirmed",
    "Testing Strategy/Approach",
]

def assess_dor_quality(team_name, dor_text):
    """Assess how many of the 10 standard criteria the team's DoR covers."""
    dor_lower = dor_text.lower()
    covered = []
    missing = []

    # 1. User Story/Requirement Clarity
    if any(t in dor_lower for t in ["user story", "requirement clarity", "clearly articulated",
                                      "clear description", "well described", "clear problem statement",
                                      "task subject"]):
        covered.append(QUALITY_CRITERIA[0])
    else:
        missing.append(QUALITY_CRITERIA[0])

    # 2. Acceptance Criteria
    if any(t in dor_lower for t in ["acceptance criteria", "measurable ac", "verifiable ac",
                                      "testable acceptance", "defined ac"]):
        covered.append(QUALITY_CRITERIA[1])
    else:
        missing.append(QUALITY_CRITERIA[1])

    # 3. Estimation/Sizing
    if any(t in dor_lower for t in ["estimate", "estimation", "story points", "sizing",
                                      "estimated by the team", "planning poker"]):
        covered.append(QUALITY_CRITERIA[2])
    else:
        missing.append(QUALITY_CRITERIA[2])

    # 4. Dependencies Identified & Resolved
    if any(t in dor_lower for t in ["dependencies", "blocking tasks", "blockers are resolved",
                                      "blocking", "dependent"]):
        covered.append(QUALITY_CRITERIA[3])
    else:
        missing.append(QUALITY_CRITERIA[3])

    # 5. Design/UX Specification
    if any(t in dor_lower for t in ["design", "ux", "figma", "mockup", "wireframe",
                                      "ui/ux", "visual", "mock"]):
        covered.append(QUALITY_CRITERIA[4])
    else:
        missing.append(QUALITY_CRITERIA[4])

    # 6. Scope/Sprint Fit
    if any(t in dor_lower for t in ["scope", "sprint fit", "fit within a sprint",
                                      "broken down", "decomposed", "small enough",
                                      "work size"]):
        covered.append(QUALITY_CRITERIA[5])
    else:
        missing.append(QUALITY_CRITERIA[5])

    # 7. Risks/Blockers Identified
    if any(t in dor_lower for t in ["risk", "blocker", "risks are estimated",
                                      "potential blocker"]):
        covered.append(QUALITY_CRITERIA[6])
    else:
        missing.append(QUALITY_CRITERIA[6])

    # 8. Stakeholder Alignment
    if any(t in dor_lower for t in ["stakeholder", "po approval", "po responsibility",
                                      "confirmed with the team", "agreement with team",
                                      "collaborative", "contact person"]):
        covered.append(QUALITY_CRITERIA[7])
    else:
        missing.append(QUALITY_CRITERIA[7])

    # 9. Technical Feasibility Confirmed
    if any(t in dor_lower for t in ["technical feasibility", "techspec", "tech spec",
                                      "investigated by engineering", "investigation",
                                      "technically feasible", "architect"]):
        covered.append(QUALITY_CRITERIA[8])
    else:
        missing.append(QUALITY_CRITERIA[8])

    # 10. Testing Strategy/Approach
    if any(t in dor_lower for t in ["testing", "test", "testcases", "test approach",
                                      "test data", "monitoring and alerting"]):
        covered.append(QUALITY_CRITERIA[9])
    else:
        missing.append(QUALITY_CRITERIA[9])

    coverage = len(covered) * 10
    note = f"Missing: {', '.join(missing)}" if missing else "All 10 criteria covered"

    return coverage, note


quality_data = []
for team in teams_config["teams"]:
    team_name = team["name"]
    if team_name in TEAMS_WITHOUT_DOR:
        continue
    if team_name not in team_dors:
        continue

    coverage, note = assess_dor_quality(team_name, team_dors[team_name])
    quality_data.append({
        "team": team_name,
        "coverage": coverage,
        "note": note,
    })

# Write outputs
with open(os.path.join(OUTPUT_DIR, "compliance_data.json"), "w", encoding="utf-8") as f:
    json.dump(compliance_data, f, indent=2, ensure_ascii=False)

with open(os.path.join(OUTPUT_DIR, "summary_data.json"), "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)

with open(os.path.join(OUTPUT_DIR, "quality_data.json"), "w", encoding="utf-8") as f:
    json.dump(quality_data, f, indent=2, ensure_ascii=False)

# Print statistics
total_issues = len(compliance_data)
total_pass = sum(1 for d in compliance_data if d["dor_compliance"] == "Pass")
total_fail = total_issues - total_pass
fail_rate = round(total_fail / total_issues * 100, 1) if total_issues > 0 else 0

print(f"=== DoR Compliance Analysis Complete ===")
print(f"  Total issues analyzed: {total_issues}")
print(f"  Pass: {total_pass}")
print(f"  Fail: {total_fail}")
print(f"  Failure rate: {fail_rate}%")
print(f"")
print(f"=== DoR Quality Assessment ===")
for q in quality_data:
    print(f"  {q['team']}: {q['coverage']}/100")
print(f"")
print(f"Files written:")
print(f"  - compliance_data.json")
print(f"  - summary_data.json")
print(f"  - quality_data.json")
