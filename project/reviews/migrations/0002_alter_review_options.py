# Generated by Django 4.1.1 on 2022-10-16 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'review', 'verbose_name_plural': 'reviews'},
        ),
    ]
