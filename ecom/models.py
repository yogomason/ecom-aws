from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.FloatField()
    stock = models.CharField(max_length=200, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    image = models.ImageField(default='default.png', null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True,)
    complete = models.BooleanField(default=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product,blank=True, null=True, on_delete= models.SET_NULL)
    order = models.ForeignKey(Order, blank=True,null=True, on_delete= models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

        def __str__(self):
            return self.product

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete= models.SET_NULL)
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    address2 = models.CharField(max_length=200, null=True, default=None)
    city = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    #
    def __str__(self):
        return self.city
