# Generated by Django 2.1.3 on 2019-03-12 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20190312_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastproductsincart',
            name='carts',
        ),
        migrations.AddField(
            model_name='cart',
            name='show',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='LastProductsInCart',
        ),
    ]
