from django.contrib import admin
# Register your models here.
from .models import Seller, City


# class CityAdmin(OSMGeoAdmin):
#     default_lon = -93
#     default_lat = 27
#     default_zoom = 15
#     readonly_fields = ('Latitude', 'Longitude')


admin.site.register(Seller)
admin.site.register(City)
