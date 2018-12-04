# Generated by Django 2.1.3 on 2018-12-04 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20181203_1639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproxy',
            options={'verbose_name': 'Order Status', 'verbose_name_plural': 'Orders Status'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Status'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=None, help_text='you can change the status form the states list', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Status', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='status',
            name='status_name',
            field=models.CharField(help_text='Status name', max_length=50, verbose_name='Status name'),
        ),
    ]
