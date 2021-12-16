from fastapi import APIRouter, Depends
from models import PhoneVerify, CodeVerify
from sqlalchemy.orm import Session
from db import get_db
import random
import crud
from tokens import Returns

authentication_router = APIRouter()

@authentication_router.get("/get-users")
def get_users(db: Session = Depends(get_db)):
    result = crud.read_all_users(db)
    if result:
        return Returns.object(result)
    else: 
        return Returns.NULL


@authentication_router.post("/phone-verification")
def phone_verification(req: PhoneVerify, db: Session = Depends(get_db)):
    generated_code = random.randint(1000, 9999)
    return Returns.object(generated_code)
    
    
@authentication_router.post("/code-verification")
def code_verification(req: CodeVerify, db: Session = Depends(get_db)):
    get_user = crud.read_user_by_phone_number(db, phone_number=req.phone_number)
    if get_user:
        return Returns.object(get_user)
    else:
        new_add = crud.create_user(db=db, req=req) 
        if new_add:
            return Returns.INSERTED
        else:
            return Returns.NOT_INSERTED