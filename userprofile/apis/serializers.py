from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from userprofile.models import Seller, Contact, Buyer
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