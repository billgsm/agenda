DEBUG = True
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
##################################################################
############First one works#######################################
##################################################################
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
##################################################################
############Second one works######################################
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/bilou/Documents/projects/github/agenda/django_dev_emails'
##################################################################
############Third one works#######################################
##################################################################
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'ad.dydict.min@gmail.com'
#EMAIL_HOST_PASSWORD = 'testsendingmail'
#EMAIL_PORT = 587
