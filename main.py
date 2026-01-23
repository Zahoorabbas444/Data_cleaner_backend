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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://data-cleaner-frontend.netlify.app", "http://localhost:5173", "http://localhost:3000", "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(payment_router)

@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running on Vercel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}



