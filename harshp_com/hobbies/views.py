from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random
from utils.pagecommons import pagecommon
from .models import Movie, MovieList
from .models import Book, BookList, BookAnnotation


def home(request):
    return render(request, 'hobbies/homepage.html')


def movie_homepage(request):
    movies = Movie.objects.order_by('title').all()
    lists = MovieList.objects.order_by('title').all()
    template_objects = {
        'movies': movies,
        'lists': lists}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/movies.html', template_objects)


def movie_list(request, slug):
    movie_list = get_object_or_404(MovieList, slug=slug)
    movies = movie_list.movies.order_by('title').all()
    template_objects = {
        'list': movie_list,
        'movies': movies
    }
    pagecommon(request, template_objects)
    return render(request, 'hobbies/movielist.html', template_objects)


def book_list(request, slug):
    book_list = get_object_or_404(BookList, slug=slug)
    books = book_list.books.order_by('title').all()
    template_objects = {
        'list': book_list,
        'books': books,
    }
    pagecommon(request, template_objects)
    return render(request, 'hobbies/booklist.html', template_objects)


def watchlist(request):
    movies = Movie.objects.filter(seen=False).order_by('title')
    template_objects = {'movies': movies}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/watchlist.html', template_objects)


def books_homepage(request):
    books = Book.objects.filter(read=True).order_by('title')
    reading = BookList.objects.get(title='Now Reading').books.order_by('title')
    lists = BookList.objects.exclude(title='Now Reading').order_by('title')
    readlist = Book.objects.filter(read=False).order_by('title')
    annotation_count = BookAnnotation.objects.count()
    random_annotation = BookAnnotation.objects.all()[
            random.randint(0, annotation_count)]
    template_objects = {
        'annotation': random_annotation,
        'reading': reading,
        'books': books,
        'lists': lists,
        'readlist': readlist,
        }
    pagecommon(request, template_objects)
    return render(request, 'hobbies/books.html', template_objects)


def videogame_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/videogames.html', template_objects)


def music_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/music.html', template_objects)


def photography_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/photography.html', template_objects)


def origami_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/origami.html', template_objects)


def teacoffee_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/teacoffee.html', template_objects)


def polymathy_homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'hobbies/polymathy.html', template_objects)
