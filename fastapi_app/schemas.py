from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date


class CreateBuyer(BaseModel):
    username: str
    password: str
    balance: Decimal = Field(max_digits=11, decimal_places=2, default=0.00)
    age: int


class UpdateBuyer(BaseModel):
    username: str
    password: str
    balance: Decimal = Field(max_digits=11, decimal_places=2)
    age: int


class CreateArt(BaseModel):
    title: str
    cost: Decimal = Field(max_digits=11, decimal_places=2)
    description: str
    age_limited: bool


class UpdateArt(BaseModel):
    title: str
    cost: Decimal = Field(max_digits=11, decimal_places=2)
    description: str
    age_limited: bool


class CreateNews(BaseModel):
    title: str
    content: str
    date: date


class UpdateNews(BaseModel):
    title: str
    content: str
    date: date
