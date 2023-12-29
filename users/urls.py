from django.urls import path
from users import views
from .views import MyTokenObtainPairView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('changepassword/', views.UserChangePasswordView, name='changepassword'),
    path('api/password_reset/request/', reset_password_request_token, name='reset_password_request_token'),
    path('api/password_reset/confirm/', reset_password_confirm, name='reset_password_confirm'),

    path('register/', views.registerUser, name='register'),
    path('users/', views.getUsers, name='users'),
    path('users/<str:pk>/', views.getUserId, name='user'),
    path('create_profile/', views.createProfile, name='create_profile'),

    
]