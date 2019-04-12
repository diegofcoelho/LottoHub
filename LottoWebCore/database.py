# encoding: utf-8
import os

from django.conf import settings

from LottoHub.settings import HEROKU, DEBUG

engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
    'oracle': 'mysql.connector.django',
}


def config():
    credentials = None
    #
    if HEROKU:
        credentials = {
            'ENGINE': engines['mysql'],
            'NAME': 'DATABASE',
            'USER': 'USER',
            'PASSWORD': 'PWD',
            'HOST': 'IP_ADDRESS',
            'PORT': 'PORT',
            'OPTIONS': {'charset': 'utf8mb4', 'init_command': "SET sql_mode='STRICT_TRANS_TABLES';"},
        }
    elif DEBUG:
        credentials = {
            'ENGINE': engines['sqlite'],
            'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
        }
    return credentials


