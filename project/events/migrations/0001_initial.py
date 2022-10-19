# Generated by Django 4.1.1 on 2022-10-19 08:39

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
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('place', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Man', 'Man'), ('Woomen', 'Woomen')], max_length=10)),
                ('date_and_time', models.DateTimeField()),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('need_ball', models.BooleanField()),
                ('amount_members', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(6), django.core.validators.MaxValueValidator(50)])),
                ('type', models.CharField(choices=[('Football', 'Football'), ('Futsal', 'Futsal')], max_length=15)),
                ('price', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('price_description', models.CharField(blank=True, max_length=500, null=True)),
                ('need_form', models.BooleanField()),
                ('privacy', models.BooleanField()),
                ('duration', models.PositiveSmallIntegerField(choices=[(10, 'Minutes 10'), (20, 'Minutes 20'), (30, 'Minutes 30'), (40, 'Minutes 40'), (50, 'Minutes 50'), (60, 'Minutes 60'), (70, 'Minutes 70'), (80, 'Minutes 80'), (90, 'Minutes 90'), (100, 'Minutes 100'), (110, 'Minutes 110'), (120, 'Minutes 120'), (130, 'Minutes 130'), (140, 'Minutes 140'), (150, 'Minutes 150'), (160, 'Minutes 160'), (170, 'Minutes 170'), (180, 'Minutes 180')])),
                ('forms', models.CharField(choices=[('Shirt-Front', 'Shirt Front'), ('T-Shirt', 'T Shirt'), ('Any', 'Any')], max_length=15)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('Active', 'Active'), ('Finished', 'Finished')], default='Planned', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_fans', models.ManyToManyField(blank=True, related_name='current_views_rooms', to=settings.AUTH_USER_MODEL)),
                ('current_users', models.ManyToManyField(blank=True, related_name='current_rooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='RequestToParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('event_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'request to participation',
                'verbose_name_plural': 'requests to participation',
                'db_table': 'request_to_participation',
            },
        ),
        migrations.CreateModel(
            name='InviteToEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'invite to event',
                'verbose_name_plural': 'invites to event',
                'db_table': 'invite_to_event',
            },
        ),
        migrations.CreateModel(
            name='EventTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('event_data', models.JSONField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'event template',
                'verbose_name_plural': 'events templates',
                'db_table': 'event_template',
            },
        ),
    ]
