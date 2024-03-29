# Generated by Django 4.1.1 on 2022-11-03 17:05

import authentication.models.profile_model
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_alter_profile_about_me_alter_profile_age_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="code",
            name="dop_info",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="code",
            name="life_time",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birthday",
            field=models.DateField(
                null=True,
                validators=[authentication.models.profile_model.validate_birthday],
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="height",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(30),
                    django.core.validators.MaxValueValidator(210),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="authentication.profile",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="raiting",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("User", "User"), ("Admin", "Admin")], max_length=10, null=True
            ),
        ),
    ]
