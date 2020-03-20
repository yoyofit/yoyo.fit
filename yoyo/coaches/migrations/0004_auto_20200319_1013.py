# Generated by Django 3.0.4 on 2020-03-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo_institutes', '0001_initial'),
        ('yoyo_coaches', '0003_auto_20200319_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='documents',
            field=models.ManyToManyField(blank=True, to='yoyo_institutes.Doc', verbose_name='Documents'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='specializations',
            field=models.ManyToManyField(blank=True, to='yoyo_coaches.Specialization', verbose_name='Specialization'),
        ),
    ]