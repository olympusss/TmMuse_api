from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base

class Users(Base):
    __tablename__      = "users"
    id                 = Column(Integer, primary_key=True, index=True)
    fullname           = Column(String)
    phone_number       = Column(String)
    token              = Column(String)
    notif_token        = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())