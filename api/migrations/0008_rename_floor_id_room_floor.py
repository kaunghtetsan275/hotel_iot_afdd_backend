# Generated by Django 5.2 on 2025-04-15 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_room_floor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='floor_id',
            new_name='floor',
        ),
    ]
