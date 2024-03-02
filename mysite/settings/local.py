from .base import *
ALLOWED_HOSTS = ['*']
ADMINS = [
    ('Antonio M', 'sayeem.shaikh@gmail.com'),
]
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1:81')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL
