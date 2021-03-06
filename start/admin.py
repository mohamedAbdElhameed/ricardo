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
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(StartDetail, StartDetailAdmin)

admin.site.site_header = "Artesanías de Boyacá"
admin.site.site_title = "Artesanías de Boyacá"
admin.site.index_title = "Artesanías de Boyacá"
