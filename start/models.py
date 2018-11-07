from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
from products.models import Product
from django.utils.translation import gettext_lazy as _


class StartDetail(models.Model):
    banner_image = models.ImageField(help_text=_("Banner Image"), verbose_name=_("Banner Image"))
    title = models.CharField(max_length=100, help_text=_("Title"), verbose_name=_("Title"))
    products = models.ManyToManyField(Product, help_text=_("Products"), verbose_name=_("Products"))
    below_image = models.ImageField(help_text=_("Below Image"), verbose_name=_("Below Image"))
    below_title = models.CharField(max_length=100, help_text=_("Below Title"), verbose_name=_("Below Title"))
    below_detail = RichTextField(help_text=_("Below Detail"), verbose_name=_("Below Detail"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Start Detail")
        verbose_name_plural = _("Start Details")
