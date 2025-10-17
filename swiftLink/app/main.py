from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.routers.urls import router as urls_router
from app.routers.analytics import router as analytics_router
from app import crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SwiftLink URL Shortener",
    description="A fast and simple URL shortener service",
    version="1.0.0"
)

# Serve static files
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# Check if static directory exists before mounting
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(urls_router, prefix="/api/v1", tags=["urls"])
app.include_router(analytics_router, prefix="/api/v1", tags=["analytics"])

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/r/{short_code}")
def redirect_short_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect short URL to original URL"""
    db_url = crud.get_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if not db_url.is_active:
        raise HTTPException(status_code=410, detail="URL is no longer active")
    
    crud.increment_click_count(db, short_code)
    crud.log_click_analytics(db, short_code)
    
    return RedirectResponse(url=db_url.original_url)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# For Render, we need to handle the PORT environment variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)