import json, re

filepath = r'C:\Users\i.klyha\.claude\projects\C--Users-i-klyha-Desktop-Claude-wow-scanner-tool\3c910122-fd15-42f2-901c-1da80a2b7c0a\tool-results\mcp-plugin_atlassian_atlassian-getConfluencePage-1784196271075.txt'
f = open(filepath, 'r', encoding='utf-8')
data = json.loads(f.read())
f.close()
html = data['content']['nodes'][0]['body']

tbody_match = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
tbody = tbody_match.group(1)
rows = re.findall(r'<tr>(.*?)</tr>', tbody, re.DOTALL)

# Find which rows/cells contain PEPI
for row_idx, row in enumerate(rows):
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    for cell_idx, cell in enumerate(cells):
        if 'PEPI' in cell:
            print(f"Row {row_idx}, Col {cell_idx}: contains PEPI")
            # Show just the links
            links = re.findall(r'href="([^"]*PEPI[^"]*)"', cell)
            for l in links:
                print(f"  link: {l}")
