from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
import crud
from tokens import Returns

home_router = APIRouter()

@home_router.get("/get-home")
def get_home(db: Session = Depends(get_db)):
    get_banner = crud.read_banner(db=db)
    get_movie  = crud.read_movies(db=db)
    get_promotion = crud.read_promotions(db=db)
    result = {}
    result["banners"] = get_banner
    result["new_movies"] = get_movie
    result["promotions"] = get_promotion
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL