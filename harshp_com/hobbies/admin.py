from django.contrib import admin

from .models import Movie, MovieList
from .models import Book, BookList, BookAnnotation


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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'read', 'liked')
    list_filter = ('read', 'liked')
    search_fields = ('title',)

    @staticmethod
    def mark_favourite(modeladmin, request, queryset):
        '''marks selected books as favourites'''
        for q in queryset:
            q.liked = True
            q.save()

    actions = ['mark_favourite']


@admin.register(BookList)
class BookListAdmin(admin.ModelAdmin):
    list_display = ('title', 'no_books')
    search_fields = ('title',)
    filter_horizontal = ('books',)

    def no_books(self, booklist):
        return booklist.books.count()


@admin.register(BookAnnotation)
class BookAnnotationAdmin(admin.ModelAdmin):
    list_display = ('content', 'book')
    search_fields = ('content',)
    list_filter = ('book',)
