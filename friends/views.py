"""views for friends
"""

from django.shortcuts import render_to_response


def sup_bday_2015(request):
    """sup bday 2015

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success

    Raises:
        None
    """
    return render_to_response('friends/sup_bday_2015.html')
