# Production backend without OpenCV dependencies
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import json
import asyncio
from typing import List

# Include routers
app = FastAPI(
    title="Smart Guard API - Production",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check
@app.get("/")
async def root():
    return {"message": "Smart Guard API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "smart-guard-api"}

# Authentication endpoints
@app.post("/auth/signin")
async def signin(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        # Simple mock authentication for demo
        if email and password:
            return {
                "success": True,
                "user": {
                    "id": 1,
                    "email": email,
                    "name": "Demo User",
                    "role": "security_personnel",
                    "organization": "Smart Guard"
                },
                "token": "demo_token_12345"
            }
        else:
            return {"success": False, "error": "Missing credentials"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/auth/signup")
async def signup(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        role = data.get("role", "security_personnel")
        organization = data.get("organization", "Smart Guard")
        
        # Simple mock signup for demo
        if email and password and name:
            return {
                "success": True,
                "user": {
                    "id": 1,
                    "email": email,
                    "name": name,
                    "role": role,
                    "organization": organization
                },
                "token": "demo_token_12345"
            }
        else:
            return {"success": False, "error": "Missing required fields"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/users/me")
async def get_current_user():
    # Mock current user endpoint
    return {
        "id": 1,
        "email": "demo@smartguard.com",
        "name": "Demo User",
        "role": "security_personnel",
        "organization": "Smart Guard"
    }

@app.get("/events")
async def get_events():
    # Mock events endpoint
    return [
        {
            "id": 1,
            "type": "suspicious_behavior",
            "score": 0.85,
            "timestamp": "2026-04-10T01:30:00Z",
            "location": "Camera 1",
            "description": "Suspicious activity detected",
            "severity": "high"
        },
        {
            "id": 2,
            "type": "normal_activity",
            "score": 0.15,
            "timestamp": "2026-04-10T01:25:00Z",
            "location": "Camera 2",
            "description": "Normal activity",
            "severity": "low"
        }
    ]

# Include all routers (without video processing) - commented out for now
# try:
#     from routers.auth import router as auth_router
#     app.include_router(auth_router, prefix="/auth", tags=["authentication"])
# except ImportError:
#     print("Warning: Auth router not found")

# try:
#     from routers.users import router as users_router
#     app.include_router(users_router, prefix="/users", tags=["users"])
# except ImportError:
#     print("Warning: Users router not found")

# try:
#     from routers.events import router as events_router
#     app.include_router(events_router, prefix="/events", tags=["events"])
# except ImportError:
#     print("Warning: Events router not found")

# try:
#     from routers.detection import router as detection_router
#     app.include_router(detection_router, prefix="/detection", tags=["detection"])
# except ImportError:
#     print("Warning: Detection router not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("main_production:app", host=host, port=port, loop="asyncio")
