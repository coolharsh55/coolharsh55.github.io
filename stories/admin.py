"""admin for stories

    StoryPost: StoryPostAdmin
"""

from django.contrib import admin
from .models import StoryPost


@admin.register(StoryPost)
class StoryPostAdmin(admin.ModelAdmin):

    """Admin for story
    """
    list_display = (
        'title',
        'published',
        'post_id',
        'tags_count',
    )
    ordering = (
        '-post_id',
        'published',
        'title'
    )
    search_fields = (
        'title',
    )
    date_hierarchy = 'published'
    list_filter = (
        'published',
        'tags',
        'modified',
    )
    filter_horizontal = (
        'tags',
    )
    # exclude = ('')
    readonly_fields = (
        'post_id',
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'post_id',
                'title',
                'published',
                'modified',
            )
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'body',
            )
        }),
        ('Extras', {
            'classes': ('collapse',),
            'fields': (
                'headerimage',
                'tags',
                'slug',
            )
        }),
    )

    # future: status/draft or published/NO or publish/future
    # def suit_row_attributes(self, obj, request):
    #     return {'class': 'error'}

    def tags_count(self, obj):
        """tag count

        count the tags associated with a story
        """
        return obj.tags.count()
