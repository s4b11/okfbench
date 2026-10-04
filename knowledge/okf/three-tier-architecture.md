---
type: Concept
title: Three-Tier Architecture
description: Browser dashboards, Python application logic, and a relational database
  layer.
tags:
- architecture
---

1. **Presentation** — parent, clinician, and staff dashboards in HTML/CSS/JS with a responsive layout kit.
2. **Application** — Python web framework for auth, visits, immunizations, charts, nutrition drafting, risk flags, and notices.
3. **Data** — relational database (PostgreSQL in production-shaped demos, SQLite locally) for infants, visits, plans, and alerts.

## Related concepts

- [Tech Stack](tech-stack.md)
- [Database Design](database-design.md)
- [Parent Dashboard](parent-dashboard.md)
- [Doctor Dashboard](doctor-dashboard.md)
- [Admin Dashboard](admin-dashboard.md)
