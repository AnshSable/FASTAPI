from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/analytics/{short_code}", response_model=schemas.AnalyticsResponse)
def get_url_analytics(short_code: str, db: Session = Depends(get_db)):
    """Get analytics for a short URL"""
    analytics = crud.get_url_analytics(db, short_code)
    
    if not analytics:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return analytics