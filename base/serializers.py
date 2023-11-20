from rest_framework import serializers
from django.contrib.auth.models import User

from.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    

class CustomerSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()


    class Meta:
        model=Customer
        fields = ['id', 'username','first_name', 'last_name','email', 'phone_number', 'country', 'gender', 'state', 'profile_pic', 'date_created']
        extra_kwargs = {'user': {'read_only': True}}

    def get_country(self, obj):
        return obj.country.name if obj.country else None    

        


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


class OrderSerializer(serializers.ModelSerializer):
    total_quantity_in_cart = serializers.SerializerMethodField(read_only=True)
    cart_total = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

    def get_total_quantity_in_cart(self, obj):
        order_items = obj.orderitem_set.all()
        total_quantity = sum([item.quantity for item in order_items])
        return total_quantity
    
    def get_cart_total(self,obj):
        order_items = obj.orderitem_set.all()
        cart_total= sum([item.get_item_total() for item in order_items])
        return cart_total


class OrderItemSerializer(serializers.ModelSerializer):
    item_total=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=OrderItem
        fields = '__all__'

    def get_item_total(self, obj):
        item_total = obj.product.price * obj.quantity
        return item_total



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
        