# Generated by Django 4.0.5 on 2022-06-19 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0006_alter_apikey_expired_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideo',
            name='published_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]