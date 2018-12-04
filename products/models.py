from django.db import models
from django.db.models import Model
# Create your models here.
from userprofile.models import Seller, Buyer
from django.utils.translation import gettext_lazy as _


class Category(Model):
    name = models.CharField(max_length=35, help_text=_("Name"), verbose_name=_("Name"))
    description = models.TextField(help_text=_("Description"), verbose_name=_("Description"))
    image = models.ImageField(help_text=_("Image"), verbose_name=_("Image"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class SubCategory(Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.SET_NULL, null=True, help_text=_("Category"), verbose_name=_("Category"))
    name = models.CharField(max_length=50, help_text=_("Name"), verbose_name=_("Name"))
    image = models.ImageField(help_text=_("Image"), verbose_name=_("Image"))
    description = models.TextField(help_text=_("Description"), verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def __str__(self):
        return self.name


class Product(Model):
    sub_category = models.ForeignKey(SubCategory, related_name="subcategory_products", on_delete=models.SET_NULL, null=True, help_text=_("Sub Category"), verbose_name=_("Sub Category"))
    seller = models.ForeignKey(Seller, related_name="seller_products", on_delete=models.SET_NULL, null=True, help_text=_("Seller"), verbose_name=_("Seller"))
    name = models.CharField(max_length=50, help_text=_("Name"), verbose_name=_("Name"))
    description = models.TextField(help_text=_("Description"), verbose_name=_("Description"))
    price = models.FloatField(help_text=_("Price"), verbose_name=_("Price"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductImage(Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, help_text=_("Product"), verbose_name=_("Product"))
    image = models.ImageField(help_text=_("Image"), verbose_name=_("Image"))
    order = models.IntegerField(help_text=_("Order"), verbose_name=_("Order"))
    alt_text = models.CharField(max_length=100, help_text=_("Alt Text"), verbose_name=_("Alt Text"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


class ProductAdditionalAttributeName(Model):
    name = models.CharField(max_length=50, help_text=_("Name"), verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Product Additional Attribute Name")
        verbose_name_plural = _("Product Additional Attribute Names")

    def __str__(self):
        return self.name


class ProductAdditionalAttributeValue(Model):
    product = models.ForeignKey(Product, related_name="additional_attributes", on_delete=models.SET_NULL, null=True, help_text=_("Product"), verbose_name=_("Product"))
    product_additional_attribute = models.ForeignKey(ProductAdditionalAttributeName, related_name="product_additional_attributes", on_delete=models.SET_NULL, null=True, help_text=_("Product Additional Attributes"), verbose_name=_("Product Additional Attributes"))
    additional_attribute_value = models.CharField(max_length=120, help_text=_("Additional Attributes Values"), verbose_name=_("Additional Attributes Values"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Product Additional Attribute Value")
        verbose_name_plural = _("Product Additional Attribute Values")

    def __str__(self):
        return self.product.name + self.product_additional_attribute.name + " " + self.additional_attribute_value


class Cart(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text=_("Product"), verbose_name=_("Product"))
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, help_text=_("Buyer"), verbose_name=_("Buyer"))
    quantity = models.IntegerField(help_text=_("Quantity"), verbose_name=_("Quantity"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    @property
    def total_cost(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class Status(models.Model):
    status_name = models.CharField(max_length=50, help_text=_("Status name"), verbose_name=_("Status name"))

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")


class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, help_text=_("Buyer"), verbose_name=_("Buyer"))
    paid = models.BooleanField(default='False', help_text=_("Paid"), verbose_name=_("Paid"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, default=None, help_text=_("you can change the status form the states list"), verbose_name=_("Status"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def email(self):
        return self.buyer.user.email

    def address(self):
        return self.buyer.address

    def phone_number(self):
        return self.buyer.phone_number

    def total_quantity(self, order):
        items = order.order_items.all()
        quantity = 0
        for item in items:
            quantity += item.quantity
        return quantity

    def total_price(self, order):
        items = order.order_items.all()
        print(items)
        price = 0
        for item in items:
            price += item.product.price * item.quantity
        return price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', help_text=_("Order"), verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, help_text=_("Product"), verbose_name=_("Product"))
    quantity = models.IntegerField(help_text=_("quantity"), verbose_name=_("quantity"))

    def __str__(self):
        return ""

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def total(self):
        return '$ ' + str(self.quantity * self.product.price)

    def price(self):
        return '$ ' + str(self.product.price)


class OrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _("Order Status")
        verbose_name_plural = _("Orders Status")