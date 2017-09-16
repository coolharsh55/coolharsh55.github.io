from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Movie, MovieList


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


def watchlist(request):
    movies = Movie.objects.filter(seen=False).order_by('title')
    return render(request, 'hobbies/watchlist.html', {'movies': movies})


def books_homepage(request):
    return render(request, 'hobbies/books.html')


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
