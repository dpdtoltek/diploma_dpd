from fastapi import FastAPI
from routers import art, buyer, news, pages
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(buyer.router)
app.include_router(art.router)
app.include_router(news.router)
app.include_router(pages.router)


# @app.get('/')
# async def welcome():
#     # return {'message': 'Главная страница'}
#     html_content = "<h2>Добро пожаловать!</h2>"
#     return HTMLResponse(content=html_content)
