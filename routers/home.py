from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import crud
from tokens import Returns

home_router = APIRouter()

@home_router.get("/get-home")
def get_home(db: Session = Depends(get_db)):
    get_banner    = crud.read_banner(db=db)
    get_movie     = crud.read_movies(db=db)
    get_promotion = crud.read_promotions(db=db)
    get_ads       = crud.read_ads(db=db)
    newList = []
    for elem in get_ads:
        get_categories = crud.read_categories_by_ads(db=db, ads_id=elem.id)
        text = []
        for elems in get_categories:
            text.append(elems)
        elem = dict(elem)
        elem["categories"] = text
        newList.append(elem)
    get_ads = newList
    result = {}
    result["banners"] = get_banner
    result["new_movies"] = get_movie
    result["promotions"] = get_promotion
    result["ads"] = get_ads
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL