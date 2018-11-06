from django.shortcuts import render

# Create your views here.
from products.models import Category


def sub_categories(request, pk):
    category = Category.objects.get(id=pk)
    categories = Category.objects.all()
    context = {
        "category": category,
        "categories": categories
    }
    return render(request, 'products/sub_categories.html', context)