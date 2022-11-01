# Generated by Django 4.1.1 on 2022-10-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_author_alter_event_black_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitetoevent',
            name='status',
        ),
        migrations.AddField(
            model_name='requesttoparticipation',
            name='status',
            field=models.CharField(choices=[('Waiting', 'Waiting'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Waiting', max_length=10),
        ),
    ]