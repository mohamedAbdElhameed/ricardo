from rest_framework import serializers

from products.models import *
from userprofile.models import *


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'seller_name', 'price', 'first_image']

    def get_seller_name(self, product):
        if product.seller is None:
            return None
        return product.seller.name

    def get_first_image(self, product):
        if len(product.images.all()) > 0:
            return self.context['request'].build_absolute_uri(product.images.all()[0].image.url) or None
        else:
            return None


class SellerSerializerForProductDetail(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'avatar', 'rate', 'description']

    def get_rate(self, seller):
        if seller.number_of_rates == 0 :
            return 0
        return seller.rate / seller.number_of_rates


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    seller = SellerSerializerForProductDetail()
    additional_attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'seller', 'images', 'price', 'description', 'additional_attributes']

    def get_images(self, product):
        d = []
        for i in product.images.all():
            d.append({
                'order': i.order,
                'image': self.context['request'].build_absolute_uri(i.image.url)
            })
        return d

    def get_additional_attributes(self, product):
        attributes = []
        for i in product.additional_attributes.all():
            attributes.append(
                {
                    'name': i.product_additional_attribute.name,
                    'value': i.additional_attribute_value
                }
            )
        return attributes


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image']


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        validated_data['buyer'] = Buyer.objects.get(user=self.context['request'].user)
        validated_data['product'] = Product.objects.get(id=validated_data['product_id'])
        return Cart.objects.create(**validated_data)


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', ]


class CategorySerializer(serializers.ModelSerializer):
    first_subcat_id = serializers.SerializerMethodField()
    first_subcat_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'first_subcat_id', 'first_subcat_name']

    def get_first_subcat_id(self, category):
        return category.subcategories.first().id

    def get_first_subcat_name(self, category):
        return category.subcategories.first().name


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True)
    seller = SellerSerializerForProductDetail()

    class Meta:
        model = Order
        fields = ['id', 'seller', 'status', 'rated', 'order_items', 'total_price']

