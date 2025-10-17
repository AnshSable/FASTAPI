import secrets
import string
from sqlalchemy.orm import Session
from . import models,schemas

def create_short_code(length:int=6)->str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet)for _ in range(length))

def create_short_url(db:Session,url:schemas.URLCreate)-> models.URL:

    if url.custom_code:
        db_url = get_url_by_short_code(db,url.custom_code)
        if db_url:
            raise ValueError('custom code already exists')
        short_code = url.custom_code

    else:
        while True:
            short_code = create_short_code()
            if not get_url_by_short_code(db,short_code):
                break

    db_url = models.URL(
        short_code = short_code,
        original_url =url.original_url,
        title= url.title
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_code(db:Session,short_code:str)->models.URL:
    return db.query(models.URL).filter(models.URL.short_code==short_code).first()

def increment_click_count(db:Session,short_code:str):
    db_url = get_url_by_short_code(db,short_code)
    if db_url:
        db_url.clicks +=1
        db.commit()

def log_click_analytics(db:Session,short_code:str,ip_address:str = None,user_agent:str=None,referrer:str =None):
    click = models.URLClick(
        short_code = short_code,
        ip_address = ip_address,
        user_agent=user_agent,
        referrer=referrer
    )
    db.add(click)
    db.commit()

def get_url_analytics(db:Session,short_code:str):
    url = get_url_by_short_code(db,short_code)
    if not url:
        return None
    
    recent_clicks = db.query(models.URLClick).filter(
        models.URLClick.short_code == short_code
    ).order_by(models.URLClick.clicked_at.desc()).limit(50).all()

    return{
        "total_clicks":url.clicks,
        "recent_clicks":recent_clicks
    }