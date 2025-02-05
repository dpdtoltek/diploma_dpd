from sqlalchemy import Column, Integer, String, DATE
from backend.db import Base
from models import *


class News(Base):
    __tablename__ = 'news'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    date = Column(DATE)
    slug = Column(String, unique=True, index=True)


# from sqlalchemy.schema import CreateTable
# print(CreateTable(News.__table__))
