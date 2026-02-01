# User Service

User management microservice handling CRUD operations for user data.

## Overview

| Property | Value |
|----------|-------|
| **Port** | 3001 |
| **Host** | 0.0.0.0 |
| **VM** | VM3 (ubuntu 2) |
| **IP Address** | 192.168.29.235 |

## Features

- User creation and retrieval operations
- Email validation using Pydantic
- Duplicate email detection
- In-memory data storage with sample data
- Health check endpoint with user count
- Auto-generated Swagger documentation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information |
| GET | `/health` | Health check with user count |
| GET | `/users` | Get all users |
| GET | `/users/{id}` | Get user by ID |
| POST | `/users` | Create new user (validates unique email) |

## Data Model

### User
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-01-30T10:00:00"
}
```

### Create User Request
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Installation

```bash
# Create directory
mkdir -p ~/microservices/user-service
cd ~/microservices/user-service

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
sudo systemctl start user-service
sudo systemctl status user-service
```

## Dependencies

- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic[email]==2.5.3

## Testing

```bash
# Health check
curl http://192.168.29.235:3001/health

# Get all users
curl http://192.168.29.235:3001/users

# Get user by ID
curl http://192.168.29.235:3001/users/1

# Create new user
curl -X POST http://192.168.29.235:3001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

## Initial Data

The service starts with 3 sample users:
1. John Doe (john@example.com)
2. Jane Smith (jane@example.com)
3. Bob Johnson (bob@example.com)

## SystemD Service Configuration

A SystemD service file (`user-service.service`) is included for production deployment.

### Installation
```bash
# Copy service file to systemd directory
sudo cp user-service.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable user-service

# Start the service
sudo systemctl start user-service

# Check service status
sudo systemctl status user-service
```

### Service Management
```bash
# Start service
sudo systemctl start user-service

# Stop service
sudo systemctl stop user-service

# Restart service
sudo systemctl restart user-service

# View logs
sudo journalctl -u user-service -f
```

## Files

| File | Description |
|------|-------------|
| `main.py` | Main application code |
| `requirements.txt` | Python dependencies |
| `user-service.service` | SystemD service configuration |
| `README.md` | This documentation |

## Access URLs

- **User Service**: http://192.168.29.235:3001
- **Documentation**: http://192.168.29.235:3001/docs
