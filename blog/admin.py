from django.contrib import admin
from .models import Blog, Category, Tag, Comment

admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'created_date']
    list_filter = ['category', 'tags']
    date_hierarchy = 'created_date'
    search_fields = ['title']
    filter_horizontal = ['tags', ]
