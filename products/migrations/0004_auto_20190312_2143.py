# Generated by Django 2.1.3 on 2019-03-12 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190312_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastproductsincart',
            name='buyer',
        ),
        migrations.AddField(
            model_name='lastproductsincart',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
