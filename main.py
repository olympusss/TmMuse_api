from fastapi import FastAPI
from db import Base, engine
from routers import authentication_router
from routers import interest_router
from routers import home_router

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(authentication_router   , tags=["Authentication"])
app.include_router(interest_router         , tags=["Interest"])
app.include_router(home_router             , tags=["Home"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=False)