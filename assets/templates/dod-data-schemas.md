# DoD Scanner - Report Data Schemas

These schemas define the exact JSON format expected by `generate_dod_reports.py`.
The LLM produces these JSON files; Python renders the reports.

## summary_data.json

Array of exactly 15 entries (one per SRPOL team, in fixed order):

```json
[
  {
    "team": "string - team display name",
    "dod": "Yes | No"
  }
]
```

Rules:
- Always 15 entries in order: Abyss, Radium, Europium, Copernicium, Mouflons, Wolves, Polonium UF, Bigos, Capybaras, ML Serving Sturgeons, ML Platform Pandas, EP Core, Zurek, Igni, SRE
- `dod`: "Yes" if team has DoD extracted successfully; "No" otherwise
- No other fields allowed

## quality_data.json

Array of entries for teams with DoD defined (excludes teams where dod == "No"):

```json
[
  {
    "team": "string - team display name",
    "overall": "number 0-100 (weighted score, 1 decimal allowed)",
    "coverage": "integer 0-100 (Coverage dimension score)",
    "clarity": "integer 0-100 (Clarity & Specificity dimension score)",
    "measurability": "integer 0-100 (Measurability dimension score)",
    "company_alignment": "integer 0-100 (Company Standard Alignment score)",
    "industry_alignment": "integer 0-100 (Industry Best Practices score)",
    "actionability": "integer 0-100 (Actionability score)",
    "evidence": "integer 0-100 (Evidence Requirements score)",
    "note": "string - short specific comment on main gaps/weaknesses, max 80 chars"
  }
]
```

Rules:
- Only includes teams where `dod == "Yes"` in summary_data.json
- `overall` = weighted average: coverage*0.25 + clarity*0.20 + measurability*0.15 + company_alignment*0.15 + industry_alignment*0.10 + actionability*0.10 + evidence*0.05
- `note`: focuses on what is MISSING or WEAK (not positive feedback). If DoD is excellent (score >= 90): "Comprehensive, minor gaps only"
- Teams without DoD are excluded from this file entirely
- Sorted by `overall` descending before writing

## Dimension Weights

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| Coverage | 25% | How many of 10 essential DoD areas are addressed |
| Clarity & Specificity | 20% | Are criteria specific and unambiguous |
| Measurability | 15% | Can each criterion be objectively verified |
| Company Standard Alignment | 15% | Alignment with company DoD page (21735212005) |
| Industry Best Practices | 10% | Adherence to Scrum Guide, SAFe practices |
| Actionability | 10% | Does DoD drive specific behaviors |
| Evidence Requirements | 5% | Does DoD specify what evidence is needed |

## 10 Essential DoD Areas (for Coverage dimension)

1. Code Review Completed
2. Unit/Integration Tests Written and Passing
3. Acceptance Criteria Met and Verified
4. CI/CD Pipeline Passing
5. Deployed to Staging/Production
6. Documentation Updated
7. No Known Defects / Technical Debt Documented
8. Performance/Security Validated (if applicable)
9. Monitoring/Alerting Configured
10. PO/Stakeholder Acceptance
