from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import crud
from tokens import Returns

home_router = APIRouter()

@home_router.get("/get-home")
def get_home(page: int, db: Session = Depends(get_db)):
    result = {}
    if page == 1:
        result["banners"] = crud.read_banner(db=db)
        result["new_movies"] = crud.read_movies(db=db)
        result["promotions"] = crud.read_promotions(db=db, page=page)
        result["ads"] = crud.read_ads(db=db)
    else:
        result["promotions"] = crud.read_promotions(db=db, page=page)
        
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    