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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

##################################################################
############Second one works######################################
##################################################################
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = project_path + '/django_dev_emails'
