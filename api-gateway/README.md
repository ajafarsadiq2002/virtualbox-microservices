# API Gateway Service

Central entry point for the microservices architecture that routes client requests to backend services.

## Overview

| Property | Value |
|----------|-------|
| **Port** | 3000 |
| **Host** | 0.0.0.0 |
| **VM** | VM1 (ubuntu) |
| **IP Address** | 192.168.29.233 |

## Features

- Request routing to backend microservices
- Request logging middleware
- Unified API endpoint for clients
- Health check monitoring
- Auto-generated Swagger documentation

## Backend Services

| Service | URL |
|---------|-----|
| User Service | http://192.168.29.235:3001 |
| Order Service | http://192.168.29.234:3002 |

## API Endpoints

### Gateway Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation |

### User Endpoints (Proxied)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| GET | `/api/users/{id}` | Get user by ID |
| POST | `/api/users` | Create new user |

### Order Endpoints (Proxied)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Get all orders |
| GET | `/api/orders/{id}` | Get order with user details |
| POST | `/api/orders` | Create new order (validates user exists) |

## Installation

```bash
# Create directory
mkdir -p ~/microservices/api-gateway
cd ~/microservices/api-gateway

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Service

### Development Mode
```bash
source venv/bin/activate
python main.py
```

### Production Mode (SystemD)
```bash
sudo systemctl start api-gateway
sudo systemctl status api-gateway
```

## Configuration

Update the service URLs in `main.py` if your VM IPs differ:

```python
USER_SERVICE_URL = "http://192.168.29.235:3001"
ORDER_SERVICE_URL = "http://192.168.29.234:3002"
```

## Dependencies

- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- httpx==0.26.0

## Testing

```bash
# Health check
curl http://192.168.29.233:3000/health

# Get all users via gateway
curl http://192.168.29.233:3000/api/users

# Get all orders via gateway
curl http://192.168.29.233:3000/api/orders
```

## SystemD Service Configuration

A SystemD service file (`api-gateway.service`) is included for production deployment.

### Installation
```bash
# Copy service file to systemd directory
sudo cp api-gateway.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable api-gateway

# Start the service
sudo systemctl start api-gateway

# Check service status
sudo systemctl status api-gateway
```

### Service Management
```bash
# Start service
sudo systemctl start api-gateway

# Stop service
sudo systemctl stop api-gateway

# Restart service
sudo systemctl restart api-gateway

# View logs
sudo journalctl -u api-gateway -f
```

## Files

| File | Description |
|------|-------------|
| `main.py` | Main application code |
| `requirements.txt` | Python dependencies |
| `api-gateway.service` | SystemD service configuration |
| `README.md` | This documentation |

## Access URLs

- **API Gateway**: http://192.168.29.233:3000
- **Documentation**: http://192.168.29.233:3000/docs
