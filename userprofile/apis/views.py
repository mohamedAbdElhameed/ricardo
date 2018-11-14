from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from userprofile.apis.serializers import SellerSerializer, ContactSerializer, SellersSerializer, UserSerializer
from userprofile.models import Seller, Contact


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


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=HTTP_400_BAD_REQUEST)