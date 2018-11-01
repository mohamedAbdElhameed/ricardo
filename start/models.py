from django.db import models


# Create your models here.
from products.models import Product


class StartDetail(models.Model):
    banner_image = models.ImageField()
    title = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    below_image = models.ImageField()
    below_title = models.CharField(max_length=100)
    below_detail = models.TextField()

