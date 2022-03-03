from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

from .models import Profile, Followsystem
from users.backends import  EmailBackend

email_object = EmailBackend()

class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response_data = { "Restricted entry passed!" }

        return Response(data=response_data)


             
class Follow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        follower = Profile.objects.get(user_id = request.user.id)
        following = Profile.objects.get(user_id = id) 

        if not Followsystem.objects.filter(from_profile = follower, to_profile = following).exists():
            Followsystem.objects.create(from_profile = follower, to_profile = following) 
        else:
            return Response("You already follow this person!") 

        return Response("Following action complete") 

class Unfollow(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, id):

        follower = Profile.objects.get(user_id = request.user.id)
        following = Profile.objects.get(user_id = id) 

        if not Followsystem.objects.filter(from_profile = follower, to_profile = following).exists():
            return Response("You dont follow this account")


        object = Followsystem.objects.get(from_profile = follower, to_profile = following)
        object.delete()

        return Response("Unfollow action complete") 

class ViewProfile(APIView):
    
    def get(self, request):
        
        if not Profile.objects.filter(user_id = request.user.id).exists():
            return Response("The user doenot exist")
        
        user_profile = Profile.objects.get(user_id = request.user.id)

        return Response({ 
            f'User name is { user_profile.username }',
            f'Number of following is { user_profile.following.all().count() }',
            f'Number of followers is { user_profile.follower.all().count() }'
         })