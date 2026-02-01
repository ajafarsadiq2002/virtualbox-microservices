# Microservices Architecture on VirtualBox

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)](https://ubuntu.com/)
[![VirtualBox](https://img.shields.io/badge/VirtualBox-7.0+-red.svg)](https://www.virtualbox.org/)

A complete microservices architecture deployed across multiple Virtual Machines using VirtualBox, demonstrating distributed system concepts and inter-service communication.

## Project Overview

This project implements a production-ready microservices system with:
- **3 Virtual Machines** running Ubuntu Server 22.04
- **Python FastAPI** microservices
- **API Gateway pattern** for centralized request routing
- **RESTful APIs** with automatic Swagger documentation
- **Inter-service HTTP communication**
- **SystemD service management** for production deployment

## Architecture

```
                    ┌─────────────────┐
                    │     Client      │
                    │  (Host Machine) │
                    └────────┬────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │        API Gateway           │
              │   VM1 (ubuntu)               │
              │   192.168.29.233:3000        │
              └──────────┬───────────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
┌───────────────────────┐  ┌───────────────────────┐
│    Order Service      │  │     User Service      │
│   VM2 (ubuntu 1)      │  │    VM3 (ubuntu 2)     │
│   192.168.29.234:3002 │──│   192.168.29.235:3001 │
└───────────────────────┘  └───────────────────────┘
```

## Repository Structure

```
virtualbox-microservices/
├── .gitignore                       # Git ignore rules
├── README.md                        # Project overview and setup guide
├── GIT_SETUP.md                     # Git repository setup guide
├── ARCHITECTURE_DESIGN.md           # Architecture diagrams and design
│
├── api-gateway/
│   ├── main.py                      # API Gateway application
│   ├── requirements.txt             # Python dependencies
│   ├── api-gateway.service          # SystemD service file
│   └── README.md                    # Service documentation
│
├── user-service/
│   ├── main.py                      # User Service application
│   ├── requirements.txt             # Python dependencies
│   ├── user-service.service         # SystemD service file
│   └── README.md                    # Service documentation
│
└── order-service/
    ├── main.py                      # Order Service application
    ├── requirements.txt             # Python dependencies
    ├── order-service.service        # SystemD service file
    └── README.md                    # Service documentation
```

## Services Overview

| Service | VM | IP Address | Port | Description |
|---------|-----|------------|------|-------------|
| API Gateway | VM1 (ubuntu) | 192.168.29.233 | 3000 | Central entry point, request routing |
| Order Service | VM2 (ubuntu 1) | 192.168.29.234 | 3002 | Order management, user integration |
| User Service | VM3 (ubuntu 2) | 192.168.29.235 | 3001 | User data management |

## Quick Start

### Prerequisites
- VirtualBox 7.0+
- 3 Ubuntu Server 22.04 VMs configured with Bridged Adapter
- Python 3.12+ installed on each VM

### Installation on Each VM

**VM3 - User Service (192.168.29.235):**
```bash
mkdir -p ~/microservices/user-service
cd ~/microservices/user-service

# Copy files from repository
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**VM2 - Order Service (192.168.29.234):**
```bash
mkdir -p ~/microservices/order-service
cd ~/microservices/order-service

# Copy files from repository
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**VM1 - API Gateway (192.168.29.233):**
```bash
mkdir -p ~/microservices/api-gateway
cd ~/microservices/api-gateway

# Copy files from repository
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Production Deployment (SystemD)

Each service includes a `.service` file for SystemD deployment.

```bash
# Copy service file to systemd
sudo cp <service-name>.service /etc/systemd/system/

# Reload daemon and enable service
sudo systemctl daemon-reload
sudo systemctl enable <service-name>
sudo systemctl start <service-name>

# Check status
sudo systemctl status <service-name>
```

## API Endpoints

### API Gateway (http://192.168.29.233:3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI documentation |

### User Endpoints (via Gateway)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List all users |
| GET | `/api/users/{id}` | Get user by ID |
| POST | `/api/users` | Create new user (validates unique email) |

### Order Endpoints (via Gateway)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | List all orders |
| GET | `/api/orders/{id}` | Get order with user details |
| POST | `/api/orders` | Create new order (validates user exists) |

## Testing

### Health Checks
```bash
curl http://192.168.29.233:3000/health
curl http://192.168.29.234:3002/health
curl http://192.168.29.235:3001/health
```

### Create User
```bash
curl -X POST http://192.168.29.233:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Create Order
```bash
curl -X POST http://192.168.29.233:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "product": "Laptop",
    "quantity": 1,
    "amount": 999.99
  }'
```

### Get Order with User Details (Inter-Service Communication)
```bash
curl http://192.168.29.233:3000/api/orders/1
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Virtualization | VirtualBox 7.0+ | VM creation and management |
| Operating System | Ubuntu Server 22.04 LTS | Server platform |
| Programming Language | Python 3.12+ | Application development |
| Web Framework | FastAPI 0.109.0 | REST API development |
| HTTP Server | Uvicorn 0.27.0 | ASGI server |
| Data Validation | Pydantic 2.5.3 | Request/Response validation |
| HTTP Client | HTTPX 0.26.0 | Inter-service communication |
| Service Management | SystemD | Process lifecycle management |

## Features

- Interactive API Documentation (Swagger UI) at `/docs`
- Type-safe request/response with Pydantic models
- Async/await support for high performance
- Inter-service HTTP communication
- Health check endpoints for monitoring
- SystemD service management for production
- Automatic request validation
- CORS support for cross-origin requests

## Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Project overview and setup guide |
| [GIT_SETUP.md](GIT_SETUP.md) | Git repository setup and commands |
| [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) | System architecture and design diagrams |
| [api-gateway/README.md](api-gateway/README.md) | API Gateway service documentation |
| [user-service/README.md](user-service/README.md) | User Service documentation |
| [order-service/README.md](order-service/README.md) | Order Service documentation |

## Project Deliverables

| Deliverable | Status | File/Folder |
|-------------|--------|-------------|
| Architecture Design | Complete | ARCHITECTURE_DESIGN.md |
| API Gateway Source | Complete | api-gateway/ |
| User Service Source | Complete | user-service/ |
| Order Service Source | Complete | order-service/ |
| SystemD Configurations | Complete | *.service files |
| Git Setup Guide | Complete | GIT_SETUP.md |

## Access URLs

| Service | URL | Documentation |
|---------|-----|---------------|
| API Gateway | http://192.168.29.233:3000 | http://192.168.29.233:3000/docs |
| User Service | http://192.168.29.235:3001 | http://192.168.29.235:3001/docs |
| Order Service | http://192.168.29.234:3002 | http://192.168.29.234:3002/docs |

## Author

**Jafar Sadiq A**
- **Student ID:** M25AI2113
- **Email:** m25ai2113@iitj.ac.in
- **Course:** Virtualization and Cloud Computing
- **Institution:** Indian Institute of Technology, Jodhpur
- **Instructor:** Sumit Kalra
- **Date:** January 30, 2026

## License

This project is for educational purposes as part of the Virtualization and Cloud Computing course at IIT Jodhpur.

---

**Quick Access:**
- Main API: http://192.168.29.233:3000
- Interactive Docs: http://192.168.29.233:3000/docs
