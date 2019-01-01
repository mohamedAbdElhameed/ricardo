# Generated by Django 2.1.3 on 2018-12-18 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Created At', verbose_name='Created At'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At'),
        ),
        migrations.AlterField(
            model_name='post',
            name='details',
            field=models.TextField(help_text='Details', verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(help_text='Image', upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Title', max_length=100, verbose_name='Title'),
        ),
    ]