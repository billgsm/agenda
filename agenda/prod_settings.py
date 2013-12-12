import os

from credentials import *
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'agenda',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = login
EMAIL_HOST_PASSWORD = password
EMAIL_PORT = 587
