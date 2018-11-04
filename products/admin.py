from django.contrib import admin

# Register your models here.
from django.forms import BaseInlineFormSet
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import Category, Product, ProductImage, ProductAdditionalAttributeValue, \
    ProductAdditionalAttributeName, SubCategory, Cart


class RequiredInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    formset = RequiredInlineFormSet


class ProductAdditionalAttributeValueInline(admin.StackedInline):
    model = ProductAdditionalAttributeValue
    autocomplete_fields = ['product_additional_attribute']
    extra = 0


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['category']
    list_display = ['id', 'name', 'category', 'image']
    list_filter = ['category']
    search_fields = ['id', 'name' , 'category__name']
    list_filter = ['category', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductAdditionalAttributeValueInline, ]
    list_display = ['id', 'name', 'sub_category', 'seller', 'description', 'price']
    search_fields = ['id', 'seller__user__username', 'name', 'description', 'price', ]
    autocomplete_fields = ['sub_category', 'seller']
    list_filter = ['seller', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image', ]
    search_fields = ['id', 'name', 'description', ]
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class ProductAdditionalAttributeNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    search_fields = ['id', 'name', ]


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'quantity', ]
    autocomplete_fields = ['product', 'buyer']
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