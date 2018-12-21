from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Seller, Buyer
from products.models import *
from products.apis.serializers import *


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
        products = subcategory.subcategory_products.all()
        return products


class CartView(CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        buyer = Buyer.objects.get(user=user)
        product = Product.objects.get(id=request.data['product_id'])
        quantity = request.data['quantity']

        if len(Cart.objects.filter(buyer=buyer, product=product)) > 0:
            cart = Cart.objects.get(buyer=buyer, product=product)
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
        cart = Cart.objects.filter(buyer=buyer)
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
