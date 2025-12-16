
# alx_travel_app/settings/test.py
from .base import *

DEBUG = False

# Use MySQL for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME', 'test_db'),
        'USER': os.getenv('DATABASE_USER', 'test_user'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'test_password'),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'TEST': {
            'NAME': 'test_db',
        },
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable Celery for testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Chapa test mode
CHAPA_TEST_MODE = True

# Media files for testing
MEDIA_ROOT = '/tmp/media_test'
