"""views for Hobbies

    hobby_index: hobby homepage/index
    type_index: generic index for hobby types
    type_item: generic item page for hobby type instance

    supported hobby types:
        Book, Movie, TV Show, Game
"""

from django.shortcuts import render_to_response
from django.shortcuts import Http404
from django.apps import apps

# from hobbies.models import Book
# from hobbies.models import Movie
# from hobbies.models import TVShow
# from hobbies.models import Game

_MODELS = apps.get_app_config('hobbies')

"""TYPE PROPERTIES
Descriptions for various hobby types for use by type_generator
"""
_TYPE_PROPERTIES = {
    'book': (
        lambda i: i.finished,  # condition
        'date_start',  # date start
        'date_end',  # date end
        'Started Reading',  # msg start
        'Stopped Reading',  # msg stop
        'Finished Reading',  # msg end
        'Reading since',  # msg continuation
    ),

    'movie': (
        lambda i: i.finished,  # condition
        'date_seen',  # date start
        None,  # date end
        None,  # msg start
        None,  # msg stop
        'Watched',  # msg end
        'Watched incomplete',  # msg continuation
    ),

    'tvshow': (
        lambda i: i.finished,  # condition
        'date_start',  # date start
        'date_end',  # date end
        'Started Watching',  # msg start
        'Stopped Watching',  # msg stop
        'Finished Watching',  # msg end
        'Watching since',  # msg continuation
    ),

    'game': (
        lambda i: i.finished,  # condition
        'date_start',  # date start
        'date_end',  # date end
        'Started Playing',  # msg start
        'Stopped Playing',  # msg stop
        'Finished Playing',  # msg end
        'Playing since',  # msg continuation
    ),
}


def _type_generator(objects):
    """Template data generator for given type

    Will extract objects from given iterable and save it along with
    its description in a list of tuples. Assumes that the fields
    `date_start` and `date_end` are present.

    Args:
        objects(iterable): iterable of objects to be processed
    Returns:
        list: list of tuples in the format: (object, description)
    Raises:
        None
    """

    assert hasattr(objects, '__iter__')

    condition, date_start, date_end, msg_start, msg_stop, msg_end, \
        msg_continuation = _TYPE_PROPERTIES[objects[0]._meta.model_name]

    items = []

    for obj in objects:
        # if I've finished with the hobby
        if condition(obj) and date_end:
            description = "%s: %s. %s: %s." % (
                msg_start, getattr(obj, date_start),
                msg_end, getattr(obj, date_end),
            )
        # if I've left the hobby incomplete
        elif date_end and getattr(obj, date_end):
            description = "%s: %s. %s: %s." % (
                msg_start, getattr(obj, date_start),
                msg_stop, getattr(obj, date_end),
            )
        # I'm still doing the hobby, or it's a continous one
        else:
            if condition(obj):
                msg = msg_end
            else:
                msg = msg_continuation
            description = "%s: %s." % (
                msg, getattr(obj, date_start),
            )
        items.append((obj, description))
    return items


def type_index(request, hobbytype):
    """Generic index for 'type'

    Generates index views for:
        Books
        Movies
        TV Shows
        Games

    Args:
        request(HttpRequest)
        hobbytype(str): parameter specifying the hobby
    Returns:
        HttpResponse: 200 on success, 404 on error

    Raises:
        Http404 on error
    """
    items = None
    for model in _MODELS.get_models():
        if ''.join((model._meta.model_name, 's')) == hobbytype:
            items = _type_generator(objects=model.objects.all())
    if items is None:
        raise Http404('%s is not really my kind of Hobby!' % hobbytype)

    return render_to_response(
        'hobbies/type_index.html',
        {
            'items': items,
            'urlstag': 'hobbies:' + hobbytype[:-1],
            'hobbytype': hobbytype,
        }
    )


def hobby_index(request):
    """Index view for all hobbies

    Shows 5 latest items from hobbies:
        Book, Movie, TV Show, Game

    Args:
        request(HttpRequest)

    Returns:
        HttpResponse: 200 on success

    Raises:
        None
    """
    hobbyitems = []
    for model in _MODELS.get_models():
        hobbyitems.append((
            model.__name__,
            ''.join((model._meta.model_name, 's')),
            _type_generator(objects=model.objects.all()[:5]),
            ':'.join(('hobbies', model._meta.model_name)),
        ))

    return render_to_response(
        'hobbies/hobby_index.html',
        {
            'hobbies': hobbyitems,
        },
    )


def type_item(request, hobbytype, hobbytitle):
    """
    """
    item = None
    for model in _MODELS.get_models():
        if ''.join((model._meta.model_name, 's')) == hobbytype:
            try:
                item = _type_generator(
                    objects=[model.objects.get(slug=hobbytitle)]
                )[0]
            except model.DoesNotExist:
                raise Http404("%s is not something I've tried" % hobbytitle)
    if item is None:
        raise Http404('%s is not really my kind of Hobby!' % hobbytype)
    return render_to_response(
        'hobbies/type_item.html',
        {
            'item': item[0],
            'description': item[1],
            'hobbytype': hobbytype,
        }
    )
