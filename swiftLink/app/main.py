from fastapi import FastAPI
from app.database import engine, Base
from app.routers import urls, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SwiftLink URL Shortener",
    description="A fast and simple URL shortener service",
    version="1.0.0"
)

# Include routers
app.include_router(urls.router, prefix="/api/v1", tags=["urls"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftLink URL Shortener API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}