"""subdomain config for harshp.com

"""

ROOT_URLCONF = 'harshp.urls'

SUBDOMAIN_URLCONFS = {
    None: 'harshp.urls',  # no subdomain, e.g. ``example.com``
    'www': 'harshp.urls',
    'admin': 'harshp.adminurls',
    'articles': 'articles.urls',
    'blog': 'blog.urls',
    'brainbank': 'brainbank.urls',
    'friends': 'friends.urls',
    'lifex': 'lifeX.urls',
    'poems': 'poems.urls',
    'stories': 'stories.urls',
    'hobbies': 'hobbies.urls',
    'dev': 'devblog.urls',
}
