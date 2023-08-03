# Generated by Django 4.1.1 on 2022-11-03 17:01

import authentication.models.profile_model
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_profile_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="about_me",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="age",
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                null=True, upload_to=authentication.models.profile_model.image_file_name
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birthday",
            field=models.DateField(
                blank=True,
                validators=[authentication.models.profile_model.validate_birthday],
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="position",
            field=models.CharField(
                choices=[
                    ("GK", "Gk"),
                    ("LB", "Lb"),
                    ("RB", "Rb"),
                    ("CB", "Cb"),
                    ("LWB", "Lwb"),
                    ("RWB", "Rwb"),
                    ("CDM", "Cdm"),
                    ("CM", "Cm"),
                    ("CAM", "Cam"),
                    ("RM", "Rm"),
                    ("LM", "Lm"),
                    ("RW", "Rw"),
                    ("LW", "Lw"),
                    ("RF", "Rf"),
                    ("CF", "Cf"),
                    ("LF", "Lf"),
                    ("ST", "St"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="weight",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(30),
                    django.core.validators.MaxValueValidator(210),
                ],
            ),
        ),
    ]
