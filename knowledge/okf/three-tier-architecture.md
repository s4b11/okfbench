---
id: three-tier-architecture
title: "Three-Tier Architecture"
summary: "Browser dashboards, Python application logic, and a relational database layer."
links:
  - tech-stack
  - database-design
  - parent-dashboard
  - doctor-dashboard
  - admin-dashboard
tags:
  - architecture
---

1. **Presentation** — parent, clinician, and staff dashboards in HTML/CSS/JS with a responsive layout kit.
2. **Application** — Python web framework for auth, visits, immunizations, charts, nutrition drafting, risk flags, and notices.
3. **Data** — relational database (PostgreSQL in production-shaped demos, SQLite locally) for infants, visits, plans, and alerts.
