from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


# This provides the data type of each field of my form
class SuggestionForm(forms.Form):
    suggestion = forms.CharField(label='Post', max_length=1000) # label shows up on actual form
    image = forms.ImageField(label = 'Image File')
    image_description = forms.CharField(label = 'Image Description', max_length = 100)

    def save(self, request, commit=True):
        new_sugg = models.Suggestion(
            suggestion = self.cleaned_data["suggestion"],
            image = self.cleaned_data["image"],
            image_description = self.cleaned_data["image_description"],
            author = request.user
            )

        if commit:
            new_sugg.save()
        return new_sugg

class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=1000) #validators=[validate_slug]

    def save(self, request, sugg_id, commit=True):
        sugg_instance = models.Suggestion.objects.get(id=sugg_id)
        new_comm = models.Comment(
            suggestion=sugg_instance,
            comment=self.cleaned_data["comment"])
        new_comm.author = request.user
        if commit:
            new_comm.save()
        return new_comm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class SubredditForm(forms.Form):
    TOPIC_CHOICES=[
        ('activism', 'Activism'),
        ('advice', 'Advice'),
        ('animal', 'Animal'),
        ('anime', 'Anime'),
        ('art', 'Art'),
        ('beauty', 'Beauty'),
        ('careers', 'Careers'),
        ('cars', 'Cars'),
        ('celebrity', 'Celebrity'),
        ('crypto', 'Crypto'),
        ('entertainment', 'Entertainment'),
        ('family & relationship', 'Family & Relationship'),
        ('fitness', 'Fitness'),
        ('food & drink', 'Food & Drink'),
        ('funny & humor', 'Funny & Humor'),
        ('Health & Wellbeing', 'Health & Wellbeing'),
        ('help', 'Help'),
        ('history', 'History'),
        ('home & garden', 'Home & Garden'),
        ('internet culture', 'Internet Culture'),
        ('learning culture', 'Learning Culture'),
        ('learning', 'Learning'),
        ('mature themes', 'Mature Themes'),
        ('men\'s fashion', 'Men\'s Fasion'),
        ('movies', 'Movies'),
        ('nature', 'Nature'),
        ('news', 'News'),
        ('outdoors', 'Outdoors'),
        ('parenting', 'Parenting'),
        ('pets', 'Pets'),
        ('place', 'Place'),
        ('politics', 'Politics'),
        ('programming', 'Programming'),
        ('reaction fuel', 'Reaction Fuel'),
        ('reading & literature', 'Reading & Literature'),
        ('religion & spirituality', 'Religion & Spirituality'),
        ('science', 'Science'),
        ('sports', 'Sports'),
        ('style', 'Style'),
        ('tabletop games', 'Tabletop Games'),
        ('technology', 'Technology'),
        ('television', 'Television'),
        ('travel', 'Travel'),
        ('video gaming', 'Video Gaming'),
        ('women\'s fashion', 'Women\'s Fasion'),
    ]


    title = forms.CharField(label='Name', max_length=25)
    topics = forms.CharField(label='What\'s the topic?', widget=forms.Select(choices=TOPIC_CHOICES))
    description = forms.CharField(max_length=240)
    # image = forms.ImageField(label = 'Subreddit logo')

    def save(self, request, commit=True):
        new_subreddit = models.Subreddit(
            title = self.cleaned_data["title"],
            topics = self.cleaned_data["topics"],
            description = self.cleaned_data["description"],
            # image = self.cleaned_data["image"],
        )
        if commit:
            new_subreddit.save()
        return new_subreddit

