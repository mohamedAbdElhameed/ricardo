from django.contrib import admin

# Register your models here.
from start.models import StartDetail


class StartDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_image', 'below_image', 'below_title', 'below_detail' ]
    autocomplete_fields = ['products']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(StartDetail, StartDetailAdmin)