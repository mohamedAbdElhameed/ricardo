from django.contrib import admin

# Register your models here.
from django.forms import BaseInlineFormSet
from django import forms
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.utils.translation import gettext_lazy as _

from userprofile.models import Seller
from .models import Category, Product, ProductImage, ProductAdditionalAttributeValue, \
    ProductAdditionalAttributeName, SubCategory, Cart, Order, OrderItem, Status, OrderProxy


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """Check that at least one service has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Al menos una imagen requerida.')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    formset = AtLeastOneRequiredInlineFormSet


class ProductAdditionalAttributeValueInline(admin.TabularInline):
    model = ProductAdditionalAttributeValue
    # autocomplete_fields = ['product_additional_attribute']
    extra = 0


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # autocomplete_fields = ['category']
    list_display = ['id', 'name', 'category', 'image']
    list_filter = ['category']
    search_fields = ['id', 'name' , 'category__name']
    list_filter = ['category', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductAdditionalAttributeValueInline, ]
    list_display = ['id', 'name', 'sub_category', 'seller', 'description', 'price', 'active']
    search_fields = ['id', 'seller__user__username', 'name', 'description', 'price', ]
    # autocomplete_fields = ['sub_category', 'seller']
    list_filter = ['seller', 'active', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]
    list_editable = ['active']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('seller')  # here!
            self.exclude.append('active')

        return super(ProductAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser or not hasattr(request.user, 'Seller'):
            return qs
        return qs.filter(seller=request.user.seller)

    def get_list_display(self, request):
        self.list_editable = []
        if request.user.is_superuser:
            self.list_editable = ['active']

        return super(ProductAdmin, self).get_list_display(request)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'seller', None) is None:
            obj.seller = Seller.objects.get(user=request.user)
        if not request.user.is_superuser:
            obj.active = False
        super(ProductAdmin, self).save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image', ]
    search_fields = ['id', 'name', 'description', ]
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class ProductAdditionalAttributeNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    search_fields = ['id', 'name', ]


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'quantity', ]
    # autocomplete_fields = ['product', 'buyer']
    search_fields = ['id', 'product__name', 'buyer__user__username', 'quantity', ]
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAdditionalAttributeName, ProductAdditionalAttributeNameAdmin)
admin.site.register(Cart, CartAdmin)


class OrderItemForm(forms.ModelForm):
    total = forms.CharField(required=False)
    price = forms.CharField(required=False)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'total']


class InlineOrderItems(admin.TabularInline):
    model = OrderItem
    extra = 1
    form = OrderItemForm

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class OrderAdminForm(forms.ModelForm):
    email = forms.EmailField(help_text=_("Email"), required=False)
    phone_number = forms.CharField(help_text=_("Phone_Number"), required=False)
    address = forms.CharField(help_text=_("Address"), required=False)
    total_price = forms.CharField(required=False)
    total_quantity = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = ['buyer', 'address', 'phone_number', 'email', 'total_price', 'total_quantity', 'status', 'paid']


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    inlines = [InlineOrderItems, ]
    list_display = ['id', 'buyer', 'email', 'phone_number', 'address', 'paid', 'status', 'total_quantity', 'total_price']
    list_filter = ['buyer', 'paid']
    search_fields = ['buyer__name', 'id']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

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

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser or not hasattr(request.user, 'Seller'):
            return qs
        # order_items = OrderItem.objects.filter(product__in= [product for product in request.user.seller.seller_products.all()])
        return qs.filter(seller=request.user.seller)

admin.site.register(Order, OrderAdmin)


class StatusAdmin(admin.ModelAdmin):
    search_fields = ['name']


class OrderProxyAdmin(admin.ModelAdmin):
    readonly_fields = ['buyer', 'paid', 'seller', 'rated']
    list_display = ['id', 'buyer', 'paid', 'status']
    list_filter = ['buyer', 'paid', 'status']
    list_editable = ['status']
    exclude = ['seller', 'rated']
    # autocomplete_fields = ['status']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(OrderProxyAdmin, self).get_queryset(request)
        if request.user.is_superuser or not hasattr(request.user, 'Seller'):
            return qs
        return qs.filter(seller=request.user.seller)


admin.site.register(Status, StatusAdmin)
admin.site.register(OrderProxy, OrderProxyAdmin)
