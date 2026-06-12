import re
import json

html_content = '''[HTML CONTENT WILL BE PASSED]'''

# Extract table rows from tbody
tbody_match = re.search(r'<tbody>(.*?)</tbody>', html_content, re.DOTALL)
if not tbody_match:
    print("Error: Could not find tbody")
    exit(1)

tbody = tbody_match.group(1)

# Find all table rows
rows = re.findall(r'<tr>(.*?)</tr>', tbody, re.DOTALL)

teams = []

for row in rows:
    # Extract all td cells
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    
    if len(cells) < 5:
        continue  # Skip template row or incomplete rows
    
    # First cell - team page link
    first_cell = cells[0]
    team_link_match = re.search(r'<a href="([^"]+)"', first_cell)
    
    if not team_link_match:
        continue
    
    team_link = team_link_match.group(1)
    
    # Extract page ID from URL
    # Patterns: /pages/[PAGE_ID]/ or /wiki/x/[TINY_ID]
    page_id = None
    if '/wiki/x/' in team_link:
        page_id = team_link.split('/wiki/x/')[1].split('/')[0].split('?')[0].split('#')[0]
    elif '/pages/' in team_link:
        page_id = re.search(r'/pages/(\d+)', team_link)
        if page_id:
            page_id = page_id.group(1)
    
    if not page_id:
        continue
    
    # Fifth cell - sprint board link
    sprint_board_link = None
    if len(cells) >= 5:
        fifth_cell = cells[4]
        board_link_match = re.search(r'<a href="([^"]+)"', fifth_cell)
        if board_link_match:
            sprint_board_link = board_link_match.group(1)
    
    teams.append({
        "pageLink": team_link,
        "sprintBoardLink": sprint_board_link,
        "pageId": page_id
    })

print(json.dumps(teams, indent=2))
