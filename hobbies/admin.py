"""Admin for Hobbies
    Book: BookAdmin
    Movie: MovieAdmin
    TVShow: TVShowAdmin
    Game: GameAdmin
"""
from django.contrib import admin

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
        'date_start',
        'date_end',
        'finished',
    )
    ordering = (
        '-date_start',
        '-date_end',
        'title',
        'finished',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'date_start',
        'date_end',
        'finished',
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
                'date_start',
                'date_end',
                'finished',
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
        'finished',
    )
    ordering = (
        '-date_seen',
        'title',
        'finished',
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
                'finished',
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
        'date_start',
        'date_end',
        'finished',
    )
    ordering = (
        '-date_start',
        '-date_end',
        'title',
        'finished',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'date_start',
        'date_end',
        'finished',
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
                'date_start',
                'date_end',
                'finished',
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
        'date_start',
        'date_end',
        'finished',
    )
    ordering = (
        '-date_start',
        '-date_end',
        'title',
        'finished',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'date_start',
        'date_end',
        'finished',
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
                'date_start',
                'date_end',
                'finished',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )
