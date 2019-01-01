from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from userprofile.apis.serializers import *
from userprofile.models import Seller, Contact
from products.models import *


class SellerDetailView(RetrieveAPIView):
    serializer_class = SellerSerializer
    permission_classes = ()

    def get_object(self):
        return Seller.objects.get(pk=self.kwargs['pk'])


class ContactView(CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = ()


class SellersView(ListAPIView):
    serializer_class = SellersSerializer
    queryset = Seller.objects.all()
    permission_classes = ()


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            return Response({
                'msg': 'este correo electrónico ya existe',
            }, status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        email = request.data.get("username")
        username = User.objects.filter(email=email)
        if len(username) > 0:
            username = username[0].username
        else:
            username = None
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=HTTP_400_BAD_REQUEST)


class ReviewView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        order_id = request.data['order_id']

        order = Order.objects.get(id=order_id)
        buyer = request.user.buyer

        if order.rated or order.buyer != buyer:
            return Response({
                'msg': 'this order is already rated or you are not allowed to review this order'
            }, status=HTTP_400_BAD_REQUEST)
        order.rated = True
        order.save()
        return super().post(request, *args, **kwargs)


class BuyerProfileView(RetrieveUpdateAPIView):
    serializer_class = BuyerProfileSerializer

    def get_object(self):
        return self.request.user.buyer