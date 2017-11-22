from django.shortcuts import render
from utils.pagecommons import pagecommon


def homepage(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'me/homepage.html', template_objects)
