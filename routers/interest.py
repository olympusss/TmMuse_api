from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from models import AddUserInterest
import crud
from tokens import Returns, check_token, token

interest_router = APIRouter()

@interest_router.get("/get-interest")
def get_interest(db: Session = Depends(get_db)):
    get_interest = crud.read_interests(db=db)
    newList = []
    for elem in get_interest:
        elem = dict(elem)
        get_interest_items = crud.read_interest_items_by_interest_id(db=db, interest_id=elem["id"])
        elem["item"] = get_interest_items
        newList.append(elem)
    return Returns.object(newList)

@interest_router.post("/add-user-interest")
def add_user_interest(header_param: Request, req: AddUserInterest, db: Session = Depends(get_db)):
    token = check_token(header_param=header_param)
    # delete_user_interest = crud.delete_user_interest(db=db, user_id=req.user_id)
    # if not delete_user_interest:
    #     return Returns.NOT_DELETED
    if not token:
        return Returns.TOKEN_NOT_FOUND
    for elem in req.items_id:
        result = crud.create_user_interest_item(db=db, user_id=req.user_id, item_id=elem)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED