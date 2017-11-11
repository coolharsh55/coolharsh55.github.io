from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from utils.pagecommons import pagecommon
from .models import Feedback


def tags(request):
    return HttpResponse('OK - TAGS')


def tag(request, tag):
    return HttpResponse('OK - {}'.format(tag))


def authors(request):
    return HttpResponse('OK - AUTHORS')


def author(request, author):
    return HttpResponse('OK - {}'.format(author))


def feedback_add(request, url):
    full_url = request.build_absolute_uri(url)
    if request.method == "POST":
        # get values from post
        url = request.POST.get("url", None)
        text = request.POST.get("text", None)
        user = request.POST.get("user", None)
        category = request.POST.get("category", None)
        title = request.POST.get("title", None)
        if not all((url, text)):
            return redirect(url)
        feedback = Feedback()
        feedback.url = url
        feedback.text = text
        feedback.user = user
        feedback.category = category
        feedback.title = title
        feedback.save()
        return redirect(url)
    url_data = resolve(url)
    category = '-'.join(url_data.namespaces)
    title = request.GET.get("title", url_data.url_name)
    return render(
        request, 'sitebase/feedback_add.html', {
            'url': full_url, 'category': category, 'title': title})


def feedbacks(request):
    feedbacks = Feedback.objects.order_by('-pk').all()
    template_objects = {'all_feedbacks': feedbacks}
    pagecommon(request, template_objects)
    return render(
        request, 'sitebase/feedbacks.html', template_objects)


def feedback_view(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    template_objects = {'feedback': feedback}
    pagecommon(request, template_objects)
    return render(
        request, 'sitebase/feedback_view.html', template_objects)


def discover(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'sitebase/discover.html', template_objects)


def random(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'sitebase/random.html', template_objects)


def search(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'sitebase/search.html', template_objects)


def linkfarm(request):
    template_objects = {}
    pagecommon(request, template_objects)
    return render(request, 'sitebase/linkfarm.html', template_objects)
