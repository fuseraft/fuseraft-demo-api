# fuseraft-demo-api

A local test bed for [fuseraft-cli](https://github.com/fuseraft/fuseraft-cli).

```
fuseraft-demo-api/
├── fakeapi/           Mock "production" REST API (FastAPI + Swagger UI)
└── incident-triage/   fuseraft project: agents triage incidents via the mock API
```

---

## fakeapi

A local REST API that mimics a production system. Pre-seeded with 12 users, 15 incidents, and 20 orders. All data is generated at startup (`random.seed(42)`) so the seed data is always consistent across restarts.

**Start the server:**

```bash
cd fakeapi
./start.sh          # default port 8000
./start.sh 9000     # custom port
```

The script auto-creates a virtualenv and installs dependencies on first run.

**Auth:** `Authorization: Bearer dev-secret-token-abc123`  
Override the token by setting `FAKEPROD_API_KEY` before starting the server.

```bash
FAKEPROD_API_KEY=my-custom-token ./start.sh
```

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check (no auth required) |
| GET | `/users` | List users (`?active=`, `?department=`) |
| GET | `/users/{id}` | Get one user |
| POST | `/users` | Create a user |
| GET | `/incidents` | List incidents (`?status=`, `?priority=`, `?category=`) |
| GET | `/incidents/{id}` | Get one incident |
| POST | `/incidents` | Create an incident |
| PATCH | `/incidents/{id}` | Update status, priority, or append a note |
| GET | `/orders` | List orders (`?status=`, `?customer_id=`) |
| GET | `/orders/{id}` | Get one order |
| PATCH | `/orders/{id}` | Update order status |

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

---

## incident-triage

A fuseraft project that tasks a four-agent team (Planner, Developer, Tester, Reviewer) with fetching incidents from the FakeProd API, escalating P1/P2 open incidents, and producing a Markdown triage report.

The agents are sandboxed to `~/fuseraft-demo-api/incident-triage` — they cannot read files outside that directory (including `fakeapi/`).

**Run:**

```bash
# In your terminal, start the mock API first
cd ~/fuseraft-demo-api/fakeapi
FAKEPROD_API_KEY=dev-secret-token-abc123 ./start.sh

# In a second terminal, run the fuseraft session
cd ~/fuseraft-demo-api/incident-triage
fuseraft run --config fuseraft.yaml --task-file task.md --tools
```

**Config highlights (`fuseraft.yaml`):**

```yaml
Security:
  FileSystemSandboxPath: ~/fuseraft-demo-api/incident-triage
  AllowPrivateHosts: true     # required for localhost API access
  HttpAllowedHosts:
    - localhost
    - "127.0.0.1"

ApiProfiles:
  fakeprod:
    BaseUrl: "http://localhost:8000"
    TimeoutSeconds: 15
    DefaultHeaders:
      Authorization: "Bearer ${FAKEPROD_API_KEY}"
```

Set `FAKEPROD_API_KEY` in your environment before running fuseraft, it is expanded at startup and injected into every API call made by the agents:

```bash
export FAKEPROD_API_KEY=dev-secret-token-abc123
```

## cleanup.kiwi

Use the [Kiwi](https://github.com/fuseraft/kiwi) cleanup script to remove all agent-generated content to replay the orchestration from scratch.

**Run the cleanup script:**
```bash
kiwi cleanup
```