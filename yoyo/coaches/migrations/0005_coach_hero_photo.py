# Generated by Django 3.0.4 on 2020-03-21 13:09

from django.db import migrations, models
import yoyo.coaches.uploader


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo_coaches', '0004_auto_20200319_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='hero_photo',
            field=models.ImageField(blank=True, help_text='This photo does have a 1080x720px', null=True, upload_to=yoyo.coaches.uploader.upload_hero_photo, verbose_name='Big cover photo'),
        ),
    ]
