from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Suggestion)
admin.site.register(models.Comment)
admin.site.register(models.Subreddit)
admin.site.register(models.chatroom)
admin.site.register(models.Profile)


# from django.contrib import admin
# from . import models
# # Register your models here.


# admin.site.register(models.Suggestion)
# admin.site.register(models.Comment)

# #admin.site.register(models.Image)