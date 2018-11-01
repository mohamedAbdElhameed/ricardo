from django.db import models


# Create your models here.
class Post(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.title