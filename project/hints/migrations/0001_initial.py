# Generated by Django 4.1.1 on 2023-05-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("page", models.CharField(max_length=255)),
                ("time_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "hint",
                "verbose_name_plural": "hints",
                "db_table": "hint",
                "ordering": ["-id"],
            },
        ),
    ]