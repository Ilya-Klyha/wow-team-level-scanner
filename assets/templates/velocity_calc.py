"""
Velocity Calculation Template
==============================
Primary source: Greenhopper velocity API (exact match with Jira sprint report)
Fallback: Attribution-based calculation (most-recent-sprint logic)

Required environment:
- .env file with JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN (for Greenhopper API)
- pip install python-dotenv requests

Usage: python velocity_calc.py
"""
import json
import os
import glob
import re
from datetime import datetime, timedelta
from collections import defaultdict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    requests = None

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL_RESULTS_DIR = r"<SET_BY_SKILL>"  # Replaced per-session
SCAN_DATE = datetime.now()
CUTOFF_DATE = SCAN_DATE - timedelta(days=84)

TEAM_NAME_PATTERNS = {
    "Abyss": "PE - WAW - Abyss",
    "Radium": "AE - WAW - Radium",
    "Europium": "AP - WAW - Europium",
    "Copernicium": "AE - WAW - Copernicium",
    "Mouflons": "AS - WAW - Mouflons",
    "Wolves": "AS - WAW - Wolves",
    "Polonium UF": "AS - WAW - Polonium UF",
    "Bigos": "AS - WAW - Bigos",
    "Capybaras": "AS - WAW - Capybaras",
    "ML Serving Sturgeons": "T - WAW - ML Sturgeons",
    "ML Platform Pandas": "T - WAW - ML Pandas",
    "Zurek": "T - WAW - Zurek",
    "EP Core": "T - WAW - EP Core",
    "Igni": "AP - WAW - Igni",
    "SRE": "T - WAW - Embedded SREs SRPOL",
}

SPRINT_NAME_PATTERNS = {
    "Abyss": re.compile(r"abyss", re.IGNORECASE),
    "Radium": re.compile(r"radium", re.IGNORECASE),
    "Europium": re.compile(r"europium", re.IGNORECASE),
    "Copernicium": re.compile(r"copernicium", re.IGNORECASE),
    "Mouflons": re.compile(r"mouflons", re.IGNORECASE),
    "Wolves": re.compile(r"wolves", re.IGNORECASE),
    "Polonium UF": re.compile(r"polonium", re.IGNORECASE),
    "Bigos": re.compile(r"bigos", re.IGNORECASE),
    "Capybaras": re.compile(r"capybaras", re.IGNORECASE),
    "ML Serving Sturgeons": re.compile(r"ml.?serving", re.IGNORECASE),
    "ML Platform Pandas": re.compile(r"ml.?platform", re.IGNORECASE),
    "Zurek": re.compile(r"zurek", re.IGNORECASE),
    "EP Core": re.compile(r"ep.?core", re.IGNORECASE),
    "Igni": re.compile(r"igni", re.IGNORECASE),
    "SRE": re.compile(r"srpol.*sre", re.IGNORECASE),
}

PROJECT_TEAMS = {
    "AENW": ["Europium", "Radium"],
    "AETVP": ["Copernicium"],
    "ASPW": ["Igni"],
    "EEEW": ["SRE"],
    "EPCW": ["EP Core"],
    "MAW": ["Abyss", "Bigos"],
    "MLI": ["ML Platform Pandas", "ML Serving Sturgeons"],
    "PEA": ["Zurek"],
    "RSW": ["Capybaras", "Polonium UF"],
    "TVPP": ["Mouflons"],
    "TVPW": ["Wolves"],
}

DISPLAY_NAMES = {"Polonium UF": "Polonium"}


def get_expected_projects(team):
    return [k for k, teams in PROJECT_TEAMS.items() if team in teams]


def fetch_greenhopper_velocity(board_id):
    """Fetch velocity data from Greenhopper API. Returns dict of sprint_id -> completed_sp, or None on failure."""
    base_url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")

    if not all([base_url, email, token]):
        print("[WARNING] JIRA credentials not configured (.env). Using fallback attribution-based velocity.")
        return None

    if requests is None:
        print("[WARNING] 'requests' library not installed. Using fallback attribution-based velocity.")
        return None

    url = f"{base_url}/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId={board_id}"
    auth = (email, token)

    try:
        resp = requests.get(url, auth=auth, timeout=30)
        if resp.status_code != 200:
            print(f"[WARNING] Greenhopper API returned {resp.status_code} for board {board_id}. Using fallback.")
            return None
        data = resp.json()
        result = {}
        for sprint_id_str, entry in data.get("velocityStatEntries", {}).items():
            completed = entry.get("completed", {}).get("value", 0)
            result[int(sprint_id_str)] = completed
        return result
    except Exception as e:
        print(f"[WARNING] Greenhopper API failed for board {board_id}: {e}. Using fallback.")
        return None


def load_velocity_issues():
    all_issues = []
    seen_keys = set()

    files = sorted(glob.glob(os.path.join(TOOL_RESULTS_DIR, "mcp-plugin_atlassian_atlassian-searchJiraIssuesUsingJql-*.txt")))
    for f in files:
        ts = int(os.path.basename(f).split("-")[-1].replace(".txt", ""))
        if ts < 0:  # Set per-session timestamp cutoff
            continue
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        url = d["issues"].get("webUrl", "")
        if "closedSprints" not in url:
            continue
        for issue in d["issues"]["nodes"]:
            key = issue.get("key")
            if key and key not in seen_keys:
                seen_keys.add(key)
                all_issues.append(issue)

    for f in glob.glob(os.path.join(TOOL_RESULTS_DIR, "toolu_*.txt")):
        with open(f, encoding="utf-8") as fh:
            try:
                d = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
        if "issues" not in d:
            continue
        url = d["issues"].get("webUrl", "")
        if "closedSprints" in url:
            for issue in d["issues"]["nodes"]:
                key = issue.get("key")
                if key and key not in seen_keys:
                    seen_keys.add(key)
                    all_issues.append(issue)

    print(f"Loaded {len(all_issues)} unique velocity issues")
    return all_issues


def get_team_for_issue(issue):
    team_field = issue.get("fields", {}).get("customfield_10114")
    if team_field and isinstance(team_field, dict):
        team_name = team_field.get("name", "")
        for team, pattern in TEAM_NAME_PATTERNS.items():
            if team_name == pattern:
                return team
    return None


def get_sprint_attribution(issue, team):
    sprints = issue.get("fields", {}).get("customfield_10115", [])
    if not sprints:
        return None

    pattern = SPRINT_NAME_PATTERNS.get(team)
    if not pattern:
        return None

    matching_sprints = []
    for sprint in sprints:
        if not isinstance(sprint, dict):
            continue
        if sprint.get("state") != "closed":
            continue
        if not pattern.search(sprint.get("name", "")):
            continue
        complete_date_str = sprint.get("completeDate")
        if not complete_date_str:
            continue
        try:
            complete_date = datetime.fromisoformat(complete_date_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            continue
        if complete_date < CUTOFF_DATE:
            continue
        matching_sprints.append({
            "name": sprint.get("name"),
            "completeDate": complete_date,
            "id": sprint.get("id"),
            "boardId": sprint.get("boardId"),
        })

    if not matching_sprints:
        return None

    matching_sprints.sort(key=lambda s: s["completeDate"], reverse=True)
    return matching_sprints[0]


def calculate_velocity():
    print("Loading velocity issues...")
    all_issues = load_velocity_issues()

    team_sprint_data = {}
    for team in TEAM_NAME_PATTERNS:
        team_sprint_data[team] = {}

    team_board_ids = {}

    for issue in all_issues:
        fields = issue.get("fields", {})
        project_key = fields.get("project", {}).get("key", "") or issue.get("key", "").split("-")[0]

        team = get_team_for_issue(issue)
        if not team:
            continue

        # Project key validation (Bug 1 fix)
        expected_projects = get_expected_projects(team)
        if expected_projects and project_key not in expected_projects:
            continue

        sprint_info = get_sprint_attribution(issue, team)
        if not sprint_info:
            continue

        # Track boardId for Greenhopper API
        if sprint_info.get("boardId") and team not in team_board_ids:
            team_board_ids[team] = sprint_info["boardId"]

        sp = fields.get("customfield_10200")
        if sp is None:
            sp = 0
        else:
            try:
                sp = float(sp)
            except (ValueError, TypeError):
                sp = 0

        sprint_key = sprint_info["name"]
        if sprint_key not in team_sprint_data[team]:
            team_sprint_data[team][sprint_key] = {
                "name": sprint_info["name"],
                "completeDate": sprint_info["completeDate"].isoformat(),
                "sprint_id": sprint_info.get("id"),
                "board_id": sprint_info.get("boardId"),
                "total_sp": 0,
                "issue_count": 0,
            }
        team_sprint_data[team][sprint_key]["total_sp"] += sp
        team_sprint_data[team][sprint_key]["issue_count"] += 1

    # Greenhopper velocity API override (Bug 2 fix)
    print("\n=== Greenhopper Velocity API ===")
    for team, board_id in team_board_ids.items():
        velocity_data = fetch_greenhopper_velocity(board_id)
        if not velocity_data:
            continue
        for sprint_key, sprint_info in team_sprint_data[team].items():
            sprint_id = sprint_info.get("sprint_id")
            if sprint_id and sprint_id in velocity_data:
                old_sp = sprint_info["total_sp"]
                new_sp = velocity_data[sprint_id]
                if old_sp != new_sp:
                    sprint_info["total_sp"] = new_sp
                    print(f"  [INFO] {team} {sprint_info['name']}: {old_sp} -> {new_sp} SP (Greenhopper)")

    # Final calculation
    velocity_results = {}
    for team, sprints in team_sprint_data.items():
        sprint_list = sorted(sprints.values(), key=lambda s: s["completeDate"], reverse=True)
        last_3 = sprint_list[:3]

        if not last_3:
            velocity_results[team] = {"velocity_avg": None, "sprints_used": 0, "sprint_details": []}
            continue

        total_sp = sum(s["total_sp"] for s in last_3)
        velocity_avg = round(total_sp / len(last_3), 1)

        velocity_results[team] = {
            "velocity_avg": velocity_avg,
            "sprints_used": len(last_3),
            "sprint_details": [
                {
                    "name": s["name"],
                    "completeDate": s["completeDate"],
                    "sp_completed": s["total_sp"],
                    "issues_completed": s["issue_count"],
                }
                for s in last_3
            ],
        }

    return velocity_results


def main():
    velocity_results = calculate_velocity()

    velocity_data = {
        "scan_date": SCAN_DATE.strftime("%Y-%m-%d"),
        "cutoff_date": CUTOFF_DATE.strftime("%Y-%m-%d"),
        "lookback_weeks": 12,
        "sprints_used": 3,
        "method": "greenhopper_velocity_api_with_attribution_fallback",
        "teams": {},
    }

    for team, result in velocity_results.items():
        display_name = DISPLAY_NAMES.get(team, team)
        velocity_data["teams"][display_name] = {
            "velocity_avg": result["velocity_avg"],
            "sprints_used": result["sprints_used"],
            "sprint_details": result["sprint_details"],
        }

    velocity_file = os.path.join(OUTPUT_DIR, "velocity_data.json")
    with open(velocity_file, "w", encoding="utf-8") as f:
        json.dump(velocity_data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved velocity_data.json")

    # Update summary_data.json if it exists
    summary_file = os.path.join(OUTPUT_DIR, "summary_data.json")
    if os.path.exists(summary_file):
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        for entry in summary_data:
            team_display = entry["team"]
            team_key = None
            for t, dn in DISPLAY_NAMES.items():
                if dn == team_display:
                    team_key = t
                    break
            if team_key is None:
                for t in TEAM_NAME_PATTERNS:
                    if t == team_display:
                        team_key = t
                        break

            if team_key and team_key in velocity_results:
                result = velocity_results[team_key]
                entry["velocity_avg"] = result["velocity_avg"]
                entry["velocity_sprints"] = [
                    {"name": s["name"], "completed_sp": s["sp_completed"], "issues_completed": s["issues_completed"]}
                    for s in result["sprint_details"]
                ]

                if result["velocity_avg"] and result["velocity_avg"] > 0:
                    dor_ready_sp = entry.get("dor_ready_sp", 0)
                    if dor_ready_sp > 0:
                        runway = round(dor_ready_sp / result["velocity_avg"], 1)
                        entry["sprint_runway"] = runway
                        if runway >= 3.0:
                            entry["runway_status"] = "Healthy"
                        elif runway >= 1.0:
                            entry["runway_status"] = "Attention"
                        else:
                            entry["runway_status"] = "Critical"
                    else:
                        entry["sprint_runway"] = 0.0
                        entry["runway_status"] = "Critical"
                else:
                    entry["sprint_runway"] = None
                    entry["runway_status"] = "No Data"

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        print(f"Updated summary_data.json with velocity and runway data")

    print("\n=== VELOCITY SUMMARY ===")
    print(f"{'Team':<22} {'Velocity':>8} {'Sprints':>7}")
    print("-" * 40)
    for entry_team in sorted(velocity_results.keys()):
        display = DISPLAY_NAMES.get(entry_team, entry_team)
        vel = velocity_results[entry_team]["velocity_avg"]
        sprints = velocity_results[entry_team]["sprints_used"]
        vel_str = f"{vel:.1f}" if vel else "N/A"
        print(f"{display:<22} {vel_str:>8} {sprints:>7}")


if __name__ == "__main__":
    main()
