from sqlalchemy import Column, Integer, Float, String, Boolean
from backend.db import Base
from models import *


class Art(Base):
    __tablename__ = 'arts'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    cost = Column(Float)
    description = Column(String)
    age_limited = Column(Boolean)
    slug = Column(String, unique=True, index=True)


# from sqlalchemy.schema import CreateTable
# print(CreateTable(Art.__table__))
