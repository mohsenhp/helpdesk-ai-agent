# Fictional Enterprise Dataset for Hybrid AI Agent

This dataset is designed for a LangChain/LangGraph AI agent that searches both:

1. Normal relational data
2. Vector-searchable documents

## SQL data

Located in `sql/`:

- users.csv
- assets.csv
- software_versions.csv
- tickets.csv
- incidents.csv
- changes.csv

## Vector documents

Located in `documents/`:

- kb_articles/
- incident_reports/
- runbooks/
- support_emails/
- release_notes/

Use these files for embedding and vector search.

## Good demo questions

SQL-only:

- How many open Critical VPN tickets are there?
- Which department has the most laptop tickets?
- List unresolved SEV1 incidents.

Vector-only:

- How do I troubleshoot VPN after a Windows update?
- What should I check when Azure SSO fails?
- Find runbooks about database timeouts.

Hybrid:

- Which users have open VPN tickets and what KB article should support follow?
- Are there Critical Azure Login tickets that match known conditional access issues?
- Which recent changes may be related to unresolved SEV1 incidents?
- Find departments affected by printer issues and summarize the recommended troubleshooting steps.

## Suggested stack

- SQLite for local development
- PostgreSQL for production
- Chroma or pgvector for vector search
- LangChain document loaders
- LangGraph for routing
- Gemini API for answer generation