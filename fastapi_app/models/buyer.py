from sqlalchemy import Column, Integer, String, Float
from backend.db import Base
from models import *


class Buyer(Base):
    __tablename__ = 'buyers'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Float)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)


# from sqlalchemy.schema import CreateTable
# print(CreateTable(Buyer.__table__))
