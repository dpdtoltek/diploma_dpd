from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import News
from schemas import CreateNews, UpdateNews
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/news', tags=['news'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def all_news(db: DbSession):
    news = db.scalars(select(News)).all()
    return news


@router.get('/news_id')
async def news_by_id(news_id, db: DbSession):
    news = db.scalar(select(News).where(News.id == news_id))
    if news is not None:
        return news
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News was not found')


@router.post('/create')
async def create_news(db: DbSession, create_news: CreateNews):
    db.execute(insert(News).values(title=create_news.title,
                                   content=create_news.content,
                                   date=create_news.date,
                                   slug=slugify(create_news.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_news(news_id: int, db: DbSession, update_news: UpdateNews):
    news = db.scalar(select(News).where(News.id == news_id))
    if news is not None:
        db.execute(update(News).where(News.id == news_id).values(
            title=update_news.title,
            content=update_news.content,
            date=update_news.date,
            slug=slugify(update_news.title)))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'News update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News was not found')


@router.delete('/delete')
async def delete_buyer(news_id: int, db: DbSession):
    news = db.scalar(select(News).where(News.id == news_id))
    if news is not None:
        db.execute(delete(News).where(News.id == news_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'News delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News was not found')
