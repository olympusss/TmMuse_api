from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud
from models import CreateCardUsers
from cloud_messaging.cloud_messaging import send_to_topic
card_router = APIRouter()

    
@card_router.get("/get-card-promotion")
async def get_card_promotion(limit: int, page: int, db: Session = Depends(get_db)):
    result = await crud.read_profile_card_promotion(db=db, limit=limit, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL    
    
@card_router.post("/create-card-user", dependencies=[Depends(HTTPBearer())])
async def create_card_user(header_param: Request, req: CreateCardUsers, db: Session = Depends(get_db)):
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    
    result = await crud.create_card_user(db=db, req=req, userID=user_id)
    if not result:
        return Returns.NOT_INSERTED
    
    user = await crud.read_current_user(db=db, user_id=user_id)
    if not user:
        return Returns.USER_NOT_FOUND
    
    new_dict = {
        "title"     : "Täze kart sargyt edildi / Заказана новая карточка",
        "message"   : f"{user['fullname']} müşderi täze kart sargyt etdi / Пользователь {user['fullname']} заказал новую карточку"
    }
    
    new_inbox = await crud.create_inbox_card(db=db, req=new_dict)
    if not new_inbox:
        return Returns.NOT_INSERTED
    else:
        return new_inbox
    
    # inbox_id = await crud.read_inbox_by_title_and_message(db=db, title=new_dict["title"], message=new_dict["message"])
    # if not inbox_id:
    #     return Returns.NULL
    
    # new_send_user = await crud.create_send_user(db=db, userID=user_id, inboxID=inbox_id["id"])
    # if not new_send_user:
    #     return Returns.NOT_INSERTED
    
    # await send_to_topic(topic="new_card", title=new_dict["title"], body=new_dict["message"])
    
    # if new_send_user:
    #     return Returns.INSERTED
    # else:
    #     return Returns.NOT_INSERTED