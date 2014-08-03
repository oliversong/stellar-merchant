import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
ENV = 'development'

ADMINS = frozenset(['me@olli.es'])
SECRET_KEY = 'allyourbasearebelongtome'

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/astral'

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'allyourbaseyourbase'
