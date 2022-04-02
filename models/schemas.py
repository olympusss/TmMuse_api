from pydantic import BaseModel
from typing import List

class PhoneVerify(BaseModel):
    phone_number    : str
    
    class Config:
        orm_mode = True
        
class CodeVerify(BaseModel):
    fullname        : str
    phone_number    : str
    code            : str
    
    class Config:
        orm_mode = True
        
class AddUserInterest(BaseModel):
    user_id         : int
    items_id        : List[int] = []
    
    class Config:
        orm_mode = True
        
class GetProfile(BaseModel):
    category        : List[int] = []
    sort            : int
    tags_id         : List[int] = []
    limit           : int
    page            : int
    
    class Config:
        orm_mode = True
        
class CreateCardUsers(BaseModel):
    date            : str
    gender          : int
    email           : str
    is_sms          : bool
    status          : int
    
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
        
class Search(BaseModel):
    page            : int
    limit           : int
    text            : str
    
    class Config:
        orm_mode = True
        
class Ticket_insert_schema(BaseModel):
    cinema_id       : int
    profile_id      : int
    user_id         : int
    movie_date      : str
    movie_time      : str
    ticket_count    : int
    ticket_price    : float
    ticket_discount : float
    
    class Config:
        orm_mode = True
        
        
class ViewCountSchema(BaseModel):
    ads_id          : int
    type            : str
    user_id         : int = None
    
    class Config:
        orm_mode = True
        
        
class LikeDislikeSchema(BaseModel):
    id              : int
    column_type     : str
    table_type      : str
    type            : bool
    
    class Config:
        orm_mode = True
        
        
class SendUserIsReadSchema(BaseModel):
    is_read         : bool
    
    class Config:
        orm_mode = True
        
        
class TicketStatusUpdateSchema(BaseModel):
    status              : int
    
    class Config:
        orm_mode = True
        
        
class cloud_messaging_token(BaseModel):
    title               : str
    body                : str
    token               : str