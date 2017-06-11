from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import Story
from .models import StorySeries


@admin.register(Story)
class StoryAdmin(PostAdmin):
    """admin for Story"""

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'authors', 'series', 'short_description', 'slug'],
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
        'title', 'series',
        'date_published', 'date_updated', 'highlight', 'is_published')
    list_display_editable = ('is_published', 'highlight')
    list_display_links = (
        'title', 'series', 'date_published', 'date_updated')
    list_filter = ['is_published', 'authors', 'tags', 'series']
    ordering = (
        '-date_updated', '-date_published',
        'title', 'series',
        'highlight', 'is_published')
    search_fields = ['title', 'short_description', 'series__short_description']


@admin.register(StorySeries)
class StorySeriesAdmin(admin.ModelAdmin):
    """admin for Story Series"""

    list_display = ('title', 'blogs')
    ordering = ('title',)
    search_fields = ('title',)

    def blogs(self, obj):
        return obj.story_set.count()
