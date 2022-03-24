from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import Search
import crud

search_router = APIRouter()

@search_router.post("/search-profile")
async def search_profile(req: Search, db: Session = Depends(get_db)):
    result_history = await crud.create_search_history(db=db, txt=req.text)
    if not result_history:
        return Returns.NULL
    result = await crud.search_profile_by_like(db=db, req=req, page=req.page, limit=req.limit)
    if not result:
        return Returns.NULL
    else:
        return Returns.object(result)
    
@search_router.get("/get-search-history")
async def get_search_history(db: Session = Depends(get_db)):
    result = await crud.read_search_history(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    