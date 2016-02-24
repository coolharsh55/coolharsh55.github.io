"""admin for sitedata
    Tag: TagAdmin
"""

from django import forms
from django.contrib import admin

from sitedata.models import Tag
from sitedata.models import Feedback
from sitedata.models import FileUpload
from sitedata.models import CSSLink
from sitedata.models import JSLink


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


class FileUploadForm(forms.ModelForm):

    """form for file upload
    """
    class Meta:
        model = FileUpload
        exclude = ['pk', ]


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):

    """admin class for File Upload
    """

    form = FileUploadForm


@admin.register(CSSLink)
class CSSLinkAdmin(admin.ModelAdmin):

    """admin class for css links
    """

    list_display = ('name', 'link', 'dependencies')
    ordering = ('name', )
    search_fields = ('name', 'link')
    filter_horizontal = ('dependency',)

    def dependencies(self, obj):
        """count of dependencies
        """
        return obj.dependency.count()


@admin.register(JSLink)
class JSLinkAdmin(admin.ModelAdmin):

    """admin class for css links
    """

    list_display = ('name', 'link', 'dependencies')
    ordering = ('name', )
    search_fields = ('name', 'link')
    filter_horizontal = ('dependency',)

    def dependencies(self, obj):
        """count of dependencies
        """
        return obj.dependency.count()
