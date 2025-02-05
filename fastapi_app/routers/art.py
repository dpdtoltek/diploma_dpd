from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Art
from schemas import CreateArt, UpdateArt
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/art', tags=['art'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def all_arts(db: DbSession):
    arts = db.scalars(select(Art)).all()
    return arts


@router.get('/art_id')
async def art_by_id(art_id, db: DbSession):
    art = db.scalar(select(Art).where(Art.id == art_id))
    if art is not None:
        return art
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Art was not found')


@router.post('/create')
async def create_art(db: DbSession, create_art: CreateArt):
    db.execute(insert(Art).values(title=create_art.title,
                                  cost=create_art.cost,
                                  description=create_art.description,
                                  age_limited=create_art.age_limited,
                                  slug=slugify(create_art.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_art(art_id: int, db: DbSession, update_art: UpdateArt):
    art = db.scalar(select(Art).where(Art.id == art_id))
    if art is not None:
        db.execute(update(Art).where(Art.id == art_id).values(
            title=update_art.title,
            cost=update_art.cost,
            description=update_art.description,
            age_limited=update_art.age_limited))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Art update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Art was not found')


@router.delete('/delete')
async def delete_art(art_id: int, db: DbSession):
    art = db.scalar(select(Art).where(Art.id == art_id))
    if art is not None:
        db.execute(delete(Art).where(Art.id == art_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Art delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Art was not found')
