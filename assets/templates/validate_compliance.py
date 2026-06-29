#!/usr/bin/env python3
"""
Validate that DoR compliance analysis was performed correctly.
Checks the mechanical enforcement constraints:
1. issue_descriptions.json exists (descriptions were fetched)
2. compliance_data.json is consistent with descriptions
3. Empty descriptions result in Fail verdicts
4. Non-zero failure rate on sufficient sample size

Usage: python3 validate_compliance.py <output_dir>
Exit code 0 = passed, 1 = failed
"""
import json
import os
import sys


def validate(output_dir):
    errors = []
    warnings = []

    # Check 1: issue_descriptions.json must exist
    desc_file = os.path.join(output_dir, "issue_descriptions.json")
    if not os.path.exists(desc_file):
        errors.append(
            "CRITICAL: issue_descriptions.json does not exist - "
            "descriptions were NOT fetched (Step 11.2 skipped)"
        )
        # Cannot continue validation without this file
        return errors, warnings

    with open(desc_file, "r", encoding="utf-8") as f:
        desc_data = json.load(f)

    # Check 2: compliance_data.json must exist
    comp_file = os.path.join(output_dir, "compliance_data.json")
    if not os.path.exists(comp_file):
        errors.append(
            "CRITICAL: compliance_data.json does not exist - "
            "analysis was not completed"
        )
        return errors, warnings

    with open(comp_file, "r", encoding="utf-8") as f:
        comp_data = json.load(f)

    # Check 3: Issue count consistency
    fetched_count = desc_data.get("issues_fetched", 0)
    compliance_count = len(comp_data)
    if fetched_count != compliance_count:
        warnings.append(
            f"Issue count mismatch: {fetched_count} descriptions fetched "
            f"vs {compliance_count} compliance entries"
        )

    # Check 4: Empty descriptions must be Fail
    desc_entries = desc_data.get("data", {})
    comp_lookup = {c["issue_key"]: c for c in comp_data}

    empty_but_pass = []
    for issue_key, desc_info in desc_entries.items():
        if not desc_info.get("has_content", True):
            if issue_key in comp_lookup and comp_lookup[issue_key]["dor_compliance"] == "Pass":
                empty_but_pass.append(issue_key)

    if empty_but_pass:
        errors.append(
            f"Issues with NO description marked as Pass "
            f"(violates calibration rule 1): {empty_but_pass}"
        )

    # Check 5: Non-zero failure rate
    if compliance_count > 0:
        fail_count = sum(1 for c in comp_data if c["dor_compliance"] == "Fail")

        if compliance_count >= 50 and fail_count == 0:
            errors.append(
                f"CRITICAL: 0% failure rate on {compliance_count} issues - "
                f"analysis is almost certainly invalid"
            )
        elif compliance_count >= 20 and fail_count == 0:
            warnings.append(
                f"0% failure rate on {compliance_count} issues - "
                f"unusual, verify descriptions were actually read"
            )

    # Check 6: Fail entries must have non-empty notes
    for c in comp_data:
        if c["dor_compliance"] == "Fail" and not c.get("note", "").strip():
            errors.append(
                f"Issue {c['issue_key']} is Fail but has empty note "
                f"(must explain why)"
            )

    # Check 7: No heuristic analysis scripts
    heuristic_patterns = [
        "analyze_dor", "analyze_compliance", "heuristic", "keyword_match"
    ]
    for f in os.listdir(output_dir):
        if f.endswith(".py") and any(p in f for p in heuristic_patterns):
            warnings.append(
                f"Suspicious script found: {f} - "
                f"may indicate heuristic analysis was used"
            )

    return errors, warnings


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    print(f"Validating compliance analysis in: {output_dir}")
    print("=" * 60)

    errors, warnings = validate(output_dir)

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  [FAIL] {e}")
        print("\nCOMPLIANCE VALIDATION FAILED")
        sys.exit(1)
    else:
        print("\nCOMPLIANCE VALIDATION PASSED")
        sys.exit(0)
