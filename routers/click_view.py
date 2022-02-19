from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import ViewCountSchema, LikeDislikeSchema
import crud


view_count_router = APIRouter()

@view_count_router.post("/add-view-count", dependencies=[Depends(HTTPBearer())])
async def add_view_count(view: ViewCountSchema, db: Session = Depends(get_db)):
    result = await crud.create_view_count(db=db, view=view)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@view_count_router.post("/add-click-count", dependencies=[Depends(HTTPBearer())])
async def add_click_count(click: ViewCountSchema, db: Session = Depends(get_db)):
    result = await crud.create_click_count(db=db, click=click)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@view_count_router.post("/add-like-dislike", dependencies=[Depends(get_db)])
async def add_like_dislike(like: LikeDislikeSchema, db: Session = Depends(get_db)):
    result = await crud.create_like_dislike(db=db, like=like)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED