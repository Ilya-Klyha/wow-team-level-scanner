# SRPOL Teams DoR Extraction Report

**Extraction Date:** 2026-05-26  
**Extraction Time:** 11:00  
**Cloud ID:** adgear.atlassian.net  
**Criteria:** Definition of Ready (DoR) - STORY/TASK only

---

## Summary

- **Total Teams Processed:** 16
- **Teams with DoR:** 12
- **Teams without DoR:** 4
- **Output Directory:** `assets/teams/20260526 11-00/`

---

## Teams Processed

### Teams with Complete DoR - STORY/TASK

1. **Abyss** (formerly "1 Beacon")
   - Page ID: WID6RQU
   - File: Abyss-dor.txt
   - Status: Already fetched by user

2. **TV Native Ad Experiences** (Radium)
   - Page ID: 20720615642
   - File: TV-Native-Ad-Experiences-dor.txt
   - Format: Table with 4 criteria

3. **Family Hub Creative Preview DSP** (Europium)
   - Page ID: 22431629392
   - File: Family-Hub-Creative-Preview-DSP-dor.txt
   - Format: List with Ready/Not Ready conditions

4. **TV Plus Ad Experiences** (Copernicium)
   - Page ID: 20734247032
   - File: TV-Plus-Ad-Experiences-dor.txt
   - Format: Table with 5 criteria

5. **CTV-2-Mobile** (Mouflons)
   - Page ID: 22381756417
   - File: CTV-2-Mobile-dor.txt
   - Format: Principle-based table (3 principles)

6. **CTV-2-CTV and CTV-2-Web** (Wolves)
   - Page ID: 22374940673
   - File: CTV-2-CTV-and-CTV-2-Web-dor.txt
   - Format: Principle-based table (3 principles)

7. **Polonium Upper Funnel** (Polonium UF)
   - Page ID: 22606053416
   - File: Polonium-UF-dor.txt
   - Format: Table with 3 criteria

8. **Audience Reporting** (Bigos)
   - Page ID: 21748023571
   - File: Audience-Reporting-dor.txt
   - Note: References external page for detailed DoR

9. **Zurek** (Component Team)
   - Page ID: 21748023571
   - File: Zurek-dor.txt
   - Format: List with detailed acceptance criteria

10. **MLE OTS OR** (Capybaras)
    - Page ID: 22696132609
    - File: MLE-OTS-OR-dor.txt
    - Format: Table with 4 criteria

11. **Engineering Platform** (EP Core)
    - Page ID: 22817472513
    - File: Engineering-Platform-dor.txt
    - Format: List with 6 criteria

12. **DSP Ad Serving** (Igni)
    - Page ID: 22435922026
    - File: DSP-Ad-Serving-dor.txt
    - Format: Table with 6 criteria

---

### Teams without DoR - STORY/TASK

1. **Polonium LF**
   - Page ID: 22606054953
   - File: Polonium-LF-dor.txt
   - Issue: Page marked WIP (Work In Progress), no detailed DoR section

2. **MLOps Serving** (Sturgeons)
   - Page ID: 21732425749
   - File: MLOps-Serving-dor.txt
   - Issue: Brief page focused on responsibilities, no DoR section

3. **MLOps Platform** (Pandas)
   - Page ID: 21732360213
   - File: MLOps-Platform-dor.txt
   - Issue: Brief page focused on infrastructure, no DoR section

4. **SRE** (SRPOL SRE)
   - Page ID: 22719529363
   - File: SRE-dor.txt
   - Issue: References external page, no DoR content on main page

---

## Key Findings

### DoR Patterns Observed

1. **Table Format** (Most common)
   - Criterion/Principle | Description | Comments
   - Used by: Radium, Copernicium, Polonium UF, Capybaras, Igni

2. **List Format**
   - Bullet points with clear conditions
   - Used by: Europium, EP Core, Zurek

3. **Principle-Based**
   - Organized by principles (Clear Description, Acceptance Criteria, Collaboration)
   - Used by: Mouflons, Wolves

### Common DoR Elements Across Teams

1. **User Story/Requirement Clarity** (Present in 11/12 teams)
2. **Acceptance Criteria** (Present in 11/12 teams)
3. **Estimates/Story Points** (Present in 9/12 teams)
4. **Dependencies** (Present in 10/12 teams)
5. **Monitoring/Alerting** (Present in 3/12 teams)

### Unique DoR Elements

- **Contact Persons** (Igni only)
- **Collaborative Progress** (Mouflons, Wolves)
- **Work Size Limits** (Polonium UF, Capybaras)
- **Rollback Procedures** (Zurek)

---

## Files Created

Total: 17 files (16 DoR text files + 1 JSON metadata + 1 report)

```
Abyss-dor.txt (425 bytes)
TV-Native-Ad-Experiences-dor.txt (1.1K)
Family-Hub-Creative-Preview-DSP-dor.txt (931 bytes)
TV-Plus-Ad-Experiences-dor.txt (960 bytes)
CTV-2-Mobile-dor.txt (2.1K)
CTV-2-CTV-and-CTV-2-Web-dor.txt (2.1K)
Polonium-LF-dor.txt (558 bytes)
Polonium-UF-dor.txt (844 bytes)
Audience-Reporting-dor.txt (853 bytes)
Zurek-dor.txt (1.1K)
MLE-OTS-OR-dor.txt (1.9K)
MLOps-Serving-dor.txt (693 bytes)
MLOps-Platform-dor.txt (984 bytes)
Engineering-Platform-dor.txt (604 bytes)
DSP-Ad-Serving-dor.txt (1.3K)
SRE-dor.txt (773 bytes)
teams.json (4.8K)
```

---

## Recommendations

1. **Incomplete Teams:**
   - Polonium LF: Complete the WIP page and add DoR criteria
   - MLOps Serving & Platform: Consider adding DoR sections
   - SRE: Either include DoR on main page or add link to external DoR page

2. **Standardization Opportunities:**
   - Consider standardizing DoR format across teams
   - Common elements identified could form a baseline DoR template
   - Contact persons (from Igni) could be added to all external-facing work

3. **Best Practices to Share:**
   - Mouflons/Wolves principle-based approach is comprehensive
   - Zurek's inclusion of rollback procedures shows operational maturity
   - Capybaras' tagging system ([SRPOL-OR], [SRPOL-OTS]) aids tracking

---

## Extraction Method

- MCP Atlassian plugin via getConfluencePage
- HTML content format parsing
- Manual extraction of DoR - STORY/TASK sections
- Excluded: OFFERING/EPIC level DoR sections
- Preserved: Table structures and formatting where possible

---

**Report Generated:** 2026-05-26 13:07 UTC
