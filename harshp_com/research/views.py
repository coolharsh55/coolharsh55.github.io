from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import ResearchBlogSeries, ResearchBlogPost


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


def blog_home(request):
	series = ResearchBlogSeries.objects.order_by('title')
	posts = ResearchBlogPost.objects.order_by('-date_published')
	return render(request, 'research/blog/homepage.html')


def blog_series(request, series):
	series = get_object_or_404(ResearchBlogSeries, slug=series)
	return render(
		request, 'research/blog/series.html',
		{
			'series': series,
			'posts': series.researchblogpost_set.order_by('-date_published')
		})


def blog_post(request, series, post):
	series = get_object_or_404(ResearchBlogSeries, slug=series)
	post = get_object_or_404(ResearchBlogPost, series=series, slug=post)
	return render(request, 'research/blog/post.html', {'post': post})
