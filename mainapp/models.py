from django.db import models

# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.CharField(max_length=10)

    parcel_height = models.CharField(max_length=10)
    parcel_width = models.CharField(max_length=10)
    parcel_length = models.CharField(max_length=10)
    parcel_weight = models.CharField(max_length=10)
    total_price = models.CharField(max_length=10)

    sender_name = models.CharField(max_length=150)
    sender_phone = models.CharField(max_length=20)

    receiver_name = models.CharField(max_length=150)
    receiver_phone = models.CharField(max_length=20)

    pickup_address = models.CharField(max_length=120)
    deliver_address = models.CharField(max_length=120)

    delman_name = models.CharField(max_length=150)
    delman_phone = models.CharField(max_length=20)
    delman_address = models.CharField(max_length=120)

    order_status = models.CharField(max_length=20, default='default')

    def __str__(self):
        return self.order_id