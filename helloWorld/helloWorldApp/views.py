# STEP 4, create view

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# from django.contrib.auth.models import User

from . import models
from . import forms


# Create your views here.
def index(request, page=0):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.SuggestionForm(request.POST)
            if form_instance.is_valid():
                new_sugg = models.Suggestion(suggestion=form_instance.cleaned_data["suggestion"])
                new_sugg.author = request.user
                new_sugg.save()
                form_instance = forms.SuggestionForm()
        else:
            form_instance = forms.SuggestionForm()
    else:
        form_instance = forms.SuggestionForm()
    suggestion_query = models.Suggestion.objects.all()
    suggestion_list = {"suggestions":[]}
    for s_q in suggestion_query:
        comment_query = models.Comment.objects.filter(suggestion=s_q)
        comment_list = []
        for c_q in comment_query:
            can_delete=False
            if request.user == c_q.author:
                can_delete=True
            comment_list += [{
            "comment":c_q.comment,
            "author":c_q.author.username,
            "created_on":c_q.created_on,
            "id":c_q.id,
            "delete":can_delete
            }]
        suggestion_list["suggestions"] += [{
            "id":s_q.id,
            "header":s_q.header,
            "suggestion":s_q.suggestion,
            "author":s_q.author.username,
            "created_on":s_q.created_on,
            "image":s_q.image,
            "image_description":s_q.image_description,
            "video":s_q.video,
            "video_description":s_q.video_description,
            "comments":comment_list
            }]
    context = {
        "variable":"Hello World",
        "title":"reddit: the front page of the internet",
        "form":form_instance,
        "some_list":suggestion_list["suggestions"]
    }
    return render(request, "index.html", context=context)

@csrf_exempt
@login_required(login_url='/login/')
def suggestions_view(request):
    if request.method == "GET":
        suggestion_query = models.Suggestion.objects.all().order_by('-created_on')
        suggestion_list = {"suggestions":[]}
        for s_q in suggestion_query:
            comment_query = models.Comment.objects.filter(suggestion=s_q)
            comment_list = []
            for c_q in comment_query:
                can_delete=False
                if request.user == c_q.author:
                    can_delete=True
                comment_list += [{
                "comment":c_q.comment,
                "author":c_q.author.username,
                "created_on":c_q.created_on,
                "published_on":c_q.whenpublished(),
                "id":c_q.id,
                "delete":can_delete
                }]
            url = ""
            url1 = ""
            if not str(s_q.image)=="":
                url=s_q.image.url
            if not str(s_q.video)=="":
                url1=s_q.video.url
            suggestion_list["suggestions"] += [{
                "id":s_q.id,
                "header":s_q.header,
                "suggestion":s_q.suggestion,
                "author":s_q.author.username,
                "created_on":s_q.created_on,
                "published_on":s_q.whenpublished(),
                "comments":comment_list,
                "image":url,
                "image_description":s_q.image_description, # These are what I use to call from index
                "video":url1,
                "video_description":s_q.video_description
                }]
        return JsonResponse(suggestion_list)
    return HttpResponse("Unsupported HTTP Method")

@login_required(login_url='/login/')
def comments_view(request, instance_id, delete=0):
    if delete==1:
        print("Should delete the comment here")
        instance = models.Comment.objects.get(id=instance_id)
        if request.user == instance.author:
            instance.delete()
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.CommentForm(request.POST)
            if form_instance.is_valid():
                new_comm = form_instance.save(request=request, sugg_id=instance_id)
                return redirect("/")
        else:
            form_instance = forms.CommentForm()
    else:
        form_instance = forms.CommentForm()
    context = {
        "title":"Comment Form",
        "form":form_instance,
        "sugg_id":instance_id
    }
    return render(request, "comment.html", context=context)




# This handles all of the redirection of user actions
# If they click something on the form what happens and where they go
@login_required(login_url='/login/')
def suggestion_form_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.SuggestionForm(request.POST, request.FILES)
            if form_instance.is_valid():
                new_sugg = form_instance.save(request=request)
                return redirect("/")
        else:
            return redirect("/")
    else:
        form_instance = forms.SuggestionForm()
    context = {
        "title":"Suggestion Form",
        "form":form_instance
    }
    return render(request, "suggestion.html", context=context)



def logout_view(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
            # print("Hi")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

# @login_required(login_url='/login/')
# def vote(request, instance_id):
#     # if delete == 1:
#     #     instance = models.Vote.objects.get(id=instance_id)
#     #     if request.user == instance.author:
#     #         instance.delete()
#     #     return redirect("/")
#     if request.method == "POST":
#         if request.user.is_authenticated:

#Subreddit views
def create_subreddit(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = forms.SubredditForm(request.POST)
            if form.is_valid():
                new_subreddit = form.save(request=request)
                return redirect('/r/' + form.data['title'])
        else:
            return redirect("/create_subreddit/")
    else:
        form = forms.SubredditForm()

    context = {
        "title":"Subreddit Form",
        "form":form,
    }
    return render(request, "subreddit_create.html", context=context)

def created_subreddits(request):
    if request.method == "GET":
        subreddit_query = models.Subreddit.objects.all()
        subreddit_list = {"subreddit":[]}
        for s in subreddit_query:
            subreddit_list["subreddit"] += [{
                "id":s.id,
                "title":s.title,
            }]
        return JsonResponse(subreddit_list)
    return HttpResponse("Unsupported HTTP method")
            

def success(request, subreddit_id):
    #TODO: add views here for new subreddit created
    return render(request, "subreddit.html")



