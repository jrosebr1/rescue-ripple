# import the necessary packages
from django.contrib import admin
from . import models

# register models
admin.site.register(models.SocialMediaPost)
