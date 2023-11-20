from django.urls import path
from base import views

urlpatterns = [
    path('', views.productList, name="products"),

    

    path('create/', views.createProduct, name="create"),
    path('product/<str:pk>/', views.getProduct, name='product'),
    path('update_product/<str:pk>/', views.actionProduct, name='update_product'),
    path('category/', views.getCategory, name='category'),
    path('product/<str:pk>/reviews/', views.createProductReview, name="create-review"),
]