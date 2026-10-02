---
id: database-design
title: "Database Design"
summary: "Relational tables for infants, parents, clinicians, visits, immunization rows, nutrition plans, and risk assessments."
links:
  - centralized-health-records
  - vaccination-scheduling
  - nutrition-plan-module
  - malnutrition-risk-analysis
tags:
  - database
  - schema
---

Core entities include infants, parents, clinicians, visits, immunization schedule rows, nutrition plans, and growth risk assessments.

Foreign keys keep charts linked to the right family and clinician. The physical store is PostgreSQL when hosted, SQLite when running locally without a server database.
