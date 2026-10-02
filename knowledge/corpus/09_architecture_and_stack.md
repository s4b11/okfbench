# Architecture and Stack Notes

The demo uses a classic three-tier shape. Browser dashboards present parent, clinician, and staff views with responsive HTML and JavaScript. A Python web application layer enforces auth, runs workflows, drafts nutrition plans, scores risk flags, and sends notices. A relational database stores infants, visits, plans, and alerts.

Local clone-and-run prefers SQLite. Hosted demos can point at PostgreSQL. Email-style notices use an SMTP-compatible path so free tiers stay simple.
