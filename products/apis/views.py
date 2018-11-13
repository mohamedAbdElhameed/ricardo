from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Seller
from products.models import Product, SubCategory

from products.apis.serializers import ProductSerializer, ProductDetailSerializer, SubCategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailViewSet(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_object(self):
        return Product.objects.get(pk=self.kwargs['pk'])


class SubCategoryList(ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class ProductsInSubCategoryList(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory = SubCategory.objects.get(pk=self.kwargs['pk'])
        products = subcategory.subcategory_products.all()
        return products
