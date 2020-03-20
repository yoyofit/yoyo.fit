# Generated by Django 3.0.4 on 2020-03-19 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyo_institutes', '0001_initial'),
        ('yoyo_coaches', '0002_coach_documents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Specialization',
                'verbose_name_plural': 'Specializations',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='coach',
            name='documents',
            field=models.ManyToManyField(to='yoyo_institutes.Doc', verbose_name='Documents'),
        ),
        migrations.AddField(
            model_name='coach',
            name='specializations',
            field=models.ManyToManyField(to='yoyo_coaches.Specialization', verbose_name='Specialization'),
        ),
    ]
