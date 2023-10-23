# import the necessary packages
from django.conf import settings
from celery import Celery
import os

# set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rescue_ripple.settings")

# instantiate the Celery app
app = Celery("rescue_ripple")

# add Django's settings as a configuration source for Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# load task modules from all registered Django app configs
app.autodiscover_tasks()
