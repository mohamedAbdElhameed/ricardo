from django.shortcuts import render
# Create your views here.
from products.models import Category


def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'start/base.html', context)