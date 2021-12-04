from fastapi import APIRouter, Depends, Request
from models import Users
from sqlalchemy.orm import Session
from db import get_db

authentication_router = APIRouter()

@authentication_router.get("/get-user")
def authentication(db: Session = Depends(get_db)):
    result = db.query(Users).all()