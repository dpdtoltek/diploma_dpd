from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('username', 'balance', 'age')
    list_filter = ('balance', 'age')
    search_fields = ('username',)
    list_per_page = 30

    readonly_fields = ('balance',)


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'description')
    list_filter = ('title',)
    search_fields = ('title', 'cost')
    list_per_page = 20


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')
    list_filter = ('title', 'date')
    search_fields = ('title',)
    list_per_page = 30
