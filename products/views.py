import hashlib

from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime

from products.models import Category, SubCategory, Product, Cart, Order, OrderItem
from ricardo import settings
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
    buyer = user.buyer
    currency = 'COP'
    date = str(datetime.now())
    if settings.DEBUG:
        action_url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/"
        apikey = '4Vj8eK4rloUd272L48hsrarnUA'
        merchant_id = '508029'
        account_id = '512321'
        test = '1'
        host = 'http://ricardoooo123123123.pythonanywhere.com/'
    # else:
    #     action_url = "https://checkout.payulatam.com/ppp-web-gateway-payu"
    #     apikey = config('payu_api_key')
    #     merchant_id = config('merchant_id')
    #     account_id = config('account_id')
    #     test = '0'
    #     host = 'https://peaku.co/'

    response_url = host + 'resumen/'
    confirmation_url = host + 'products/payment_confirmation/'
    reference_code = str(buyer.id) + date
    amount = 20000

    signature = hashlib.md5((apikey + "~" + merchant_id + "~" + reference_code + "~" + str(amount) + "~" + currency).encode('utf-8')).hexdigest()
    description = "this is test for buying "
    tax = 3193
    base = 16807


    categories = Category.objects.all()
    number_of_products = carts.aggregate(Sum('quantity'))['quantity__sum']
    total_price = 0
    for product in carts:
        total_price += product.quantity * product.product.price

    context = {
        "categories": categories,
        'carts': carts,
        'number_of_products': number_of_products,
        "total_price": total_price,
        "action_url": action_url,
        "apikey": apikey,
        "merchant_id": merchant_id,
        "account_id": account_id,
        "currency": currency,
        "test": test,
        "description": description,
        "buyer_name": buyer.user.username,
        "buyer_email": buyer.user.email,
        "reference_code": reference_code,
        "amount": amount,
        "tax": tax,
        "base": base,
        "signature": signature,
        "response_url": response_url,
        "confirmation_url": confirmation_url,
        "currency": currency

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


def payment_confirmation(request):
    # This is Payu transaction approved code, only for confirmation page, not global variable
    PAYU_APPROVED_CODE = '4'
    if settings.DEBUG:
        buyer = request.user.buyer
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
        carts = Cart.objects.filter(buyer=buyer)

        if create_signature == sign:
            message = '<h1>0K</h1>'
            order = Order(buyer=buyer, paid=True)
            order.save()
            for cart in carts:
                OrderItem(order=order, product=cart.product, quantity=cart.quantity).save()
                cart.delete()
        else:
            message = '<h1>Sign is wrong check why!!!</h1>'
        return HttpResponse(message, status=200)
    else:
        message = '<h1>Something is wrong</h1>' + transaction_final_state
        return HttpResponse(message, status=400)