from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import UserSerializer,UserChangePasswordSerializer,CustomerSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from django.urls import reverse


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from base.models import Customer


# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer   



@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UserChangePasswordView(request):
    if request.method == 'PUT':
            serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                return Response({"detail": "Password successfully changed "}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                


# @api_view(['POST'])
# def SendPasswordResetEmailView(request):
#     if request.method == 'POST':
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def UserPasswordResetView(request, uid, token):
#     if request.method == 'POST':
#         serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
def getUserId(request, pk):
    if request.method == 'GET':
        user=User.objects.get(id=pk)
        serializer=UserSerializer(user, many=False)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        userDeletion=User.objects.get(id=pk)
        userDeletion.delete()
        return Response('User Was Deleted')
    



@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def createProfile(request):
    if request.method == 'POST' or request.method == 'PUT':
        user = request.user
        customer = user.customer  

        serializer = CustomerSerializer(customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






