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

# Simple endpoints for testing
@app.get("/auth/test")
async def auth_test():
    return {"message": "Auth endpoint working", "status": "ok"}

@app.get("/users/test")
async def users_test():
    return {"message": "Users endpoint working", "status": "ok"}

@app.get("/events/test")
async def events_test():
    return {"message": "Events endpoint working", "status": "ok"}

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
