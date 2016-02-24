"""admin configuration for poems

    Poem: PoemAdmin
"""

from django.contrib import admin
from .models import Poem


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    """Admin for Poem

    list: title, published, post id, tags count
    ordering: post id, published(hierarchy), title,
    search: title
    readonly: post id
    prepopulated: slug=title
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

        count number of tags associated with poem

        Args:
            self(PoemAdmin)
            obj(Poem)

        Returns:
            int: no of tags

        Raises:
            None
        """
        return obj.tags.count()
