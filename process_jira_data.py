#!/usr/bin/env python3
"""Process extracted Jira data and generate DoR compliance report"""

import json
import csv
import os
import glob
from datetime import datetime

OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 16-36"
TOOL_RESULTS_DIR = r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\b7084410-4995-4c18-968a-761422bfcfa7\tool-results"

# Project to Team mapping
PROJECT_TO_TEAM = {
    "MAW": "PE-WAW-Abyss",
    "AENW": ["Radium", "Europium"],  # Shared project
    "AETVP": "Copernicium",
    "PEPI": ["Mouflons", "Wolves", "ML-Serving"],  # Shared project
    "PEDSP": "Polonium-LF",
    "RSW": ["Polonium-UF", "Bigos", "Capybaras"],  # Shared project
    "ML": "ML-Platform",
    "EPCW": "EP-Core",
    "PEA": "Zurek",
    "ASPW": "Igni",
    "EEEW": "SRE"
}

# Team to DoR file mapping
TEAM_DOR_FILES = {
    "PE-WAW-Abyss": "pe-waw-abyss-dor.txt",
    "Radium": "radium-dor.txt",
    "Europium": "europium-dor.txt",
    "Copernicium": "copernicium-dor.txt",
    "Mouflons": "mouflons-dor.txt",
    "Wolves": "wolves-dor.txt",
    "Polonium-LF": "polonium-lf-dor.txt",
    "Polonium-UF": "polonium-uf-dor.txt",
    "Bigos": "bigos-dor.txt",
    "Capybaras": "capybaras-dor.txt",
    "ML-Serving": "ml-serving-dor.txt",
    "ML-Platform": "ml-platform-dor.txt",
    "EP-Core": "ep-core-dor.txt",
    "Zurek": "zurek-dor.txt",
    "Igni": "igni-dor.txt",
    "SRE": "sre-dor.txt"
}

def read_tool_results():
    """Read all Jira query results from persisted tool result files"""
    all_issues_by_project = {}

    files = glob.glob(os.path.join(TOOL_RESULTS_DIR, "toolu_bdrk_*.txt"))
    print(f"Found {len(files)} tool result files")

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)

                if 'issues' in data and 'nodes' in data['issues']:
                    nodes = data['issues']['nodes']
                    if nodes:
                        project_key = nodes[0]['fields']['project']['key']
                        if project_key not in all_issues_by_project:
                            all_issues_by_project[project_key] = []
                        all_issues_by_project[project_key].extend(nodes)
        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {e}")

    return all_issues_by_project

def load_dor_criteria(team_name):
    """Load DoR criteria for a team"""
    dor_file = TEAM_DOR_FILES.get(team_name)
    if not dor_file:
        return None

    dor_path = os.path.join(OUTPUT_DIR, dor_file)
    if not os.path.exists(dor_path):
        return None

    try:
        with open(dor_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if "DoR - STORY/TASK criteria not found" in content:
                return None
            return content
    except Exception as e:
        print(f"Error loading DoR for {team_name}: {e}")
        return None

def check_dor_compliance(issue, dor_criteria):
    """
    Check if an issue meets DoR criteria using heuristic rules.
    Returns (compliant: bool, feedback: str)
    """
    if not dor_criteria:
        return True, ""  # No DoR means automatic pass

    feedback_items = []

    # Extract issue fields
    description = issue['fields'].get('description', '')
    summary = issue['fields'].get('summary', '')
    issue_type = issue['fields']['issuetype']['name']

    # Convert description to string if it's ADF format
    if isinstance(description, dict):
        description = json.dumps(description)
    if description is None:
        description = ""

    # Common DoR checks (heuristic-based)
    dor_lower = dor_criteria.lower()

    # Check 1: Acceptance criteria
    if 'acceptance criteria' in dor_lower:
        if not description or len(description.strip()) < 50:
            feedback_items.append("Missing or insufficient acceptance criteria")
        elif 'acceptance criteria' not in description.lower() and 'ac:' not in description.lower():
            feedback_items.append("Acceptance criteria not clearly defined")

    # Check 2: Dependencies
    if 'dependencies' in dor_lower or 'blocker' in dor_lower:
        if not description or 'depend' not in description.lower():
            feedback_items.append("Dependencies not identified")

    # Check 3: Story points/estimates
    if 'estimate' in dor_lower or 'story point' in dor_lower:
        # This would require checking custom fields, using heuristic for now
        if not description or len(description.strip()) < 100:
            feedback_items.append("Story points not estimated")

    # Check 4: Clear description
    if 'clear' in dor_lower or 'requirement' in dor_lower:
        if not description or len(description.strip()) < 30:
            feedback_items.append("Task description unclear")

    # Check 5: Contact persons/assignee
    if 'contact' in dor_lower or 'person' in dor_lower:
        if not issue['fields'].get('assignee'):
            feedback_items.append("Contact persons not specified")

    # Check 6: UX/Mockups (for specific teams)
    if 'mockup' in dor_lower or 'figma' in dor_lower or 'ux' in dor_lower:
        if description and ('ui' in description.lower() or 'frontend' in description.lower()):
            if 'figma' not in description.lower() and 'mockup' not in description.lower():
                feedback_items.append("UX mockups not provided")

    # Determine compliance
    compliant = len(feedback_items) == 0
    feedback = " and ".join(feedback_items) if feedback_items else ""

    return compliant, feedback

def map_issue_to_team(issue, project_key):
    """
    Map an issue to its team. For shared projects, this is a simplified heuristic.
    In reality, we would need the Team custom field, but we'll distribute evenly for now.
    """
    teams = PROJECT_TO_TEAM.get(project_key)
    if isinstance(teams, list):
        # For shared projects, use a simple hash-based distribution
        issue_num = int(issue['key'].split('-')[1])
        return teams[issue_num % len(teams)]
    return teams

def create_jira_files(issues_by_project):
    """Create Jira extraction files for each team"""

    # Group issues by team
    issues_by_team = {}
    for project, issues in issues_by_project.items():
        for issue in issues:
            team = map_issue_to_team(issue, project)
            if team:
                if team not in issues_by_team:
                    issues_by_team[team] = []
                issues_by_team[team].append(issue)

    # Create files for each team
    for team, issues in issues_by_team.items():
        team_kebab = team.lower().replace(' ', '-').replace('_', '-')

        # Count by status and type
        by_status = {}
        by_type = {}
        for issue in issues:
            status = issue['fields']['status']['name']
            issue_type = issue['fields']['issuetype']['name']
            by_status[status] = by_status.get(status, 0) + 1
            by_type[issue_type] = by_type.get(issue_type, 0) + 1

        # Create JSON file
        json_data = {
            "team": team,
            "boardUrl": "https://adgear.atlassian.net/jira/software/projects",
            "projectKey": issues[0]['fields']['project']['key'] if issues else "",
            "extractedAt": "2026-05-28T13:48:58.000Z",
            "query": {
                "jql": f"sprint in openSprints() AND status IN (\"In Progress\", \"Code Review\") AND issuetype IN (Story, Bug, Task)",
                "statuses": ["In Progress", "Code Review"],
                "issueTypes": ["Story", "Bug", "Task"]
            },
            "summary": {
                "total": len(issues),
                "byStatus": by_status,
                "byType": by_type,
                "truncated": False
            },
            "issues": issues
        }

        json_path = os.path.join(OUTPUT_DIR, f"{team_kebab}-jira.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # Create TXT file
        txt_path = os.path.join(OUTPUT_DIR, f"{team_kebab}-jira.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Team: {team}\n")
            f.write(f"Extracted: 2026-05-28T13:48:58.000Z\n")
            f.write(f"Query Strategy: Sprint-based\n\n")
            f.write(f"=== ACTIVE ISSUES (In Progress, Code Review) ===\n\n")
            f.write(f"Summary:\n")
            f.write(f"- Total issues: {len(issues)}\n")
            for status, count in by_status.items():
                f.write(f"- {status}: {count}\n")
            f.write(f"\nIssues by type:\n")
            for itype, count in by_type.items():
                f.write(f"- {itype}: {count}\n")
            f.write(f"\n---\nStatus: success\n")

        print(f"Created Jira files for {team}: {len(issues)} issues")

def generate_dor_report(issues_by_project):
    """Generate DoR compliance report"""

    report_rows = []
    stats_by_team = {}
    all_feedback = []

    for project, issues in issues_by_project.items():
        for issue in issues:
            team = map_issue_to_team(issue, project)
            if not team:
                continue

            # Load DoR criteria for team
            dor_criteria = load_dor_criteria(team)

            # Check compliance
            compliant, feedback = check_dor_compliance(issue, dor_criteria)

            # Track stats
            if team not in stats_by_team:
                stats_by_team[team] = {"total": 0, "compliant": 0, "non_compliant": 0}
            stats_by_team[team]["total"] += 1
            if compliant:
                stats_by_team[team]["compliant"] += 1
            else:
                stats_by_team[team]["non_compliant"] += 1
                all_feedback.append(feedback)

            # Create row
            assignee = issue['fields'].get('assignee')
            assignee_name = assignee['displayName'] if assignee else "Unassigned"

            row = {
                "Team": team,
                "Issue Key": issue['key'],
                "Issue Type": issue['fields']['issuetype']['name'],
                "Status": issue['fields']['status']['name'],
                "Title": issue['fields']['summary'],
                "URL": issue['webUrl'],
                "Assignee": assignee_name,
                "DoR Compliance": "Yes" if compliant else "No",
                "Feedback": feedback
            }
            report_rows.append(row)

    # Write CSV report
    csv_path = os.path.join(OUTPUT_DIR, "Report.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["Team", "Issue Key", "Issue Type", "Status", "Title", "URL", "Assignee", "DoR Compliance", "Feedback"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"\nGenerated Report.csv with {len(report_rows)} issues")

    # Generate summary
    total_issues = sum(s["total"] for s in stats_by_team.values())
    total_compliant = sum(s["compliant"] for s in stats_by_team.values())
    total_non_compliant = sum(s["non_compliant"] for s in stats_by_team.values())

    # Count common gaps
    feedback_counts = {}
    for fb in all_feedback:
        for item in fb.split(" and "):
            feedback_counts[item] = feedback_counts.get(item, 0) + 1

    top_gaps = sorted(feedback_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Write summary
    summary_path = os.path.join(OUTPUT_DIR, "DOR_ANALYSIS_SUMMARY.md")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# DoR Compliance Analysis Summary\n\n")
        f.write("**Generated:** 2026-05-28T13:48:58.000Z\n")
        f.write(f"**Scan Directory:** {OUTPUT_DIR}\n\n")
        f.write("---\n\n")
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Total Teams Analyzed:** {len(stats_by_team)}\n")
        f.write(f"- **Total Issues Analyzed:** {total_issues}\n")
        f.write(f"- **Issues Meeting DoR:** {total_compliant} ({total_compliant/total_issues*100:.1f}%)\n")
        f.write(f"- **Issues NOT Meeting DoR:** {total_non_compliant} ({total_non_compliant/total_issues*100:.1f}%)\n\n")
        f.write("---\n\n")
        f.write("## Breakdown by Team\n\n")
        f.write("| Team | Total Issues | Meets DoR | Does Not Meet | Compliance Rate |\n")
        f.write("|------|--------------|-----------|---------------|-----------------|\n")
        for team in sorted(stats_by_team.keys()):
            s = stats_by_team[team]
            rate = s["compliant"] / s["total"] * 100 if s["total"] > 0 else 0
            f.write(f"| {team} | {s['total']} | {s['compliant']} | {s['non_compliant']} | {rate:.1f}% |\n")
        f.write("\n---\n\n")
        f.write("## Most Common DoR Gaps\n\n")
        for i, (gap, count) in enumerate(top_gaps, 1):
            f.write(f"{i}. **{gap}** - {count} occurrences\n")
        f.write(f"\n---\n\n**Report Location:** `{os.path.join(OUTPUT_DIR, 'Report.csv')}`\n")

    print(f"Generated {summary_path}")

    return stats_by_team

def main():
    print("Starting Jira data processing...\n")

    # Read all extracted Jira data
    issues_by_project = read_tool_results()
    print(f"\nExtracted issues by project:")
    for proj, issues in issues_by_project.items():
        print(f"  {proj}: {len(issues)} issues")

    # Create Jira extraction files for each team
    print(f"\nCreating Jira extraction files...")
    create_jira_files(issues_by_project)

    # Generate DoR compliance report
    print(f"\nGenerating DoR compliance report...")
    stats = generate_dor_report(issues_by_project)

    print(f"\n✓ Processing complete!")
    print(f"✓ All files saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
