# Generated by Django 3.0.4 on 2020-03-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo_institutes', '0001_initial'),
        ('yoyo_coaches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='documents',
            field=models.ManyToManyField(to='yoyo_institutes.Doc'),
        ),
    ]
