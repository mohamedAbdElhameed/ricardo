from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from likert_field.models import LikertField
from django.core.mail import EmailMessage

User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True
User._meta.get_field('email')._required = True
from django.core.validators import RegexValidator


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
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Longitude"),
                                    verbose_name=_("Longitude"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Latitude"),
                                   verbose_name=_("Latitude"))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("City"),
                             verbose_name=_("City"))
    address = models.TextField(help_text=_("Address"), verbose_name=_("Address"))
    avatar = models.ImageField(help_text=_("Avatar"), verbose_name=_("Avatar"))
    description = models.TextField(help_text=_("Description"), verbose_name=_("Description"))
    rate = models.FloatField(default=0.0, help_text=_("Rate"), verbose_name=_("Rate"))
    number_of_rates = models.IntegerField(default='0', help_text=_("Number"), verbose_name=_("Number"))
    phone_number = models.CharField(max_length=20, help_text=_("Phone Number"), verbose_name=_("Phone Number"))
    APIKEY = models.CharField(max_length=100, null=True, blank=True)
    account_id = models.CharField(max_length=100, null=True, blank=True)
    merchant_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")

    def __str__(self):
        return self.user.username


class Buyer(Model):
    name_validator = RegexValidator(regex=r'^[a-zA-Z\s]*$', message=_('Only English letters and spaces'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer', help_text=_("User"),
                                verbose_name=_("User"))
    avatar = models.ImageField(null=True, blank=True, help_text=_("Avatar"), verbose_name=_("Avatar"))
    phone_number = models.CharField(max_length=15, null=True, blank=True, help_text=_("Phone Number"),
                                    verbose_name=_("Phone Number"))
    address = models.CharField(max_length=250, null=True, blank=True, help_text=_("Address"), verbose_name=_("Address"))
    full_name = models.CharField(max_length=150, null=True, blank=True, help_text=_("full_name"),
                                 verbose_name=_("full_name"), validators=[name_validator])
    national_id = models.CharField(max_length=20, null=True, blank=True, help_text=_("national_id"),
                                   verbose_name=_("national_id"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Buyer")
        verbose_name_plural = _("Buyers")

    def __str__(self):
        return self.user.username


class Review(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Seller"),
                               verbose_name=_("Seller"), related_name='reviews')
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Buyer"),
                              verbose_name=_("Buyer"))
    details = models.TextField(help_text=_("Details"), verbose_name=_("Details"))
    rate = LikertField(help_text=_("Rate"), verbose_name=_("Rate"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, help_text=_("Modified At"), verbose_name=_("Modified At"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Contact(models.Model):
    name = models.CharField(max_length=50, help_text=_("name"), verbose_name=_("name"))
    phone = models.CharField(max_length=15, help_text=_("phone_number"), verbose_name=_("phone_number"))
    email = models.EmailField(max_length=50, help_text=_("email"), verbose_name=_("email"))
    message = models.TextField(max_length=500, help_text=_("message"), verbose_name=_("message"))
    read = models.BooleanField(default=False, help_text=_("Done"), verbose_name=_("Done"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Created At"), verbose_name=_("Created At"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")


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


@receiver(post_save, sender=Contact)
def send_email(sender, instance, **kwargs):
    email_body = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    <b>
    <table align="center" border="10">
    <tr>
        <td>nombre</td>
        <td>""" + instance.name + """</td>
    </tr>
    <tr>
        <td>correo electrónico</td>
        <td>""" + instance.email + """</td>
    </tr>
    <tr>
        <td>número de teléfono</td>
        <td>""" + instance.phone +"""</td>
    </tr>
    <tr>
        <td>mensaje</td>
        <td>""" + instance.message+"""</td>
    </tr>
    </table>
    </b>
    </body>
    </html>
    """ + "\n"
    email = EmailMessage('Artesanias de Boyacá', email_body, to=['info@artesaniasdeboyaca.com'])
    email.content_subtype = "html"
    email.send()