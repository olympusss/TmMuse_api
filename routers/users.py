from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud

users_router = APIRouter()

@users_router.get("/get-users")
async def get_users(db: Session = Depends(get_db)):
    result = crud.read_all_users(db)
    if result:
        return Returns.object(result)
    else: 
        return Returns.NULL
    
    
@users_router.get("/get-user-info", dependencies=[Depends(HTTPBearer())])
async def get_user_info(header_param: Request, db: Session = Depends(get_db)):
    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)
    if not user_id:
        return Returns.USER_NOT_FOUND
    result = crud.read_user_info(db=db, user_id=user_id)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL