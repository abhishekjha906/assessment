
"""
Main entrypoint for HR Employee Search API microservice.
Handles app setup, health check, CORS, and API router inclusion.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.apis.employee_api import router as employee_router

app = FastAPI(
    title="HR Employee Search API",
    description="Search API for HR employee directory.",
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
def health() -> dict:
    """
    Health check endpoint for service monitoring.
    Returns status OK if service is running.
    """
    return {"status": "ok"}

# Enable CORS for all origins (customize for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(employee_router)
