# Generated by Django 2.1.3 on 2019-03-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20190312_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
