# Generated by Django 4.1.1 on 2023-05-19 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hints", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hint",
            name="page",
        ),
    ]
