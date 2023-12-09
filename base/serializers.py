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
    ShippingAddress=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_cart_items(self, obj):
        return obj.get_cart_items
    
    def get_cart_total(self, obj):
        return obj.get_cart_total
    
   
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address





class WishlistSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True)
    class Meta:
        model=Wishlist
        fields='__all__'

        

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields='__all__'
        