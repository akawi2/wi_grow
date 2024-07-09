# Generated by Django 5.0.6 on 2024-07-06 10:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='id',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='id',
        ),
        migrations.RemoveField(
            model_name='environmentalmonitoring',
            name='id',
        ),
        migrations.RemoveField(
            model_name='farm',
            name='id',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='id',
        ),
        migrations.RemoveField(
            model_name='planningcrop',
            name='id',
        ),
        migrations.RemoveField(
            model_name='plot',
            name='id',
        ),
        migrations.AlterField(
            model_name='action',
            name='actionId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='action',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='crop',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='crop',
            name='cropId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='environmentalmonitoring',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='environmentalmonitoring',
            name='environmentalId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='farm',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='farm',
            name='farmId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='incident',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incidentId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='planningcrop',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='planningcrop',
            name='planningCropId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plot',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='plot',
            name='plotId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
