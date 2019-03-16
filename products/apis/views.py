import hashlib
from datetime import datetime
from django.db.models import Sum
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ricardo import settings
from userprofile.models import Seller, Buyer
from products.models import *
from products.apis.serializers import *
import time
from sequences import get_next_value


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    permission_classes = ()


class ProductDetailViewSet(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = ()

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])


class SubCategoryList(ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = ()


class ProductsInSubCategoryList(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = ()

    def get_queryset(self):
        subcategory = SubCategory.objects.get(pk=self.kwargs['pk'])
        products = subcategory.subcategory_products.all().filter(active=True)
        return products


class CartView(CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        buyer = Buyer.objects.get(user=user)
        product = Product.objects.get(id=request.data['product_id'])
        quantity = request.data['quantity']

        if len(Cart.objects.filter(buyer=buyer, product=product, show=True)) > 0:
            cart = Cart.objects.get(buyer=buyer, product=product, show=True)
            cart.quantity += int(quantity)
            cart.save()
            if cart.quantity <= 0:
                cart.delete()

            return Response({
                'status': 'updated',
                'product_id': product.id,
                'quantity': cart.quantity
            }, status=status.HTTP_201_CREATED)
        else:
            if int(quantity) <= 0:
                return Response({
                    'status': 'BAD_REQUEST',
                    'product_id': product.id,
                    'quantity': quantity
                }, status=status.HTTP_400_BAD_REQUEST)
            return super().post(request, *args, **kwargs)


class CartListView(ListAPIView):
    serializer_class = CartListSerializer

    def get_queryset(self):
        buyer = Buyer.objects.get(user=self.request.user)
        cart = Cart.objects.filter(buyer=buyer, show=True)
        return cart


class CategoriesView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = ()


class SubCatInCat(ListAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = ()

    def get_queryset(self):
        return SubCategory.objects.filter(category=self.kwargs['pk'])


class OrderView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(buyer=Buyer.objects.get(user=self.request.user))


class CartViewForMobile(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        carts = Cart.objects.filter(buyer=Buyer.objects.get(user=user), show=True)
        unique_code = get_next_value('orders', initial_value=113151)
        for cart in carts:
            i = Cart.objects.select_for_update().get(pk=cart.id)
            i.code = unique_code
            i.save()
        small_carts = []
        sellers = []
        description = ''
        for item in carts:
            if item.product.seller not in sellers:
                sellers.append(item.product.seller)

        for seller in sellers:
            if seller.APIKEY is None or seller.merchant_id is None or seller.account_id is None:
                apikey = '4Vj8eK4rloUd272L48hsrarnUA'
                merchant_id = '508029'
                account_id = '512321'
            else:
                apikey = seller.APIKEY
                merchant_id = seller.merchant_id
                account_id = seller.account_id

            date = str(int(round(time.time() * 1000)))
            reference_code = str(user.buyer.id) + date
            products = Cart.objects.filter(buyer=Buyer.objects.get(user=user), product__seller=seller, show=True)
            amount = 0
            description = ''
            number_of_products = 0
            for product in products:
                amount += product.product.price * product.quantity
                number_of_products += product.quantity
                description += product.product.name + ' '
            currency = 'COP'
            tax = str(0)
            base = str(0)
            signature = hashlib.md5((apikey + "~" + merchant_id + "~" + reference_code + "~" + str(
                round(float(amount), 1)) + "~" + currency).encode('utf-8')).hexdigest()
            form = '''
            <!DOCTYPE html>
                <html lang="es">
                    <head>
                        <meta charset="utf-8">
                        <script src="http://www.artesaniasdeboyaca.com/static/start/js/jquery-3.3.1.min.js"></script>
                        <style>
                            .loader {
                              border: 16px solid #f3f3f3;
                              border-radius: 50%;
                              border-top: 16px solid #3498db;
                              width: 120px;
                              height: 120px;
                              -webkit-animation: spin 2s linear infinite; /* Safari */
                              animation: spin 2s linear infinite;
                            }

                            /* Safari */
                            @-webkit-keyframes spin {
                              0% { -webkit-transform: rotate(0deg); }
                              100% { -webkit-transform: rotate(360deg); }
                            }

                            @keyframes spin {
                              0% { transform: rotate(0deg); }
                              100% { transform: rotate(360deg); }
                            }
                        </style>
                    </head>
                    <body>


                        <h2>Procesando pago, por favor espere… </h2>

                        <div class="loader" style="text-align:center"></div>

                        <form id="lol" method="post" onsubmit="return false;" style="text-align:center;display:none">
                                    <input name="merchantId" type="hidden" value="{{cart.merchant_id}}">
                                    <input name="referenceCode" type="hidden" value="{{cart.reference_code}}">
                                    <input name="description" type="hidden" value="{{description}}">
                                    <input name="amount" type="hidden" value="{{cart.amount}}">
                                    <input name="tax" type="hidden" value="{{cart.tax}}">
                                    <input name="taxReturnBase" type="hidden" value="{{cart.base}}">
                                    <input name="signature" type="hidden" value="{{cart.signature}}">
                                    <input name="accountId" type="hidden" value="{{account_id}}">
                                    <input name="currency" type="hidden" value="{{currency}}">
                                    <input name="buyerFullName" type="hidden" value="{{buyer_name}}">
                                    <input name="buyerEmail" type="hidden" value="{{buyer_email}}">
                                    <input name="shippingAddress" type="hidden" value="{{user.buyer.address}}">
                                    <input name="shippingCity" type="hidden" value="Tunja">
                                    <input name="shippingCountry" type="hidden" value="COP">
                                    <input name="telephone" type="hidden" value="{{buyer_phone}}">
                                    <input name="test" type="hidden" value="{{test}}">
                                    <input name="extra1" type="hidden" value="{{ request.user.id }}">
                                    <input name="extra2" type="hidden" value="{{cart.seller.id}}">
                                    <input name="extra3" type="hidden" value="{{extra3}}">
                                    <input name="responseUrl" type="hidden" value="{{response_url}}">
                                    <input name="confirmationUrl" type="hidden" value="{{confirmation_url}}">
                                    <input class="button" name="Submit" type="submit" onClick="submit_form(this.form, {{cart.seller.id}})"value="Procesando pago, por favor espere… " style="align:center; font-size:72px; padding:30px;margin-top:200px">
                                </form>
                            <script>
                            function hideshow() {
                                document.getElementById('lol').style.display = 'none';
                            }
                                function submit_2(){
                                    form = document.getElementById("lol");
                                    form.action = "{{action_url}}";
                                    hideshow();
                                    form.submit();
                                }

                                function submit_form(seller){
                                    $.ajax({
                                        url: "http://www.artesaniasdeboyaca.com/products/hide_cart/{{extra3}}/"+seller+"/",
                                        type: 'GET',
                                        dataType: 'json',
                                        contentType: "application/x-www-form-urlencoded",
                                        success: function(res) {
                                            submit_2();
                                        },
                                        error: function(res) {
                                            console.log('Request Status: ' + res.status + ' Status Text: ' + res.statusText + ' ' + res.responseText);
                                        }
                                    });

                                }
                                submit_form({{seller.id}});
                            </script>
                    </body>
                </html>


        '''
            form = form.replace('{{cart.merchant_id}}', merchant_id)
            form = form.replace('{{cart.reference_code}}', reference_code)
            form = form.replace('{{description}}', description)
            form = form.replace('{{cart.amount}}', str(amount))
            form = form.replace('{{cart.tax}}', str(tax))
            form = form.replace('{{cart.base}}', str(base))
            form = form.replace('{{cart.signature}}', signature)
            form = form.replace('{{account_id}}', account_id)
            form = form.replace('{{currency}}', 'COP')
            form = form.replace('{{buyer_name}}', self.request.user.buyer.full_name)
            form = form.replace('{{buyer_email}}', self.request.user.email)
            form = form.replace('{{ request.user.id }}', str(request.user.id))
            form = form.replace('{{cart.seller.id}}', str(seller.id))
            form = form.replace('{{seller.id}}', str(seller.id))
            form = form.replace('{{buyer_phone}}', request.user.buyer.phone_number)
            form = form.replace('{{response_url}}', 'http://www.artesaniasdeboyaca.com/')
            form = form.replace('{{extra3}}', str(unique_code))
            form = form.replace('{{confirmation_url}}',
                                'http://www.artesaniasdeboyaca.com/products/payment_confirmation/')
            form = form.replace('{{action_url}}', "https://checkout.payulatam.com/ppp-web-gateway-payu/")
            small_carts.append({
                'seller': seller.name,
                # 'data': products.values('id', 'product', 'quantity'),
                'data': [
                    {
                        "id": cart.id,
                        "product": {
                            'id': cart.product.id,
                            'price': cart.product.price,
                            'name': cart.product.name,
                            'image': request.build_absolute_uri(cart.product.images.all()[0].image.url) or None
                        },
                        "quantity": cart.quantity
                    }
                    for cart in products],
                'payment_form': form,
                # 'APIKEY': apikey,
                # 'merchant_id': merchant_id,
                'amount': amount,
                # 'signature': signature,
                # 'reference_code': reference_code,
                # 'tax': tax,
                # 'base': base,
                'number_of_products': number_of_products,
            })
        buyer = user.buyer
        currency = 'COP'
        if settings.DEBUG:
            action_url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/"
            account_id = '512321'
            test = '1'
            host = 'http://www.artesaniasdeboyaca.com/'
        else:
            action_url = "https://checkout.payulatam.com/ppp-web-gateway-payu"
            account_id = '512321'
            test = '0'
            host = 'https://peaku.co/'

        response_url = host
        confirmation_url = host + 'products/payment_confirmation/'
        description = "this is test for buying "

        categories = Category.objects.all()
        number_of_products = carts.aggregate(Sum('quantity'))['quantity__sum']
        total_price = 0
        for product in carts:
            total_price += product.quantity * product.product.price

        context = {
            'small_carts': small_carts,
            'number_of_products': number_of_products,
            "total_price": total_price,
            # "action_url": action_url,
            # "account_id": account_id,
            # "currency": currency,
            # "test": test,  # to test credit card
            # "description": description,
            # "buyer_name": buyer.user.username,
            # "buyer_email": buyer.user.email,
            # "response_url": response_url,
            # "confirmation_url": confirmation_url,
        }
        return Response(context)
