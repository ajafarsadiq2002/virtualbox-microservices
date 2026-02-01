# Order Service

Order management microservice with User Service integration for data enrichment.

## Overview

| Property | Value |
|----------|-------|
| **Port** | 3002 |
| **Host** | 0.0.0.0 |
| **VM** | VM2 (ubuntu 1) |
| **IP Address** | 192.168.29.234 |

## Features

- Order creation and retrieval operations
- User validation via User Service integration
- Order data enrichment with user details
- Inter-service communication with User Service (HTTPX)
- Health check endpoint with order count
- Auto-generated Swagger documentation

## Service Dependencies

| Service | URL | Purpose |
|---------|-----|---------|
| User Service | http://192.168.29.235:3001 | User validation and data enrichment |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information |
| GET | `/health` | Health check with order count |
| GET | `/orders` | Get all orders |
| GET | `/orders/{id}` | Get order by ID with user details |
| POST | `/orders` | Create new order (validates user exists) |

## Data Model

### Order
```json
{
  "id": 1,
  "userId": 1,
  "product": "Laptop",
  "quantity": 1,
  "amount": 999.99,
  "status": "pending",
  "created_at": "2026-01-30T10:00:00",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Create Order Request
```json
{
  "userId": 1,
  "product": "Laptop",
  "quantity": 1,
  "amount": 999.99
}
```

### Order Statuses
New orders are created with `pending` status. Sample data includes various statuses:
- `pending` - Order created, awaiting processing
- `processing` - Order being processed
- `shipped` - Order shipped
- `delivered` - Order delivered

## Installation

```bash
# Create directory
mkdir -p ~/microservices/order-service
cd ~/microservices/order-service

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
sudo systemctl start order-service
sudo systemctl status order-service
```

## Configuration

Update the User Service URL in `main.py` if your VM IP differs:

```python
USER_SERVICE_URL = "http://192.168.29.235:3001"
```

## Dependencies

- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic==2.5.3
- httpx==0.26.0

## Testing

```bash
# Health check
curl http://192.168.29.234:3002/health

# Get all orders
curl http://192.168.29.234:3002/orders

# Get order by ID (includes user details from User Service)
curl http://192.168.29.234:3002/orders/1

# Create new order (requires valid userId)
curl -X POST http://192.168.29.234:3002/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "product": "Keyboard",
    "quantity": 1,
    "amount": 79.99
  }'
```

## Initial Data

The service starts with 3 sample orders:
1. Laptop ($999.99) - delivered
2. Mouse ($29.99) - processing
3. Cable ($15.99) - shipped

## Inter-Service Communication

When fetching an order by ID, this service calls the User Service to enrich the order data with user details. This demonstrates microservices communication pattern.

```
Client -> Order Service -> User Service
         (get order)      (get user details)
```

## SystemD Service Configuration

A SystemD service file (`order-service.service`) is included for production deployment.

### Installation
```bash
# Copy service file to systemd directory
sudo cp order-service.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable order-service

# Start the service
sudo systemctl start order-service

# Check service status
sudo systemctl status order-service
```

### Service Management
```bash
# Start service
sudo systemctl start order-service

# Stop service
sudo systemctl stop order-service

# Restart service
sudo systemctl restart order-service

# View logs
sudo journalctl -u order-service -f
```

## Files

| File | Description |
|------|-------------|
| `main.py` | Main application code |
| `requirements.txt` | Python dependencies |
| `order-service.service` | SystemD service configuration |
| `README.md` | This documentation |

## Access URLs

- **Order Service**: http://192.168.29.234:3002
- **Documentation**: http://192.168.29.234:3002/docs
