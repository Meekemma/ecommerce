from django.contrib import admin
from .models import *


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'country')
    list_filter = ('country', 'gender')
    search_fields = ('username', 'email')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('product__title', 'user__username')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'complete', 'date_ordered', 'transaction_id')
    list_filter = ('complete', 'customer__country')
    search_fields = ('customer__username', )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'date_added')
    list_filter = ('order__complete', )
    search_fields = ('product__title', )


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address', 'city', 'state', 'zipcode', 'date_added')
    list_filter = ('customer__country', 'state')
    search_fields = ('customer__username', 'address')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', )
    


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to')
    

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Coupon, CouponAdmin)


