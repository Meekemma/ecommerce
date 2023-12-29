from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from base.utils import Util

from.models import *


class UserSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)    

    class Meta:
        model =User
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user =self.context.get('user')

        if password!= password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        user.set_password(password)
        user.save()
        return attrs
    

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)






    
    

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

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields= '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item_total=serializers.SerializerMethodField()
    price=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model=OrderItem
        fields = '__all__'

    def get_item_total(self, obj):
        return obj.get_item_total    


    def get_price(self, obj):
        return obj.product.price
    
    def get_title(self, obj):
        return obj.product.title
    
    def get_image(self, obj):
        return obj.product.images.url


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    cart_items=serializers.SerializerMethodField()
    cart_total=serializers.SerializerMethodField()
    # ShippingAddress=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_cart_items(self, obj):
        return obj.get_cart_items
    
    def get_cart_total(self, obj):
        return obj.get_cart_total
        
    

    
   
    # def get_shippingAddress(self, obj):
    #     try:
    #         address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
    #     except:
    #         address = False
    #     return address





class WishlistSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True)
    class Meta:
        model=Wishlist
        fields='__all__'

        

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields='__all__'
        