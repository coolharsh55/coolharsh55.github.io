from django.contrib import admin

from .models import Author
from .models import Tag
from .models import Feedback


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ['name', 'email']
    ordering = ['name']
    search_fields = [
        'name', 'email', 'short_description', 'long_description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']
    ordering = ['name']
    search_fields = ['name', 'description']


class PostAdmin(admin.ModelAdmin):
    """admin for Post"""

    date_hierarchy = 'date_published'
    filter_horizontal = ['tags']
    empty_value_display = 'N/A'
    fieldsets = [
        ('info', {
            'fields': ['title', 'authors', 'short_description', 'slug'],
        }),
        ('publish', {
            'fields': ['date_created', 'date_published', 'is_published'],
        }),
        ('meta', {
            'fields': ['tags'],
        }),
    ]
    list_display = [
        'title', 'date_published', 'date_updated', 'is_published']
    list_display_editable = ['is_published']
    list_filter = ['is_published', 'authors', 'tags']
    list_display_links = ['title', 'date_published', 'date_updated']
    ordering = [
        'title', 'date_published', 'date_updated', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'body_type': admin.VERTICAL}
    search_fields = ['title', 'short_description']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    '''Admin for Feedbacks'''
    date_hierarchy = 'timestamp'
    list_display = ['pk', 'timestamp', 'url']
    list_display_links = ['pk', 'timestamp', 'url']
    search_fields = ['category', 'title', 'user', 'text']
