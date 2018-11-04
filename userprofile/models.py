from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Seller(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField()
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    number_of_rates = models.IntegerField(default='0')
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Buyer(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField()
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Review)
def increment_rate(sender, instance, **kwargs):
    seller = Seller.objects.get(user=instance.seller.user)
    seller.number_of_rates += 1
    seller.rate += instance.rate
    seller.save()


@receiver(post_delete, sender=Review)
def decrement_rate(sender, instance, **kwargs):
    seller = Seller.objects.get(user=instance.seller.user)
    seller.number_of_rates -= 1
    seller.rate -= instance.rate
    seller.save()