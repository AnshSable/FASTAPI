from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from app import crud,schemas,models
from app.database import get_db

router = APIRouter()

@router.post("/shorten",response_model=schemas.URLResponse)
def create_short_url(
    url:schemas.URLCreate,
    request:Request,
    db:Session = Depends(get_db)
):
    try:
        db_url = crud.create_short_url(db,url)

        base_url =str(request.base_url)
        short_url = f"{base_url}r/{db_url.short_code}"

        created_at = getattr(db_url, 'created_at', None)
        if created_at is None:
            from datetime import datetime
            created_at = datetime.utcnow()

        return schemas.URLResponse(
            short_code=db_url.short_code,
            original_url=db_url.original_url,
            short_url=short_url,
            created_at=db_url.created_at,
            clicks=db_url.clicks,
            title=db_url.title,
            is_active=db_url.is_active
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.get("/r/{short_code}")
def redirect_to_url(
    short_code:str,
    request:Request,
    db:Session = Depends(get_db)
):
    db_url = crud.get_url_by_short_code(db,short_code)

    if not db_url:
        raise HTTPException(status_code=404,detail="URL not found")
    
    if not db_url.is_active:
        raise HTTPException(status_code=410,detail ="URL is no longer active")
    
    crud.increment_click_count(db,short_code)

    crud.log_click_analytics(
        db,
        short_code,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer")
    )

    return RedirectResponse(url = db_url.original_url)

@router.get("/url/{short_code}",response_model=schemas.URLResponse)

def get_url_info(
    short_code:str,
    request:Request,
    db:Session=Depends(get_db)
):
    db_url = crud.get_url_by_short_code(db,short_code)

    if not db_url:
        raise HTTPException(status_code=404,detail="URL not found")
    
    base_url = str(request.base_url)
    short_url = f"{base_url}r/{db_url.short_code}"

    created_at = getattr(db_url, 'created_at', None)
    if created_at is None:
        from datetime import datetime
        created_at = datetime.utcnow()

    return schemas.URLResponse(
        short_code=db_url.short_code,
        original_url=db_url.original_url,
        short_url=short_url,
        created_at=created_at,
        clicks=getattr(db_url, 'clicks', 0),
        title=db_url.title,
        is_active=getattr(db_url, 'is_active', True)
    )

@router.delete("/url/{short_code}")

def delete_url(short_code:str,db:Session=Depends(get_db)):
    db_url = crud.get_url_by_short_code(db,short_code)

    if not db_url:
        raise HTTPException(status_code=404,detail="URL not found")
    
    db.delete(db_url)
    db.commit()

    return {"message":"URL deleted successfully"}
