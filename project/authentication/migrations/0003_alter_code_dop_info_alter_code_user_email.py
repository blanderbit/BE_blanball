# Generated by Django 4.1.1 on 2022-09-25 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='dop_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='code',
            name='user_email',
            field=models.CharField(max_length=255),
        ),
    ]
