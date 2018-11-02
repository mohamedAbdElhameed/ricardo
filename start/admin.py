from django.contrib import admin

# Register your models here.
from start.models import StartDetail


class StartDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_image', 'below_image', 'below_title', 'below_detail' ]
    autocomplete_fields = ['products']


admin.site.register(StartDetail, StartDetailAdmin)