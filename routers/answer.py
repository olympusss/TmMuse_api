from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud
from models import CreateInbox, SendUserIsReadSchema

answers_router = APIRouter()

@answers_router.get("/answers", dependencies=[Depends(HTTPBearer())])
def get_answers(header_param: Request, db: Session = Depends(get_db)):
    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)
    if user_id:
        first_response = crud.read_inbox_by_user_id(db=db, user_id=user_id)
        second_response = crud.read_inbox(db=db)
        third_response = crud.read_answered_messages_by_user_id(db=db, user_id=user_id)
    else:
        first_response = None
        second_response = crud.read_inbox(db=db)
        third_response = None
    results = {}
    results["first"] = first_response
    results["second"] = second_response
    results["third"] = third_response
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
    
@answers_router.post("/insert-inbox", dependencies=[Depends(HTTPBearer())])
async def insert_inbox(req: CreateInbox, header_param: Request, db: Session = Depends(get_db)):
    result_inbox = crud.create_inbox(db=db, req=req)
    if not result_inbox:
        return Returns.NOT_INSERTED
    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    inbox_id = crud.read_inbox_by_title_and_message(db=db, title=req.title, message=req.message)
    if not inbox_id:
        return Returns.NULL
    result = crud.create_send_user(db=db, userID=user_id, inboxID=inbox_id["id"])
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@answers_router.put("/update-is-read", dependencies=[Depends(HTTPBearer())])
async def update_is_read(id: int, req: SendUserIsReadSchema, header_param: Request, db: Session = Depends(get_db)):
    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    result = await crud.update_send_user_is_read(db=db, id=id, req=req)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    