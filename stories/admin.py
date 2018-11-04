from django.contrib import admin

# Register your models here.
from stories.models import Achievement, ArtisanMaster, Tale
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1


class ArtisanMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller']
    search_fields = ['id', 'seller__user__username']
    filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]
    inlines = [AchievementInline, ]
    autocomplete_fields = ['seller']


class TaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'details', 'video_url']
    search_fields = ['id', 'title', 'details', 'video_url']
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]
admin.site.register(ArtisanMaster, ArtisanMasterAdmin)
admin.site.register(Tale, TaleAdmin)
