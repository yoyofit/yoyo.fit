# Generated by Django 3.0.4 on 2020-03-18 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0008_city_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60, verbose_name='First name')),
                ('last_name', models.CharField(max_length=120, verbose_name='Last name')),
                ('second_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Second name')),
                ('born', models.DateField(blank=True, null=True, verbose_name='Born date')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.City', verbose_name='City')),
            ],
            options={
                'verbose_name': 'Coach',
                'verbose_name_plural': 'Coaches',
            },
        ),
    ]
