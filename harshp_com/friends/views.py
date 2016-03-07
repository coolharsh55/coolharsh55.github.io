from django.shortcuts import render


def home(request):
    return render(request, 'friends/homepage.html')
