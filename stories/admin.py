from django.contrib import admin

# Register your models here.
from stories.models import Achievement, ArtisanMaster, Tale


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1


class ArtisanMasterAdmin(admin.ModelAdmin):
    inlines = [AchievementInline, ]
    autocomplete_fields = ['seller']


class TaleAdmin(admin.ModelAdmin):
    list_display = ['title', 'details', 'video_url']

admin.site.register(ArtisanMaster, ArtisanMasterAdmin)
admin.site.register(Tale, TaleAdmin)
