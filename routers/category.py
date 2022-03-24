from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud

category_router = APIRouter()

@category_router.get("/get-category")
async def get_category(db: Session = Depends(get_db)):
    get_category = await crud.read_category(db=db)
    if get_category:
        return Returns.object(get_category)
    else:
        return Returns.NULL