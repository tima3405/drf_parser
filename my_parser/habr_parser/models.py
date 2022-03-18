from django.db import models


class Article(models.Model):
    author = models.CharField(
        verbose_name='Автор Статьи',
        max_length=255)
    title = models.CharField(
        verbose_name='Заголовок статьи',
        max_length=255)
    url = models.URLField(
        verbose_name='url статьи',
        default='qwe')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title



