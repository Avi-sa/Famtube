# Generated by Django 4.0.5 on 2022-06-17 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideos',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 19, 44, 15, 319592)),
        ),
    ]
