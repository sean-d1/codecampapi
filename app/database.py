from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg.connect(
#         "host=localhost dbname=fastapi user=postgres password=password",
#         row_factory=dict_row,
#     )
#     cursor = conn.cursor()
#     print("Database connection was successful")
# except Exception as error:
#     print("Connection to db failed")
#     print("Error: ", error)
