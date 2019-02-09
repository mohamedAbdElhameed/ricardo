from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_auth.views import PasswordResetView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
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
        username = request.data.get("username")
        email = User.objects.filter(email=username)
        if len(email) > 0:
            username = email[0].username

        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Datos incorrectos, intente nuevamente."}, status=HTTP_400_BAD_REQUEST)


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


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Contraseña anterior incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            Token.objects.filter(user=request.user).delete()
            Token.objects.create(user=request.user)
            return Response({
                'token': request.user.auth_token.key
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetMyPassword(PasswordResetView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is None:
            return Response({
                'detail': 'Este correo electrónico no existe en el sistema.',
            }, status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)