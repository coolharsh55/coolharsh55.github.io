"""urls configuration for harshp_com"""

ROOT_URLCONF = 'harshp_com.urls'

SITE_ID = 86

SUBDOMAIN_URLCONFS = {
    # base
    None: 'harshp_com.urls',
    'www': 'harshp_com.urls',

    # admin
    'admin': 'harshp_com.adminurls',

    # creative & writing
    # 'articles': 'articles.urls',
    'blog': 'blog.urls',
    # 'poems': 'poems.urls',
    # 'stories': 'stories.urls',

    # personal
    # 'friends': 'friends.urls',
    # 'hobbies': 'hobbies.urls',
    # 'journal': 'journal.urls',
    # 'lifeX': 'lifeX.urls',

    # research / dev / compsci
    # 'brainbank': 'brainbank.urls',
    # 'dev': 'devblog.urls',
    # 'research': 'research.urls',

    # about me
    # 'me': 'me.urls',
}
