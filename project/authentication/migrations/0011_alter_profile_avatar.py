# Generated by Django 4.1.1 on 2022-11-21 15:34

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0010_alter_profile_place"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default=None,
                null=True,
                upload_to=authentication.models.image_file_name,
                validators=[authentication.models.validate_image],
            ),
        ),
    ]
