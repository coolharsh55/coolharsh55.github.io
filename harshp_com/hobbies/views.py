from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random

from .models import Movie, MovieList
from .models import Book, BookList, BookAnnotation


def home(request):
    return render(request, 'hobbies/homepage.html')


def movie_homepage(request):
    movies = Movie.objects.order_by('title').all()
    lists = MovieList.objects.order_by('title').all()
    return render(request, 'hobbies/movies.html', {
        'movies': movies,
        'lists': lists})


def movie_list(request, slug):
    movie_list = get_object_or_404(MovieList, slug=slug)
    movies = movie_list.movies.order_by('title').all()
    return render(request, 'hobbies/movielist.html', {
        'list': movie_list,
        'movies': movies
    })


def book_list(request, slug):
    book_list = get_object_or_404(BookList, slug=slug)
    books = book_list.books.order_by('title').all()
    return render(request, 'hobbies/booklist.html', {
        'list': book_list,
        'books': books,
    })


def watchlist(request):
    movies = Movie.objects.filter(seen=False).order_by('title')
    return render(request, 'hobbies/watchlist.html', {'movies': movies})


def books_homepage(request):
    books = Book.objects.filter(read=True).order_by('title')
    reading = BookList.objects.get(title='Now Reading').books.order_by('title')
    lists = BookList.objects.exclude(title='Now Reading').order_by('title')
    readlist = Book.objects.filter(read=False).order_by('title')
    annotation_count = BookAnnotation.objects.count()
    random_annotation = BookAnnotation.objects.all()[
            random.randint(0, annotation_count)]
    return render(request, 'hobbies/books.html', {
        'annotation': random_annotation,
        'reading': reading,
        'books': books,
        'lists': lists,
        'readlist': readlist,
        })


def videogame_homepage(request):
    return render(request, 'hobbies/videogames.html')


def music_homepage(request):
    return render(request, 'hobbies/music.html')


def photography_homepage(request):
    return render(request, 'hobbies/photography.html')


def origami_homepage(request):
    return render(request, 'hobbies/origami.html')


def teacoffee_homepage(request):
    return render(request, 'hobbies/teacoffee.html')


def polymathy_homepage(request):
    return render(request, 'hobbies/polymathy.html')
