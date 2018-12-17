from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

# Register your models here.
from django import forms
from start.models import StartDetail


class StartDetailAdminForm(forms.ModelForm):
    below_detail = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = StartDetail
        fields = '__all__'


class StartDetailAdmin(admin.ModelAdmin):
    form = StartDetailAdminForm
    list_display = ['title', 'banner_image', 'below_image', 'below_title', 'below_detail' ]
    # autocomplete_fields = ['products']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(StartDetail, StartDetailAdmin)

admin.site.site_header = "Ricardo"
admin.site.site_title = "Ricardo"
admin.site.index_title = "Ricardo"
