"""Social Meta Tags generator
    Creates and returns a Meta object
    OpenGraph(Facebook), Twitter, and Schema.org(G+)
"""

# load meta app settings
from django.conf import settings


def create_meta(title, description, keywords, url, image=None):
    """Create Meta Object
    create meta object containing the common meta tags
    Args:
        title(str)
        description(str)
        keywords(list)
        url(url)
        image(url)
    Returns:
        dict
    Raises:
        ValueError: field not found
    """
    meta = {}

    if settings.META_USE_OG_PROPERTIES:
        meta['use_og'] = True
        meta['use_facebook'] = True
    if settings.META_USE_TWITTER_PROPERTIES:
        meta['use_twitter'] = True
        meta['twitter_site'] = 'coolharsh55'
        meta['twitter_creator'] = 'coolharsh55'
    if settings.META_USE_GOOGLEPLUS_PROPERTIES:
        meta['use_googleplus'] = True
    if not title:
        raise ValueError('Missing Title in meta tags')
    meta['title'] = title
    # meta['object_type'] = 'article'
    if not description:
        raise ValueError('Missing description in meta tags')
    meta['description'] = description
    if not keywords:
        raise ValueError('Missing keywords in meta tags')
    meta['keywords'] = keywords
    if not url:
        raise ValueError('Missing url in meta tags')
    meta['url'] = url
    if image:
        meta['image'] = image
    return meta
