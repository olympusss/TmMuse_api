from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import crud
from tokens import Returns

home_router = APIRouter()

@home_router.get("/get-home")
async def get_home(page: int, user_id: int = None, db: Session = Depends(get_db)):
    result = {}
    if page == 1:
        result["banners"] = await crud.read_banner(db=db)
        result["new_movies"] = await crud.read_movies(db=db)
        result["promotions"] = await crud.read_promotions(db=db, page=page)
        result["ads"] = await crud.read_ads(db=db)
        result["popup"] = await crud.read_popup(db=db)
        result["card_user"] = await crud.read_card_user_by_user_id(db=db, user_id=user_id)
    else:
        result["promotions"] = await crud.read_promotions(db=db, page=page)
    db.close()
    if result:
        await crud.create_app_visitors(db=db)
        db.close()
        return Returns.object(result)
    else:
        return Returns.NULL
    