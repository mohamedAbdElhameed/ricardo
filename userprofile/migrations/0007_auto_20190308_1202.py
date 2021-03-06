# Generated by Django 2.1.3 on 2019-03-08 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20190308_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='full_name',
            field=models.CharField(blank=True, help_text='full_name', max_length=150, null=True, validators=[django.core.validators.RegexValidator(message='Only English letters and spaces', regex='^[a-zA-Z\\s]*$')], verbose_name='full_name'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(help_text='Name', max_length=50, verbose_name='Name'),
        ),
    ]
