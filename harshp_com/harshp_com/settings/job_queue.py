"""settings for jobs and queues"""

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360
    }
}

RQ_JOBS_MODULE = tuple()
