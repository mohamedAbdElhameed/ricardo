# Generated by Django 2.1.3 on 2018-11-04 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20181104_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-modified_at']},
        ),
    ]
