from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Suggestion)
admin.site.register(models.Comment)
admin.site.register(models.Subreddit)


# from django.contrib import admin
# from . import models
# # Register your models here.


# admin.site.register(models.Suggestion)
# admin.site.register(models.Comment)

# #admin.site.register(models.Image)