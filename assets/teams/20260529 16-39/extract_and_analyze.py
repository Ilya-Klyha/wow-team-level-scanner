#!/usr/bin/env python3
"""
WoW Team Scanner - Extract DoR and Analyze Jira Issues
This script processes all team data and generates the comprehensive DoR compliance report.
"""
import json
import re
from datetime import datetime

# Team data structure with page content
teams_data = []

def clean_team_name(title):
    """Clean team name by removing common suffixes"""
    # Remove "Team", "Team Space", "Team Page", etc.
    patterns = [
        r'\s*Team\s+Space\s*$',
        r'\s*Team\s+Page\s*$',
        r'\s*Team\s*$',
        r'\s*Space\s*$',
        r'\s+\[WIP\]\s*$',
    ]
    cleaned = title
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    return cleaned.strip()

def extract_dor_from_html(html_content, team_name):
    """Extract DoR - STORY/TASK criteria from HTML"""
    # Look for DoR headings
    dor_patterns = [
        r'<h[1-6][^>]*>.*?DEFINITION OF READY.*?STORY.*?TASK.*?</h[1-6]>',
        r'<h[1-6][^>]*>.*?Definition of Ready.*?STORY.*?TASK.*?</h[1-6]>',
        r'<h[1-6][^>]*>.*?Team DoR.*?story/task.*?</h[1-6]>',
        r'<h[1-6][^>]*>.*?Team DoR.*?</h[1-6]>',
    ]

    # Find the DoR section
    dor_start = -1
    for pattern in dor_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if match:
            dor_start = match.start()
            break

    if dor_start == -1:
        return None

    # Find the end of the DoR section (next major heading or DoD)
    dod_match = re.search(r'<h[1-6][^>]*>.*?(DoD|Definition of Done|DEFINITION OF DONE).*?</h[1-6]>',
                          html_content[dor_start:], re.IGNORECASE)
    offering_match = re.search(r'<h[1-6][^>]*>.*?OFFERING.*?EPIC.*?</h[1-6]>',
                              html_content[dor_start:], re.IGNORECASE)

    dor_end = len(html_content)
    if dod_match:
        dor_end = dor_start + dod_match.start()
    if offering_match and (dor_start + offering_match.start()) < dor_end:
        dor_end = dor_start + offering_match.start()

    dor_html = html_content[dor_start:dor_end]

    # Convert HTML to plain text
    # Remove HTML tags but preserve structure
    dor_text = re.sub(r'<br\s*/?>', '\n', dor_html)
    dor_text = re.sub(r'</p>', '\n', dor_text)
    dor_text = re.sub(r'<li[^>]*>', '\n- ', dor_text)
    dor_text = re.sub(r'<[^>]+>', '', dor_text)

    # Clean up whitespace
    dor_text = re.sub(r'\n\s*\n', '\n', dor_text)
    dor_text = re.sub(r' +', ' ', dor_text)
    dor_text = dor_text.strip()

    return dor_text if len(dor_text) > 50 else None

# Output directory
OUTPUT_DIR = r"C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260529 16-39"

print(f"Processing teams and extracting DoR criteria...")
print(f"Output directory: {OUTPUT_DIR}")
print("=" * 80)
