from fastapi import FastAPI
from db import Base, engine
from routers import authentication_router

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(authentication_router, tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=False)