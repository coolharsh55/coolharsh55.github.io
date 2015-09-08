"""editor config for harshp.com
"""

# ####### CKEDITOR START ##########
CKEDITOR_UPLOAD_PATH = '/media/'
CKEDITOR_JQUERY_URL = '''
    //ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js'''
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
# ####### CKEDITOR END ############


# ####### REDACTOR START ############
REDACTOR_OPTIONS = {
    'lang': 'en',
    'plugins': [
        'filemanager',
        'fontcolor',
        'fontfamily',
        'fontsize',
        'fullscreen',
        'imagemanager',
        'table',
    ]
}
REDACTOR_UPLOAD = '/media/'
# ####### REDACTOR END ##############
