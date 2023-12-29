import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER =(
    ('Female', 'F'),
    ('Male', 'M'),
    ('Others', 'O')
)

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username=models.CharField(max_length=50, unique=True)
    first_name=models.CharField(max_length=50, null=True, blank=True)
    last_name=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(unique=True, max_length=50)
    address=models.CharField(max_length=200, null=True, blank=True)
    phone_number=models.CharField(max_length=15)
    country = models.TextField()
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER)
    state = models.CharField(max_length=50, null=True, blank=True) 
    profile_pic = models.ImageField(upload_to='profile_pics/', default="profile.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.username

    class Meta:
        ordering=['-date_created']


class Product(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    images = models.ImageField(upload_to='product_img/', default="product.png", null=True, blank=True)
    reviews = models.ManyToManyField('Review', related_name='products', blank=True)

    def __str__(self):
        return f"{self.title} - {self.price}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE,null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product} by {self.user}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"Order for {self.customer}"
    

    @property
    def get_cart_items(self):
        """
        Get the total quantity of items in the order.
        """
        order_items = self.orderitem_set.all()
        total_quantity = sum([item.quantity for item in order_items])
        return total_quantity
    
    @property
    def get_cart_total(self):
        """
        Get the total cost of items in the order.
        """
        order_items = self.orderitem_set.all()
        cart_total= sum([item.get_item_total for item in order_items])
        return cart_total
    
    
    



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order for {self.order.customer}"

    @property
    def get_item_total(self):
        item_total=self.product.price * self.quantity
        return item_total

    
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
    


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.customer}"
    

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code    





    


    



