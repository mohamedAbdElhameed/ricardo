from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Seller
from products.models import Product, SubCategory, Cart
from products.apis.serializers import ProductSerializer, ProductDetailSerializer, SubCategorySerializer, CartSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
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
