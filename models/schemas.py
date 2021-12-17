from pydantic import BaseModel
from typing import List

from db.connection import Base


class PhoneVerify(BaseModel):
    phone_number    : str
    
    class Config:
        orm_mode = True
        
class CodeVerify(BaseModel):
    fullname        : str
    phone_number    : str
    
    class Config:
        orm_mode = True
        
class AddUserInterest(BaseModel):
    user_id         : int
    items_id        : List[int] = []
    
    class Config:
        orm_mode = True
        
class GetProfile(BaseModel):
    category        : List[int]
    sort            : int
    tags_id         : List[int]
    limit           : int
    page            : int
    
    class Config:
        orm_mode = True
        
class CreateCardUsers(BaseModel):
    date            : str
    gender          : int
    passport_info   : str
    email           : str
    is_sms          : bool
    status          : int
    job_id          : int
    
    class Config:
        orm_mode = True
        
class CreateInbox(BaseModel):
    title           : str
    message         : str
    
    class Config:
        orm_mode = True
        
class GetPromoCodes(BaseModel):
    profile_id      : int
    
    class Config:
        orm_mode = True
        
class AddCertificate(BaseModel):
    amount          : int
    profile_id      : int
    
    class Config:
        orm_mode = True