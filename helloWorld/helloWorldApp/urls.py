from django.urls import path, re_path
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
    path('upvote/<int:instance_id>/', views.upvote),
    path('downvote/<int:instance_id>/', views.downvote),
    path('post/<int:instance_id>/', views.post_page),
    path('register/', views.register),

    path('create_subreddit/', views.create_subreddit),
    path('r/<str:subreddit_id>/', views.success, name='subreddit_id'),

    path('getSubreddit', views.created_subreddits)
]

