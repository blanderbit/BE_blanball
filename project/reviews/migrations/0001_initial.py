# Generated by Django 4.0.4 on 2022-08-30 16:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=255)),
                ('text', models.CharField(max_length=200)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('stars', models.PositiveSmallIntegerField(verbose_name=django.core.validators.MaxValueValidator(5))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]