from fastapi import FastAPI, Request, Response, HTTPException
import httpx
import uvicorn
from datetime import datetime

app = FastAPI(title="API Gateway")

USER_SERVICE_URL = "http://192.168.29.235:3001"
ORDER_SERVICE_URL = "http://192.168.29.234:3002"

@app.get("/health")
async def health_check():
    return {"status": "UP", "service": "api-gateway", "timestamp": datetime.now().isoformat()}

@app.api_route("/api/users", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str = ""):
    target_url = f"{USER_SERVICE_URL}/users/{path}" if path else f"{USER_SERVICE_URL}/users"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            body = await request.body()
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers.items() if k.lower() not in ['host', 'connection']},
                content=body if body else None
            )
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail={"error": "User service unavailable"})

@app.api_route("/api/orders", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_orders(request: Request, path: str = ""):
    target_url = f"{ORDER_SERVICE_URL}/orders/{path}" if path else f"{ORDER_SERVICE_URL}/orders"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            body = await request.body()
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={k: v for k, v in request.headers.items() if k.lower() not in ['host', 'connection']},
                content=body if body else None
            )
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail={"error": "Order service unavailable"})

@app.get("/")
async def root():
    return {
        "message": "🚀 Microservices API Gateway",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "users": "/api/users",
            "orders": "/api/orders"
        }
    }

if __name__ == "__main__":
    print("🚀 API Gateway Started on http://192.168.29.233:3000")
    print("📖 Docs available at: http://192.168.29.233:3000/docs")
    uvicorn.run(app, host="0.0.0.0", port=3000)