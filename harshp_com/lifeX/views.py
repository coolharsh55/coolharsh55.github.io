from django.shortcuts import render


def home(request):
    return render(request, 'lifeX/homepage.html')
