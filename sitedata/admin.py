"""admin for sitedata
    Tag: TagAdmin
"""

from django.contrib import admin

from sitedata.models import Tag
from sitedata.models import Feedback


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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    """Admin for Feedback
    List: date, title, name, replied
    Order: date
    Search: title
    """
    list_display = (
        'published',
        'title',
        'user_name',
        'reply_date',
    )
    ordering = (
        '-published',
        '-reply_date',
    )
    search_fields = (
        'title',
    )
    readonly_fields = (
        'id',
        'published',
        'title',
        'text',
        'user_name',
        'user_email',
        'reply_date',
    )
    view_on_site = True
    fieldsets = (
        ('About', {
            'fields': (
                'id',
                'published',
                'title',
                'user_name',
                'user_email',
            )
        }),
        ('Contents', {
            'classes': ('full-width',),
            'description': 'source can be selected',
            'fields': (
                'text',
            )
        }),
        ('Reply', {
            'classes': ('collapse',),
            'fields': (
                'reply_date',
                'reply',
            )
        }),
    )
