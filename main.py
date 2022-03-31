from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
import random
import crud
from tokens import Returns
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
from routers import users_router
from models import PhoneVerify
import uvicorn
import socketio


app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socketio_app = socketio.ASGIApp(sio, app)

@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.on('onMessage')
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit('onMessage', 'hi ' + data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)



@authentication_router.post("/phone-verification")
async def phone_verification(req: PhoneVerify, db: Session = Depends(get_db)):
    generated_code = random.randint(1000, 9999)
    result = await crud.create_number_socket(db=db, number=req, code=generated_code)
    data = {
        "phone_number" : req.phone_number,
        "code"         : generated_code
    }

    await sio.emit("onMessage", data)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED


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
app.include_router(users_router            , tags=["Users"])
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

    
       
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)