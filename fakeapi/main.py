"""
FakeProd API is a mock "production" REST API for fuseraft-cli sandbox testing.

Endpoints:
  /health                     GET  — liveness check
  /users                      GET  — list users
  /users/{id}                 GET  — get one user
  /users                      POST — create user
  /incidents                  GET  — list incidents (filter: ?status=open|closed)
  /incidents/{id}             GET  — get one incident
  /incidents                  POST — create incident
  /incidents/{id}             PATCH — update incident (e.g. close it)
  /orders                     GET  — list orders
  /orders/{id}                GET  — get one order
  /orders/{id}                PATCH — update order status

Auth: Bearer token in Authorization header.
  Valid token: the value of the FAKEPROD_API_KEY env var (default: dev-secret-token-abc123)

Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
"""

import os
import random
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_KEY = os.getenv("FAKEPROD_API_KEY", "dev-secret-token-abc123")

app = FastAPI(
    title="FakeProd API",
    description=(
        "Mock production REST API for fuseraft-cli sandbox testing. "
        "Authenticate with `Authorization: Bearer dev-secret-token-abc123` "
        "(or set `FAKEPROD_API_KEY` to a custom value)."
    ),
    version="1.0.0",
)

bearer_scheme = HTTPBearer()


def require_auth(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if creds.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return creds.credentials


# ---------------------------------------------------------------------------
# Seed data (generated once at startup)
# ---------------------------------------------------------------------------

def _rand_date(days_ago_max=30) -> str:
    delta = timedelta(days=random.randint(0, days_ago_max), hours=random.randint(0, 23))
    return (datetime.now(timezone.utc) - delta).isoformat()

def _rand_id() -> str:
    return str(uuid.uuid4())[:8]

FIRST_NAMES = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank",
               "Iris", "Jack", "Karen", "Leo", "Mia", "Nick", "Olivia", "Paul"]
LAST_NAMES  = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller",
               "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson"]
DEPARTMENTS = ["Engineering", "Finance", "HR", "Legal", "Marketing", "Operations", "Sales", "Support"]

INCIDENT_TITLES = [
    "Login page returns 500 after deploy",
    "Database connection pool exhausted",
    "Scheduled job did not run at midnight",
    "API rate-limit exceeded on payment gateway",
    "SSL certificate expires in 3 days",
    "Memory leak in report-generation service",
    "Disk usage at 92% on prod-db-02",
    "Mobile app crashes on iOS 17.4 upgrade",
    "Email notifications delayed by 40 minutes",
    "Search index out of sync with database",
    "OAuth token refresh loop detected",
    "CDN purge failed after content update",
    "Kafka consumer lag spiking on orders topic",
    "PDF export produces blank pages for large datasets",
    "Two-factor auth codes rejected intermittently",
]

INCIDENT_CATEGORIES = ["Infrastructure", "Application", "Security", "Performance", "Data"]
INCIDENT_PRIORITIES = ["P1", "P2", "P3", "P4"]
INCIDENT_STATUSES   = ["open", "in_progress", "resolved", "closed"]

ORDER_STATUSES   = ["pending", "confirmed", "shipped", "delivered", "cancelled", "refunded"]
PRODUCT_NAMES    = ["Widget Pro", "Gadget Lite", "Doohickey Plus", "Thingamajig X",
                    "Gizmo Standard", "Contraption Elite", "Doodad Ultra", "Whatchamacallit"]

def _build_users(n=12):
    users = {}
    for _ in range(n):
        uid = _rand_id()
        first = random.choice(FIRST_NAMES)
        last  = random.choice(LAST_NAMES)
        users[uid] = {
            "id":         uid,
            "name":       f"{first} {last}",
            "email":      f"{first.lower()}.{last.lower()}@fakeprod.example",
            "department": random.choice(DEPARTMENTS),
            "role":       random.choice(["admin", "member", "viewer"]),
            "active":     random.choice([True, True, True, False]),
            "created_at": _rand_date(180),
        }
    return users

def _build_incidents(n=15, user_ids=None):
    incidents = {}
    for i in range(n):
        iid = f"INC-{1000 + i}"
        incidents[iid] = {
            "id":          iid,
            "title":       random.choice(INCIDENT_TITLES),
            "category":    random.choice(INCIDENT_CATEGORIES),
            "priority":    random.choice(INCIDENT_PRIORITIES),
            "status":      random.choice(INCIDENT_STATUSES),
            "assignee_id": random.choice(user_ids) if user_ids else None,
            "created_at":  _rand_date(30),
            "updated_at":  _rand_date(5),
            "notes":       [],
        }
    return incidents

def _build_orders(n=20, user_ids=None):
    orders = {}
    for i in range(n):
        oid = f"ORD-{5000 + i}"
        qty = random.randint(1, 10)
        price = round(random.uniform(9.99, 299.99), 2)
        orders[oid] = {
            "id":          oid,
            "customer_id": random.choice(user_ids) if user_ids else None,
            "product":     random.choice(PRODUCT_NAMES),
            "quantity":    qty,
            "unit_price":  price,
            "total":       round(qty * price, 2),
            "status":      random.choice(ORDER_STATUSES),
            "created_at":  _rand_date(60),
            "updated_at":  _rand_date(10),
        }
    return orders

random.seed(42)
USERS     = _build_users()
USER_IDS  = list(USERS.keys())
INCIDENTS = _build_incidents(user_ids=USER_IDS)
ORDERS    = _build_orders(user_ids=USER_IDS)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class CreateUserRequest(BaseModel):
    name:       str
    email:      str
    department: Optional[str] = "Engineering"
    role:       Optional[str] = "member"

class CreateIncidentRequest(BaseModel):
    title:    str
    category: Optional[str] = "Application"
    priority: Optional[str] = "P3"

class PatchIncidentRequest(BaseModel):
    status:   Optional[str] = None
    priority: Optional[str] = None
    note:     Optional[str] = None

class PatchOrderRequest(BaseModel):
    status: Optional[str] = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Meta"])
def health():
    """Liveness check — no auth required."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


# Users

@app.get("/users", tags=["Users"])
def list_users(
    active: Optional[bool] = Query(None, description="Filter by active status"),
    department: Optional[str] = Query(None, description="Filter by department name"),
    _: str = Depends(require_auth),
):
    """List all users. Optionally filter by active status or department."""
    result = list(USERS.values())
    if active is not None:
        result = [u for u in result if u["active"] == active]
    if department:
        result = [u for u in result if u["department"].lower() == department.lower()]
    return {"total": len(result), "users": result}


@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: str, _: str = Depends(require_auth)):
    """Get a single user by ID."""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found.")
    return USERS[user_id]


@app.post("/users", status_code=201, tags=["Users"])
def create_user(body: CreateUserRequest, _: str = Depends(require_auth)):
    """Create a new user."""
    uid = _rand_id()
    user = {
        "id":         uid,
        "name":       body.name,
        "email":      body.email,
        "department": body.department,
        "role":       body.role,
        "active":     True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    USERS[uid] = user
    return user


# Incidents

@app.get("/incidents", tags=["Incidents"])
def list_incidents(
    status: Optional[str] = Query(None, description="Filter by status: open, in_progress, resolved, closed"),
    priority: Optional[str] = Query(None, description="Filter by priority: P1, P2, P3, P4"),
    category: Optional[str] = Query(None, description="Filter by category"),
    _: str = Depends(require_auth),
):
    """List incidents. Optionally filter by status, priority, or category."""
    result = list(INCIDENTS.values())
    if status:
        result = [i for i in result if i["status"] == status]
    if priority:
        result = [i for i in result if i["priority"] == priority]
    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]
    return {"total": len(result), "incidents": result}


@app.get("/incidents/{incident_id}", tags=["Incidents"])
def get_incident(incident_id: str, _: str = Depends(require_auth)):
    """Get a single incident by ID."""
    if incident_id not in INCIDENTS:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return INCIDENTS[incident_id]


@app.post("/incidents", status_code=201, tags=["Incidents"])
def create_incident(body: CreateIncidentRequest, _: str = Depends(require_auth)):
    """Create a new incident."""
    n   = len(INCIDENTS) + 1
    iid = f"INC-{1000 + n}"
    incident = {
        "id":          iid,
        "title":       body.title,
        "category":    body.category,
        "priority":    body.priority,
        "status":      "open",
        "assignee_id": None,
        "created_at":  datetime.now(timezone.utc).isoformat(),
        "updated_at":  datetime.now(timezone.utc).isoformat(),
        "notes":       [],
    }
    INCIDENTS[iid] = incident
    return incident


@app.patch("/incidents/{incident_id}", tags=["Incidents"])
def patch_incident(incident_id: str, body: PatchIncidentRequest, _: str = Depends(require_auth)):
    """Update an incident's status, priority, or append a note."""
    if incident_id not in INCIDENTS:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

    inc = INCIDENTS[incident_id]
    if body.status is not None:
        valid = {"open", "in_progress", "resolved", "closed"}
        if body.status not in valid:
            raise HTTPException(status_code=422, detail=f"Invalid status '{body.status}'. Must be one of: {sorted(valid)}")
        inc["status"] = body.status
    if body.priority is not None:
        inc["priority"] = body.priority
    if body.note:
        inc["notes"].append({"text": body.note, "timestamp": datetime.now(timezone.utc).isoformat()})

    inc["updated_at"] = datetime.now(timezone.utc).isoformat()
    return inc


# Orders

@app.get("/orders", tags=["Orders"])
def list_orders(
    status: Optional[str] = Query(None, description="Filter by status"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    _: str = Depends(require_auth),
):
    """List orders. Optionally filter by status or customer."""
    result = list(ORDERS.values())
    if status:
        result = [o for o in result if o["status"] == status]
    if customer_id:
        result = [o for o in result if o["customer_id"] == customer_id]
    return {"total": len(result), "orders": result}


@app.get("/orders/{order_id}", tags=["Orders"])
def get_order(order_id: str, _: str = Depends(require_auth)):
    """Get a single order by ID."""
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return ORDERS[order_id]


@app.patch("/orders/{order_id}", tags=["Orders"])
def patch_order(order_id: str, body: PatchOrderRequest, _: str = Depends(require_auth)):
    """Update an order's status."""
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    order = ORDERS[order_id]
    if body.status is not None:
        valid = {"pending", "confirmed", "shipped", "delivered", "cancelled", "refunded"}
        if body.status not in valid:
            raise HTTPException(status_code=422, detail=f"Invalid status '{body.status}'. Must be one of: {sorted(valid)}")
        order["status"] = body.status

    order["updated_at"] = datetime.now(timezone.utc).isoformat()
    return order
