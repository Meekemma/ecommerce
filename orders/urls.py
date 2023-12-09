from django.urls import path
from orders import views

urlpatterns = [
    path('orders/', views.getOrders, name="orders"),
    path('order/<str:pk>/', views.getOrder, name="order"),
    path('create_order/', views.createOder, name='create_order'),
    path('myorders/', views.getMyOrder, name='myorders'),
    path('create-wishlist/', views.createWishlist, name='create-wishlist'),
    path('wish-list/<str:pk>/',views.updateWishlist, name="wish-list"),
    
]