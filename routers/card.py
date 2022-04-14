from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud
from models import CreateCardUsers
# from redis_handler import get_routes_from_cache, set_routes_to_cache

card_router = APIRouter()

    
@card_router.get("/get-card-promotion")
async def get_card_promotion(limit: int, page: int, db: Session = Depends(get_db)):
    # result = get_routes_from_cache(key='card')
    # if result:
    #     return Returns.object(result)
    
    result = await crud.read_profile_card_promotion(db=db, limit=limit, page=page)
    # set_routes_to_cache(key='card', value=result)
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
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED