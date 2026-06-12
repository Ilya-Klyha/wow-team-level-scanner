#!/usr/bin/env python3
"""
Process SRPOL Teams data and extract DoR content
"""
import re
import json
from html.parser import HTMLParser

class DoRExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_dor_section = False
        self.dor_content = []
        self.current_tag = None
        self.heading_level = 0
        self.skip_offering_epic = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in ['h2', 'h3', 'h4']:
            self.heading_level = int(tag[1])

    def handle_data(self, data):
        data_upper = data.strip().upper()

        # Check for DoR - STORY/TASK heading
        if self.current_tag in ['h2', 'h3', 'h4']:
            if ('DEFINITION OF READY' in data_upper or 'DOR' in data_upper):
                if 'OFFERING' in data_upper or 'EPIC' in data_upper:
                    if 'STORY' not in data_upper and 'TASK' not in data_upper:
                        self.skip_offering_epic = True
                        self.in_dor_section = False
                    else:
                        # This is STORY/TASK section
                        self.skip_offering_epic = False
                        self.in_dor_section = True
                        self.dor_content = []
                elif 'STORY' in data_upper or 'TASK' in data_upper:
                    # Explicit STORY/TASK
                    self.skip_offering_epic = False
                    self.in_dor_section = True
                    self.dor_content = []
                elif not self.skip_offering_epic:
                    # Plain DoR without specifier
                    self.in_dor_section = True
                    self.dor_content = []
            elif self.in_dor_section and self.current_tag in ['h2', 'h3']:
                # Stop at next major heading
                self.in_dor_section = False

        # Collect content if in DoR section
        if self.in_dor_section and data.strip():
            self.dor_content.append(data.strip())

    def get_dor_text(self):
        if not self.dor_content:
            return "DoR - STORY/TASK criteria not found on team page."
        return '\n'.join(self.dor_content)

def extract_dor_from_html(html_content):
    """Extract DoR - STORY/TASK content from HTML"""
    parser = DoRExtractor()
    parser.feed(html_content)
    return parser.get_dor_text()

def clean_team_name(title):
    """Clean team name by removing common suffixes"""
    # Remove common patterns
    patterns_to_remove = [
        r'\s*team\s*space\s*$',
        r'\s*team\s*page\s*$',
        r'\s*-\s*team\s*page\s*$',
        r'^\s*team\s+',
        r'\s+team\s*$',
        r'\s*\[wip\]\s*$',
        r'\s*space\s*$'
    ]

    cleaned = title
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    # Normalize spaces and hyphens
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = re.sub(r'\s*-\s*', '-', cleaned)

    return cleaned

def team_name_to_kebab(name):
    """Convert team name to kebab-case for filename"""
    # Replace spaces and underscores with hyphens
    kebab = re.sub(r'[\s_]+', '-', name)
    # Remove special characters except hyphens
    kebab = re.sub(r'[^a-zA-Z0-9-]', '', kebab)
    # Convert to lowercase
    return kebab.lower()

# Team data structure
teams_data = []

# Example team entry format:
# {
#     "name": "PE-WAW-Abyss",
#     "page_link": "https://adgear.atlassian.net/wiki/x/WID6RQU",
#     "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980",
#     "dor_file": "pe-waw-abyss-dor.txt",
#     "page_id": "WID6RQU",
#     "extraction_status": "success",
#     "extraction_error": None,
#     "dor_source": "direct"
# }

print("Team data processing script ready")
print(f"Functions available: extract_dor_from_html, clean_team_name, team_name_to_kebab")
