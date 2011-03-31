import os
import sys
import site

PROJECT_ROOT = '/home/nick/code/python/beersocial/src'
site_packages = '/home/nick/code/python/beersocial/lib/python2.6/site-packages'

site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(1, site_packages)
os.environ['DJANGO_SETTINGS_MODULE'] = 'beersocial.staging_settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/nick/.python-eggs'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()