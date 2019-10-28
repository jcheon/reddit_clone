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
            suggestion = form.cleaned_data["suggestion"],
            image = form.cleaned_data["image"],
            image_description = form.cleaned_data["image_description"],
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

# from django import forms
# from django.core.validators import validate_slug
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User, AnonymousUser

# # Creates a class which will accept user input, max length 240 and store it in the suggestioin variable
# # a form is meant for accepting user input in some fashion

# class SuggestionForm(forms.Form):
# 	suggestion = forms.CharField(label='Input', max_length=240, validators=[validate_slug]) # suggestion name is arbitrary, this is used for checking validity

# class CommentForm(forms.Form):
#     comment = forms.CharField(label='Comment', max_length=240, validators=[validate_slug])

#     def save(self, request, sugg_id, commit=True):
#         sugg_instance = models.Suggestion.objects.get(id=sugg_id)
#         new_comm = models.Comment(
#             suggestion=sugg_instance,
#             comment=self.cleaned_data["comment"])
#         new_comm.author = request.user
#         if commit:
#             new_comm.save()
#         return new_comm

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(
#         label="Email",
#         required=True
#         )

#     class Meta:
#         model = User
#         fields = ("username", "email",
#                   "password1", "password2")

#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user