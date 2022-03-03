from unicodedata import name
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ( 
    EmailTokenObtainPairView, 
    RegisterView, 
    LoginView, 
    Follow, 
    Unfollow,
    ViewProfile
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('api/authenticate', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('api/follow/<int:id>', Follow.as_view(), name="follow"),
    path('api/unfollow/<int:id>', Unfollow.as_view(),name='unfollow'),
    path('api/user', ViewProfile.as_view(), name="user_profile") 
]