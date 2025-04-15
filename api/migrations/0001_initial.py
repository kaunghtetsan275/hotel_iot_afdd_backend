# Generated by Django 5.2 on 2025-04-09 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IoTDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=50)),
                ('device_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('message', models.TextField()),
                ('acknowledged', models.BooleanField(default=False)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.iotdevice')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.floor')),
            ],
        ),
        migrations.AddField(
            model_name='iotdevice',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.room'),
        ),
    ]
