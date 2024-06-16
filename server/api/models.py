from django.db import models

# Create your models here.

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.name


# Product Model 
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


# Order Model
class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.order_number

    #auto-generating order_number field 
    def save(self, *args, **kwargs): 
        if not self.order_number:
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                last_order_number = int(last_order.order_number[3:])
                self.order_number = f"ORD{last_order_number + 1:05d}"
            else:
                self.order_number = "ORD00001"
        super().save(*args, **kwargs)


# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='order_items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"