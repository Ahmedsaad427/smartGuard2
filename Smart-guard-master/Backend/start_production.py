# Production backend for Railway deployment
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Run without video streaming for production
    uvicorn.run("main:app", host=host, port=port, loop="asyncio")
