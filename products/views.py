from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from products.models import Category, SubCategory, Product, Cart
from userprofile.forms import LoginForm, SignUpForm
from userprofile.models import Buyer



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
    user = request.user
    buyer = []
    in_cart = False
    quantity = 0
    if user.is_authenticated:
        buyer = Buyer.objects.get(user=user)
        cart = Cart.objects.filter(buyer=buyer, product=product)
        if cart:
            in_cart = True
            quantity = cart[0].quantity

    subcategory = product.sub_category
    category = subcategory.category
    categories = Category.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    if product.seller.number_of_rates == 0:
        rate = 0
    else:
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
        "in_cart": in_cart,
        "quantity": quantity,
        "range": range(1, int(rate//1+1)),
        "range2": range(1, int(5-(rate//1+1))+flag)
    }

    return render(request, 'products/product.html', context)


def cart_view(request):
    user = request.user
    carts = Cart.objects.filter(buyer=Buyer.objects.get(user=user))
    categories = Category.objects.all()

    context = {
        "categories": categories,
        'carts': carts,
    }
    return render(request, 'products/cart.html', context)


def delete_cart_element(request, pk):
    cart_element = Cart.objects.get(pk=pk)
    cart_element.delete()
    if not cart_element:
        return HttpResponse("False")
    else:
        return HttpResponse("True")


def add_to_cart(request, product, quantity):
    user = request.user
    buyer = Buyer.objects.get(user=user)

    cart = Cart.objects.filter(buyer=buyer, product=Product.objects.get(pk=product))

    if len(cart):
        cart[0].quantity = quantity
        cart[0].save()
        return HttpResponse(quantity)
    else:
        Cart.objects.create(buyer=buyer, quantity=quantity, product=Product.objects.get(pk=product))
        return HttpResponse(quantity)
