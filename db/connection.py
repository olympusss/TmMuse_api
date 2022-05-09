from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbtype   = "postgresql"
user     = "postgres"
password = "183139"
host     = "127.0.0.1"
port     = "5432"
db       = "tmmuse"

SQLALCHEMY_DATABASE_URL = f"{ dbtype }://{ user }:{ password }@{ host }:{ port }/{ db }"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()