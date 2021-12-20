from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import Search
import crud

search_router = APIRouter()

@search_router.post("/search-profile")
def search_profile(req: Search, db: Session = Depends(get_db)):
    result = crud.search_profile_by_like(db=db, req=req)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL