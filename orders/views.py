from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import OrderSerializer,OrderItemSerializer,WishlistSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from base.models import *


# api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addOrderItems(request):
#     customer=request.user.customer
#     data=request.data

#     orderItems =data['orderItems']

#     if orderItems and len(orderItems) == 0:
#         return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST
#     else:
    

    

#     serializer= OrderSerializer(order, many=False)
#     return Response(serializer.data)


#Retrieve a list of all orders.
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()

    serializer =OrderSerializer(orders, many=True)
    return Response(serializer.data)


#Retrieve details of a specific order.
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer =OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOder(request):
    customer=request.user.customer
    data=request.data

    order_items = data.get('orderItems')
    if order_items and len(order_items) == 0:
        return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order=Order.objects.create(
            customer=customer,
            complete=False
        )

        shipping = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['ShippingAddress']['address'],
            city=data['ShippingAddress']['city'],
            state=data['ShippingAddress']['state'],
            zipcode=data['ShippingAddress']['zipcode']
        )
        



    for item_data in order_items:
        product_id = item_data.get('product')
        quantity =item_data.get('quantity')

        if product_id and quantity:
            product =Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrder(request):
    customer=request.user.customer
    orders = customer.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createWishlist(request):
    customer = request.user.customer
    data = request.data

    wishlist_items = data.get('wishlistItems', [])

    if wishlist_items and len(wishlist_items) == 0:
        return Response({'detail': 'No Wishlist Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        wishlist = Wishlist.objects.create(customer=customer)

    for item_data in wishlist_items:
        product_id = item_data.get('product')
        if product_id:
            product = Product.objects.get(id=product_id)
            wishlist.products.add(product)

    serializer = WishlistSerializer(wishlist, many=False)
    return Response(serializer.data)

@api_view(['GET','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def updateWishlist(request, pk):
    customer = request.user.customer

    if request.method == 'GET':
        wishlists = Wishlist.objects.filter(customer=customer)
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    if request.method =='PUT':
        try:
            wishlist=Wishlist.objects.get(id=pk, customer=customer)
        except Wishlist.DoesNotExist:
            return Response({'detail':'wishlist do not exixt'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method =='DELETE':
        try:
            wishlist=Wishlist.objects.get(id=pk, customer=customer)
        except Wishlist.DoesNotExist:
            return Response({'detail':'wishlist does not exixt'}, status=status.HTTP_400_BAD_REQUEST)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









    
