# Generated by Django 5.0.6 on 2024-05-25 01:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='fecha',
            field=models.TimeField(default=datetime.datetime(2024, 5, 25, 1, 16, 29, 568770, tzinfo=datetime.timezone.utc)),
        ),
    ]
