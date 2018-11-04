from django.db import models

# Create your models here.
from userprofile.models import Seller


class ArtisanMaster(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.seller.user.username


class Achievement(models.Model):
    artisan_master = models.ForeignKey(ArtisanMaster, related_name="achievements", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tale(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField()
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
