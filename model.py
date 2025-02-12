from operator import index

from pydantic.plugin import StringInput
from sqlalchemy import Column
from sqlmodel import Field,SQLModel,INTEGER,String
from database import Base

class Books(Base):
    __tablename__="books"

    id=Column(INTEGER,primary_key=True,index=True)
    title=String
    author=String
    description=String
    rating=Column(INTEGER)