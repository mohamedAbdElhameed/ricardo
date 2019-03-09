import hashlib

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from products.models import Category, Cart, Order, OrderItem
from start.models import StartDetail
from userprofile.forms import SignUpForm, LoginForm
from userprofile.models import Seller, Buyer


def index(request):

    payment_method_type = request.POST.get('payment_method_type')

    if payment_method_type == 7 or payment_method_type == 10:
        PAYU_APPROVED_CODE = '4'

        buyer = Buyer.objects.get(user=request.POST.get('extra1'))
        extra2 = request.POST.get('extra2')
        # transaction_final_state = PAYU_APPROVED_CODE

        transaction_final_state = request.POST.get('state_pol')
        response_code_pol = request.POST.get('response_code_pol')
        currency = request.POST.get('currency')
        payment_method_id = request.POST.get('payment_method_id')
        response_message_pol = request.POST.get('response_message_pol')
        apikey = Seller.objects.get(id=extra2).APIKEY
        sign = request.POST.get('sign')
        merchant_id = request.POST.get('merchant_id')
        reference_sale = request.POST.get('reference_sale')
        amount = request.POST.get('value')

        # Decimal validation, Payu requirement
        amount = round(float(amount), 1)

        if apikey is None:
            apikey = '4Vj8eK4rloUd272L48hsrarnUA'
        print(apikey)
        print(merchant_id)
        print(reference_sale)
        print(amount)
        print(currency)
        print(transaction_final_state)


        # Important validation to check the integrity of the data
        create_signature = hashlib.md5((apikey + "~" + merchant_id + "~" + reference_sale + "~" + str(amount) + "~" + currency).encode('utf-8')).hexdigest()

        carts = Cart.objects.filter(buyer=buyer, product__seller=extra2)
        print(create_signature)
        print(sign)

        message = '<h1>0K</h1>'
        order = Order.objects.create(buyer=buyer, paid=True, seller=Seller.objects.get(id=int(extra2)))
        for cart in carts:
            OrderItem.objects.create(order=order, product=cart.product, quantity=cart.quantity)
            cart.delete()
        print('good daf3')
        # else:
        #     print('bad daf3')
        #     message = '<h1>Sign is wrong check why!!!</h1>'
        return HttpResponse(message, status=200)

    categories = Category.objects.all()
    start = StartDetail.objects.last()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'categories': categories,
        'start': start,
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
    }
    return render(request, 'start/index.html', context)
