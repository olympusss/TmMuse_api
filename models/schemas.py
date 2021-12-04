from pydantic import BaseModel

class PhoneVerify(BaseModel):
    phone_number    : str
    
    class Config:
        orm_mode = True
        
class CodeVerify(BaseModel):
    fullname        : str
    phone_number    : str
    
    class Config:
        orm_mode = True