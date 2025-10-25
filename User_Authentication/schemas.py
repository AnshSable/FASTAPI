from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    username:str

class UserCreate(UserBase):
    password:str

class UserUpdate(BaseModel):
    email:Optional[EmailStr]=None
    username:Optional[str]=None
    password:Optional[str]=None

class UserResponse(UserBase):
    id:int
    is_active:bool
    is_superuser:bool
    created_at:datetime

    class Config:
        from_attributes=True

class Token(BaseModel):
        access_token:str
        token_type:str


class TokenData(BaseModel):
        username:Optional[str]=None