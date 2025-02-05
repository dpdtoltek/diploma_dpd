from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *
from django.core.paginator import Paginator

# Create your views here.
info = {}

users = Buyer.objects.all()


def index(request):
    title = 'Art shop'
    header = 'Главная страница'
    context = {"title": title,
               "header": header
               }
    return render(request, 'index.html', context)


def arts(request):
    title = 'Магазин'
    header = 'Артобъекты'
    arts_all = Art.objects.all()
    context = {"title": title,
               "header": header,
               "arts_all": arts_all
               }
    return render(request, 'arts.html', context)


def cart(request):
    title = 'Корзина'
    header = 'Корзина'
    message = 'Извините, Ваша корзина пуста'
    context = {"title": title,
               "header": header,
               "message": message
               }
    return render(request, 'cart.html', context)


def sign_up_by_django(request):
    usernames = [user.username for user in users]
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            if password == repeat_password and username not in usernames:
                new_user = Buyer.objects.create(username=f'{username}', password=f'{password}', age=f'{age}')
                new_user.save()
                return HttpResponse(f'Приветствуем, {username}!')
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
                return render(request, 'registration_page.html', context=info)
            elif username in usernames:
                info['error'] = 'Пользователь уже существует'
                return render(request, 'registration_page.html', context=info)
        else:
            info['error'] = 'Некорректный ввод данных'
            return render(request, 'registration_page.html', context=info)
    else:
        form = UserRegister()
    return render(request, 'registration_page.html', {'form': form})


def news(request):
    news = News.objects.all().order_by('-date')
    paginator = Paginator(news, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj})
