from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from products.models import Category, SubCategory, Product


def sub_categories(request, pk):
    category = Category.objects.get(id=pk)
    categories = Category.objects.all()
    context = {
        "category": category,
        "categories": categories
    }
    return render(request, 'products/sub_categories.html', context)


def products_view(request, pk):
    categories = Category.objects.all()
    subcategory = SubCategory.objects.filter(id=pk)[0]

    products = subcategory.subcategory_products.all()
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        "category": subcategory.category,
        "subcategory": subcategory,
        "categories": categories,
        'products': products
    }

    return render(request, 'products/products.html', context)


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    subcategory = product.sub_category
    category = subcategory.category
    categories = Category.objects.all()

    context = {
        "product": product,
        "subcategory": subcategory,
        "category": category,
        "categories": categories,
    }

    return render(request, 'products/product.html', context)