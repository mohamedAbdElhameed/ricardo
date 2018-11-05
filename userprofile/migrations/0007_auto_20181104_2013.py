# Generated by Django 2.1.3 on 2018-11-04 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_seller_number_of_rates'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
