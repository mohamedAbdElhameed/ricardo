from django.shortcuts import render

# Create your views here.
from news.models import Post
from products.models import Category
from userprofile.forms import SignUpForm, LoginForm


def news_view(request):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-modified_at')
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'news/news.html', context)
