from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import httpx
import uvicorn

app = FastAPI(title="Order Service")

USER_SERVICE_URL = "http://192.168.29.235:3001"

# Models
class OrderCreate(BaseModel):
    userId: int
    product: str
    quantity: int
    amount: float

# Database
orders_db = [
    {"id": 1, "userId": 1, "product": "Laptop", "quantity": 1, "amount": 999.99, "status": "delivered", "created_at": datetime.now()},
    {"id": 2, "userId": 2, "product": "Mouse", "quantity": 2, "amount": 29.99, "status": "processing", "created_at": datetime.now()},
    {"id": 3, "userId": 1, "product": "Cable", "quantity": 3, "amount": 15.99, "status": "shipped", "created_at": datetime.now()}
]

def get_next_id():
    return max(order["id"] for order in orders_db) + 1 if orders_db else 1

@app.get("/health")
async def health_check():
    return {"status": "UP", "service": "order-service", "orderCount": len(orders_db)}

@app.get("/orders")
async def get_orders():
    return {"success": True, "count": len(orders_db), "data": orders_db}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail={"error": "Order not found"})

    # Fetch user details
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{USER_SERVICE_URL}/users/{order['userId']}")
            if response.status_code == 200:
                user_data = response.json()
                order["user"] = user_data.get("data", user_data)
    except Exception as e:
        order["user"] = None

    return {"success": True, "data": order}

@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    # Verify user exists
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{USER_SERVICE_URL}/users/{order.userId}")
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail={"error": "User not found"})
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail={"error": "User service unavailable"})

    new_order = {
        "id": get_next_id(),
        "userId": order.userId,
        "product": order.product,
        "quantity": order.quantity,
        "amount": order.amount,
        "status": "pending",
        "created_at": datetime.now()
    }
    orders_db.append(new_order)
    return {"success": True, "data": new_order}

@app.get("/")
async def root():
    return {"service": "Order Service", "version": "1.0.0"}

if __name__ == "__main__":
    print("📦 Order Service Started on http://192.168.29.234:3002")
    uvicorn.run(app, host="0.0.0.0", port=3002)