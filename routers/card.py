from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from tokens import check_token, decode_token, Returns
import crud
from models import CreateCardUsers

card_router = APIRouter()

@card_router.get("/get-jobs")
def get_jobs(db: Session = Depends(get_db)):
    result = crud.read_all_jobs(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@card_router.get("/get-card-promotion")
def get_card_promotion(limit: int, page: int, db: Session = Depends(get_db)):
    result = crud.read_profile_card_promotion(db=db, limit=limit, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@card_router.post("/create-card-user")
def create_card_user(header_param: Request, req: CreateCardUsers, db: Session = Depends(get_db)):
    get_token = check_token(header_param=header_param)
    if not get_token:
        return Returns.TOKEN_NOT_FOUND
    payload = decode_token(token=get_token)
    if not payload:
        return Returns.TOKEN_NOT_DECODED
    fullname: str = payload.get("fullname")
    phone_number: str = payload.get("phone_number")
    user_id = crud.read_user_by_fullname_and_phone_number(db=db, fullname=fullname, phone_number=phone_number)
    if not user_id:
        return Returns.USER_NOT_FOUND
    result = crud.create_card_user(db=db, req=req, userID=user_id["id"])
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED