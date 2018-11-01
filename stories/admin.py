from django.contrib import admin

# Register your models here.
from stories.models import Achievement, ArtisanMaster, Tale


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1


class AchievementAdmin(admin.ModelAdmin):
    inlines = [AchievementInline, ]


admin.site.register(ArtisanMaster, AchievementAdmin)
admin.site.register(Tale)
