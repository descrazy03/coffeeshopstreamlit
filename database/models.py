from database.setup import Base
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, String, Column, Text 

'''
define database models for data validation
'''

# pydantic base models
class CafeBase(BaseModel):
    id: Optional[str] = None
    name: str
    address: str
    has_restroom: bool
    restroom_pass: str
    has_wifi: bool
    wifi_pass: str
    has_outlets: bool
    notes: str
    is_fav: bool
    mon_open: str
    mon_close: str
    tue_open: str
    tue_close: str
    wed_open: str
    wed_close: str
    thu_open: str
    thu_close: str
    fri_open: str
    fri_close: str
    sat_open: str
    sat_close: str
    sun_open: str
    sun_close: str
    updated_at: Optional[str] = None

# SQL Table Models
class Cafe(Base):
    __tablename__ = 'cafes'

    id = Column(String, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(200))
    has_restroom = Column(Boolean)
    restroom_pass = Column(String(100))
    has_wifi = Column(Boolean)
    wifi_pass = Column(String(100))
    has_outlets = Column(Boolean)
    notes = Column(Text)
    is_fav = Column(Boolean)
    mon_open = Column(String(50))
    mon_close = Column(String(50))
    tue_open = Column(String(50))
    tue_close = Column(String(50))
    wed_open = Column(String(50))
    wed_close = Column(String(50))
    thu_open = Column(String(50))
    thu_close = Column(String(50))
    fri_open = Column(String(50))
    fri_close = Column(String(50))
    sat_open = Column(String(50))
    sat_close = Column(String(50))
    sun_open = Column(String(50))
    sun_close = Column(String(50))
    updated_at = Column(String(100))