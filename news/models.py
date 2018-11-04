from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    image = models.ImageField(help_text=_("Image"), verbose_name=_("Image"))
    title = models.CharField(max_length=100, help_text=_("Title"), verbose_name=_("Title"))
    details = models.TextField(help_text=_("Details"), verbose_name=_("Details"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title