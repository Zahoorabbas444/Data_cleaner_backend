from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Ensure these imports are correct for your folder structure
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

# FIXED CORS: This must match your Netlify URL exactly
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.upload import router as upload_router

app = FastAPI()

# This pulls the variable you just set in the Vercel dashboard
#
raw_origins = os.getenv("CORS_ORIGINS", "*")
origins = [origin.strip() for origin in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


