from django.db import models

# Create your models here.
from userprofile.models import Seller


class ArtisanMaster(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)


class Achievement(models.Model):
    artisan_master = models.ForeignKey(ArtisanMaster, related_name="achievements", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    details = models.TextField()


class Tale(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField()
    video_url = models.URLField()
