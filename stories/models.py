from django.db import models

# Create your models here.
from userprofile.models import Seller
from django.utils.translation import gettext_lazy as _


class ArtisanMaster(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, help_text=_("Seller"), verbose_name=_("Seller"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Artisan Master")
        verbose_name_plural = _("Artisan Masters")

    def __str__(self):
        return self.seller.user.username


class Achievement(models.Model):
    artisan_master = models.ForeignKey(ArtisanMaster, related_name="achievements", on_delete=models.CASCADE, help_text=_("Artisan Master"), verbose_name=_("Artisan Master"))
    title = models.CharField(max_length=50, help_text=_("Title"), verbose_name=_("Title"))
    year = models.IntegerField(help_text=_("Year"), verbose_name=_("Year"))
    details = models.TextField(help_text=_("Details"), verbose_name=_("Details"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Achievement")
        verbose_name_plural = _("Achievements")

    def __str__(self):
        return self.title


class Tale(models.Model):
    title = models.CharField(max_length=50, help_text=_("Title"), verbose_name=_("Title"))
    details = models.TextField(help_text=_("Details"), verbose_name=_("Details"))
    video_url = models.URLField(help_text=_("Video Url"), verbose_name=_("Video Url"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Tale")
        verbose_name_plural = _("Tales")

    def __str__(self):
        return self.title
