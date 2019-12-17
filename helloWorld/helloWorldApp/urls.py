from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('<int:page>/', views.index),
    path('', views.index),
    path('suggestions/', views.suggestions_view),
    path('r/<str:subreddit_title>/suggestion/', views.suggestion_form_view, name='subreddit_title'),
    # path('comment/<int:instance_id>/', views.comments_view),
    # path('comment/<int:instance_id>/<int:delete>/', views.comments_view),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('upvote/<int:instance_id>/', views.upvote),
    path('downvote/<int:instance_id>/', views.downvote),
    path('post/<int:instance_id>/', views.post_page),
    path('post/<int:instance_id>/<int:delete>/', views.post_page),
    path('getPost/<int:instance_id>/', views.getPost, name='instance_id'),
    path('register/', views.register),
    path('subreddits/', views.show_subreddits),
    path('create_subreddit/', views.create_subreddit),
    path('r/<str:subreddit_title>/', views.success, name='subreddit_title'),
    path('getSubreddit/', views.created_subreddits),
    path('getSubPosts/<str:subreddit_title>/', views.getSubPosts, name='subreddit_title'),
    path('getChatrooms/', views.created_chatrooms),
    path('createChat/', views.chatroom_form_view),
    path('chat/', views.chat, name='chat'), # added this
    path('chat/<str:room_name>/', views.room, name='room'),
	path('profiles/<str:user_name>/', views.profiles, name='user_name'),
    path('updateProfile/', views.update_profile),
    path('getUserPosts/<str:user_name>/', views.getUserPosts, name='user_name')
]

