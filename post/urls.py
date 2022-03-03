from unicodedata import name
from django.contrib import admin
from django.urls import path, include 
from .views import Createpost, Deletepost, LikePost, UnlikePost, CreateComment, AllPost
urlpatterns = [
    path('api/posts/', Createpost.as_view(), name="postview"),
    path('api/posts/<int:id>', Deletepost.as_view(), name="post_delete"),
    path('api/like/<int:id>', LikePost.as_view(), name="post_like"),
    path('api/unlike/<int:id>', UnlikePost.as_view(), name="unlike_post"),
    path('api/comment/<int:id>', CreateComment.as_view(), name="post_comment"),
    path('api/all_posts', AllPost.as_view(), name="all_posts"),
]