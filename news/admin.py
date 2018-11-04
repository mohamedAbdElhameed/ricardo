from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Register your models here.
from news.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'details', 'image']
    search_fields = ['id', 'title', 'details', ]
    list_filter = [('created_at', DateRangeFilter), ('modified_at', DateRangeFilter)]

admin.site.register(Post, PostAdmin)
