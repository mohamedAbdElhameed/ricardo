from django.contrib import admin

# Register your models here.
from django.forms import BaseInlineFormSet

from .models import BigCategory, Category, Product, ProductImage, ProductAdditionalAttributeValue, \
    ProductAdditionalAttributeName, SubCategory


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
    extra = 1


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['category']
    list_display = ['name', 'category', 'image']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductAdditionalAttributeValueInline, ]
    list_display = ['name', 'sub_category', 'seller', 'description', 'price']
    search_fields = ['seller', 'name', 'description', 'price', ]
    autocomplete_fields = ['sub_category', 'seller']
    list_filter = ['seller', ]


class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'big_category', 'description', 'image', ]
    search_fields = ['name', 'big_category__name', 'description', ]
    autocomplete_fields = ['big_category']


class ProductAdditionalAttributeNameAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']
admin.site.register(BigCategory, BigCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAdditionalAttributeName, ProductAdditionalAttributeNameAdmin)