# Generated by Django 4.1.1 on 2022-11-12 14:23

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0010_alter_event_place"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="coordinates",
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=3875),
        ),
    ]
