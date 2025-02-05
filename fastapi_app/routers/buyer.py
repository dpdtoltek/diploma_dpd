from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Buyer
from schemas import CreateBuyer, UpdateBuyer
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/buyer', tags=['buyer'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def all_buyers(db: DbSession):
    users = db.scalars(select(Buyer)).all()
    return users


@router.get('/buyer_id')
async def buyer_by_id(buyer_id, db: DbSession):
    buyer = db.scalar(select(Buyer).where(Buyer.id == buyer_id))
    if buyer is not None:
        return buyer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Buyer was not found')


@router.post('/create')
async def create_buyer(db: DbSession, create_buyer: CreateBuyer):
    db.execute(insert(Buyer).values(username=create_buyer.username,
                                    password=create_buyer.password,
                                    balance=create_buyer.balance,
                                    age=create_buyer.age,
                                    slug=slugify(create_buyer.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_buyer(buyer_id: int, db: DbSession, update_buyer: UpdateBuyer):
    buyer = db.scalar(select(Buyer).where(Buyer.id == buyer_id))
    if buyer is not None:
        db.execute(update(Buyer).where(Buyer.id == buyer_id).values(
            username=update_buyer.username,
            password=update_buyer.password,
            balance=update_buyer.balance,
            age=update_buyer.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Buyer update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Buyer was not found')


@router.delete('/delete')
async def delete_buyer(buyer_id: int, db: DbSession):
    buyer = db.scalar(select(Buyer).where(Buyer.id == buyer_id))
    if buyer is not None:
        db.execute(delete(Buyer).where(Buyer.id == buyer_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Buyer delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Buyer was not found')
