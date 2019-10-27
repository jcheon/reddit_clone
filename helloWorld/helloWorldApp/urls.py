from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('<int:page>/', views.index),
    path('', views.index),
    path('suggestions/', views.suggestions_view),
    path('suggestion/', views.suggestion_form_view),
    path('comment/<int:instance_id>/', views.comments_view),
    path('comment/<int:instance_id>/<int:delete>/', views.comments_view),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('register/', views.register),
]

# This is the url and which view it will pull its user direction information from


# # STEP 2 create this folder
# from django.urls import path, include
# from django.contrib.auth import views as auth_views

# from . import views

# urlpatterns = [
# #	path('Images/', views.index),
# 	path('<int:page>/', views.index),
# 	path('', views.index),
# 	path('suggestions/', views.Suggestions_view),
# 	path('comment/<int:instance_id>/', views.comments_view),
# 	path('login/', auth_views.LoginView.as_view()),
# 	path('logout/', views.log_out),
# 	path('register/', views.register),
# 	path('Secret/', views.secret),
# ]

# # if I wanted Bob to render, I would have to add a path to bob


# # *********************************************************************
# # Every time I want to create a new page, I need to add a new url path 
# # which references some function call in views.py
# # *********************************************************************