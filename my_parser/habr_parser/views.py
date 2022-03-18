from django.shortcuts import render
from rest_framework import generics
from .models import Article
from .serializers import *


class ArticleAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
