# Generated by Django 4.0.4 on 2022-09-11 07:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='current_users',
            field=models.ManyToManyField(blank=True, related_name='current_rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='fans',
            field=models.ManyToManyField(blank=True, related_name='current_views_rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
