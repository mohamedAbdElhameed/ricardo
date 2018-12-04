import hashlib
from collections import OrderedDict

from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt

from products.models import Category, SubCategory, Product, Cart, Order, OrderItem
from ricardo import settings
from start.views import index
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
    products = subcategory.subcategory_products.filter(active=True)
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
    if not product.active:
        return HttpResponse("<P>this product is not active now<P>")
    return render(request, 'products/product.html', context)


def cart_view(request):
    user = request.user
    carts = Cart.objects.filter(buyer=Buyer.objects.get(user=user))
    small_carts = []
    sellers = []

    for item in carts:
        if item.product.seller not in sellers:
            sellers.append(item.product.seller)

    for seller in sellers:
        apikey = seller.APIKEY or '4Vj8eK4rloUd272L48hsrarnUA'
        merchant_id = seller.merchant_id or '508029'
        date = str(datetime.now())
        reference_code = str(user.buyer.id) + str(seller.name) + date
        products = Cart.objects.filter(buyer=Buyer.objects.get(user=user), product__seller=seller)
        amount = 0
        number_of_products = 0
        for product in products:
            amount += product.product.price * product.quantity
            number_of_products += product.quantity
        currency = 'COP'
        tax = str(round(amount / 100 * 17, 2))
        base = str(round(amount / 100 * 83, 2))
        signature = hashlib.md5((apikey + "~" + merchant_id + "~" + reference_code + "~" + str(amount) + "~" + currency).encode('utf-8')).hexdigest()
        small_carts.append({
            'seller': seller,
            'products': products,
            'APIKEY': apikey,
            'merchant_id': merchant_id,
            'amount': str(amount),
            'signature': signature,
            'reference_code': reference_code,
            'tax': tax,
            'base': base,
            'number_of_products': number_of_products,
        })
    buyer = user.buyer
    currency = 'COP'
    if settings.DEBUG:
        action_url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/"
        account_id = '512321'
        test = '1'
        host = 'http://ricardoooo123123123.pythonanywhere.com/'
    else:
        action_url = "https://checkout.payulatam.com/ppp-web-gateway-payu"
        account_id = '512321'
        test = '0'
        host = 'https://peaku.co/'

    response_url = host + 'products/response/'
    confirmation_url = host + 'products/payment_confirmation/'
    description = "this is test for buying "

    categories = Category.objects.all()
    number_of_products = carts.aggregate(Sum('quantity'))['quantity__sum']
    total_price = 0
    for product in carts:
        total_price += product.quantity * product.product.price

    context = {
        "categories": categories,
        'carts': carts,
        'small_carts': small_carts,
        'number_of_products': number_of_products,
        "total_price": total_price,
        "action_url": action_url,
        "account_id": account_id,
        "currency": currency,
        "test": test,    # to test credit card
        "description": description,
        "buyer_name": buyer.user.username,
        "buyer_email": buyer.user.email,
        "response_url": response_url,
        "confirmation_url": confirmation_url,
    }
    return render(request, 'products/cart.html', context)


def total_price_and_items(request):
    user = request.user
    carts = Cart.objects.filter(buyer=Buyer.objects.get(user=user))
    number_of_products = carts.aggregate(Sum('quantity'))['quantity__sum']
    total_price = 0
    for product in carts:
        total_price += product.quantity * product.product.price

    return JsonResponse({
        'total_price': total_price,
        'number_of_products': number_of_products
    })


def delete_cart_element(request, pk):
    cart_element = Cart.objects.get(pk=pk)
    cart_element.delete()
    nums = total_price_and_items(request)
    if not cart_element:
        return HttpResponse("False")
    else:
        return nums


def add_to_cart(request, product, quantity):
    user = request.user
    buyer = Buyer.objects.get(user=user)

    cart = Cart.objects.filter(buyer=buyer, product=Product.objects.get(pk=product))

    if len(cart):
        cart[0].quantity = quantity
        cart[0].save()
        return total_price_and_items(request)
    else:
        Cart.objects.create(buyer=buyer, quantity=quantity, product=Product.objects.get(pk=product))
        return HttpResponse(quantity)


@csrf_exempt
def payment_confirmation(request):
    # This is Payu transaction approved code, only for confirmation page, not global variable
    PAYU_APPROVED_CODE = '4'
    if settings.DEBUG:
        buyer = Buyer.objects.get(user=request.POST.get('extra1'))
        extra2 = request.POST.get('extra2')
        transaction_final_state = PAYU_APPROVED_CODE
        sign = '1234'
        create_signature = '1234'
    else:
        transaction_final_state = request.POST.get('state_pol')
        response_code_pol = request.POST.get('response_code_pol')
        payment_method_type = request.POST.get('payment_method_type')
        currency = request.POST.get('currency')
        payment_method_id = request.POST.get('payment_method_id')
        response_message_pol = request.POST.get('response_message_pol')
        apikey = '4Vj8eK4rloUd272L48hsrarnUA'
        sign = request.POST.get('sign')
        merchant_id = request.POST.get('merchant_id')
        reference_sale = request.POST.get('reference_sale')
        amount = request.POST.get('value')

        # Decimal validation, Payu requirement
        if amount[-1] == 0:
            amount = round(float(amount), 1)

        # Important validation to check the integrity of the data
        create_signature = hashlib.md5((apikey + "~" + merchant_id + "~" + reference_sale + "~" + str(amount) + "." + "~" + currency + "~" + transaction_final_state).encode('utf-8')).hexdigest()

    if transaction_final_state == PAYU_APPROVED_CODE:
        carts = Cart.objects.filter(buyer=buyer, product__seller=extra2)

        if create_signature == sign:
            message = '<h1>0K</h1>'
            order = Order.objects.create(buyer=buyer, paid=True)
            for cart in carts:
                OrderItem.objects.create(order=order, product=cart.product, quantity=cart.quantity)
                cart.delete()
        else:
            message = '<h1>Sign is wrong check why!!!</h1>'
        return HttpResponse(message, status=200)
    else:
        message = '<h1>Something is wrong</h1>' + transaction_final_state
        return HttpResponse(message, status=400)