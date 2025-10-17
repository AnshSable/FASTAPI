from pydantic import BaseModel,HttpUrl,validator
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    original_url:str
    custom_code:Optional[str]=None
    title:Optional[str] = None

class URLCreate(URLBase):
    @validator('custom_code')
    def validate_custom_code(cls,v):
        if v is not None:
            if len(v)<3:
                raise ValueError('custom code must be at least 3 characters')
            if not v.isalnum():
                raise ValueError('custom code must be alphanumeric')
        return v
    
class URLResponse(BaseModel):
    short_code:str
    original_url:str
    short_url:str
    created_at: datetime
    clicks:int 
    title:Optional[str]
    is_active:bool

    class Config:
        orm_mode = True

class URLClickResponse(BaseModel):
    clicked_at:datetime
    ip_address:Optional[str]
    user_agent:Optional[str]
    referrer:Optional[str]

    class Config:
        orm_mode = True

class AnalyticsResponse(BaseModel):
    total_clicks:int
    clicks_by_dat:list
    recent_clicks:list[URLClickResponse]