from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from userprofile.models import *
from products.models import Product


class SellerSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    seller_products = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'avatar', 'description', 'address', 'phone_number', 'rate', 'number_of_rates', 'seller_products']

    def get_rate(self, seller):
        if seller.number_of_rates == 0:
            return 0
        return seller.rate / seller.number_of_rates

    def get_seller_products(self, seller):
        products = seller.seller_products.all()
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'image': self.context['request'].build_absolute_uri(product.images.all()[0].image.url),
                'price': product.price
            })
        return product_list


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message', ]


class SellersSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'avatar', 'rate', 'description',]

    def get_rate(self, seller):
        if seller.number_of_rates == 0:
            return 0
        return seller.rate / seller.number_of_rates


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'token']
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        Token.objects.create(user=user)
        buyer = Buyer.objects.create(user=user)

        print(user)
        return user

    def get_token(self, user):
        return Token.objects.get(user=user).key


class ReviewSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['order_id', 'details', 'rate', 'seller']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user.buyer
        return super().create(validated_data)


class BuyerProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = ['avatar', 'phone_number', 'address', 'user_name', 'email']

    def get_user_name(self, buyer):
        return buyer.user.username

    def get_email(self, buyer):
        return buyer.user.email


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)