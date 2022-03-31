from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import AddUserInterest
import crud
from tokens import Returns, check_token

interest_router = APIRouter()

@interest_router.get("/get-interest", dependencies=[Depends(HTTPBearer())])
async def get_interest(db: Session = Depends(get_db)):
    get_interest = await crud.read_interests(db=db)
    newList = []
    for elem in get_interest:
        elem = dict(elem)
        get_interest_items = await crud.read_interest_items_by_interest_id(db=db, interest_id=elem["id"])
        elem["item"] = get_interest_items
        newList.append(elem)
    return Returns.object(newList)

@interest_router.post("/add-user-interest", dependencies=[Depends(HTTPBearer())])
async def add_user_interest(header_param: Request, req: AddUserInterest, db: Session = Depends(get_db)):
    token = await check_token(header_param=header_param)
    if not token:
        return Returns.TOKEN_NOT_FOUND
    for elem in req.items_id:
        result = await crud.create_user_interest_item(db=db, user_id=req.user_id, item_id=elem)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@interest_router.get("/get-user-interests", dependencies=[Depends(HTTPBearer())])
async def get_user_interest(header_param: Request, db: Session = Depends(get_db)):
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    result = await crud.read_interest_items_by_user_id(db=db, user_id=user_id)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    