from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import Poem


@admin.register(Poem)
class PoemAdmin(PostAdmin):
    """admin for Poem"""

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'authors', 'short_description', 'slug'],
        }),
        ('publish', {
            'fields': [
                'date_created', 'date_published',
                'is_published', 'highlight'],
        }),
        ('content', {
            'classes': ('wide',),
            'fields': ['body_type', 'body'],
        }),
        ('html', {
            'classes': ('wide',),
            'fields': ['body_text'],
        }),
        ('meta', {
            'fields': ['headerimage', 'tags'],
        }),
    ]
    list_display = (
        'title',
        'date_published', 'date_updated', 'highlight', 'is_published')
    list_display_editable = ('is_published', 'highlight')
    list_display_links = (
        'title', 'date_published', 'date_updated')
    list_filter = ['is_published', 'authors', 'tags']
    ordering = (
        '-date_updated', '-date_published',
        'title',
        'highlight', 'is_published')
    search_fields = ['title', 'short_description', 'series__short_description']
