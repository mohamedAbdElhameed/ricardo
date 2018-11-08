from django.shortcuts import render

# Create your views here.
from products.models import Category
from stories.models import ArtisanMaster, Tale


def masters_view(request):
    masters = ArtisanMaster.objects.all()
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'masters': masters,
    }

    return render(request, 'stories/artisan_master.html', context)


def tales_view(request):
    tales = Tale.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'tales': tales,
    }

    return render(request, 'stories/tales.html', context)
