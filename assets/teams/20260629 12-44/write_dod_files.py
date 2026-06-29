import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

teams_data = {
    "metadata": {
        "scan_date": "2026-06-29T10:44:00Z",
        "scan_timestamp_cet": "20260629 12-44",
        "source_page": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19470090380/SRPOL+Teams",
        "team_count": 15,
        "cloudId": "adgear.atlassian.net",
        "scanner_version": "2.0"
    },
    "teams": [
        {
            "name": "Abyss",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22648881240/PE+-+WAW+-+Abyss",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/9980",
            "dod_file": "abyss-dod.txt",
            "page_id": "22648881240",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Radium",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20720615642/Radium+Team+Space",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8976",
            "dod_file": "radium-dod.txt",
            "page_id": "20720615642",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Europium",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22431629392/Team+Europium",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AENW/boards/8979",
            "dod_file": "europium-dod.txt",
            "page_id": "22431629392",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Copernicium",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/20734247032/Copernicium+Team+Space",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/AETVP/boards/9246",
            "dod_file": "copernicium-dod.txt",
            "page_id": "20734247032",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Mouflons",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22381756417/Team+Mouflons",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4503",
            "dod_file": "mouflons-dod.txt",
            "page_id": "22381756417",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Wolves",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22374940673/Team+Wolves",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4504",
            "dod_file": "wolves-dod.txt",
            "page_id": "22374940673",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Polonium UF",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22606053416/Polonium+Upper+Funnel+-+Team+page",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10403/backlog",
            "dod_file": "polonium-uf-dod.txt",
            "page_id": "22606053416",
            "extraction_status": "success",
            "dod_source": "linked_page"
        },
        {
            "name": "Bigos",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22695936064/Bigos+-+Team+page",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/MAW/boards/11439/backlog",
            "dod_file": "bigos-dod.txt",
            "page_id": "22695936064",
            "extraction_status": "success",
            "dod_source": "linked_page"
        },
        {
            "name": "Capybaras",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22696132609/Capybaras+-+Team+page",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/RSW/boards/10156",
            "dod_file": "capybaras-dod.txt",
            "page_id": "22696132609",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "ML Serving Sturgeons",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732425749/ML+Serving+Sturgeons",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEPI/boards/4090",
            "dod_file": "ml-serving-sturgeons-dod.txt",
            "page_id": "21732425749",
            "extraction_status": "not_found",
            "dod_source": None
        },
        {
            "name": "ML Platform Pandas",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21732360213/ML+Platform+Pandas",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/projects/ML/boards/10470",
            "dod_file": "ml-platform-pandas-dod.txt",
            "page_id": "21732360213",
            "extraction_status": "success",
            "dod_source": "linked_page"
        },
        {
            "name": "EP Core",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/19133628629/EP+Team+Page",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/EPCW/boards/10972",
            "dod_file": "ep-core-dod.txt",
            "page_id": "19133628629",
            "extraction_status": "not_found",
            "dod_source": None
        },
        {
            "name": "Zurek",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/21748023571/Ads+Reporting+Bigos+Zurek",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/PEA/boards/2881?quickFilter=5159",
            "dod_file": "zurek-dod.txt",
            "page_id": "21748023571",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "Igni",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/ENG/pages/22435922026/SRPOL+Team+-+Igni",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/ASPW/boards/9477",
            "dod_file": "igni-dod.txt",
            "page_id": "22435922026",
            "extraction_status": "success",
            "dod_source": "direct"
        },
        {
            "name": "SRE",
            "page_link": "https://adgear.atlassian.net/wiki/spaces/AGILE/pages/22719529363/Team+SRPOL+SRE",
            "sprint_board_link": "https://adgear.atlassian.net/jira/software/c/projects/EEEW/boards/10332",
            "dod_file": "sre-dod.txt",
            "page_id": "22719529363",
            "extraction_status": "not_found",
            "dod_source": None
        }
    ]
}

# Write teams.json
with open(os.path.join(OUTPUT_DIR, "teams.json"), "w", encoding="utf-8") as f:
    json.dump(teams_data, f, indent=2, ensure_ascii=False)

# DoD content for each team
dod_contents = {
    "abyss-dod.txt": """Definition of Done (DoD) - STORY / TASK

The "Definition of Done" ensures that a software development ticket is truly complete and meets the required quality standards before it can be considered shippable. The DoD is applied to every piece of work and helps maintain consistency and quality across the product.

Criterion: Unit and Integration Tests Written and Passed (if applicable)
Description: Comprehensive unit and integration tests have been written for the new or modified code, and all tests pass successfully.
Comments: %code coverage check. E2E test. If below than requirements, shouldn't we check with architect to get ok for exception?

Criterion: Automated Pipeline Passed
Description: The continuous integration (CI) pipeline has run successfully, and all automated tests (unit, integration, regression) have passed.

Criterion: Acceptance Criteria Met and Measurement Ready
Description: All defined acceptance criteria for the user story have been satisfied and verified. As well as necessary monitoring and alerting for the new feature or change have been configured. Any necessary documentation (e.g., API docs, user guides, technical design docs) has been updated.

Criterion: Deployed to Staging/Pre-production (if applicable), with feature flags ready for release/rollout
Description: The code has been successfully deployed to a staging or pre-production environment for further testing and validation. All relevant code has been deployed to Production and relevant feature flags communicated with the appropriate parties for the controlled release to users.

Working agreement:
- Every team member should remember to create a UX subtask when a task or story is ready for review. The subtask should include details on where and what needs to be checked.
- Everyone remembers the checklist themselves.""",

    "radium-dod.txt": """Team Task/Story DoD (Definition of Done)

Criterion: Unit and Integration Tests (if applicable)
Description: implemented, SonarQube and review passed

Criterion: Automated Pipeline
Description: CI pass

Criterion: local test check (if applicable)
Description: regression and retest did not generate additional issues

Criterion: Acceptance Criteria
Description: Acceptance criteria are met.

Criterion: Deploy readiness
Description: Code is implemented, Code review is completed, Edge cases considered, Change is ready for deployment
Comments: Code is ready for deploy on production.

Criterion: Matches the UX design (when applicable)
Description: UX design is approved by reviewer and delivered on production
Comments: To be verified thus approval to few rtb trader instance could be up to 14 days.

Criterion: Ready for external review
Description: Reviewers are notified""",

    "europium-dod.txt": """Team DoD

A backlog item is Done when:

Engineering:
- Code is implemented.
- Code review is completed
- Tests are added/updated (if needed).
- CI passes.
- No critical warnings or TODO leftovers.

Quality:
- Acceptance criteria are met.
- Edge cases considered (known edge case)
- No known regression introduced.

UX (if applicable):
- Implementation matches approved Figma design.
- If the story/task/functionality is:
  - Related to frontend/UI
  - Ready on (at least) Pre-Prod environment.
  Then, in Jira comment section:
  - Tag related UX designer
  - Inform, when they can test the functionality, along with the link and necessary credentials
- When issue is discovered then UX designer will prepare new task

Operational:
- Feature is deployable and ready for verification
- Monitoring/logging added if required.
- Documentation updated if needed.
- If task is complex it should contain reproduction steps for AC approval

Not done if:
- Awaiting review.
- It is not validated in a production-like environment""",

    "copernicium-dod.txt": """Team DoD

Criterion: Unit and Integration Tests Written and Passed (if applicable)
Description: Comprehensive unit and integration tests have been written for the new or modified code, and all tests pass successfully.
Comments: to be taken into consideration in each repository team contributes

Criterion: Design QA check (if applicable)
Description: Information to UX when functionality is already on Pre-target environment. UX checks functionality as a whole.

Criterion: Acceptance Criteria Met and Measurement Ready
Description: All defined acceptance criteria for the user story have been satisfied and verified or separate task will be created to fulfill the commitment. As well as necessary monitoring and alerting for the new feature or change have been configured. Any necessary documentation (e.g., API docs, user guides, technical design docs) has been updated.
Comments: Regarding monitoring this will be done when the infrastructure and initial project status will apply the current need.

Criterion: Deployed to production (if applicable), with feature flags ready for release/rollout
Description: Current feature is deployed to prod and hidden under feature flag

Criterion: Dependencies
Description: Review must by accepted on repo owner/contributors before task is closed""",

    "mouflons-dod.txt": """Team DoD

Principle: Done according to the Team
Description:
- Acceptance criteria met or discussed and verified by Product Owner.
- Outputs documented in Jira comments.
- If Outcome is quantifiable, then it is measured and documented.

Comments:
- Documentation
  - Documentation should be understandable for future reference by the Team
  - Write your work so it can be taken over by another person or by you in 3 months.
  - Note things that may be useful for the team now or in the future.
  - Note things that interested you.
- Jira
  - At least 1 comment on Jira before closing a task/story/bug or before a break (e.g., vacation).
  - Information about what was achieved or what couldn't be done and why.
  - Ticket state is one of: DONE, BLOCKED, CANCELED, or POSTPONED

Principle: Done according to Developers
Description: Developers' responsibility is to Test, Review, and Check Quality.
- Common sense used.
- Code self-reviewed (using linter or AI with our Skill.md), described, and then sent for approval by Team members
- All new logic tested.
- SonarQube quality gate passes.

Comments:
- Specific quality checking methods will be developed by the team""",

    "wolves-dod.txt": """Team DoD

Principle: Done according to Team
Description:
- Acceptance criteria met or discussed and verified by Product Owner.
- Outputs documented in Jira comments.
- If Outcome is quantifiable, then it is measured and documented.

Comments:
- Documentation
  - Documentation should be understandable for future reference by the Team
  - Write your work so it can be taken over by another person or by you in 3 months.
  - Note things that may be useful for the team now or in the future.
  - Note things that interested you.
- Jira
  - At least 1 comment on Jira before closing a task/story/bug or before a break (e.g., vacation).
  - Information about what was achieved or what couldn't be done and why.
  - Ticket state is one of: DONE, BLOCKED, CANCELED, or POSTPONED

Principle: Done according to Developers
Description: Developers' responsibility is to Test, Review, and Check Quality.
- Common sense used.
- Code self-reviewed (using linter or AI with our Skill.md), described, and then sent for approval by Team members
- All new logic tested.
- SonarQube quality gate passes.

Comments:
- Specific quality checking methods will be developed by the team""",

    "polonium-uf-dod.txt": """Definition of Done (from linked page: Definition of Done / Definition of Ready)

- All acceptance criteria are met
- Relevant tests written according to ACs
- Review conducted by 2 devs (nice-to-have - depending on the workload)
- Merged to master/main and released
- PR description filled out properly
- Required documentation updated""",

    "bigos-dod.txt": """DoD: Definition of Done Task/Story (from linked page: DoR and DoD on Story/Task level)

The Definition of Done (DoD) is a clear set of criteria that must be met for a development ticket (e.g., a story or task) to be considered complete. It ensures that all aspects of the work, from coding to testing and deployment, are thoroughly addressed before the ticket is marked as "done." The DoD serves as a shared understanding among the team about what constitutes a finished piece of work, ensuring quality and consistency in deliverables.

- Acceptance criteria passed
- No known open serious defects
- Approved by:
  - PO or tech lead should get inline with Product regarding if changes can be delivered to prod
  - PO or tech lead (or other team member that is acting as tech lead when it is needed)
- Are released on production (ticket is approved by PO or Tech lead) or if other environment mentioned in AC (if the nature of the ticket is different)
- Be sure the changes are not have negative impact on production""",

    "capybaras-dod.txt": """Team DoD

The "Definition of Done" ensures that a software development ticket is truly complete and meets the required quality standards before it can be considered shippable. The DoD is applied to every piece of work and helps maintain consistency and quality across the product.

Criterion: Result summary
Description: The results of the task should have been summarized in Jira Task description after completion.

Criterion: Unit and Integration Tests Written and Passed (if applicable)
Description: TBD - Comprehensive unit and integration tests have been written for the new or modified code, and all tests pass successfully.
Comments: %code coverage check. E2E test. If below than requirements, shouldn't we check with architect to get ok for exception?

Criterion: Acceptance Criteria Met
Description: All defined acceptance criteria for the user story have been satisfied and verified.

Criterion: Deployed to Staging/Pre-production (if applicable), with feature flags ready for release/rollout
Description:
- If task contains deployment to production/dev
  - Positive merge of PR (Pipeline Passed, Automated tests passed, PER review passed)
  - Positive deploy
  - Positive test of dev environment (in case of prod deployment)
  - Positive verification of deploy by team my chosen tests approach""",

    "ml-serving-sturgeons-dod.txt": "DoD - STORY/TASK criteria not found on team page.",

    "ml-platform-pandas-dod.txt": """Team DoD (from linked page: [Pandas]DoR and DoD Team level)

Criterion: Github checks
Description: Always include testing and working github checks

Criterion: Unit and Integration Tests Written and Passed (if applicable)
Description: Comprehensive unit and integration tests have been written for the new or modified code, and all tests pass successfully.

Criterion: Acceptance Criteria Met
Description: All defined acceptance criteria for the user story/task have been satisfied and verified. Any necessary documentation (e.g., API docs, user guides, technical design docs) has been updated and links to artifacts will be provided.

Criterion: AI Agent context updated
Description: In case of new functionalities, documentation, code extension - AI Agent context will be updated.

Criterion: Dependencies
Description: Review must by accepted on repo owner/contributors before task is closed

Criterion: Ticket requires demo before sprint close.""",

    "ep-core-dod.txt": "DoD - STORY/TASK criteria not found on team page.",

    "zurek-dod.txt": """Zurek DoD - Definition of Done for story/task

- Software should be tested or described in task if tests are not needed
- Check if your code is updated with release branch
- Tested on feature branch
- Acceptance Criteria passed
- Change should be able to roll back
- Documentation should be updated
- Closed after merge to main / release branch (PER)""",

    "igni-dod.txt": """Definition of Done (DoD) - STORY / TASK

The "Definition of Done" ensures that a software development ticket is truly complete and meets the required quality standards before it can be considered shippable. The DoD is applied to every piece of work and helps maintain consistency and quality across the product.

Criterion: Unit and Integration Tests Written (if applicable) and Passed
Description: Comprehensive unit and integration tests have been written for the new or modified code, and all tests pass successfully.

Criterion: Automated Pipeline Passed
Description: The continuous integration (CI) pipeline has run successfully, and all automated tests (unit, integration, regression) have passed.

Criterion: Acceptance Criteria Met
Description: All defined acceptance criteria for the user story have been satisfied and verified.

Criterion: Documentation update
Description: tbd (still lacking documentation)

Criterion: For Data Activation: released to production
Description: The code has been successfully deployed to staging/preprod/prod.

Criterion: For Consumerd: Deployed to Staging/Pre-production (if applicable), not released to production (sidecar for gateway, bidder, delivery, catalyst). Weekly (Tuesday) task for joined deployment to prod (task will be created during planning)
Description: The code has been successfully deployed and relevant feature flags communicated with the appropriate parties according to service standards.

Criterion: Short description in the comment what was done.
Description: Before closing the ticket minimum info needs to be provided what was done. Tickets closed without any description are confusing and require managers to go, interrupt devs work and ask for explanations. Lets avoid that.""",

    "sre-dod.txt": "DoD - STORY/TASK criteria not found on team page."
}

# Write all DoD files
for filename, content in dod_contents.items():
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Written teams.json and {len(dod_contents)} DoD files.")
print(f"Teams with DoD: {sum(1 for t in teams_data['teams'] if t['extraction_status'] == 'success')}")
print(f"Teams without DoD: {sum(1 for t in teams_data['teams'] if t['extraction_status'] != 'success')}")
