from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import Ticket_insert_schema
from tokens import Returns
import crud

ticket_router = APIRouter()

@ticket_router.post("/add-ticket", dependencies=[Depends(HTTPBearer())])
async def add_ticket(ticket: Ticket_insert_schema, db: Session = Depends(get_db)):
    result = await crud.create_ticket(db=db, ticket=ticket)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@ticket_router.get("/get-current-ticket", dependencies=[Depends(HTTPBearer())])
async def get_current_ticket(user_id: int, db: Session = Depends(get_db)):
    result = await crud.read_current_ticket(db=db, user_id=user_id)
    if result:
        return Returns.object(result)
    else:
        return Returns.TICKET_NOT_FOUND