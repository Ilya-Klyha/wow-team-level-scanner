#!/usr/bin/env python3
"""
Validate team assignment correctness in WoW Scanner results.
"""

import json
import os
from pathlib import Path

OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 12-26"

def validate_team_separation():
    """Check for duplicate issue assignments across teams."""
    issue_team_map = {}
    duplicates = []

    # Scan all team JSON files
    for json_file in Path(OUTPUT_DIR).glob("*-jira.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            team_name = data["metadata"]["team_name"]

            for issue in data["issues"]:
                issue_key = issue["key"]

                if issue_key in issue_team_map:
                    duplicates.append({
                        "key": issue_key,
                        "teams": [issue_team_map[issue_key], team_name]
                    })
                else:
                    issue_team_map[issue_key] = team_name

    # Report results
    if duplicates:
        print(f"[FAIL] Found {len(duplicates)} duplicate issue assignments")
        for dup in duplicates[:10]:  # Show first 10
            print(f"  {dup['key']} assigned to: {', '.join(dup['teams'])}")
        return False
    else:
        print(f"[PASS] All {len(issue_team_map)} issues uniquely assigned")
        return True

def validate_team_field_presence():
    """Check that all issues have Team field data."""
    results = {}

    for json_file in Path(OUTPUT_DIR).glob("*-jira.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            team_name = data["metadata"]["team_name"]

            total = len(data["issues"])
            with_team_field = sum(1 for i in data["issues"] if "teamField" in i or "teamName" in i)

            results[team_name] = {
                "total": total,
                "with_team_field": with_team_field,
                "percentage": (with_team_field / total * 100) if total > 0 else 0
            }

    # Report results
    print("\nTeam Field Presence:")
    all_pass = True
    for team, stats in sorted(results.items()):
        if stats["percentage"] == 100:
            print(f"  [PASS] {team}: {stats['with_team_field']}/{stats['total']} ({stats['percentage']:.0f}%)")
        else:
            print(f"  [WARN] {team}: {stats['with_team_field']}/{stats['total']} ({stats['percentage']:.0f}%)")
            all_pass = False

    return all_pass

def validate_shared_project_separation():
    """Verify teams in shared projects have different issue sets."""
    shared_projects = {
        "AENW": ["Radium", "Europium"],
        "PEPI": ["Mouflons", "Wolves"],
        "RSW": ["Polonium UF", "Bigos", "Capybaras"]
    }

    print("\nShared Project Separation:")
    all_pass = True

    for project, teams in shared_projects.items():
        team_issues = {}

        for team in teams:
            json_file = Path(OUTPUT_DIR) / f"{team.lower().replace(' ', '-')}-jira.json"
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    team_issues[team] = {i["key"] for i in data["issues"]}

        # Check for overlaps
        if len(team_issues) >= 2:
            team_list = list(team_issues.keys())
            for i in range(len(team_list)):
                for j in range(i + 1, len(team_list)):
                    team_a = team_list[i]
                    team_b = team_list[j]

                    overlap = team_issues[team_a] & team_issues[team_b]

                    if overlap:
                        print(f"  [FAIL] {team_a} and {team_b}: {len(overlap)} overlapping issues")
                        all_pass = False
                    else:
                        print(f"  [PASS] {team_a} and {team_b}: No overlap")

    return all_pass

if __name__ == "__main__":
    print("="*80)
    print("WOW SCANNER VALIDATION")
    print("="*80)

    test1 = validate_team_separation()
    test2 = validate_team_field_presence()
    test3 = validate_shared_project_separation()

    print("\n" + "="*80)
    if test1 and test2 and test3:
        print("[SUCCESS] ALL VALIDATION TESTS PASSED")
    else:
        print("[FAILURE] SOME VALIDATION TESTS FAILED")
    print("="*80)
