# Generated by Django 4.1.1 on 2023-06-15 12:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0019_event_hidden"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="black_list",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="black_list",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="current_fans",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="current_views_rooms",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="current_users",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="current_rooms",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="event",
            name="pinned",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]