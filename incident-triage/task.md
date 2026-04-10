# Incident Triage Report

The FakeProd API (http://localhost:8000) is a live mock production system pre-seeded with
users, incidents, and orders. Your job is to produce an incident triage report by querying
the API and writing the results to disk.

## Context

- API base URL: `http://localhost:8000`
- Auth: Bearer token (pre-configured in the "fakeprod" API profile — no manual auth needed)
- Swagger UI: http://localhost:8000/docs

## What to build

Write a Python script `triage.py` that:

1. Calls `GET /incidents` to fetch all incidents.
2. Separates them into two buckets:
   - **Open** (`status` is `open` or `in_progress`)
   - **Resolved** (`status` is `resolved` or `closed`)
3. Among the open incidents, identifies the **P1 and P2 incidents** (the highest priority ones).
4. For each P1/P2 open incident, calls `PATCH /incidents/{id}` to add a note:
   `"Flagged for escalation by automated triage."`
5. Writes a Markdown report to `triage-report.md` with this structure:

```
# Incident Triage Report
Generated: <ISO timestamp>

## Summary
- Total incidents: N
- Open: N  (P1: N, P2: N, P3: N, P4: N)
- Resolved/closed: N

## P1 / P2 Open Incidents (Escalated)
| ID | Title | Priority | Status | Assignee |
|----|-------|----------|--------|----------|
| INC-XXXX | ... | P1 | open | <user name or "Unassigned"> |
...

## All Open Incidents
| ID | Title | Priority | Status |
|----|-------|----------|--------|
...

## Resolved / Closed Incidents
| ID | Title | Priority |
|----|-------|----------|
...
```

6. Prints a one-line summary to stdout:
   `Triage complete. N open (N escalated), N resolved. Report: triage-report.md`

## Requirements

- Use only the Python standard library plus `urllib` (no `requests` or `httpx`).
- The script must be runnable as: `python triage.py`
- If the API returns a non-2xx response, print an error to stderr and exit 1.
- For the assignee name in the escalated table, look up `GET /users/{assignee_id}` to get
  the user's name. If `assignee_id` is null, show "Unassigned".

## Acceptance criteria

1. `python triage.py` exits with code 0
2. `triage-report.md` is created and contains a `# Incident Triage Report` heading
3. `triage-report.md` contains a `## Summary` section with total, open, and resolved counts
4. `triage-report.md` contains a `## P1 / P2 Open Incidents (Escalated)` section
5. Each P1 or P2 open incident in the report has its note updated via PATCH (verified by calling
   GET /incidents/{id} and confirming the notes array is non-empty)
6. `triage-report.md` contains an `## All Open Incidents` section
7. `triage-report.md` contains a `## Resolved / Closed Incidents` section
8. The stdout summary line matches the format: `Triage complete. N open (N escalated), N resolved. Report: triage-report.md`
