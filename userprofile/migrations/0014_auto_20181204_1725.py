# Generated by Django 2.1.3 on 2018-12-04 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0013_auto_20181127_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='APIKEY',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='merchant_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
