from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud
from models import CreateInbox, SendUserIsReadSchema

answers_router = APIRouter()



@answers_router.get("/answers", dependencies=[Depends(HTTPBearer())])
async def get_answers(header_param: Request, db: Session = Depends(get_db)):
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    new_list = []
    if user_id:
        first_response = await crud.read_inbox_by_user_id(db=db, user_id=user_id)
        if first_response:
            for first in first_response:
                new_list.append(first)
        third_response = await crud.read_answered_messages_by_user_id(db=db, user_id=user_id)
        if third_response:
            for third in third_response:
                new_list.append(third)
    second_response = await crud.read_inbox(db=db)
    if second_response:
        for second in second_response:
            new_list.append(second)
    results = new_list
    results = sorted(results, key=lambda d: d["created_at"], reverse=True)
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
    
@answers_router.post("/insert-inbox", dependencies=[Depends(HTTPBearer())])
async def insert_inbox(req: CreateInbox, header_param: Request, db: Session = Depends(get_db)):
    result_inbox = await crud.create_inbox(db=db, req=req)
    if not result_inbox:
        return Returns.NOT_INSERTED
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    inbox_id = await crud.read_inbox_by_title_and_message(db=db, title=req.title, message=req.message)
    if not inbox_id:
        return Returns.NULL
    result = await crud.create_send_user(db=db, userID=user_id, inboxID=inbox_id["id"])
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@answers_router.put("/update-is-read", dependencies=[Depends(HTTPBearer())])
async def update_is_read(id: int, req: SendUserIsReadSchema, header_param: Request, db: Session = Depends(get_db)):
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    result = await crud.update_send_user_is_read(db=db, id=id, req=req)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    