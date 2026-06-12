================================================================================
                    STEP 11: DoR COMPLIANCE ANALYSIS
                              QUICK START
================================================================================

WHAT IS THIS?
-------------
This folder contains everything needed to analyze Definition of Ready (DoR)
compliance for 149 Jira issues across 7 SRPOL teams.

HOW TO RUN?
-----------
Double-click:   RUN_DOR_ANALYSIS.bat

OR from command line:
    cd "C:\Users\i.klyha\Desktop\Claude\wow-scanner-tool\assets\teams\20260528 16-36"
    python generate_dor_report.py

WHAT WILL IT DO?
----------------
1. Analyze 149 issues from 7 teams against their DoR criteria
2. Generate Report.xlsx with 9-column schema
3. Create DOR_ANALYSIS_SUMMARY.md with statistics
4. Update teams.json with analysis metadata

Runtime: ~5-10 seconds

OUTPUT FILES
------------
After running, you will find:

  Report.xlsx                    - Excel report (9 columns, green/red highlighting)
  DOR_ANALYSIS_SUMMARY.md        - Summary with statistics and insights
  teams.json                     - Updated with dor_analysis section

TEAMS ANALYZED
--------------
1. PE-WAW-Abyss     (15 issues)
2. Radium           (16 issues)
3. Europium         (17 issues)
4. Copernicium      (15 issues)
5. Capybaras        (8 issues)
6. EP Core          (25 issues)
7. Igni             (53 issues)

TOTAL: 7 teams, 149 issues

REQUIREMENTS
------------
- Python 3.7 or later
- openpyxl library (will auto-install if needed)

VALIDATION
----------
To verify the report has correct schema:
    python validate_schema.py

REPORT SCHEMA (9 COLUMNS)
--------------------------
A. Team
B. Issue Key
C. Issue Type
D. Status
E. Title
F. URL (hyperlinked)
G. Assignee
H. DoR Compliance ("Yes" or "No" only)
   - Green fill for "Yes"
   - Red fill for "No"
I. Feedback (empty if Yes, explanation if No)

DOCUMENTATION
-------------
For detailed instructions, see:
  - STEP_11_INSTRUCTIONS.md       (Usage guide)
  - STEP_11_COMPLETION_REPORT.md  (Implementation report)

TROUBLESHOOTING
---------------
Problem: "Python not found"
Solution: Install Python from python.org

Problem: "openpyxl not found"
Solution: Run: py -m pip install openpyxl

Problem: "CSV created instead of Excel"
Solution: Install openpyxl: py -m pip install openpyxl

QUESTIONS?
----------
Review STEP_11_INSTRUCTIONS.md for comprehensive documentation.

================================================================================
                              READY TO RUN!
                     Double-click: RUN_DOR_ANALYSIS.bat
================================================================================
