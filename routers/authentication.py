from fastapi import APIRouter, Depends, Request
from models import Users, PhoneVerify, CodeVerify
from sqlalchemy.orm import Session
from db import get_db
import random
from tokens import Returns, create_access_token

authentication_router = APIRouter()

@authentication_router.post("/phone-verification")
def phone_verification(req: PhoneVerify, db: Session = Depends(get_db)):
    generated_code = random.randint(1000, 9999)
    return Returns.object(generated_code)
    
    
@authentication_router.post("/code-verification")
def code_verification(req: CodeVerify, db: Session = Depends(get_db)):
    get_user = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number
    ).first()
    if get_user:
        return Returns.object(get_user)
    else:
        newDict = {
            "fullname"      : req.fullname,
            "phone_number"  : req.phone_number
        }
        access_token = create_access_token(newDict)
        new_add = Users(
            fullname     = req.fullname,
            phone_number = req.phone_number,
            token        = access_token
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        if new_add:
            return Returns.INSERTED
        else:
            return Returns.NOT_INSERTED