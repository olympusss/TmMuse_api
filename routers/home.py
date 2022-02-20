from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import crud
from tokens import Returns

home_router = APIRouter()

@home_router.get("/get-home")
async def get_home(page: int, db: Session = Depends(get_db)):
    result = {}
    if page == 1:
        result["banners"] = await crud.read_banner(db=db)
        result["new_movies"] = await crud.read_movies(db=db)
        result["promotions"] = await crud.read_promotions(db=db, page=page)
        result["ads"] = await crud.read_ads(db=db)
        result["popup"] = await crud.read_popup(db=db)
    else:
        result["promotions"] = crud.read_promotions(db=db, page=page)
    if result:
        await crud.create_app_visitors(db=db)
        return Returns.object(result)
    else:
        return Returns.NULL
    