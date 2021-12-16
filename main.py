from fastapi import FastAPI
from db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_router
from routers import interest_router
from routers import home_router
from routers import profile_router
from routers import category_router
from routers import answers_router
from routers import card_router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=False)