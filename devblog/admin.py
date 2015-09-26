from django.contrib import admin

from .models import DevBlogPost
from .models import DevBlogSeries


@admin.register(DevBlogPost)
class DevBlogPostAdmin(admin.ModelAdmin):

    """Admin for dev blog posts
    """
    list_display = (
        'title',
        'series',
        'published',
        'draft',
        'future',
    )
    ordering = (
        'published',
        'series',
        'modified',
        'draft',
        'future',)
    date_hierarchy = 'published'
    filter_horizontal = ('tags', 'css', 'js',)
    search_fields = (
        'title',
        'slug',
    )
    readonly_fields = (
        'post_id',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'post_id',
                'title',
                'series',
                'published',
                'modified',
                'draft',
                'future',
                'headerimage',
            ),
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': ('body', )
        }),
        ('Extras', {
            'classes': ('collapse',),
            'fields': (
                'tags', 'css', 'js',),
        }),
    )


@admin.register(DevBlogSeries)
class DevBlogSeriesAdmin(admin.ModelAdmin):

    """Admin for dev blog posts
    """
    list_display = (
        'name',
    )
    ordering = (
        'name',
    )
    prepopulated_fields = {
        'slug': ('name', )
    }
    search_fields = (
        'name',
        'slug')
    # readonly_fields = (
    #     'slug',)
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'name',
                'slug',
            ),
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': ('description', )
        }),
    )
