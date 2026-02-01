from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="User Service")

# Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class User(UserCreate):
    id: int
    created_at: datetime

# Database
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": datetime.now()},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": datetime.now()},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "created_at": datetime.now()}
]

def get_next_id():
    return max(user["id"] for user in users_db) + 1 if users_db else 1

@app.get("/health")
async def health_check():
    return {"status": "UP", "service": "user-service", "userCount": len(users_db)}

@app.get("/users")
async def get_users():
    return {"success": True, "count": len(users_db), "data": users_db}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail={"success": False, "error": "User not found"})
    return {"success": True, "data": user}

@app.post("/users", status_code=201)
async def create_user(user: UserCreate):
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=409, detail={"success": False, "error": "Email exists"})

    new_user = {
        "id": get_next_id(),
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    return {"success": True, "data": new_user, "message": "User created"}

@app.get("/")
async def root():
    return {"service": "User Service", "version": "1.0.0"}

if __name__ == "__main__":
    print("👤 User Service Started on http://192.168.29.235:3001")
    uvicorn.run(app, host="0.0.0.0", port=3001)