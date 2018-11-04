from django.db import models
from django.db.models import Model
# Create your models here.
from userprofile.models import Seller, Buyer


class Category(Model):
    name = models.CharField(max_length=35)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubCategory(Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(Model):
    sub_category = models.ForeignKey(SubCategory, related_name="subcategory_products", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, related_name="seller_products", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()
    order = models.IntegerField()
    alt_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductAdditionalAttributeName(Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductAdditionalAttributeValue(Model):
    product = models.ForeignKey(Product, related_name="additional_attributes", on_delete=models.SET_NULL, null=True)
    product_additional_attribute = models.ForeignKey(ProductAdditionalAttributeName, related_name="product_additional_attributes", on_delete=models.SET_NULL, null=True)
    additional_attribute_value = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name + self.product_additional_attribute.name + " " + self.additional_attribute_value


class Cart(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)