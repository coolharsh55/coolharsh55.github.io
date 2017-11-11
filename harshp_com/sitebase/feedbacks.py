from sitebase.models import Feedback


def attach_feedbacks(request, dictionary=None):
    url = request.build_absolute_uri()
    # FIXME: this is a stopgap measure for now
    url = url.replace('localhost:8000', 'harshp.com')
    feedbacks = Feedback.objects.filter(url=url)
    if dictionary:
        dictionary['feedbacks'] = feedbacks
        return
    return feedbacks
