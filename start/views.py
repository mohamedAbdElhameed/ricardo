from django.shortcuts import render
# Create your views here.
from products.models import Category

from start.models import StartDetail


def index(request):
    categories = Category.objects.all()
    start = StartDetail.objects.last()

    context = {
        'categories': categories,
        'start': start,
    }
    return render(request, 'start/index.html', context)
