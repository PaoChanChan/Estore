# Generated by Django 5.0.4 on 2024-05-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
