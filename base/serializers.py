from rest_framework import serializers
from.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        exclude = ['user', 'date_created']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields= '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    reviews_count=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields='__all__'

    def get_reviews(self, obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews, many=True)
        return serializer.data  
    
    def get_reviews_count(self, obj):
        return obj.review_set.count()  


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

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
        