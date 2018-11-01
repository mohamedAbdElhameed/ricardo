from django.contrib import admin

# Register your models here.
from django.forms import BaseInlineFormSet

from .models import BigCategory, Category, Product, ProductImage, ProductAdditionalAttributeValue, \
    ProductAdditionalAttributeName


class RequiredInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    formset = RequiredInlineFormSet


class ProductAdditionalAttributeValueInline(admin.TabularInline):
    model = ProductAdditionalAttributeValue
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductAdditionalAttributeValueInline,]


admin.site.register(BigCategory)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAdditionalAttributeName)