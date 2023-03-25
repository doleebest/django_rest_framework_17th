from .base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('everytime'),
        'USER': env('root'),
        'PASSWORD': env('0000'),
        'HOST': env('localhost'),
        'PORT': env('3306'),
    }
}