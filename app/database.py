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

# Перевірка наявності даних для підключення
if not all([postgres_name, postgres_password, postgres_db_name]):
    raise ValueError("Потрібно задати всі змінні середовища для підключення до бази даних.")

engine = create_engine(POSTGRES_DATABASE_URL) # створюю енджін
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # створюю сесію

Base = declarative_base() # базовий клас для можделей


# Функція для отримання сесії бази даних (піде в dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
