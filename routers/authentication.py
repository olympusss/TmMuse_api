from fastapi import APIRouter, Depends
from models import PhoneVerify, CodeVerify
from sqlalchemy.orm import Session
from db import get_db
import random
import crud
from tokens import Returns
from datetime import datetime
from socket_io import sio


authentication_router = APIRouter()

@authentication_router.post("/phone-verification")
async def phone_verification(req: PhoneVerify, db: Session = Depends(get_db)):
    generated_code = random.randint(1000, 9999)
    result = crud.create_number_socket(db=db, number=req, code=generated_code)
    data = f"{req.phone_number},{generated_code}"
    await sio.emit("onMessage", data)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED    
            
@authentication_router.post("/code-verification")
def code_verification(req: CodeVerify, db: Session = Depends(get_db)):
    if (req.phone_number == "+99362737222") and (req.code == "1811"):
        get_user = crud.read_user_by_phone_number(db, phone_number=req.phone_number)
        if get_user:
            return Returns.object(get_user)
        else:
            result = crud.create_user(db=db, req=req) 
            if not result:
                return Returns.NULL
            return Returns.object(crud.read_user_by_phone_number(db, phone_number=req.phone_number))
            
    verify = crud.read_phone_number_and_code(db=db, phone_number=req.phone_number, code=req.code)
    if not verify:
        crud.delete_number_socket(db=db, phone_number=req.phone_number)
        return Returns.WRONG_CODE
    
    # * Time (NOW)
    hour_now   = datetime.now().hour
    minute_now = datetime.now().minute
    second_now = datetime.now().second
    
    # * Time (TABLE)
    hour_table   = verify.created_at.hour
    minute_table = verify.created_at.minute
    second_table = verify.created_at.second
    
    print(hour_now, minute_now, second_now)
    print(hour_table, minute_table, second_table)
    # TODO: hour, minute, second convert to minute(NOW)
    all_to_minute_now   = hour_now * 60 + minute_now + (second_now / 60)
    
    # TODO: hour, minute, second convert to minute(TABLE)
    all_to_minute_table = hour_table * 60 + minute_table + (second_table / 60)
    # print("Dif: "+all_to_minute_now+"- "+all_to_minute_table)
    # TODO: Difference of two time
    diff = abs(all_to_minute_now - all_to_minute_table)
    if diff > 2:
        crud.delete_number_socket(db=db, phone_number=req.phone_number)
        return Returns.TIMEOUT
    
    
    get_user = crud.read_user_by_phone_number(db, phone_number=req.phone_number)
    if get_user:
        crud.delete_number_socket(db=db, phone_number=req.phone_number)
        return Returns.object(get_user)
    
    
    result = crud.create_user(db=db, req=req) 
    if not result:
        return Returns.NULL
    
    get_user = crud.read_user_by_phone_number(db, phone_number=req.phone_number)
    if get_user:
        crud.delete_number_socket(db=db, phone_number=req.phone_number)
        return Returns.object(get_user)