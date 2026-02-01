# Architecture Design Document

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Browser  │  │ Postman  │  │   cURL   │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       │             │              │                         │
│       └─────────────┴──────────────┘                         │
│                     │                                        │
│              HTTP/REST (JSON)                               │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              VIRTUALBOX ENVIRONMENT                          │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           VM1: API GATEWAY                            │  │
│  │           192.168.29.233:3000                         │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  FastAPI Application                            │  │  │
│  │  │  • Request Routing                              │  │  │
│  │  │  • Proxying to backend services                │  │  │
│  │  │  • Request/Response logging                     │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │  OS: Ubuntu 22.04 | RAM: ~5GB | CPU: 1 core        │  │
│  └─────────┬──────────────────────┬─────────────────────┘  │
│            │                      │                         │
│    /api/users              /api/orders                      │
│            │                      │                         │
│    ┌───────▼──────┐      ┌───────▼──────┐                 │
│    │   VM2:       │      │   VM3:       │                 │
│    │   ORDER      │      │   USER       │                 │
│    │   SERVICE    │      │   SERVICE    │                 │
│    │192.168.29.234│      │192.168.29.235│                 │
│    │   :3002      │      │   :3001      │                 │
│    │              │      │              │                 │
│    │ ┌──────────┐ │      │ ┌──────────┐│                 │
│    │ │Order CR  │ │      │ │User CR   ││                 │
│    │ │Create    │ │─────►│ │Create    ││                 │
│    │ │Read      │ │      │ │Read      ││                 │
│    │ └──────────┘ │      │ └──────────┘│                 │
│    │              │      │              │                 │
│    │  [Orders DB] │      │  [Users DB]  │                 │
│    │  In-Memory   │      │  In-Memory   │                 │
│    └──────────────┘      └──────────────┘                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Legend:
  ──▶  HTTP Request Flow
  ◄──  HTTP Response Flow
  [ ]  Data Store
```

### Network Topology

```
┌────────────────────────────────────────┐
│         Physical Network                │
│         192.168.29.0/24                 │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │      Router/Gateway               │  │
│  │      192.168.29.1 (DHCP)         │  │
│  └─────────────┬────────────────────┘  │
│                │                        │
│    ┌───────────┼───────────┐           │
│    │           │           │           │
│    ▼           ▼           ▼           │
│ ┌─────┐    ┌─────┐    ┌─────┐        │
│ │ VM1 │    │ VM2 │    │ VM3 │        │
│ │.233 │    │.234 │    │.235 │        │
│ │:3000│    │:3002│    │:3001│        │
│ └─────┘    └─────┘    └─────┘        │
└────────────────────────────────────────┘
```

### Request Flow Sequence

```
Client → Gateway → Order Service → User Service

1. Client: GET /api/orders/1
2. Gateway proxies to Order Service
3. Order Service fetches order from DB
4. Order Service calls User Service for user details
5. User Service returns user data
6. Order Service enriches order with user data
7. Order Service returns to Gateway
8. Gateway returns to Client
```

## Component Design

### 1. API Gateway (VM1)

**Responsibilities:**
- Single entry point for all requests
- Request routing to appropriate services
- Protocol translation
- Request/response logging

**Endpoints:**
```
GET  /health                # Health check
GET  /docs                  # API documentation
GET  /api/users             # Proxy to User Service
GET  /api/users/{id}        # Proxy to User Service
POST /api/users             # Proxy to User Service
GET  /api/orders            # Proxy to Order Service
GET  /api/orders/{id}       # Proxy to Order Service
POST /api/orders            # Proxy to Order Service
```

**Technology:**
- FastAPI (web framework)
- HTTPX (HTTP client for proxying)
- Uvicorn (ASGI server)

### 2. User Service (VM3)

**Responsibilities:**
- User data management
- Create and Read operations for users
- Email validation (unique email check)
- Duplicate detection

**Data Model:**
```python
User {
    id: int
    name: str
    email: str (validated)
    created_at: datetime
}
```

**Endpoints:**
```
GET  /health        # Health check
GET  /users         # List all users
GET  /users/{id}    # Get specific user
POST /users         # Create new user
```

### 3. Order Service (VM2)

**Responsibilities:**
- Order data management
- Create and Read operations for orders
- User verification via User Service
- Order-User data enrichment

**Data Model:**
```python
Order {
    id: int
    userId: int
    product: str
    quantity: int
    amount: float
    status: str
    created_at: datetime
}
```

**Endpoints:**
```
GET  /health            # Health check
GET  /orders            # List all orders
GET  /orders/{id}       # Get order + user details
POST /orders            # Create new order
```

**Inter-Service Communication:**
```python
# Fetch user details
async with httpx.AsyncClient() as client:
    response = await client.get(
        f"http://192.168.29.235:3001/users/{userId}"
    )
```

## Data Flow Diagrams

### User Creation Flow

```
Client
  │
  ├─ POST /api/users {"name": "Alice", "email": "alice@example.com"}
  │
  ▼
API Gateway
  │
  ├─ Proxy to User Service
  │
  ▼
User Service
  │
  ├─ Validate email format
  ├─ Check email uniqueness  
  ├─ Generate ID
  ├─ Save to database
  │
  ▼
Return 201 Created
```

### Order Creation with User Verification

```
Client
  │
  ├─ POST /api/orders
  │
  ▼
API Gateway
  │
  ├─ Proxy to Order Service
  │
  ▼
Order Service
  │
  ├─ Verify user exists
  │   │
  │   ├─ Call User Service: GET /users/{id}
  │   │
  │   ▼
  │  User Service returns user data
  │
  ├─ User exists? Yes
  ├─ Create order
  ├─ Save to database
  │
  ▼
Return 201 Created
```

### Order Retrieval with User Enrichment

```
Client
  │
  ├─ GET /api/orders/1
  │
  ▼
API Gateway
  │
  ├─ Proxy to Order Service
  │
  ▼
Order Service
  │
  ├─ Fetch order from database
  ├─ Call User Service: GET /users/{userId}
  │   │
  │   ▼
  │  User Service returns user data
  │
  ├─ Enrich order with user info
  │
  ▼
Return order + user details
```

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Application** | FastAPI | 0.109.0 |
| **Server** | Uvicorn | 0.27.0 |
| **Validation** | Pydantic | 2.5.3 |
| **HTTP Client** | HTTPX | 0.26.0 |
| **Language** | Python | 3.10+ |
| **OS** | Ubuntu Server | 22.04 LTS |
| **Virtualization** | VirtualBox | 7.0+ |

## Network Configuration

### IP Allocation

| Component | IP | Port | Access |
|-----------|---------|------|--------|
| Router | 192.168.29.1 | - | Gateway |
| API Gateway (VM1) | 192.168.29.233 | 3000 | Public |
| Order Service (VM2) | 192.168.29.234 | 3002 | Internal |
| User Service (VM3) | 192.168.29.235 | 3001 | Internal |

### Network Type

**Bridged Adapter:**
- Direct connection to physical network
- Each VM gets its own IP on local network
- Allows VM-to-VM communication
- Allows internet access from VMs
- Allows host-to-VM access

## Scalability Considerations

### Current Architecture (Single Instance)
```
Client → API Gateway → User Service
                    → Order Service
```

### Scaled Architecture (Multiple Instances)
```
                    ┌─→ User Service 1
Client → Load → Gateway → User Service 2
         Balancer      └─→ User Service 3
```

### Future Enhancements

1. **Database Layer**: PostgreSQL for persistence
2. **Caching**: Redis for frequently accessed data
3. **Message Queue**: RabbitMQ for async processing
4. **Service Discovery**: Consul for dynamic registration
5. **Containerization**: Docker + Kubernetes

## Security Architecture

### Current Measures
- Private network (192.168.29.x)
- Input validation (Pydantic)
- Proper HTTP status codes
- No sensitive data in errors

### Recommended Enhancements
- JWT authentication
- HTTPS/TLS encryption
- Rate limiting
- API keys
- RBAC (Role-Based Access Control)

## Conclusion

This architecture demonstrates:
- ✅ Microservices pattern
- ✅ API Gateway design
- ✅ Service decomposition
- ✅ Inter-service communication
- ✅ RESTful API design
- ✅ Scalable foundation

**System Status:**
- 3 VMs configured and networked
- All services running and tested
- Complete inter-service communication
- Production-ready deployment

---

**Version:** 1.0
**Date:** January 30, 2026
**Status:** Complete
