from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models
# Create your models here.


class City(Model):
    name = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class Seller(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField()
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username