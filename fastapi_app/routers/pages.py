from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from .art import all_arts
from .news import all_news
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from typing import Annotated
from backend.db_depends import get_db
from models import Buyer
from slugify import slugify


router = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='templates')
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def registration_page_html(request: Request):
    return templates.TemplateResponse(name='registration_page.html', context={'request': request})


@router.post('/')
async def sign_up(request: Request, db: DbSession,
                  username: str = Form(min_length=2, max_length=30),
                  password: str = Form(min_length=8, max_length=30),
                  repeat_password: str = Form(min_length=8, max_length=20),
                  age: int = Form()):
    users = db.scalars(select(Buyer)).all()
    usernames = [user.username for user in users]
    if request.method == 'POST':
        if password == repeat_password and username not in usernames and age > 13:
            db.execute(insert(Buyer).values(username=username,
                                            password=password,
                                            age=age,
                                            slug=slugify(username)))
            db.commit()
            info = f'Приветствуем, {username}!'
            return templates.TemplateResponse(name='index.html',
                                              context={'request': request, 'content': info})
        elif password != repeat_password:
            info = 'Пароли не совпадают'
            return templates.TemplateResponse(name='registration_page.html',
                                              context={'request': request, 'content': info})
        elif age < 14:
            info = 'Вы должны быть старше 14'
            return templates.TemplateResponse(name='registration_page.html',
                                              context={'request': request, 'content': info})
        elif username in usernames:
            info = 'Пользователь уже существует'
            return templates.TemplateResponse(name='registration_page.html',
                                              context={'request': request, 'content': info})
    else:
        return templates.TemplateResponse(name='registration_page.html', context={'request': request})


@router.get('/index')
async def index_html(request: Request):
    info = 'Добро пожаловать!'
    return templates.TemplateResponse(name='index.html', context={'request': request, 'content': info})


@router.get('/arts')
async def arts_html(request: Request, arts=Depends(all_arts)):
    return templates.TemplateResponse(name='arts.html', context={'request': request, 'arts': arts})


@router.get('/cart')
async def cart_html(request: Request):
    info = 'Извините, Ваша корзина пуста'
    return templates.TemplateResponse(name='cart.html', context={'request': request, 'content': info})


@router.get('/news')
async def news_html(request: Request, news_all=Depends(all_news)):
    return templates.TemplateResponse(name='news.html', context={'request': request, 'news_all': news_all})
