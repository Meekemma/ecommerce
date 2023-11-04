from rest_framework import serializers
from.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        exclude = ['user', 'date_created']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        exclude = ['user', 'date_created']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__' 

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        exclude = ['date_created']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        exclude = ['date_created']

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        exclude = ['date_created'] 


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields='__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields='__all__'
        