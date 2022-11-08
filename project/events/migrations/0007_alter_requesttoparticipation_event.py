# Generated by Django 4.1.1 on 2022-11-01 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_remove_invitetoevent_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requesttoparticipation",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invites",
                to="events.event",
            ),
        ),
    ]
