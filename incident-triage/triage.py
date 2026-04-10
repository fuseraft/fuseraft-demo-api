import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime
from collections import Counter

BASE_URL = 'http://localhost:8000'
TOKEN = os.environ.get('FAKEPROD_API_KEY')
if not TOKEN:
    print("Error: FAKEPROD_API_KEY environment variable not set", file=sys.stderr)
    sys.exit(1)

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Authorization': f'Bearer {TOKEN}'}
    if data:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data.encode('utf-8') if data else None, method=method)
    for key, value in headers.items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            if status not in [200, 204]:
                body = response.read().decode('utf-8')
                print(f"API request failed with status {status}: {body}", file=sys.stderr)
                sys.exit(1)
            if status == 204:
                return None
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode('utf-8')
        except:
            error_body = ''
        print(f"HTTP error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

def get_user_name(assignee_id):
    if not assignee_id:
        return "Unassigned"
    try:
        user_data = make_request('GET', f'/users/{assignee_id}')
        return user_data['name']
    except:
        return "Unknown"

# Fetch all incidents
incidents_data = make_request('GET', '/incidents')
incidents = incidents_data['incidents']
total = incidents_data.get('total', len(incidents))

# Categorize incidents
open_incidents = [inc for inc in incidents if inc['status'] in ['open', 'in_progress']]
resolved_incidents = [inc for inc in incidents if inc['status'] in ['resolved', 'closed']]

# Priority counts for open
open_priorities = Counter(inc['priority'] for inc in open_incidents)

# Escalated: P1 and P2 open
escalated_incidents = [inc for inc in open_incidents if inc['priority'] in ['P1', 'P2']]

# Add notes to escalated incidents
for inc in escalated_incidents:
    note_data = json.dumps({"note": "Flagged for escalation by automated triage."})
    make_request('PATCH', f'/incidents/{inc["id"]}', note_data)

# Generate timestamp
generated = datetime.now().isoformat()

# Build report
report = f"""# Incident Triage Report
Generated: {generated}

## Summary
- Total incidents: {total}
- Open: {len(open_incidents)}  (P1: {open_priorities.get('P1', 0)}, P2: {open_priorities.get('P2', 0)}, P3: {open_priorities.get('P3', 0)}, P4: {open_priorities.get('P4', 0)})
- Resolved/closed: {len(resolved_incidents)}

"""

# Escalated table
if escalated_incidents:
    report += "## P1 / P2 Open Incidents (Escalated)\n"
    report += "| ID | Title | Priority | Status | Assignee |\n"
    report += "|----|-------|----------|--------|----------|\n"
    for inc in escalated_incidents:
        assignee = get_user_name(inc.get('assignee_id'))
        report += f"| {inc['id']} | {inc['title']} | {inc['priority']} | {inc['status']} | {assignee} |\n"
else:
    report += "## P1 / P2 Open Incidents (Escalated)\nNo escalated incidents.\n"

# All open
report += "\n## All Open Incidents\n"
if open_incidents:
    report += "| ID | Title | Priority | Status |\n"
    report += "|----|-------|----------|--------|\n"
    for inc in open_incidents:
        report += f"| {inc['id']} | {inc['title']} | {inc['priority']} | {inc['status']} |\n"
else:
    report += "No open incidents.\n"

# Resolved
report += "\n## Resolved / Closed Incidents\n"
if resolved_incidents:
    report += "| ID | Title | Priority |\n"
    report += "|----|-------|----------|\n"
    for inc in resolved_incidents:
        report += f"| {inc['id']} | {inc['title']} | {inc['priority']} |\n"
else:
    report += "No resolved incidents.\n"

# Write report
with open('triage-report.md', 'w') as f:
    f.write(report)

# Print summary
print(f"Triage complete. {len(open_incidents)} open ({len(escalated_incidents)} escalated), {len(resolved_incidents)} resolved. Report: triage-report.md")

# Exit successfully
sys.exit(0)