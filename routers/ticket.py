from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import Ticket_insert_schema, TicketStatusUpdateSchema
from cloud_messaging import send_to_token
from tokens import Returns
import crud

ticket_router = APIRouter()

@ticket_router.post("/add-ticket", dependencies=[Depends(HTTPBearer())])
async def add_ticket(ticket: Ticket_insert_schema, db: Session = Depends(get_db)):
    result = await crud.create_ticket(db=db, ticket=ticket)
    get_notif_token = await crud.read_admin_notif_token_by_cinema_id(db=db, cinema_id=ticket.cinema_id)
    if not get_notif_token:
        if result:
            return Returns.id(result)
        else:
            return Returns.NOT_INSERTED
    await send_to_token(
        token=get_notif_token.notif_token,
        ticket_id=f"{result}",
        date=ticket.movie_date,
        time=ticket.movie_time,
        count_ticket=ticket.ticket_count
    )
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
    
    
@ticket_router.put("/ticket-status-update", dependencies=[Depends(HTTPBearer())])
async def ticket_status_update(id: int, ticket: TicketStatusUpdateSchema, db: Session = Depends(get_db)):
    result = await crud.update_ticket_status(db=db, id=id, ticket=ticket)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED