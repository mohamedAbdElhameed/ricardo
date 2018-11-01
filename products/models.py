from django.db import models
from django.db.models import Model
# Create your models here.
from userprofile.models import Seller


class BigCategory(Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Category(Model):
    big_category = models.ForeignKey(BigCategory, related_name="categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name


class Product(Model):
    category = models.ForeignKey(Category, related_name="category_products", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, related_name="seller_products", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name


class ProductImage(Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()
    order = models.IntegerField()
    alt_text = models.CharField(max_length=100)


class ProductAdditionalAttributeName(Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductAdditionalAttributeValue(Model):
    product = models.ForeignKey(Product, related_name="additional_attributes", on_delete=models.SET_NULL, null=True)
    product_additional_attribute = models.ForeignKey(ProductAdditionalAttributeName, related_name="product_additional_attributes", on_delete=models.SET_NULL, null=True)
    additional_attribute_value = models.CharField(max_length=120)

    def __str__(self):
        return self.product.name + self.product_additional_attribute.name + " " + self.additional_attribute_value