"""views for sitedata
"""

from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from sitedata.forms import FeedbackForm
from sitedata.models import Tag
from sitedata.models import Feedback
from urllib2 import unquote


def tag_index(request):
    """index view for tags
    """
    try:
        tags = Tag.objects.all()
    except Exception as e:
        print e
    return render_to_response(
        'sitedata/tagindex.html',
        {
            'tags': tags,
        },
    )


def tag(request, tagname):
    """view for tag
    """
    try:
        tag = Tag.objects.get(slug=tagname)
        links = tagcount(tag)
    except Tag.DoesNotExist:
        return Http404('Tag does not exist')
    return render_to_response(
        'sitedata/tag.html',
        {
            'tag': tag,
            'links': links,
        }
    )


def tagcount(tag, sort=True):
    """count of tag linked objects
    """
    xitems = []
    items = []
    for x in Tag.__dict__:
        if x.endswith('_set'):
            xitems.append(getattr(tag, x))
    for x in xitems:
        print x
        items.append(x.order_by('-published'))
    print items
    links = []
    for item in items:
        if item:
            links.append((item, item[0].__class__.__name__))
    return links


def feedback_index(request):
    """index view for feedback
    """
    try:
        print 'feedback index'
        feedbacks = Feedback.objects.order_by('-published')
        return render_to_response(
            'sitedata/feedback_index.html',
            {
                'feedbacks': feedbacks,
            }
        )
    except Feedback.DoesNotExist:
        pass


def feedback(request, feedback_no):
    """view for feedback
    """
    try:
        feedback = Feedback.objects.get(id=feedback_no)
    except Feedback.DoesNotExist:
        raise Http404('Feedback does not exist!')
    return render_to_response(
        'sitedata/feedback.html',
        {
            'feedback': feedback,
        }
    )


def feedback_add(request, url=None):
    """add feedback
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sitedata:feedback_index')
    else:
        form = FeedbackForm()
        if url is not None:
            form.fields['linked_post'].initial = unquote(url)
        feedback_id = Feedback.objects.order_by('-published')[0].id + 1
        return render(
            request,
            'sitedata/feedback_add.html',
            {
                'feedback_id': feedback_id,
                'form': form,
            }
        )
