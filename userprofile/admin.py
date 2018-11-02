from django.contrib import admin
# Register your models here.
from .models import Seller, City


# class CityAdmin(OSMGeoAdmin):
#     default_lon = -93
#     default_lat = 27
#     default_zoom = 15
#     readonly_fields = ('Latitude', 'Longitude')

class SellerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['user', 'city', 'avatar', 'description', 'rate', 'phone_number', ]
    #search_fields = ['user__username', 'city__name', 'description', 'rate', 'phone_number']
    # list_filter = ['user__username', 'city__name']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'longitude', 'latitude', ]

admin.site.register(Seller, SellerAdmin)
admin.site.register(City, CityAdmin)
