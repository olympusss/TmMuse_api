from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from tokens import check_token, decode_token, Returns
import crud
from models import CreateInbox

answers_router = APIRouter()

@answers_router.get("/answers")
def get_answers(header_param: Request, db: Session = Depends(get_db)):
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
    first_response = crud.read_inbox_by_user_id(db=db, user_id=user_id["id"])
    second_response = crud.read_inbox(db=db)
    third_response = crud.read_answered_messages_by_user_id(db=db, user_id=user_id["id"])
    results = {}
    results["first"] = first_response
    results["second"] = second_response
    results["third"] = third_response
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
    
@answers_router.post("/insert-inbox")
async def insert_inbox(req: CreateInbox, header_param: Request, db: Session = Depends(get_db)):
    result_inbox = crud.create_inbox(db=db, req=req)
    if not result_inbox:
        return Returns.NOT_INSERTED
    get_token = check_token(header_param=header_param)
    if not get_token:
        return Returns.INSERTED
    else:
        payload = decode_token(token=get_token)
        if not payload:
            return Returns.TOKEN_NOT_DECODED
        fullname: str = payload.get("fullname")
        phone_number: str = payload.get("phone_number")
        user_id = crud.read_user_by_fullname_and_phone_number(db=db, fullname=fullname, phone_number=phone_number)
        if not user_id:
            return Returns.USER_NOT_FOUND
        inbox_id = crud.read_inbox_by_title_and_message(db=db, title=req.title, message=req.message)
        if not inbox_id:
            return Returns.NULL
        result = crud.create_send_user(db=db, userID=user_id["id"], inboxID=inbox_id["id"])
        if result:
            return Returns.INSERTED
        else:
            return Returns.NOT_INSERTED
        