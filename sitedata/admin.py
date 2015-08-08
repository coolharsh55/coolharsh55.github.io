"""admin for sitedata
    Tag: TagAdmin
"""

from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    """Admin for Tags
    List: tagname, count of linked objects
    Order: tagname, tag id
    Search: tagname
    Tag ID is a readonly field
    """
    list_display = (
        'tagname',
        'slug',
        'linked_objects',
    )
    ordering = (
        'tagname',
        'slug',
        'tagid',
    )
    search_fields = (
        'tagname',
        'slug',
    )
    readonly_fields = (
        'tagid',
        'slug',
    )
    view_on_site = True

    def linked_objects(self, obj):
        """linked objects using the tag
        count number of objects using this tag

        Args:
            self(TagAdmin)
            obj(Tag)

        Returns:
            int: no of objects

        Raises:
            None
        """
        linked_objects = \
            obj.blogpost_set.count() + \
            obj.storypost_set.count() + \
            obj.poem_set.count() + \
            obj.article_set.count() + \
            obj.brainbankpost_set.count() + \
            obj.lifexpost_set.count() + obj.lifexblog_set.count() + \
            obj.book_set.count() + obj.movie_set.count() + \
            obj.tvshow_set.count() + obj.game_set.count()
        return linked_objects
