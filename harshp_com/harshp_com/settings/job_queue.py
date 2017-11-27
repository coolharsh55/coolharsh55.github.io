"""settings for jobs and queues"""

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360
    },
    'gnib-worker': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360
    }
}

RQ_JOBS_MODULE = (
    'finance.jobs',
    'apps.jobs.gnib',
    )

CRON_CLASSES = (
    'apps.jobs.gnib.GnibAppointmentJob',
    )
