from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud

constant_router = APIRouter()

@constant_router.get("/get-constant")
async def get_constant(type: str, db: Session = Depends(get_db)):
    result = await crud.read_constant_by_type(db=db, type=type)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL