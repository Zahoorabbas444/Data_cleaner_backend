from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from routers.upload import router as upload_router
from routers.payment import router as payment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Data Cleaner & Visual Insight Tool",
    version="1.0.0",
    lifespan=lifespan,
)

# 1. FIXED: Dynamically load CORS from your Vercel Environment Variables
# This uses the variable seen in your screenshot
raw_origins = os.getenv("CORS_ORIGINS", "https://data-cleaner-project.netlify.app")
origins = [origin.strip() for origin in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. FIXED: Keep the prefix, but you MUST update your frontend api.js 
# to use 'https://data-cleaner-backend.vercel.app/api' as the baseURL
app.include_router(upload_router, prefix="/api")
app.include_router(payment_router, prefix="/api")

.

@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running on Vercel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


