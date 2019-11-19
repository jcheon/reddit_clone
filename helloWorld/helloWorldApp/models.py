from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
import math


# Create your models here.
class Suggestion(models.Model):
    header = models.CharField(max_length=240)
    suggestion = models.CharField(max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    # upvote = models.IntegerField(default = 0)
    image = models.ImageField(max_length=144, upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    image_description = models.CharField(max_length=240, blank=True)
    video = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    video_description = models.CharField(max_length=240, blank=True)

    # downvote = models.IntegerField(default=0)

    def __str__(self):
        return self.author.username + " " + self.suggestion

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(models.Model):
    comment = models.CharField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + " " + self.comment

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Subreddit(models.Model):
    title = models.CharField(max_length=25)
    topics = models.CharField(max_length=25)
    description = models.TextField()
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    num_members = models.IntegerField(null=True)
    birthday = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(max_length=144, upload_to='subreddit/pic', null=True)
    image_description = models.CharField(max_length=240, null=True)

    def __str__(self):
        return self.title

# class Vote:
#     upvote = models.IntegerField(default=0)
#     downvote = models.IntegerField(default=0)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.author.username + " " + self.suggestion
