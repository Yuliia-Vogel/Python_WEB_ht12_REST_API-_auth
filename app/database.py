import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv() # завантажуються дані з файлу .env 

postgres_name = os.getenv("POSTGRESQL_USER")
postgres_password = os.getenv("POSTGRESQL_PASS")
postgres_db_name = os.getenv("POSTGRESQL_DB_NAME")

POSTGRES_DATABASE_URL = f"postgresql://{postgres_name}:{postgres_password}@localhost/{postgres_db_name}"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # жля перевірки, чи все ок з підключенням до бази постгрес

engine = create_engine(POSTGRES_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): # піде в dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
