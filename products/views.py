from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from products.models import Category, SubCategory, Product
from userprofile.forms import LoginForm, SignUpForm


def sub_categories(request, pk):
    category = Category.objects.get(id=pk)
    categories = Category.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        "category": category,
        "categories": categories
    }
    return render(request, 'products/sub_categories.html', context)


def products_view(request, pk):
    categories = Category.objects.all()
    subcategory = SubCategory.objects.filter(id=pk)[0]
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    products = subcategory.subcategory_products.all()
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
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
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    rate = product.seller.rate / product.seller.number_of_rates
    if rate % 1 == 0:
        flag = 2
    else:
        flag = 1
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        "product": product,
        "subcategory": subcategory,
        "category": category,
        "categories": categories,
        "rate": (rate//1),
        "remainder": rate % 1,
        "the_rate": rate,
        "range": range(1, int(rate//1+1)),
        "range2": range(1, int(5-(rate//1+1))+flag)
    }

    return render(request, 'products/product.html', context)