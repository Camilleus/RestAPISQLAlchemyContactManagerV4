from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def init_db():
    """
    Inicjuje bazę danych poprzez tworzenie wszystkich tabel zdefiniowanych w bazie.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Uzyskuje sesję bazy danych, która jest używana przez zasoby w aplikacji.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
