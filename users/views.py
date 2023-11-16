from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import UserSerializer,CustomerSerializer
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
def createProfile(request):
    user = request.user

    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = None    
    if request.method == 'POST':
        if customer:
            return Response({'message': 'Customer profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method =='PUT':
        if not customer:
            return Response({'message': 'Customer profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

