from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import *


# Create your views here.




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productList(request):
    query = request.GET.get('query', '')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
    if not products:
            return Response({'message': 'No results found'})
    
        
    serializer = ProductSerializer(products, many=True)
    return Response( serializer.data)

@api_view(['POST'])
def createProduct(request):
    data = request.data

    product = Product.objects.create(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity'],
        category_id=data['category'],
        images=data['images']
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

   


@api_view(['GET'])
def getProduct(request, pk):
    try:
        product=Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)



@api_view(['GET','PUT', 'DELETE'])
def actionProduct(request, pk):
    data = request.data
    try:
        product=Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
        


    
    if request.method =='PUT':
        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        product.category_id = data.get('category', product.category_id)

        

        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    if request.method == 'DELETE':
        product.delete()
        return Response('Product Deleted')

          


@api_view(['GET'])
def getCategory(request):
    categories = Category.objects.all().order_by('name') 
    serializers= CategorySerializer(categories, many=True)
    return Response(serializers.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    data=request.data
    product=Product.objects.get(id=pk)

    # 1 - Review already exists
    existing_review= Review.objects.filter(user=user, product=product)
    if existing_review.exists():
        content = {'detail':'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # 2 - No Rating or 0
    elif data['rating'] ==0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create a new review
    else:
        review =Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
    serializers=ReviewSerializer(review)
    return Response(serializers.data)


