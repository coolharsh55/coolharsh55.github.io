from django.contrib import admin

from sitebase.admin import PostAdmin

from .models import DevSection
from .models import DevPost

@admin.register(DevSection)
class DevSectionAdmin(admin.ModelAdmin):

    list_display = ('title', 'section_type', 'posts')
    list_filter = ('section_type', )
    ordering = ('title', )
    search_fields = ('title', )

    def posts(self, obj):
        return obj.devpost_set.count()


@admin.register(DevPost)
class DevPostAdmin(PostAdmin):
    """admin for Blog Post"""

    fieldsets = [
        ('info', {
            'fields': [
                'title', 'authors', 'section', 'short_description', 'slug'],
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
        'title', 'section',
        'date_published', 'date_updated', 'highlight', 'is_published')
    list_display_editable = ('is_published', 'highlight')
    list_display_links = (
        'title', 'section', 'date_published', 'date_updated')
    list_filter = ['is_published', 'authors', 'tags', 'section']
    ordering = (
        'title', 'section',
        'date_published', 'date_updated',
        'highlight', 'is_published')
    search_fields = ['title', 'short_description']
