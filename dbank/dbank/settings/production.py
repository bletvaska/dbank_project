from .base import *

ALLOWED_HOSTS = ['atlantis.cnl.sk']

INSTALLED_APPS += [
    'mod_wsgi.server'
]

WSGI_APPLICATION = 'dbank.wsgi.application'
