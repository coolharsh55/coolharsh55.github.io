"""Utils for Django Models"""


def get_unique_slug(model, obj, field, **kwargs):
    """Get unique slug for given object.
    The unique slug is created based on the specified field
    for the given object which is an instance of the specified
    model. If the slug exists, it is suffixed with a number to
    make it unique.

    Args:
     - model: Django Model
     - obj: Model object
     - field: string reference to field for unique string

    Returns:
        str: unique slug
    """

    slug = getattr(obj, field)
    count = model.objects.filter(**kwargs).count()
    if count > 0:
        slug = '{}-{}'.format(slug, count)
    return slug
