# Generated by Django 4.0.4 on 2022-08-29 08:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('small_disc', models.CharField(max_length=200)),
                ('full_disc', models.TextField()),
                ('place', models.CharField(max_length=500)),
                ('gender', models.CharField(choices=[('Man', 'Man'), ('Woomen', 'Woomen')], max_length=10)),
                ('date_and_time', models.DateTimeField()),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('need_ball', models.BooleanField()),
                ('amount_members', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(6), django.core.validators.MaxValueValidator(50)])),
                ('type', models.CharField(choices=[('Football', 'Football'), ('Futsal', 'Futsal')], max_length=100)),
                ('price', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('price_description', models.CharField(blank=True, max_length=500, null=True)),
                ('need_form', models.BooleanField()),
                ('forms', models.CharField(max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('current_users', models.ManyToManyField(blank=True, null=True, related_name='current_rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
