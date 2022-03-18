from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'url')


admin.site.register(Article, ArticleAdmin)


