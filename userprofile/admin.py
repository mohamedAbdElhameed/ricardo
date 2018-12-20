from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Seller, Buyer, Review, City, Contact
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# class CityAdmin(OSMGeoAdmin):
#     default_lon = -93
#     default_lat = 27
#     default_zoom = 15
#     readonly_fields = ('Latitude', 'Longitude')


class SellerUserInline(admin.StackedInline):
    model = User
    exclude = ['password']


class CityAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_display = ['id', 'name']


class SellerAdmin(admin.ModelAdmin):
    # inlines = ['SellerUserInline']
    search_fields = ['id', 'user__username', 'longitude', 'latitude', 'city__name','description', 'rate', 'number_of_rates', 'phone_number']
    list_display = ['id', 'user', 'avatar', 'longitude', 'latitude', 'city', 'rate', 'number_of_rates', 'phone_number', ]
    # search_fields = ['user__username', 'city__name', 'description', 'rate', 'phone_number']
    # list_filter = ['user__username', 'city__name']
    # autocomplete_fields = ['city', 'user']
    readonly_fields = ['rate', 'number_of_rates']
    list_filter = ['city', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]


class BuyerAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user__username', 'avatar', 'phone_number', 'address']
    list_display = ['id', 'user', 'avatar', 'phone_number', 'address']
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReviewAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['seller', 'buyer']
    list_display = ['id', 'seller', 'buyer', 'details', 'rate', ]
    search_fields = ['id', 'seller__user__username', 'buyer__user__username', 'details', 'rate', ]
    list_filter = ['seller', ('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'message', 'read']
    search_fields = ['id', 'name', 'phone', 'email', 'message', 'read']
    list_filter = ['read']
    list_editable = ['read']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Seller, SellerAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Contact, ContactAdmin)


class UserAdminNew(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',  'email', 'password1', 'password2')}
         ),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdminNew)