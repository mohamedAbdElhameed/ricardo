from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Seller(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_("User"), verbose_name=_("User"))
    name = models.CharField(max_length=50, help_text=_("Name"), verbose_name=_("Name"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Longitude"), verbose_name=_("Longitude"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Latitude"), verbose_name=_("Latitude"))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("City"), verbose_name=_("City"))
    address = models.TextField(help_text=_("Address"), verbose_name=_("Address"))
    avatar = models.ImageField(help_text=_("Avatar"), verbose_name=_("Avatar"))
    description = models.TextField(help_text=_("Description"), verbose_name=_("Description"))
    rate = models.FloatField(default=0.0, help_text=_("Rate"), verbose_name=_("Rate"))
    number_of_rates = models.IntegerField(default='0', help_text=_("Number"), verbose_name=_("Number"))
    phone_number = models.CharField(max_length=20, help_text=_("Phone Number"), verbose_name=_("Phone Number"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")

    def __str__(self):
        return self.user.username


class Buyer(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_("User"), verbose_name=_("User"))
    avatar = models.CharField(max_length=50, null=True, blank=True, help_text=_("Avatar"), verbose_name=_("Avatar"))
    phone_number = models.CharField(max_length=15, null=True, blank=True, help_text=_("Phone Number"), verbose_name=_("Phone Number"))
    address = models.CharField(max_length=250, null=True, blank=True, help_text=_("Address"), verbose_name=_("Address"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Buyer")
        verbose_name_plural = _("Buyers")

    def __str__(self):
        return self.user.username


class Review(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Seller"), verbose_name=_("Seller"))
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Buyer"), verbose_name=_("Buyer"))
    details = models.TextField(help_text=_("Details"), verbose_name=_("Details"))
    rate = models.FloatField(help_text=_("Rate"), verbose_name=_("Rate"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


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