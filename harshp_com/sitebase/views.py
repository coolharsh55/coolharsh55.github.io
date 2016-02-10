from django.shortcuts import render
from django.http import HttpResponse


def tags(request):
    return HttpResponse('OK - TAGS')


def tag(request, tag):
    return HttpResponse('OK - {}'.format(tag))


def authors(request):
    return HttpResponse('OK - AUTHORS')


def author(request, author):
    return HttpResponse('OK - {}'.format(author))
