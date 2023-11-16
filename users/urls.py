from django.urls import path
from users import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.registerUser, name='register'),
    path('users/', views.getUsers, name='users'),
    path('users/<str:pk>/', views.getUserId, name='user'),
    path('create_profile/', views.createProfile, name='create_profile'),

    
]