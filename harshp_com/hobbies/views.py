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
