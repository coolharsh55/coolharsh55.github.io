"""admin config for harshp.com

"""

ADMINS = (
    ('Harshvardhan Pandit', 'me@harshp.com'),
)

MANAGERS = ADMINS

# ####### SUIT ADMIN START ##########
SUIT_CONFIG = {
    'ADMIN_NAME': 'harshp.com',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'SEARCH_URL': 'admin:auth_user_changelist',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_ICONS': {
        'sites': 'icon-star',
        'auth': 'icon-lock',
    },
    'MENU': (
        {'app': 'robots', 'label': 'robots.txt', 'icon': 'icon-wrench'},
        'sites',
        {'app': 'blog', 'label': 'Blog', 'icon': 'icon-pencil'},
        {'app': 'stories', 'label': 'Stories', 'icon': 'icon-book'},
        {'app': 'poems', 'label': 'Poems', 'icon': 'icon-asterisk'},
        {'app': 'articles', 'label': 'Articles', 'icon': 'icon-tag'},
        {'app': 'brainbank', 'label': 'Brain Bank', 'icon': 'icon-qrcode'},
        {'app': 'lifex', 'label': 'Life X', 'icon': 'icon-road'},
        {'app': 'hobbies', 'label': 'Hobbies', 'icon': 'icon-time'},
        {'app': 'sitedata', 'label': 'Site data', 'icon': 'icon-wrench'},
    ),

}
# ####### SUIT ADMIN END ############
