
from sqlalchemy import Boolean,Column,Integer,String,DateTime,Text
from sqlalchemy.sql import func
from app.database import Base

class URL(Base):
    __tablename__ ="urls"

    id = Column(Integer,primary_key=True,index=True)
    short_code=Column(String(10),unique=True,index=True,nullable=False)
    original_url = Column(Text,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    clicks = Column(Integer,default=True)
    is_active = Column(Boolean,default=True)
    title = Column(String(200))
    #user_id=Column(Integer,ForeignKey("users.id"))

class URLClick(Base):
    __tablename__ ="url_clicks"

    id = Column(Integer,primary_key=True,index=True)
    short_code = Column(String(10),nullable=False)
    clicked_at = Column(DateTime(timezone=True),server_default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(Text)
    referrer = Column(Text)
 