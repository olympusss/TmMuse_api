from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_router
from routers import interest_router
from routers import home_router
from routers import profile_router
from routers import category_router
from routers import answers_router
from routers import card_router
from routers import constant_router
from routers import search_router
from routers import ticket_router
from routers import view_count_router
import uvicorn
from socket_io import socket_app


app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

Base.metadata.create_all(engine)
app.include_router(authentication_router   , tags=["Authentication"])
app.include_router(interest_router         , tags=["Interest"])
app.include_router(home_router             , tags=["Home"])
app.include_router(profile_router          , tags=["Profile"])
app.include_router(category_router         , tags=["Category"])
app.include_router(answers_router          , tags=["Answer"])
app.include_router(card_router             , tags=["Card"])
app.include_router(constant_router         , tags=["Constant"])
app.include_router(search_router           , tags=["Search"])
app.include_router(ticket_router           , tags=["Ticket"])
app.include_router(view_count_router       , tags=["Click_View"])

    
app.mount("/", socket_app)
       
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)