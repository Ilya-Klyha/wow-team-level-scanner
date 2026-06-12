#!/usr/bin/env python3
"""Helper script to track team extraction progress"""

teams = [
    {
        "name": "PE-WAW-Abyss",
        "pageId": "22648881240",
        "pageLink": "https://adgear.atlassian.net/wiki/x/WID6RQU",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980",
        "boardId": "9980",
        "projectKey": "MAW"
    },
    {
        "name": "Radium",
        "pageId": "20720615642",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20720615642",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
        "boardId": "8976",
        "projectKey": "AENW"
    },
    {
        "name": "Europium",
        "pageId": "22431629392",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22431629392",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
        "boardId": "8979",
        "projectKey": "AENW"
    },
    {
        "name": "Copernicium",
        "pageId": "20734247032",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20734247032",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246",
        "boardId": "9246",
        "projectKey": "AETVP"
    },
    {
        "name": "Mouflons",
        "pageId": "22381756417",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22381756417",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503",
        "boardId": "4503",
        "projectKey": "PEPI"
    },
    {
        "name": "Wolves",
        "pageId": "22374940673",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22374940673",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504",
        "boardId": "4504",
        "projectKey": "PEPI"
    },
    {
        "name": "Polonium-LF",
        "pageId": "22606054953",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606054953",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEDSP/boards/8973",
        "boardId": "8973",
        "projectKey": "PEDSP"
    },
    {
        "name": "Polonium-Upper-Funnel",
        "pageId": "22606053416",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606053416",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403",
        "boardId": "10403",
        "projectKey": "RSW"
    },
    {
        "name": "Bigos",
        "pageId": "22695936064",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22695936064",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10157",
        "boardId": "10157",
        "projectKey": "RSW"
    },
    {
        "name": "Capybaras",
        "pageId": "22696132609",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22696132609",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156",
        "boardId": "10156",
        "projectKey": "RSW"
    },
    {
        "name": "ML-Serving",
        "pageId": "21732425749",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732425749",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090",
        "boardId": "4090",
        "projectKey": "PEPI"
    },
    {
        "name": "ML-Platform",
        "pageId": "21732360213",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732360213",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470",
        "boardId": "10470",
        "projectKey": "ML"
    },
    {
        "name": "EP-Core",
        "pageId": "22817472513",
        "pageLink": "https://adgear.atlassian.net/wiki/x/AQAHUAU",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972",
        "boardId": "10972",
        "projectKey": "EPCW"
    },
    {
        "name": "Zurek",
        "pageId": "21748023571",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21748023571",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881",
        "boardId": "2881",
        "projectKey": "PEA"
    },
    {
        "name": "Igni",
        "pageId": "22435922026",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22435922026",
        "sprintBoardLink": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477",
        "boardId": "9477",
        "projectKey": "ASPW"
    },
    {
        "name": "SRPOL-SRE",
        "pageId": "22719529363",
        "pageLink": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22719529363",
        "sprintBoardLink": "TBD",
        "boardId": None,
        "projectKey": None
    }
]

print(f"Total teams to process: {len(teams)}")
for team in teams:
    print(f"- {team['name']}: board {team['boardId']} ({team['projectKey']})")
