# STEP 4, create view

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db import transaction
import json
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
        url = "Error.src"
        url1 = "Error.src"
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
                "upvote_count":s_q.upvoteCount(),
                "downvote_count":s_q.downvoteCount(),
                "total_votes":s_q.totalVotes(),
                "subreddit":s_q.title,
                "comments":comment_list,
                "comment_count":s_q.comment_count,
                "image":url,
                "image_description":s_q.image_description, # These are what I use to call from index
                "video":url1,
                "video_description":s_q.video_description
                }]
    context = {
        "variable":"Hello World",
        "title":"reddit: the front page of the internet",
        #"karma":request.user.profile.karma,
        "form":form_instance,
        "sugg_list":suggestion_list["suggestions"]
    }
    return render(request, "index.html", context=context)



@csrf_exempt
# @login_required(login_url='/login/')
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
            url = "Error.src"
            url1 = "Error.src"
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
                "upvote_count":s_q.upvoteCount(),
                "downvote_count":s_q.downvoteCount(),
                "total_votes":s_q.totalVotes(),
                "subreddit":s_q.title,
                "comments":comment_list,
                "comment_count":s_q.comment_count,
                "image":url,
                "image_description":s_q.image_description, 
                "video":url1,
                "video_description":s_q.video_description
                }]
        return JsonResponse(suggestion_list)
    return HttpResponse("Unsupported HTTP Method")

@login_required(login_url='/login/')
def suggestion_form_view(request, subreddit_title):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.SuggestionForm(request.POST, request.FILES)
            if form_instance.is_valid():
                new_sugg = form_instance.save(request=request,url=subreddit_title)
                return redirect("/")
        else:
            return redirect("/")
    else:
        form_instance = forms.SuggestionForm()
    context = {
        "title":"Suggestion Form",
        "form":form_instance,
        "title":subreddit_title
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

@login_required(login_url='/login/')
def upvote(request, instance_id):
    sugg = models.Suggestion.objects.get(id=instance_id)
    sugg.upvote += 1
    sugg.save()
    return HttpResponse(status=204)

@login_required(login_url='/login/')
def downvote(request, instance_id):
    sugg = models.Suggestion.objects.get(id=instance_id)
    sugg.downvote -= 1
    sugg.save()
    return HttpResponse(status=204)
   

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
        subreddit_list = {"subreddits":[]}
        for s in subreddit_query:
            subreddit_list["subreddits"] += [{
                "id":s.id,
                "title":s.title,
            }]
        return JsonResponse(subreddit_list)
    return HttpResponse("Unsupported HTTP method")
            

def success(request, subreddit_title):
    suggestion_query = models.Suggestion.objects.all()
    suggestion_list = {"suggestions":[]}

    for s_q in suggestion_query:
        if(s_q.title == subreddit_title):
            comment_query = models.Comment.objects.filter(suggestion=s_q)
            comment_list = []
            for c_q in comment_query:
                comment_list += [{
                "comment":c_q.comment,
                "author":c_q.author.username,
                "created_on":c_q.created_on,
                "id":c_q.id,
                }]
            url = "Error.src"
            url1 = "Error.src"
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
                    "upvote_count":s_q.upvoteCount(),
                    "downvote_count":s_q.downvoteCount(),
                    "total_votes":s_q.totalVotes(),
                    "subreddit":s_q.title,
                    "comments":comment_list,
                    "comment_count":s_q.comment_count,
                    "image":url,
                    "image_description":s_q.image_description, # These are what I use to call from index
                    "video":url1,
                    "video_description":s_q.video_description
                    }]
    context = {
        "sugg_list":suggestion_list["suggestions"],
        "karma":request.user.profile.karma,
        "subreddit":subreddit_title
    }
    return render(request, "subreddit.html", context=context)



def post_page(request, instance_id):
    author = ""
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.CommentForm(request.POST)
            if form_instance.is_valid():
                new_comm = form_instance.save(request=request, sugg_id=instance_id)
                sugg = models.Suggestion.objects.get(id=instance_id)
                sugg.comment_count += 1
                sugg.save()
                return redirect("/post/" + str(instance_id) + "/")
        else:
            form_instance = forms.CommentForm()
    else:
        form_instance = forms.CommentForm()

    suggestion_query = models.Suggestion.objects.all()
    suggestion_list = {"suggestions":[]}

    for s_q in suggestion_query:
        if(s_q.id == instance_id):
            comment_query = models.Comment.objects.filter(suggestion=s_q)
            comment_list = []
            for c_q in comment_query:
                comment_list += [{
                "comment":c_q.comment,
                "author":c_q.author.username,
                "created_on":c_q.created_on,
                "id":c_q.id,
                }]
            url = "Error.src"
            url1 = "Error.src"
            if not str(s_q.image)=="":
                url=s_q.image.url
            if not str(s_q.video)=="":
                url1=s_q.video.url
            author = s_q.author.username
            suggestion_list["suggestions"] += [{
                    "id":s_q.id,
                    "header":s_q.header,
                    "suggestion":s_q.suggestion,
                    "author":s_q.author.username,
                    "created_on":s_q.created_on,
                    "published_on":s_q.whenpublished(),
                    "upvote_count":s_q.upvoteCount(),
                    "downvote_count":s_q.downvoteCount(),
                    "total_votes":s_q.totalVotes(),
                    "subreddit":s_q.title,
                    "comments":comment_list,
                    "comment_count":s_q.comment_count,
                    "image":url,
                    "image_description":s_q.image_description, # These are what I use to call from index
                    "video":url1,
                    "video_description":s_q.video_description
                    }]
    aUser = User.objects.get(username = author)
    context = {
        "form":form_instance,
        "user":author,
        "request_user":request.user.username,
        "sugg_list":suggestion_list["suggestions"],
        "karma":aUser.profile.karma,
        "request_karma":request.user.profile.karma,
        "sugg_id":instance_id
    }

    return render(request, "post.html", context=context)


def show_subreddits(request):
    return render(request, "subreddits.html")


# Added this
def chat(request):
    return render(request, 'chat/chatmain.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name_json': mark_safe(json.dumps(room_name))})


def chatroom_form_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = forms.ChatForm(request.POST)
            if form.is_valid():
                new_chatroom = form.save(request=request)
                return redirect('/chat/' + new_chatroom.name + '/')
        else:
            return redirect("/createChat/")
    else:
        form = forms.ChatForm()
    return render(request, "chat/createChat.html", {"form":form})


def created_chatrooms(request):
    if request.method == "GET":
        chat_query = models.chatroom.objects.all()
        chatroom_list = {"chatrooms":[]}
        for room in chat_query:
            chatroom_list["chatrooms"] += [{
                "name":room.name
            }]
        return JsonResponse(chatroom_list)
    return HttpResponse("Unsupported HTTP method")

def profiles(request, user_name):
    name = ""
    date = request.user.date_joined

    user_post_query = models.Suggestion.objects.all().order_by('-created_on')
    post_list = {"posts":[]}

    for p in user_post_query: 
        if(str(p.author) == str(user_name)):
            url = "Error.src"
            url1 = "Error.src"
            if not str(p.image)=="":
                url=p.image.url
            if not str(p.video)=="":
                url1=p.video.url
            name = p.author
            post_list["posts"] += [{
                "id":p.id,
                "header":p.header,
                "user":p.author,
                "suggestion":p.suggestion,
                "author":p.author.username,
                "created_on":p.created_on,
                "published_on":p.whenpublished(),
                "upvote_count":p.upvoteCount(),
                "downvote_count":p.downvoteCount(),
                "total_votes":p.totalVotes(),
                "comment_count":p.comment_count,
                "subreddit":p.title,
                "image":url,
                "image_description":p.image_description, # These are what I use to call from index
                "video":url1,
                "video_description":p.video_description
                }]
    aUser = User.objects.get(username = name)
    if aUser.profile.avatar == "":
        anAvatar = '/static/images/default.png'
    else:
        anAvatar = aUser.profile.avatar
    
    context = {
        "name": user_name,
        "request_name": request.user.username,
        "date": date,
        "karma": aUser.profile.karma,
        "bio": aUser.profile.bio,
        "birthday": aUser.profile.birth_date,
        "avatar": anAvatar,
        "posts": post_list["posts"]
    }
    return render(request, "profiles.html", context=context)


def getSubPosts(request, subreddit_title):
    if request.method == "GET":
        suggestion_query = models.Suggestion.objects.all().order_by('-created_on')
        suggestion_list = {"suggestions":[]}
        for s_q in suggestion_query:
            if(s_q.title == subreddit_title):
                url = "Error.src"
                url1 = "Error.src"
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
                    "upvote_count":s_q.upvoteCount(),
                    "downvote_count":s_q.downvoteCount(),
                    "total_votes":s_q.totalVotes(),
                    "subreddit":s_q.title,
                    "comment_count":s_q.comment_count,
                    "image":url,
                    "image_description":s_q.image_description, # These are what I use to call from index
                    "video":url1,
                    "video_description":s_q.video_description
                    }]
        return JsonResponse(suggestion_list)
    return HttpResponse("Unsupported HTTP Method")



def getPost(request, instance_id):
    if request.method == "GET":
        suggestion_query = models.Suggestion.objects.all().order_by('-created_on')
        suggestion_list = {"suggestions":[]}
        for s_q in suggestion_query:
            if(s_q.id == instance_id):
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
                url = "Error.src"
                url1 = "Error.src"
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
                    "upvote_count":s_q.upvoteCount(),
                    "downvote_count":s_q.downvoteCount(),
                    "total_votes":s_q.totalVotes(),
                    "subreddit":s_q.title,
                    "comments":comment_list,
                    "comment_count":s_q.comment_count,
                    "image":url,
                    "image_description":s_q.image_description, # These are what I use to call from index
                    "video":url1,
                    "video_description":s_q.video_description
                    }]
        return JsonResponse(suggestion_list)
    return HttpResponse("Unsupported HTTP Method")

def getUserPosts(request, user_name):
    if request.method == "GET":
        suggestion_query = models.Suggestion.objects.all().order_by('-created_on')
        suggestion_list = {"suggestions":[]}
        for s_q in suggestion_query:
            if(str(s_q.author) == str(user_name)):
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
                url = "Error.src"
                url1 = "Error.src"
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
                    "upvote_count":s_q.upvoteCount(),
                    "downvote_count":s_q.downvoteCount(),
                    "total_votes":s_q.totalVotes(),
                    "subreddit":s_q.title,
                    "comments":comment_list,
                    "comment_count":s_q.comment_count,
                    "image":url,
                    "image_description":s_q.image_description, # These are what I use to call from index
                    "video":url1,
                    "video_description":s_q.video_description
                    }]
        return JsonResponse(suggestion_list)
    return HttpResponse("Unsupported HTTP Method")


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('/profiles/' + request.user.username + '/')
    else:
        profile_form = forms.ProfileForm(instance=request.user.profile)
    return render(request, 'registration/updateProfile.html', {
        'profile_form': profile_form
    })


def giveKarma(request, user_name, post_id):
    aUser = User.objects.get(username = user_name)

    if request.method == 'GET':
        karma = request.GET.get('karma')
        if int(request.user.profile.karma) > 0:
            if int(karma) <= int(request.user.profile.karma):
                aUser.profile.karma = int(karma) + aUser.profile.karma
                aUser.save()

                total = request.user.profile.karma - int(karma)

                request.user.profile.karma = total
                request.user.save()
            elif int(karma) > int(request.user.profile.karma):
                userTotal = request.user.profile.karma +  aUser.profile.karma
                aUser.profile.karma = userTotal
                aUser.save()
                request.user.profile.karma = 0
                request.user.save()


    return redirect("/post/" + str(post_id) + "/")

