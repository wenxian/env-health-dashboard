from env_health_dashboard_site.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Avoid Bad Request(400) Error https://docs.djangoproject.com/en/1.6/ref/settings/#std%3asetting-ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '.com', # Allow domain and subdomains
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.getenv("LOGGING_DIR") + '/envhealthdashboard_django.log',
            },
        },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        },
    }
