from pydantic import BaseModel
from typing import List

from sqlalchemy.sql.expression import true

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