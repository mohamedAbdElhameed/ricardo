from rest_framework import serializers

from userprofile.models import Seller

from products.models import Product


class SellerSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    seller_products = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'avatar', 'description', 'address', 'phone_number', 'rate', 'number_of_rates', 'seller_products']

    def get_rate(self, seller):
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