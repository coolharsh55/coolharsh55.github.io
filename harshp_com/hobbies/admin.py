from django.contrib import admin

from .models import Movie, MovieList


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'seen', 'liked')
    list_filter = ('seen', 'liked')
    search_fields = ('title',)


@admin.register(MovieList)
class MovieListAdmin(admin.ModelAdmin):
    list_display = ('title', 'no_movies')
    search_fields = ('title',)
    filter_horizontal = ('movies',)


    def no_movies(self, movielist):
        return movielist.movies.count()
