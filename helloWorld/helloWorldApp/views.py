# STEP 4, create view

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
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
            "suggestion":s_q.suggestion,
            "author":s_q.author.username,
            "created_on":s_q.created_on,
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
            if not str(s_q.image)=="":
                url=s_q.image.url
            suggestion_list["suggestions"] += [{
                "id":s_q.id,
                "suggestion":s_q.suggestion,
                "author":s_q.author.username,
                "created_on":s_q.created_on,
                "published_on":s_q.whenpublished(),
                "comments":comment_list,
                "image":url,
                "image_description":s_q.image_description # These are what I use to call from index
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


# Subreddit views
# @login_required(login_url='/login/')
def subreddit(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form_instance = forms.SubredditForm(request.POST)
            if form_instance.is_valid():
                new_subreddit = form_instance.save(request=request)
                return redirect("../")
        else:
            return redirect("/r/")
    else:
        form_instance = forms.SubredditForm()

    context = {
        "title":"Subreddit Form",
        "form":form_instance,
    }
    return render(request, "subreddit.html", context=context)




# @login_required(login_url='/login/')
# def suggestion_form_view(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             form_instance = forms.SuggestionForm(request.POST, request.FILES)
#             if form_instance.is_valid():
#                 new_sugg = form_instance.save(request=request)
#                 return redirect("/")
#         else:
#             return redirect("/")
#     else:
#         form_instance = forms.SuggestionForm()
#     context = {
#         "title":"Suggestion Form",
#         "form":form_instance
#     }
#     return render(request, "suggestion.html", context=context)
# from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse
# from . import models
# from . import forms
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# from django.contrib.auth.models import User, AnonymousUser

# # Create your views here.

# # Assignment 2
# #def index(request):
# #	return HttpResponse("CINS465 Hello World")


# # Assignment 3

# # page 0 by default

# def index(request, page = 0):

# 	# POST represents when a user inputs some value
# 	# request contains the information of the current authenticated user

# 	# ***************** FORMS *********************

# 	if request.method=="POST":
# 		if request.user.is_authenticated:
# 			form_instance = forms.SuggestionForm(request.POST)	# form_instance uses the suggestionForm class located in forms.py, request holds input
# 			if form_instance.is_valid():	# if input is valid
# 				new_sugg = models.Suggestion(suggestion=form_instance.cleaned_data["suggestion"]) # a new suggestion is created from models
# 				new_sugg.author = request.user            
# 				new_sugg.save()	# user input is saved to db
# 				form_instance = forms.SuggestionForm() # an empty form is returned
# 		else:
# 			form_instance = forms.SuggestionForm()
# 	else:
# 		form_instance = forms.SuggestionForm() # if not valid an empty form is returned


# 	# ***************** FORMS *********************
	
# 	value=range(10*page+5)
# 	value2=models.Suggestion.objects.all()
# 	#form_instance = forms.SuggestionForm()

# 	context={   											 # creates Django variables I can use in my html files
# 	"variable":"CINS465 Hello World",  
# 	"title":"Assignment 5 Submission",
# 		"some_list":value[page*4:(page*4 + 4)],				# some _list 		
# 		"value":value[3],
# 		"helloWorld":"CINS465 Hello World",
# 		"suggestion_list":value2, #[page*6:(page*6 + 6)],
# 		"form":form_instance								# form holds form_instance which was created above
# 		}

# 	return render(request, "index.html", context=context) # Why is index the path now? 



# # render this template with this context

# @csrf_exempt
# @login_required(login_url="/login/")
# def Suggestions_view(request):
# 	if request.method=="GET":
# 		suggestion_query = models.Suggestion.objects.all()
# 		suggestion_list = {"suggestions":[]}
# 		for s_q in suggestion_query:
# 			comment_query = models.Comment.objects.filter(suggestion=s_q)
# 			comment_list = []
# 			for c_q in comment_query:
# 				comment_list += [{"comment":c_q.comment,"author":c_q.author.username,"created_on":c_q.created_on}]
# 			suggestion_list["suggestions"] += [{"ID":s_q.id, "suggestion":s_q.suggestion, "author":s_q.author.username, "created_on": s_q.created_on, "comments":comment_list}] # these values come from my models
# 		return JsonResponse(suggestion_list)
# 	else:
# 		return HttpResponse("Unsupported HTTP Method")


# def log_out(request):
# 	logout(request)
# 	return redirect('/login/')


# def secret(request):
# 	return HttpResponse("Shhhhh, secret page.")

# def register(request):
#     if request.method == "POST":
#         form_instance = forms.RegistrationForm(request.POST)
#         if form_instance.is_valid():
#             form_instance.save()
#             return redirect("/login/")
#             # print("Hi")
#     else:
#         form_instance = forms.RegistrationForm()
#     context = {
#         "form":form_instance,
#     }
#     return render(request, "registration/register.html", context=context)


# @login_required(login_url='/login/')
# def comments_view(request, suggestion):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             form_instance = forms.CommentForm(request.POST)
#             if form_instance.is_valid():
#                 new_comm = form_instance.save(request=request, sugg_id=instance_id)
#                 return redirect("/")
#         else:
#             form_instance = forms.CommentForm()
#     else:
#         form_instance = forms.CommentForm()
#     context = {
#         "title":"Comment Form",
#         "form":form_instance,
#         "sugg_id":instance_id
#     }
#     return render(request, "comment.html", context=context)



# # Made project urls point to the app urls
# # In apps url, defined an index path
# # which will use the views.index
# # views.index will then render the request


# # *******************************************************************
# # Anytime a request comes in, it goes through helloWorld->urls.py
# # urls.py then redirects the call to here (views.py) and calls some 
# function which tells the request what to do 
# ********************************************************************