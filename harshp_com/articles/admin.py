from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import Article
from .models import ArticleSeries


@admin.register(Article)
class ArticleAdmin(PostAdmin):
    """admin for Blog Post"""

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
        'title', 'series',
        'date_published', 'date_updated',
        'highlight', 'is_published')
    search_fields = ['title', 'short_description', 'series__short_description']


@admin.register(ArticleSeries)
class ArticleSeriesAdmin(admin.ModelAdmin):
    """admin for Blog Series"""

    list_display = ('title', 'blogs')
    ordering = ('title',)
    search_fields = ('title',)

    def blogs(self, obj):
        return obj.article_set.count()