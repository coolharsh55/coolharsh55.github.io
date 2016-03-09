from django.shortcuts import render
from django.http import HttpResponse


def list(request):
    return render(request, 'dev/homepage.html')


def series_list(request):
    return HttpResponse('OK')


def series(request, series):
    """return requested Blog Series"""

    return HttpResponse('OK')


def series_post(request, series, post):
    """return requested Blog Post for Blog Series"""

    return HttpResponse('OK')


def post(request, post):
    """return requested Blog Post"""

    return HttpResponse('OK')
