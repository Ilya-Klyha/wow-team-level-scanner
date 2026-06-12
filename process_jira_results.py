#!/usr/bin/env python3
"""
Process Jira query results from temp files and create team-specific JSON and TXT files.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Output directory
OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 10-20"

# Team to project mapping (from teams.json)
TEAM_PROJECT_MAPPING = {
    "PE-WAW-Abyss": "MAW",
    "Radium": "AENW",
    "Europium": "AENW",
    "Copernicium": "AETVP",
    "Mouflons": "PEPI",
    "Wolves": "PEPI",
    "Polonium LF": "PEDSP",
    "Polonium UF": "RSW",
    "Bigos": "RSW",
    "Capybaras": "RSW",
    "ML Serving": "PEPI",
    "ML Platform": "ML",
    "EP Core": "EPCW",
    "Zurek": "PEA",
    "Igni": "ASPW",
    "SRE": "EEEW"
}

# Project to board ID mapping (extracted from teams.json sprint_board_link)
PROJECT_BOARD_MAPPING = {
    "MAW": "9980",
    "AENW": ["8976", "8979"],  # Multiple boards for shared project
    "AETVP": "9246",
    "PEPI": ["4503", "4504", "4090"],  # Multiple boards
    "PEDSP": "8973",
    "RSW": ["10403", "10157", "10156"],  # Multiple boards
    "ML": "10470",
    "EPCW": "10972",
    "PEA": "2881",
    "ASPW": "9477",
    "EEEW": "10332"
}

def team_name_to_filename(team_name):
    """Convert team name to kebab-case filename."""
    return team_name.lower().replace(" ", "-").replace("_", "-")

def parse_jira_result_file(filepath):
    """Parse a Jira result temp file and extract issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "issues" in data and "nodes" in data["issues"]:
            return data["issues"]["nodes"]
        return []
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return []

def map_issues_to_teams(all_issues):
    """Map issues to teams based on Team field (customfield_10114)."""
    team_issues = {team: [] for team in TEAM_PROJECT_MAPPING.keys()}
    unassigned_issues = []

    for issue in all_issues:
        try:
            team_assigned = False

            # PRIORITY 1: Extract from Team field (customfield_10114)
            team_field_id = "customfield_10114"
            if "fields" in issue and team_field_id in issue["fields"]:
                team_field = issue["fields"][team_field_id]

                if team_field and isinstance(team_field, dict):
                    team_full = team_field.get("name", "")

                    if " - " in team_full:
                        # Extract clean team name (last segment)
                        team_name = team_full.split(" - ")[-1].strip()

                        # Match to configured teams
                        if team_name in team_issues:
                            team_issues[team_name].append(issue)
                            team_assigned = True
                        else:
                            # Try fuzzy matching for variations
                            for configured_team in team_issues.keys():
                                if team_name in configured_team or configured_team in team_name:
                                    team_issues[configured_team].append(issue)
                                    team_assigned = True
                                    break

            # FALLBACK: Project-based assignment (only for single-team projects)
            if not team_assigned:
                project_key = issue["fields"]["project"]["key"]

                for team_name, project in TEAM_PROJECT_MAPPING.items():
                    if project == project_key:
                        team_issues[team_name].append(issue)
                        print(f"Warning: {issue['key']} assigned by project fallback (no Team field)")
                        team_assigned = True
                        break

            if not team_assigned:
                unassigned_issues.append(issue)
                print(f"Error: {issue.get('key', 'unknown')} could not be assigned to any team")

        except KeyError as e:
            print(f"Warning: Issue {issue.get('key', 'unknown')} missing field: {e}")
            unassigned_issues.append(issue)

    # Report unassigned issues
    if unassigned_issues:
        print(f"\n[WARNING] {len(unassigned_issues)} issues could not be assigned to teams")

    return team_issues

def format_issue_txt(issue):
    """Format issue for TXT output."""
    try:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        issuetype = issue["fields"]["issuetype"]["name"]

        assignee_name = "Unassigned"
        if issue["fields"].get("assignee"):
            assignee_name = issue["fields"]["assignee"]["displayName"]

        web_url = issue.get("webUrl", f"https://adgear.atlassian.net/browse/{key}")

        created = issue["fields"]["created"]
        updated = issue["fields"]["updated"]

        priority = issue["fields"].get("priority", {}).get("name", "Unknown")

        description = issue["fields"].get("description", "")
        if description and isinstance(description, dict):
            description = "[Structured content - see JSON for details]"
        elif description is None:
            description = "[No description]"

        txt = f"""
{'='*80}
Issue: {key}
Type: {issuetype}
Status: {status}
Priority: {priority}
Summary: {summary}
Assignee: {assignee_name}
URL: {web_url}
Created: {created}
Updated: {updated}
{'='*80}

Description:
{description}

"""
        return txt
    except Exception as e:
        print(f"Error formatting issue {issue.get('key', 'unknown')}: {e}")
        return ""

def save_team_jira_files(team_issues):
    """Save team-specific Jira files (JSON and TXT)."""
    for team_name, issues in team_issues.items():
        if not issues:
            print(f"Team {team_name}: 0 issues (skipping file creation)")
            continue

        filename_base = team_name_to_filename(team_name)
        json_filepath = os.path.join(OUTPUT_DIR, f"{filename_base}-jira.json")
        txt_filepath = os.path.join(OUTPUT_DIR, f"{filename_base}-jira.txt")

        # Save JSON file
        json_data = {
            "metadata": {
                "team_name": team_name,
                "issue_count": len(issues),
                "extraction_date": datetime.now().isoformat(),
                "project_key": TEAM_PROJECT_MAPPING[team_name]
            },
            "issues": issues
        }

        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # Save TXT file
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Team: {team_name}\n")
            f.write(f"Project: {TEAM_PROJECT_MAPPING[team_name]}\n")
            f.write(f"Total Issues: {len(issues)}\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n{'='*80}\n\n")

            for issue in issues:
                f.write(format_issue_txt(issue))

        print(f"Team {team_name}: {len(issues)} issues -> {filename_base}-jira.json, {filename_base}-jira.txt")

def main():
    # Find all temp result files
    temp_dir = r"C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\e73da338-927d-4b32-bdd4-f654f453eca8\tool-results"
    temp_files = list(Path(temp_dir).glob("toolu_bdrk_*.txt"))

    print(f"Found {len(temp_files)} temp files to process")

    # Parse all Jira result files
    all_issues = []
    for temp_file in temp_files:
        issues = parse_jira_result_file(temp_file)
        all_issues.extend(issues)
        print(f"Parsed {temp_file.name}: {len(issues)} issues")

    print(f"\nTotal issues collected: {len(all_issues)}")

    # Map issues to teams
    team_issues = map_issues_to_teams(all_issues)

    # Save team-specific files
    print("\nSaving team-specific Jira files...")
    save_team_jira_files(team_issues)

    # Print summary
    print("\n" + "="*80)
    print("JIRA EXTRACTION SUMMARY")
    print("="*80)
    for team_name in sorted(TEAM_PROJECT_MAPPING.keys()):
        count = len(team_issues[team_name])
        print(f"{team_name:20s}: {count:3d} issues")
    print("="*80)
    print(f"Total: {sum(len(issues) for issues in team_issues.values())} issues")

if __name__ == "__main__":
    main()
