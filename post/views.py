from dataclasses import fields
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.core import serializers


# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import simplejson as json

from rest_framework.permissions import IsAuthenticated

from users.models import Profile, Followsystem
from users.backends import EmailBackend
from .models import Post, Like, Comment
from rest_framework import generics


class Createpost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))
        print(data)
        title = data['Title']
        description = data['Description']

        post = Post()
        post.title = title
        post.created_by = Profile.objects.get(user_id=request.user.id)
        post.description = description

        post.save()

        return Response(
            {
                "Post-ID": post.id,
                "Title": post.title,
                "Description": post.description,
                "Created Time(UTC)": post.date_posted_on
            }
        )


class Deletepost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        try:
            post_obj = Post.objects.get(id=id)
            post_obj.delete()
        except:
            return Response("Post deletion unsucessful")

        return Response("The post has been successfully deleted")

    def get(self, request, id):
        try:
            post_obj = Post.objects.get(id=id)
        except:
            return Response(f"Post with id { id } does not exist")
        content = post_obj.description

        post_id = post_obj.id

        number_of_likes = post_obj.post_likes.all().count()
        number_of_comment = post_obj.post_comments.all().count()

        return Response(
            {
                "id": post_id,
                "content": content,
                "number of likes": number_of_likes,
                "number of comments": number_of_comment
            }
        )


class LikePost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        try:
            profile_obj = Profile.objects.get(user_id=request.user.id)

            try:
                post_obj = Post.objects.get(id=id)
            except:
                return Response("Post with this id doesnt exist")

            Like.objects.create(liked_by=profile_obj, posts_liked=post_obj)

        except:
            return Response("Post liking unsuccessfull")

        return Response(f"Post with id { id } liked successfully")


class UnlikePost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            profile_obj = Profile.objects.get(user_id=request.user.id)

            try:
                post_obj = Post.objects.get(id=id)
            except:
                return Response("Post with this id doesnt exist")

            like_obj = Like.objects.get(
                liked_by=profile_obj, posts_liked=post_obj)

            like_obj.delete()

        except:
            return Response("Deletion unsuccessful")

        return Response(f'Post with { id } unliked succesffully!')


class CreateComment(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            post_obj = Post.objects.get(id=id)
            profile_obj = Profile.objects.get(user_id=request.user.id)
            data = json.loads(request.body.decode("utf-8"))

            comment = data['Comment']

            comment_obj = Comment()
            comment_obj.user_id = profile_obj
            comment_obj.content = comment
            comment_obj.post_associated_id = post_obj
            comment_obj.save()
        except:
            return Response("Comment unsuccessful")

        return Response({
            "Comment ID": comment_obj.id
        })


# GET /api/all_posts would return all posts created by authenticated user sorted by post time.

class AllPost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            profile_obj = Profile.objects.get(user_id=request.user.id)
            all_posts = profile_obj.posts_created.all()
        except:
            return Response("Unsuccessfull")

        final_list = []

        for post in all_posts:
            dict = {}
            dict['id'] = str(post.id)
            dict['title'] = str(post.title)
            dict['desc'] = str(post.description)
            dict['created_at'] = str(post.date_posted_on)
            dict['comments'] = []
            all_comments = post.post_comments.all()
            for comment in all_comments:
                dict['comments'].append(str(comment.content))
            dict['likes'] = str(post.post_likes.all().count())
            final_list.append(dict)

        final_list.sort(key = lambda x: x['created_at'])

        return JsonResponse(final_list, safe=False)