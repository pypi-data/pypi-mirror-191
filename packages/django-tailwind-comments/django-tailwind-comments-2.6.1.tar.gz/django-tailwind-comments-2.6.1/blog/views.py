from blog.models import Article
from django.shortcuts import render, get_object_or_404


def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'detail.html', {'article': article})
