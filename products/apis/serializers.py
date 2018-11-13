from rest_framework import serializers

from products.models import Product, SubCategory, ProductImage

from userprofile.models import Seller


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'seller_name', 'price', 'first_image']

    def get_seller_name(self, product):
        return product.seller.name

    def get_first_image(self, product):
        return self.context['request'].build_absolute_uri(product.images.all()[0].image.url)


class SellerSerializerForProductDetail(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'avatar', 'rate', 'description']

    def get_rate(self, seller):
        return seller.rate / seller.number_of_rates


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    seller = SellerSerializerForProductDetail()
    additional_attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'seller', 'images', 'price', 'additional_attributes']

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

