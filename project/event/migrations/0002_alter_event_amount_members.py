# Generated by Django 4.0.4 on 2022-08-10 09:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='amount_members',
            field=models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(6), django.core.validators.MaxValueValidator(50)]),
        ),
    ]
