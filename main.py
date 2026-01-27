from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from routers.upload import router as upload_router
from routers.payment import router as payment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Vercel is serverless; we cannot run background cleanup tasks here.
    # We only ensure the /tmp directory is used if needed.
    yield

app = FastAPI(
    title="Data Cleaner & Visual Insight Tool",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# Production origins from environment variable
env_origins = os.getenv("CORS_ORIGINS", "")
if env_origins:
    production_origins = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
    allowed_origins = production_origins + default_origins
else:
    allowed_origins = ["https://data-cleaner-project.netlify.app"] + default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origins=[
        "https://data-cleaner-project.netlify.app", "http://localhost:5173", "http://localhost:3000", "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
    ],
)

app.include_router(upload_router, prefix="/api")
app.include_router(payment_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running on Vercel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)