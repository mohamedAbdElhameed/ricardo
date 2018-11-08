from django.shortcuts import render

# Create your views here.
from news.models import Post
from products.models import Category


def news_view(request):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-modified_at')
    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'news/news.html', context)
