"""check for duplicates in models
"""

from django.utils.text import slugify


def _validate(obj, slugfield, *args, **kwargs):
    """validate the parameters passed to duplicate methods
    """
    # get class of the object instance
    # this is the model used to make queries
    model = obj.__class__
    assert model is not None
    # assert we have some arguments to filter duplicates
    assert (len(args) > 0) or (len(kwargs) > 0)
    assert slugfield is not None
    try:
        # get the max length for the slug field
        slugfield_length = obj._meta.get_field('slug').max_length
    except Exception:
        raise AssertionError('is this a valid django model instance?')

    return slugfield_length


def _query_duplicates(model, *args, **kwargs):
    """query the model to search for duplicates
    this is just a stub to run the query
    """
    dup = model.objects.filter(*args, **kwargs)

    return len(dup)


def _make_duplicate_slug(slugfield, slugfield_length, nos_dups):
    """create a slug from the slugfield of the given length
    """
    nos = str(nos_dups)
    slug = slugify(slugfield[:slugfield_length - len(nos)] + '-' + nos)

    return slug


def duplicate_slug_vanilla(obj, slugfield, *args, **kwargs):
    """assign unique slug even when object is a duplicate

    checks if the object is duplicate by filtering similar
    objects from the database
    if a duplicate, appends a number to the front of the slug
    depicting the index of current object amongst duplicates
    the index is based on published date

    to be used before primary key is assigned

    Args:
        obj(object): object instance
        slugfield(str): field used for creating slug

    Returns:
        str: slug

    Raises:
        None
    """
    slugfield_length = _validate(obj, slugfield, *args, **kwargs)

    # make the query to get duplicates
    # duplicates for this objects are all objects with the same
    # parameters that have been published previously
    nos_dups = _query_duplicates(obj.__class__, *args, **kwargs)

    if nos_dups > 0:
        # there are duplicates, let's append an index
        slug = _make_duplicate_slug(slugfield, slugfield_length, nos_dups)
    else:
        # there are no duplicates
        slug = slugify(slugfield)

    return slug


def duplicate_slug(obj, slugfield, *args, **kwargs):
    """assign unique slug even when object is a duplicate

    checks if the object is duplicate by filtering similar
    objects from the database
    if a duplicate, appends a number to the front of the slug
    depicting the index of current object amongst duplicates
    the index is based on published date

    Args:
        obj(object): object instance
        slugfield(str): field used for creating slug

    Returns:
        str: slug

    Raises:
        None
    """
    slugfield_length = _validate(obj, slugfield, *args, **kwargs)

    # make the query to get duplicates
    # duplicates for this objects are all objects with the same
    # parameters that have been published previously
    nos_dups = _query_duplicates(
        obj.__class__, *args, published__lt=obj.published, **kwargs)

    if nos_dups > 0:
        # there are duplicates, let's append an index
        slug = _make_duplicate_slug(slugfield, slugfield_length, nos_dups + 1)
    else:
        # there are no duplicates
        slug = slugify(slugfield)

    return slug
