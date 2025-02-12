from lib2to3.fixes.fix_next import bind_warning
# from sqlmodel import Field,Session,SQLModel,create_engine,select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL="sqlite:///./books.db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}
)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()