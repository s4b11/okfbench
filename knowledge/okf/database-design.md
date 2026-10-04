---
type: Concept
title: Database Design
description: Relational tables for infants, parents, clinicians, visits, immunization
  rows, nutrition plans, and risk assessments.
tags:
- database
- schema
---

Core entities include infants, parents, clinicians, visits, immunization schedule rows, nutrition plans, and growth risk assessments.

Foreign keys keep charts linked to the right family and clinician. The physical store is PostgreSQL when hosted, SQLite when running locally without a server database.

## Related concepts

- [Centralized Health Records](centralized-health-records.md)
- [Vaccination Scheduling](vaccination-scheduling.md)
- [Nutrition Plan Module](nutrition-plan-module.md)
- [Malnutrition Risk Analysis](malnutrition-risk-analysis.md)
