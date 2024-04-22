"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

import environ
from split_settings.tools import include
from pathlib import Path
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    DJANGO_ENV=(str, 'development'),
    REDIS_URL=(str, 'redis://:{password}@{host}:{port}'.format(
        password=getenv('REDIS_PASSWORD', 'redis'),
        host=getenv('REDIS_HOST', 'redis'),
        port=getenv('REDIS_PORT', '6379'),
    )),
    CELERY_DEFAULT_QUEUE=(str, 'ecoinomy'),
)

ENV = env('DJANGO_ENV').replace("\r", "")

modular_settings = [
    f'{ENV}.py',
]

# Include settings:
include(*modular_settings)