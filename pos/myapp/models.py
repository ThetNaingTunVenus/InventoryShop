from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=225)
    address = models.CharField(max_length=225)

    def __del__(self):
        return self.supplier_name

class Category(models.Model):
    category_name = models.CharField(max_length=225)

    def __str__(self):
        return self.category_name

class Items(models.Model):
    item_name = models.CharField(max_length=225)
    category = models.CharField(max_length=225)
    pruchase_price = models.FloatField(default=0.00)
    sell_price = models.FloatField(default=0.00)
    balance_qty = models.IntegerField(default=0)


    def __str__(self):
        return self.item_name

class Cart(models.Model):
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    super_total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart : "+ str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    remain_balance = models.IntegerField()

    def __str__(self):
        return "Cart : "+ str(self.cart.id)+ "CartProduct : " + str(self.id)

STATUS=(
    ("Ordering","Ordering"),("Delivered","Delivered"),("Cash","Cash"),("Credit","Credit"),("Consignment","Consignment"),("Complete","Complete")
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=255,null=True, blank=True)
    shipping_address = models.CharField(max_length=255, default='local')
    mobile = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    all_total = models.PositiveIntegerField()
    ordered_staus = models.CharField(max_length=255, choices=STATUS, default='Ordering')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Order : " + str(self.id)


class PurchaseList(models.Model):
    supplier_name = models.CharField(max_length=225)
    item_name = models.CharField(max_length=225)
    purchase_qty = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    p_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item_name