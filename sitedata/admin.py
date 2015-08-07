"""admin for sitedata
    Tag: TagAdmin
    Book: BookAdmin
    Movie: MovieAdmin
    TVShow: TVShowAdmin
    Game: GameAdmin
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

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    """Admin for Books
    List: title, read, start date, end date
    Order: title, read, start date, end date
    Search: title
    Filter: Read, start date, end date
    Form: (ID is readonly) title, read, start/end date, slug, tags
    """
    list_display = (
        'title',
        'read',
        'date_start',
        'date_end',
    )
    ordering = (
        'title',
        'read',
        'date_start',
        'date_end',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'read',
        'date_start',
        'date_end',
    )
    readonly_fields = (
        '_id',
    )
    filter_horizontal = (
        'tags',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'title',
                '_id',
                'read',
                'date_start',
                'date_end',
                'slug',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    """Admin for Movies
    List: title, read, seen date
    Order: title, read, seen date
    Search: title
    Date: seen date
    Form: (ID is readonly) title, seen date, slug, tags
    """
    list_display = (
        'title',
        'date_seen',
    )
    ordering = (
        'title',
        'date_seen',
    )
    search_fields = (
        'title',
    )
    date_hierarchy = 'date_seen'
    readonly_fields = (
        '_id',
    )
    filter_horizontal = (
        'tags',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'title',
                '_id',
                'date_seen',
                'slug',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )

from .models import TVShow


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):

    """Admin for TV Shows
    List: title, watched, start date, end date
    Order: title, watched, start date, end date
    Search: title
    Filter: watched, start date, end date
    Form: (ID is readonly) title, watched, start/end date, slug, tags
    """
    list_display = (
        'title',
        'watched',
        'date_start',
        'date_end',
    )
    ordering = (
        'title',
        'watched',
        'date_start',
        'date_end',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'watched',
        'date_start',
        'date_end',
    )
    readonly_fields = (
        '_id',
    )
    filter_horizontal = (
        'tags',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'title',
                '_id',
                'watched',
                'date_start',
                'date_end',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    """Admin for Games
    List: title, finished, start date, end date
    Order: title, finished, start date, end date
    Search: title
    Filter: finished, start date, end date
    Form: (ID is finishedonly) title, finished, start/end date, slug, tags
    """
    list_display = (
        'title',
        'finished',
        'date_start',
        'date_end',
    )
    ordering = (
        'title',
        'finished',
        'date_start',
        'date_end',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'finished',
        'date_start',
        'date_end',
    )
    finishedonly_fields = (
        '_id',
    )
    filter_horizontal = (
        'tags',
    )
    view_on_site = True
    fieldsets = (
        ('Details', {
            'fields': (
                'title',
                '_id',
                'finished',
                'date_start',
                'date_end',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )
