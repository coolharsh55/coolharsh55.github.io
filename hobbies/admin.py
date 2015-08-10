"""Admin for Hobbies
    Book: BookAdmin
    Movie: MovieAdmin
    TVShow: TVShowAdmin
    Game: GameAdmin
"""
from django.contrib import admin

from hobbies.models import Book
from hobbies.models import Movie
from hobbies.models import TVShow
from hobbies.models import Game


@admin.register(Book)
@admin.register(TVShow)
@admin.register(Game)
class GenericAdmin(admin.ModelAdmin):

    """Admin for Generic Models
    List: title, finished, start date, end date
    Order: title, finished, start date, end date
    Search: title
    Filter: finished, start date, end date
    Form: (ID is readonly) title, finished, start/end date, slug, tags
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
                'headerimage',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )


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
                'headerimage',
            ),
        }),
        ('Tags', {
            'fields': (
                'tags',
            ),
        }),
    )
