from django.shortcuts import render


def home(request):
    return render(request, 'research/homepage.html')


def publications(request):
    return render(request, 'research/publications.html')


def interests(request):
    return render(request, 'research/interests.html')


def phd_home(request):
    return render(request, 'research/phd/homepage.html')


def phd_directed_study(request):
    return render(request, 'research/phd/directed_study.html')


def msc_home(request):
    return render(request, 'research/msc/homepage.html')


def b_engg_home(request):
    return render(request, 'research/b_engg/homepage.html')
